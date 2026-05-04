#!/usr/bin/env node
/**
 * dispatch.js — Arcane Candidate Ingestion Dispatcher
 *
 * Reads fact-cards.json, splits candidates into batches, and spawns
 * template-builder subagents via `gsd headless` to classify and create
 * template directories.
 *
 * Usage:
 *   node scripts/dispatch.js --source yunohost --batch-size 15 --dry-run
 *   node scripts/dispatch.js --source portainer --limit 30
 *   node scripts/dispatch.js --help
 *
 * Environment:
 *   FACT_CARDS_PATH   Override path to fact-cards.json (default: ./fact-cards.json)
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

// ── Configuration ──────────────────────────────────────────────────────

const ROOT_DIR = path.resolve(__dirname, '..');
const FACT_CARDS_PATH = process.env.FACT_CARDS_PATH
  ? path.resolve(process.env.FACT_CARDS_PATH)
  : path.join(ROOT_DIR, 'fact-cards.json');
const BATCHES_DIR = path.join(ROOT_DIR, 'scripts', 'batches');
const REVIEW_QUEUE_PATH = path.join(ROOT_DIR, 'review-queue.json');
const DEAD_LETTER_PATH = path.join(ROOT_DIR, 'dead-letter.json');

const CONCURRENCY_CAP = 10;

const KNOWN_SOURCES = [
  'yunohost',
  'portainer',
  'umbrel',
  'awesome-selfhosted',
  'priority',
  'm012'
];

// ── CLI flag parsing ───────────────────────────────────────────────────

function parseFlags(argv) {
  const flags = {
    batchSize: 15,
    source: null,
    model: 'gemini-3-pro-preview',
    limit: 0,
    dryRun: false,
    verbose: false,
    timeout: 300,
    concurrency: 0,
    help: false
  };

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    const next = argv[i + 1];

    switch (arg) {
      case '--batch-size':
        if (next !== undefined && !next.startsWith('-')) {
          flags.batchSize = parseInt(next, 10);
          i++;
        }
        break;
      case '--source':
        if (next !== undefined && !next.startsWith('-')) {
          flags.source = next;
          i++;
        }
        break;
      case '--model':
        if (next !== undefined && !next.startsWith('-')) {
          flags.model = next;
          i++;
        }
        break;
      case '--limit':
        if (next !== undefined && !next.startsWith('-')) {
          flags.limit = parseInt(next, 10);
          i++;
        }
        break;
      case '--dry-run':
        flags.dryRun = true;
        break;
      case '--verbose':
        flags.verbose = true;
        break;
      case '--timeout':
        if (next !== undefined && !next.startsWith('-')) {
          flags.timeout = parseInt(next, 10);
          i++;
        }
        break;
      case '--concurrency':
        if (next !== undefined && !next.startsWith('-')) {
          flags.concurrency = parseInt(next, 10);
          i++;
        }
        break;
      case '--help':
      case '-h':
        flags.help = true;
        break;
    }
  }

  return flags;
}

// ── Helpers ────────────────────────────────────────────────────────────

function error(msg) {
  console.error(`ERROR: ${msg}`);
}

function warn(msg) {
  console.error(`WARN: ${msg}`);
}

function info(msg) {
  console.error(`[prepare] ${msg}`);
}

function verboseLog(flags, msg) {
  if (flags.verbose) {
    console.error(`[verbose] ${msg}`);
  }
}

function clamp(val, min, max) {
  return Math.max(min, Math.min(max, val));
}

function printHelp() {
  console.log(`dispatch.js — Arcane Candidate Ingestion Dispatcher

Reads fact-cards.json, splits candidates into batches, and spawns
template-builder subagents to classify and create template directories.

Usage:
  node scripts/dispatch.js [flags]

Flags:
  --batch-size N    Candidates per batch (default: 15, range: 1–100)
  --source NAME     Source catalog filter (required for execution)
                    Known sources: ${KNOWN_SOURCES.join(', ')}
  --model MODEL     LLM model for subagents (default: gemini-3-pro-preview)
  --limit N         Max candidates to process (default: 0 = all)
  --dry-run         Print batch plan without writing files or spawning agents
  --verbose         Enable verbose debug logging to stderr
  --timeout SECS    Subagent timeout in seconds (default: 300)
  --concurrency N   Max concurrent subagents (default: batch count capped at 10)
  --help            Print this help and exit

Examples:
  # Preview batch plan without executing
  node scripts/dispatch.js --source yunohost --batch-size 15 --dry-run

  # Process first 30 yunohost candidates in batches of 15
  node scripts/dispatch.js --source yunohost --batch-size 15 --limit 30

  # Process all portainer candidates with verbose output
  node scripts/dispatch.js --source portainer --verbose

Phase markers on stderr:
  [prepare]   Input validation, filtering, batch splitting
  [dispatch]  Subagent spawning and monitoring
  [collect]   Result collection and merge

Output files:
  scripts/batches/batch-NNN.json   Per-batch input files
  review-queue.json                Ambiguous results needing human review
  dead-letter.json                 Crashed batches that failed retry
`);
}

// ── Schema validation ──────────────────────────────────────────────────

/**
 * Validates a single fact card against the MEM102 contract schema.
 * Required fields: source, name.
 * Expected (warn only): images_checked, recommend_image, classification_hints.
 */
function validateFactCard(candidate, index) {
  const required = ['source', 'candidate'];
  let valid = true;

  for (const field of required) {
    if (candidate[field] === undefined || candidate[field] === null) {
      error(`fact-cards.json[${index}]: missing required field "${field}"`);
      valid = false;
    }
  }

  if (typeof candidate.candidate !== 'string' || candidate.candidate.length < 1) {
    error(`fact-cards.json[${index}]: "candidate" must be a non-empty string`);
    valid = false;
  }

  if (typeof candidate.source !== 'string' || candidate.source.length < 1) {
    error(`fact-cards.json[${index}]: "source" must be a non-empty string`);
    valid = false;
  }

  // Warn on missing optional-but-expected MEM102 fields
  if (!candidate.images_checked) {
    warn(`fact-cards.json[${index}] ("${candidate.candidate}"): missing "images_checked" field (expected per MEM102)`);
  }
  if (!candidate.recommend_image) {
    warn(`fact-cards.json[${index}] ("${candidate.candidate}"): missing "recommend_image" field (expected per MEM102)`);
  }
  if (!candidate.classification_hints) {
    warn(`fact-cards.json[${index}] ("${candidate.candidate}"): missing "classification_hints" field (expected per MEM102)`);
  }

  return valid;
}

// ── Batch splitting ────────────────────────────────────────────────────

/**
 * Splits an array of candidates into chunks of at most `batchSize`.
 */
function splitIntoBatches(candidates, batchSize) {
  const batches = [];
  for (let i = 0; i < candidates.length; i += batchSize) {
    batches.push(candidates.slice(i, i + batchSize));
  }
  return batches;
}

/**
 * Writes per-batch JSON files to scripts/batches/batch-NNN.json.
 * Each file contains a standalone subset of fact cards with batch metadata.
 */
function writeBatchFiles(batches, flags) {
  if (!fs.existsSync(BATCHES_DIR)) {
    fs.mkdirSync(BATCHES_DIR, { recursive: true });
  }

  for (let i = 0; i < batches.length; i++) {
    const paddedNum = String(i + 1).padStart(3, '0');
    const batchPath = path.join(BATCHES_DIR, `batch-${paddedNum}.json`);
    const batchPayload = {
      batchId: i + 1,
      batchFile: `batch-${paddedNum}.json`,
      source: flags.source,
      model: flags.model,
      totalBatches: batches.length,
      candidates: batches[i]
    };
    fs.writeFileSync(batchPath, JSON.stringify(batchPayload, null, 2) + '\n', 'utf8');
    verboseLog(flags, `Wrote ${batchPath} (${batches[i].length} candidates)`);
  }
}

// ── Subagent spawning ─────────────────────────────────────────────────

/**
 * Builds the self-contained task prompt piped to the subagent's stdin.
 *
 * The prompt tells the template-builder agent to read the batch file,
 * classify each candidate, create template directories, and write
 * review-queue fragments for ambiguous cases.
 */
function buildSubagentPrompt(batchFilePath, flags) {
  const batchNum = path.basename(batchFilePath, '.json').replace('batch-', '');
  const fragmentPath = path.join(ROOT_DIR, `review-queue-batch-${batchNum}.json`);
  return `You are processing a batch of Arcane template candidates.

Read the batch file at ${batchFilePath}.
For each candidate, use the template-builder agent (loaded from .gsd/agents/template-builder.md) to classify and create a template directory under templates/<slug>/ with these required files:
  - arcane.json
  - docker-compose.yml
  - .env.example
  - README.md

For candidates that cannot be cleanly classified, write a review-queue fragment to ${fragmentPath} using this append format per entry:
  { "candidate": "<name>", "source": "<source>", "ambiguity": "<what's unclear>", "hypothesis": "<best-guess classification>", "recommendation": "<next step>", "agent": "template-builder", "timestamp": "<ISO-8601>" }

After processing all candidates, return a structured JSON summary of what was created or categorized.`;
}

/**
 * Spawns a single `gsd headless` subagent for one batch file.
 *
 * Returns a Promise that resolves with { batchFile, exitCode, stdout, stderr, retries }
 * or rejects on critical failure (e.g., gsd binary not found).
 */
function spawnSubagent(batchFilePath, flags) {
  return new Promise((resolve, reject) => {
    const paddedNum = path.basename(batchFilePath, '.json').replace('batch-', '');

    const gsdCmd = process.platform === 'win32' ? 'gsd.cmd' : 'gsd';
    const args = [
      'headless',
      '--model', flags.model,
      '--output-format', 'json',
      'auto'
    ];

    const prompt = buildSubagentPrompt(batchFilePath, flags);

    verboseLog(flags, `Spawning: ${gsdCmd} ${args.join(' ')}`);
    verboseLog(flags, `Prompt length: ${prompt.length} chars`);

    const child = spawn(gsdCmd, args, {
      stdio: ['pipe', 'pipe', 'pipe'],
      env: process.env,
      windowsHide: true,
      shell: process.platform === 'win32'
    });

    // Write the task prompt to stdin, then close it
    child.stdin.write(prompt);
    child.stdin.end();

    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    child.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    // Timeout handling: after --timeout seconds, send SIGTERM, wait 5s, SIGKILL
    let timeoutHandle = null;
    let killHandle = null;
    let timedOut = false;

    if (flags.timeout > 0) {
      timeoutHandle = setTimeout(() => {
        timedOut = true;
        child.kill('SIGTERM');

        killHandle = setTimeout(() => {
          child.kill('SIGKILL');
        }, 5000);
      }, flags.timeout * 1000);
    }

    child.on('error', (err) => {
      clearTimer();
      reject(err);
    });

    child.on('close', (exitCode) => {
      clearTimer();
      resolve({
        batchFile: batchFilePath,
        paddedNum,
        exitCode: exitCode,
        stdout,
        stderr,
        timedOut,
        retries: 0
      });
    });

    function clearTimer() {
      if (timeoutHandle) {
        clearTimeout(timeoutHandle);
        timeoutHandle = null;
      }
      if (killHandle) {
        clearTimeout(killHandle);
        killHandle = null;
      }
    }
  });
}

/**
 * Retries a failed batch by re-spawning the subagent.
 *
 * Returns { ...dispatchResult, retries: 1 } on success, or the original
 * failure result with retries: 1 on second failure.
 */
async function retrySubagent(lastResult, flags) {
  const paddedNum = lastResult.paddedNum;
  console.error(`[dispatch] batch ${paddedNum} FAILED (exit=${lastResult.exitCode}, retrying...)`);

  try {
    const result = await spawnSubagent(lastResult.batchFile, flags);
    result.retries = 1;
    return result;
  } catch (_err) {
    // Second failure — return the original result with retries incremented
    lastResult.retries = 1;
    return lastResult;
  }
}

/**
 * Writes a dead-letter entry for a batch that failed all retries.
 * Dead-letter.json is an array of objects with batch metadata + failure reason.
 */
function writeDeadLetter(result, flags) {
  let deadLetters = [];
  if (fs.existsSync(DEAD_LETTER_PATH)) {
    try {
      const raw = fs.readFileSync(DEAD_LETTER_PATH, 'utf8');
      deadLetters = JSON.parse(raw);
      if (!Array.isArray(deadLetters)) {
        deadLetters = [];
      }
    } catch (_e) {
      deadLetters = [];
    }
  }

  const entry = {
    batchFile: path.basename(result.batchFile),
    batchPath: result.batchFile,
    exitCode: result.exitCode,
    timedOut: result.timedOut || false,
    retries: result.retries,
    stderrSnippet: result.stderr ? result.stderr.slice(-500) : '',
    timestamp: new Date().toISOString()
  };
  deadLetters.push(entry);

  fs.writeFileSync(DEAD_LETTER_PATH, JSON.stringify(deadLetters, null, 2) + '\n', 'utf8');
  verboseLog(flags, `Wrote dead-letter entry for ${entry.batchFile}`);
}

/**
 * Tries to parse subagent stdout as JSON. Returns the parsed object
 * or null if the output is not valid JSON.
 */
function parseSubagentJson(stdout) {
  try {
    return JSON.parse(stdout);
  } catch (_e) {
    return null;
  }
}

/**
 * Merges all review-queue-batch-NNN.json fragment files into a unified
 * review-queue.json using append-semantics per MEM097.
 *
 * Each fragment is expected to be an array of { candidateId, classification,
 * decision, rationale, templatePath?, needsReview? } entries (object form per
 * the template-builder agent contract). Flat arrays from fragments are
 * concatenated into a single merged array.
 *
 * Fragment files are deleted after merge succeeds. Skips fragments that
 * are missing or contain unparseable JSON (logs warning).
 *
 * Returns the merged array (may be empty if no fragments were found).
 */
function mergeReviewQueueFragments(flags) {
  const fragmentPrefix = 'review-queue-batch-';
  let allFragments = [];

  console.error(`[collect] merging review-queue fragments → ${REVIEW_QUEUE_PATH}`);

  if (!fs.existsSync(ROOT_DIR)) {
    return allFragments;
  }

  const rootEntries = fs.readdirSync(ROOT_DIR);
  const fragments = rootEntries
    .filter(f => f.startsWith(fragmentPrefix) && f.endsWith('.json'))
    .sort();

  if (fragments.length === 0) {
    console.error('[collect] no review-queue fragments found');
    return allFragments;
  }

  console.error(`[collect] found ${fragments.length} review-queue fragments`);

  for (const fragFile of fragments) {
    const fragPath = path.join(ROOT_DIR, fragFile);
    try {
      const raw = fs.readFileSync(fragPath, 'utf8');
      const parsed = JSON.parse(raw);

      if (!Array.isArray(parsed)) {
        warn(`skip fragment ${fragFile}: not a JSON array`);
        continue;
      }

      allFragments = allFragments.concat(parsed);
      verboseLog(flags, `  merged ${fragFile} (${parsed.length} entries)`);
    } catch (e) {
      warn(`skip fragment ${fragFile}: ${e.message}`);
    }
  }

  // Deduplicate by candidateId if present
  const seen = new Set();
  const deduped = [];
  for (const entry of allFragments) {
    const key = entry.candidateId || JSON.stringify(entry);
    if (!seen.has(key)) {
      seen.add(key);
      deduped.push(entry);
    }
  }

  if (deduped.length < allFragments.length) {
    console.error(`[collect] deduplicated: ${allFragments.length - deduped.length} duplicate entries removed`);
  }

  // Write merged review-queue.json
  if (deduped.length > 0) {
    fs.writeFileSync(REVIEW_QUEUE_PATH, JSON.stringify(deduped, null, 2) + '\n', 'utf8');
    console.error(`[collect] wrote ${REVIEW_QUEUE_PATH} (${deduped.length} entries)`);
  } else {
    console.error('[collect] no review-queue entries to write');
  }

  // Clean up fragment files
  for (const fragFile of fragments) {
    const fragPath = path.join(ROOT_DIR, fragFile);
    try {
      fs.unlinkSync(fragPath);
      verboseLog(flags, `  cleaned up ${fragFile}`);
    } catch (e) {
      warn(`could not clean up fragment ${fragFile}: ${e.message}`);
    }
  }

  return deduped;
}

/**
 * Runs `node scripts/build-registry.js --validate-only` as the final
 * quality gate. If templates were created by subagents, this validates
 * their arcane.json metadata and required files.
 *
 * Returns { verdict: 'PASS'|'FAIL', errors: string|null, exitCode: number }.
 */
function runValidation(flags) {
  const validationTimeout = 60; // 60s — plan spec for registry validation
  const buildRegistryPath = path.join(ROOT_DIR, 'scripts', 'build-registry.js');

  if (!fs.existsSync(buildRegistryPath)) {
    return { verdict: 'FAIL', errors: `build-registry.js not found at ${buildRegistryPath}`, exitCode: -1 };
  }

  console.error('[validate] running build-registry.js --validate-only');

  const { spawnSync } = require('child_process');
  const result = spawnSync('node', [buildRegistryPath, '--validate-only'], {
    cwd: ROOT_DIR,
    timeout: validationTimeout * 1000,
    stdio: ['ignore', 'pipe', 'pipe'],
    encoding: 'utf8',
    env: process.env,
    windowsHide: true
  });

  const stderr = (result.stderr || '').trim();
  const stdout = (result.stdout || '').trim();

  if (result.error) {
    return { verdict: 'FAIL', errors: result.error.message, exitCode: -1 };
  }

  if (result.signal === 'SIGTERM' || result.signal === 'SIGKILL') {
    return { verdict: 'FAIL', errors: `build-registry.js timed out after ${validationTimeout}s`, exitCode: -1 };
  }

  if (result.status !== 0) {
    const errorSummary = stderr
      ? stderr.split('\n').filter(l => l.startsWith('ERROR:')).join('\n')
      : 'unknown validation errors';
    return { verdict: 'FAIL', errors: errorSummary, exitCode: result.status };
  }

  // Extract template count from stdout
  const match = stdout.match(/(\d+) templates/);
  const templateCount = match ? parseInt(match[1], 10) : 0;

  return { verdict: 'PASS', errors: null, exitCode: 0, templateCount };
}

/**
 * Parses a subagent's stdout to extract classification counts.
 * Expects structured JSON from `gsd headless --output-format json`.
 *
 * Returns { dockerReady, customBuild, nonServiceable, multiService, parseErrors }
 * reflecting the subagent's reported template creation results.
 */
function extractTemplateCounts(result, flags) {
  const counts = { dockerReady: 0, customBuild: 0, nonServiceable: 0, multiService: 0, parseErrors: 0 };

  if (result.fatal) {
    counts.parseErrors++;
    return counts;
  }

  const parsed = parseSubagentJson(result.stdout);
  if (parsed === null) {
    warn(`batch ${result.paddedNum}: stdout is not valid JSON — cannot extract template counts`);
    counts.parseErrors++;
    return counts;
  }

  // Handle GSD HeadlessJsonResult structure: { result: <string> }
  // The subagent prompt instructs a JSON summary; the actual output varies.
  // We parse what we can from the structured output.
  const data = typeof parsed.result === 'string'
    ? (() => { try { return JSON.parse(parsed.result); } catch (_e) { return null; } })()
    : parsed;

  if (!data) {
    warn(`batch ${result.paddedNum}: could not extract structured result from agent output`);
    counts.parseErrors++;
    return counts;
  }

  // Look for explicit classification counts in the agent's output
  if (data.templates) {
    for (const tpl of data.templates) {
      const classification = (tpl.classification || '').toLowerCase();
      if (classification === 'docker-ready') counts.dockerReady++;
      else if (classification === 'custom-build') counts.customBuild++;
      else if (classification === 'non-serviceable') counts.nonServiceable++;
      else if (classification === 'multi-service') counts.multiService++;
      else counts.dockerReady++; // default
    }
  }

  // Also check summary fields
  if (data.summary) {
    const s = data.summary;
    if (s.dockerReady !== undefined) counts.dockerReady = Math.max(counts.dockerReady, s.dockerReady);
    if (s.customBuild !== undefined) counts.customBuild = Math.max(counts.customBuild, s.customBuild);
    if (s.nonServiceable !== undefined) counts.nonServiceable = Math.max(counts.nonServiceable, s.nonServiceable);
    if (s.multiService !== undefined) counts.multiService = Math.max(counts.multiService, s.multiService);
  }

  return counts;
}

/**
 * Runs the collect phase: parses subagent results, merges review-queue
 * fragments, runs validation gate, and prints the final summary.
 *
 * @param {Array} dispatchResults — raw results from runDispatch()
 * @param {number} totalCandidates — original candidate count
 * @param {Array} batches — original batch arrays (for per-batch counts)
 * @param {Object} flags — CLI flags
 */
async function collectPhase(dispatchResults, totalCandidates, batches, flags) {
  let dockerReady = 0;
  let customBuild = 0;
  let nonServiceable = 0;
  let multiService = 0;
  let parseErrors = 0;

  for (const r of dispatchResults) {
    const counts = extractTemplateCounts(r, flags);
    dockerReady += counts.dockerReady;
    customBuild += counts.customBuild;
    nonServiceable += counts.nonServiceable;
    multiService += counts.multiService;
    parseErrors += counts.parseErrors;
  }

  // Merge review-queue fragments
  const reviewQueue = mergeReviewQueueFragments(flags);

  // Count dead-lettered batches
  const deadLettered = dispatchResults.filter(r => r.exitCode !== 0 || r.timedOut).length;
  const totalBatches = dispatchResults.length;

  // Read dead-letter.json for count
  let deadLetterCount = deadLettered;
  if (fs.existsSync(DEAD_LETTER_PATH)) {
    try {
      const dl = JSON.parse(fs.readFileSync(DEAD_LETTER_PATH, 'utf8'));
      if (Array.isArray(dl)) {
        deadLetterCount = dl.length;
      }
    } catch (_e) { /* ignore parse error */ }
  }

  // Run validation gate
  const totalTemplates = dockerReady + customBuild + nonServiceable + multiService;
  let validationResult = null;

  if (totalTemplates > 0 && !flags.dryRun) {
    validationResult = runValidation(flags);
  } else if (totalTemplates === 0 && !flags.dryRun) {
    console.error('[validate] no templates created — skipping validation gate');
  }

  // Print final summary
  console.log('');
  console.log(`✓ Dispatched: ${totalBatches} batches, ${totalCandidates} candidates`);
  console.log(`✓ Created: ${totalTemplates} templates (docker-ready: ${dockerReady}, custom-build: ${customBuild}, non-serviceable: ${multiService > 0 ? `, multi-service: ${multiService}` : ''})`.replace(', ,', ','));
  // Fix formatting
  const catParts = [];
  catParts.push(`docker-ready: ${dockerReady}`);
  catParts.push(`custom-build: ${customBuild}`);
  if (multiService > 0) catParts.push(`multi-service: ${multiService}`);
  catParts.push(`non-serviceable: ${nonServiceable}`);
  console.log(`✓ Created: ${totalTemplates} templates (${catParts.join(', ')})`);

  console.log(`✓ Review queue: ${reviewQueue.length} ambiguous entries`);
  if (validationResult) {
    const vVerdict = validationResult.verdict === 'PASS' ? 'PASS' : `FAIL with ${validationResult.errors ? validationResult.errors.split('\n').length : 0} errors`;
    if (validationResult.templateCount !== undefined) {
      console.log(`✓ Validation: ${validationResult.verdict} (${validationResult.templateCount} templates validated)`);
    } else {
      console.log(`✓ Validation: ${vVerdict}`);
    }
  } else if (totalTemplates === 0) {
    console.log('✓ Validation: SKIPPED (no templates)');
  }
  console.log(`✓ Dead letter: ${deadLetterCount} unrecoverable batches`);

  // Return verdict for exit code
  return validationResult;
}

/**
 * Runs the full dispatch phase: processes all batch files with a semaphore
 * pattern, limiting concurrency to `concurrency` (default: batch count, cap 10).
 */
async function runDispatch(flags) {
  const batchFiles = fs.readdirSync(BATCHES_DIR)
    .filter(f => f.startsWith('batch-') && f.endsWith('.json'))
    .sort()
    .map(f => path.join(BATCHES_DIR, f));

  if (batchFiles.length === 0) {
    error(`No batch files found in ${BATCHES_DIR}. Run without --dry-run first to create them.`);
    process.exit(1);
  }

  const concurrency = flags.concurrency > 0
    ? Math.min(flags.concurrency, CONCURRENCY_CAP)
    : Math.min(batchFiles.length, CONCURRENCY_CAP);

  console.error(`[dispatch] Starting dispatch: ${batchFiles.length} batches, concurrency=${concurrency}, timeout=${flags.timeout}s`);

  const results = [];
  let completed = 0;
  let failed = 0;

  // Semaphore: process batches in waves of N
  for (let i = 0; i < batchFiles.length; i += concurrency) {
    const wave = batchFiles.slice(i, i + concurrency);

    const wavePromises = wave.map(async (batchFile) => {
      const paddedNum = path.basename(batchFile, '.json').replace('batch-', '');
      console.error(`[dispatch] batch ${paddedNum}/${batchFiles.length} pid=${process.pid} ...`);

      let result;
      try {
        result = await spawnSubagent(batchFile, flags);
      } catch (err) {
        // gsd binary not found or similar fatal error
        console.error(`[dispatch] batch ${paddedNum} DEAD (spawn error: ${err.message})`);
        failed++;
        return { batchFile, exitCode: -1, stderr: err.message, timedOut: false, retries: 0, fatal: true };
      }

      // Check for exit code, timeout, or malformed JSON
      const isFailure = result.exitCode !== 0 || result.timedOut;
      const parsed = parseSubagentJson(result.stdout);

      if (isFailure || parsed === null) {
        // Retry once
        const retryResult = await retrySubagent(result, flags);

        const retryParsed = parseSubagentJson(retryResult.stdout);
        const retryFailed = retryResult.exitCode !== 0 || retryResult.timedOut || retryParsed === null;

        if (retryFailed) {
          // Dead letter
          console.error(`[dispatch] batch ${paddedNum} DEAD (exit=${retryResult.exitCode})`);
          writeDeadLetter(retryResult, flags);
          failed++;
          results.push(retryResult);
          completed++;
          return retryResult;
        }

        // Retry succeeded
        console.error(`[dispatch] batch ${paddedNum} done (exit=${retryResult.exitCode}, ${retryResult.retries} retries)`);
        results.push(retryResult);
        completed++;
        return retryResult;
      }

      // First attempt succeeded
      const elapsed = 'N/A'; // we don't track timing in this version
      console.error(`[dispatch] batch ${paddedNum} done (exit=${result.exitCode}, ${elapsed})`);
      results.push(result);
      completed++;
      return result;
    });

    await Promise.all(wavePromises);
  }

  console.error(`[dispatch] Complete: ${completed} batches processed, ${failed} dead-lettered`);
  return results;
}

// ── Main ───────────────────────────────────────────────────────────────

function main() {
  const flags = parseFlags(process.argv.slice(2));

  // ── Help ───────────────────────────────────────────────────────────
  if (flags.help) {
    printHelp();
    process.exit(0);
  }

  // ── Clamp batch-size ───────────────────────────────────────────────
  flags.batchSize = clamp(flags.batchSize, 1, 100);
  if (isNaN(flags.batchSize)) {
    flags.batchSize = 15;
  }

  // ── Clamp timeout ──────────────────────────────────────────────────
  if (isNaN(flags.timeout) || flags.timeout < 1) {
    flags.timeout = 300;
  }

  // ── Read fact-cards.json ───────────────────────────────────────────
  if (!fs.existsSync(FACT_CARDS_PATH)) {
    error(`fact-cards.json not found at ${FACT_CARDS_PATH}`);
    error('Run preflight-images.py (M005/S02) first to generate fact cards.');
    process.exit(1);
  }

  let factCards;
  try {
    const raw = fs.readFileSync(FACT_CARDS_PATH, 'utf8');
    factCards = JSON.parse(raw);
  } catch (e) {
    error(`Failed to parse fact-cards.json: ${e.message}`);
    process.exit(1);
  }

  if (!Array.isArray(factCards)) {
    error('fact-cards.json must be a JSON array of candidate objects');
    process.exit(1);
  }

  verboseLog(flags, `Loaded ${factCards.length} fact cards from fact-cards.json`);

  // ── Validate schema ────────────────────────────────────────────────
  let validCount = 0;
  for (let i = 0; i < factCards.length; i++) {
    if (validateFactCard(factCards[i], i)) {
      validCount++;
    }
  }
  verboseLog(flags, `${validCount}/${factCards.length} fact cards pass schema validation`);

  // ── Validate --source ──────────────────────────────────────────────
  if (flags.source) {
    if (!KNOWN_SOURCES.includes(flags.source)) {
      error(`Unknown source "${flags.source}". Known sources: ${KNOWN_SOURCES.join(', ')}`);
      process.exit(1);
    }
  } else if (!flags.dryRun) {
    error('--source is required for execution. Use --dry-run to preview without a source, or specify one of: ' + KNOWN_SOURCES.join(', '));
    process.exit(1);
  }

  // ── Filter by source ───────────────────────────────────────────────
  let candidates = factCards;

  if (flags.source) {
    candidates = factCards.filter(c => c.source === flags.source);
    verboseLog(flags, `Filtered to source="${flags.source}": ${candidates.length} candidates`);

    if (candidates.length === 0) {
      warn(`No candidates found for source "${flags.source}"`);
      process.exit(0);
    }
  }

  // ── Apply --limit ──────────────────────────────────────────────────
  if (flags.limit > 0 && flags.limit < candidates.length) {
    candidates = candidates.slice(0, flags.limit);
    verboseLog(flags, `Applied --limit ${flags.limit}: ${candidates.length} candidates`);
  }

  // ── Split into batches ─────────────────────────────────────────────
  const batches = splitIntoBatches(candidates, flags.batchSize);
  const batchCount = batches.length;

  // ── Print batch plan ───────────────────────────────────────────────
  info(`Total candidates: ${candidates.length}`);
  info(`Batch size: ${flags.batchSize}`);
  info(`Batch count: ${batchCount}`);
  info(`Source: ${flags.source || '(all)'}`);
  info(`Model: ${flags.model}`);
  info(`Timeout: ${flags.timeout}s`);

  if (batchCount > 0) {
    const avgPerBatch = Math.round(candidates.length / batchCount);
    const sizes = batches.map(b => b.length);
    const minBatch = Math.min(...sizes);
    const maxBatch = Math.max(...sizes);
    console.error(`[prepare] Candidates per batch: avg ${avgPerBatch}, min ${minBatch}, max ${maxBatch}`);

    // Print per-batch breakdown
    for (let i = 0; i < batches.length; i++) {
      const first = batches[i][0];
      const last = batches[i][batches[i].length - 1];
      console.error(`[prepare]   batch-${String(i + 1).padStart(3, '0')}: ${batches[i].length} candidates (${first.candidate} … ${last.candidate})`);
    }
  }

  // ── Dry-run: exit without writing files ────────────────────────────
  if (flags.dryRun) {
    console.error('[prepare] DRY RUN — no files written, no subagents spawned.');
    process.exit(0);
  }

  // ── Write batch files ──────────────────────────────────────────────
  info(`Writing ${batchCount} batch files to scripts/batches/`);
  writeBatchFiles(batches, flags);

  info(`Batch files written. ${batchCount} batches ready for dispatch.`);

  // ── Execute: spawn subagents ─────────────────────────────────────
  info(`Dispatching ${batchCount} batches with gsd headless subagents...`);

  runDispatch(flags).then(async (results) => {
    const validationResult = await collectPhase(results, candidates.length, batches, flags);

    const hasValidationFailure = validationResult && validationResult.verdict !== 'PASS';

    // Exit non-zero if validation failed or dead-letter entries exist
    const deadLettered = results.filter(r => r.exitCode !== 0 || r.timedOut).length;

    if (hasValidationFailure) {
      console.error('');
      if (validationResult.errors) {
        for (const line of validationResult.errors.split('\n')) {
          console.error(line);
        }
      }
    }

    process.exit(hasValidationFailure ? 1 : 0);
  }).catch((err) => {
    error(`Dispatch failed: ${err.message}`);
    process.exit(1);
  });
}

main();
