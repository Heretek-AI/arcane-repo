#!/usr/bin/env node
/**
 * rewrite-readme.js — README.md Generator for Arcane templates
 *
 * Reads a template's docker-compose.yml, .env.example, and arcane.json
 * and generates a complete README.md with real upstream links, accurate
 * env var documentation, architecture table, troubleshooting, backup
 * and recovery sections, and a links section.
 *
 * Also updates arcane.json description to remove the generic
 * "Self-hosted X deployment via Docker" pattern.
 *
 * Usage:
 *   node scripts/rewrite-readme.js --template 2fauth --upstream-url https://github.com/2fauth/2fauth
 *   node scripts/rewrite-readme.js --all --upstream-url-file ./upstream-map.json
 *
 * Upstream URL file format (JSON):
 *   { "templateId": "https://github.com/org/repo", ... }
 */

'use strict';

const fs = require('fs');
const path = require('path');

// ── Argument parsing ──────────────────────────────────────────────────────

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {};

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--template':
        opts.template = args[++i];
        break;
      case '--upstream-url':
        opts.upstreamUrl = args[++i];
        break;
      case '--upstream-name':
        opts.upstreamName = args[++i];
        break;
      case '--all':
        opts.all = true;
        break;
      case '--upstream-url-file':
        opts.upstreamUrlFile = args[++i];
        break;
      case '--help':
      case '-h':
        opts.help = true;
        break;
    }
  }

  return opts;
}

// ── Template file readers ─────────────────────────────────────────────────

const TEMPLATES_DIR = path.join(__dirname, '..', 'templates');

function readJson(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  } catch {
    return null;
  }
}

function parseCompose(content) {
  // Normalize line endings
  content = content.replace(/\r\n/g, '\n');

  // Extract only the services: section
  const svcStart = content.search(/^services:\s*$/m);
  if (svcStart < 0) {
    return { services: [], volumes: [] };
  }

  // Find the next top-level key (line starting with word char + colon at column 0)
  const rest = content.slice(svcStart + 1); // skip the services: line
  const nextKey = rest.search(/\n\w[\w_-]*:\s*$/m);
  const svcEnd = nextKey > 0 ? svcStart + 1 + nextKey : content.length;
  const svcSection = content.slice(svcStart, svcEnd);
  const services = [];

  // Find all service blocks within the services section
  // Each service starts with "  name:" at 2-space indent
  const serviceBlockRegex = /^  (\w[\w-]*):\s*$/gm;
  let svcMatch;

  while ((svcMatch = serviceBlockRegex.exec(svcSection)) !== null) {
    const serviceName = svcMatch[1];
    const blockStart = svcMatch.index;
    const afterName = svcSection.slice(blockStart + svcMatch[0].length);
    // Find next service at same indent level, or end of section
    const nextMatch = afterName.search(/\n  \w[\w-]*:\s*$/);
    const blockEnd = nextMatch > 0 ? blockStart + svcMatch[0].length + nextMatch : svcSection.length;
    const block = svcSection.slice(blockStart, blockEnd);

    const svc = { name: serviceName };

    // Image
    const imgMatch = block.match(/^\s+image:\s+(.+)$/m);
    svc.image = imgMatch ? imgMatch[1].trim() : '';

    // Ports with env var defaults
    const portMatches = block.matchAll(/\$\{(\w[\w0-9_]*):-(\d+)\}:\d+/g);
    svc.ports = [];
    for (const pm of portMatches) {
      svc.ports.push({ var: pm[1], default: pm[2] });
    }

    // Ports without env var (direct)
    const directPorts = block.matchAll(/^\s+-\s+"?\d+:\d+"?$/gm);
    for (const dp of directPorts) {
      const p = dp[0].match(/"?(\d+):\d+/);
      if (p && svc.ports.length === 0) {
        svc.ports.push({ var: 'PORT', default: p[1] });
      }
    }

    // Volumes
    const volMatches = block.matchAll(/^\s+-\s+(\w[\w_]*):\/.*$/gm);
    svc.volumes = [];
    for (const vm of volMatches) {
      svc.volumes.push(vm[1]);
    }

    // Health check
    const hcTestMatch = block.match(/test:\s*\[.*?\]/s);
    const hcInterval = block.match(/interval:\s*(\d+)s/);
    const hcRetries = block.match(/retries:\s*(\d+)/);
    const hcStartPeriod = block.match(/start_period:\s*(\d+)s/);
    svc.healthCheck = hcTestMatch ? {
      test: hcTestMatch[0],
      interval: hcInterval ? hcInterval[1] : '30',
      retries: hcRetries ? hcRetries[1] : '3',
      startPeriod: hcStartPeriod ? hcStartPeriod[1] : '30'
    } : null;

    services.push(svc);
  }

  // Extract volumes section
  const volumes = [];
  const volSection = content.match(/^volumes:\s*\n((?:  \w[\w_-]*:.*\n?)*)/m);
  if (volSection) {
    const volLines = volSection[1].split('\n').filter(l => l.trim());
    for (const vl of volLines) {
      const vn = vl.match(/^  (\w[\w_-]*):/);
      if (vn) volumes.push(vn[1]);
    }
  }

  return { services, volumes };
}

function parseEnvExample(content) {
  const vars = [];
  const lines = content.split('\n');
  let currentComment = '';

  for (const line of lines) {
    const trimmed = line.trim();

    if (trimmed.startsWith('#')) {
      const comment = trimmed.replace(/^#\s*/, '');
      if (comment.toLowerCase().startsWith('--') || comment.toLowerCase().startsWith('copy') || comment === '') continue;
      currentComment = comment;
      continue;
    }

    const varMatch = trimmed.match(/^(\w[\w0-9_]*)=(.+)?$/);
    if (varMatch) {
      vars.push({
        var: varMatch[1],
        default: varMatch[2] || '',
        comment: currentComment
      });
      currentComment = '';
    }
  }

  return vars;
}

// ── Name helpers ──────────────────────────────────────────────────────────

function capitalize(name) {
  return name.charAt(0).toUpperCase() + name.slice(1);
}

function inferServicePurpose(name) {
  const nameLower = name.toLowerCase().replace(/[_-]/g, ' ');
  if (nameLower.includes('db') || nameLower.includes('database') || nameLower.includes('postgres') || nameLower.includes('mysql') || nameLower.includes('mariadb')) return 'Database storage';
  if (nameLower.includes('redis') || nameLower.includes('cache')) return 'Caching layer';
  if (nameLower.includes('proxy') || nameLower.includes('nginx') || nameLower.includes('caddy')) return 'Reverse proxy / web server';
  if (nameLower.includes('queue') || nameLower.includes('worker')) return 'Background job processor';
  return 'Main application service';
}

function inferDefaultDescription(templateId, name) {
  const nameLower = (name || templateId).toLowerCase();
  // Map of well-known services to descriptions
  const knownDescs = {
    'adminer': 'Lightweight web-based database management tool (MySQL, PostgreSQL, SQLite, and more)',
    'backdrop': 'Open-source content management system — a fork of Drupal focused on simplicity and ease of use',
    'caddy': 'Modern, automatic-HTTPS web server with a focus on simplicity and security',
    'couchdb': 'Open-source document-oriented NoSQL database with multi-master replication',
    'databend': 'Cloud-native data warehouse with instant elasticity and real-time query capabilities',
    'docsgpt': 'AI-powered documentation assistant — chat with your documentation using LLMs',
    'dokploy': 'Self-hosted deployment platform for applications and databases',
    'drupal': 'Powerful open-source content management framework for building websites and applications',
    'elasticsearch': 'Distributed search and analytics engine for all types of data',
    'friendica': 'Decentralized social networking platform in the Fediverse ecosystem',
    'ghost': 'Modern publishing platform for newsletters, blogs, and membership sites',
    'grafana': 'Open-source analytics and interactive visualization web application for infrastructure monitoring',
    'harness': 'AI-native software delivery platform for CI/CD, feature flags, and chaos engineering',
    'joomla': 'Award-winning open-source content management system for building websites',
    'matomo': 'Open-source web analytics platform — a privacy-friendly alternative to Google Analytics',
    'mediawiki': 'The wiki engine that powers Wikipedia — collaborative documentation platform',
    'minio': 'High-performance, S3-compatible object storage for AI and data workloads',
    'monica': 'Open-source personal relationship manager (PRM) for managing contacts',
    'nextcloud': 'Self-hosted productivity platform — files, calendar, contacts, and collaboration',
    'nginx': 'High-performance HTTP server, reverse proxy, and load balancer',
    'parseable': 'Observability platform for log analytics and event data at scale',
    'phpmyadmin': 'Popular web-based MySQL and MariaDB database administration tool',
    'prometheus': 'Open-source systems monitoring and alerting toolkit with a dimensional data model',
    'rabbitmq': 'Open-source message broker supporting multiple messaging protocols',
    'redis': 'In-memory data structure store — database, cache, and message broker',
    'teamspeak': 'Voice communication platform for gamers and communities',
    'tensorzero': 'Open platform for AI agent evaluation, testing, and monitoring',
    'test-app': 'Test template for verifying the Arcane build-registry script',
    'typesense': 'Open-source, typo-tolerant search engine with instant results',
    'ubuntu': 'Ubuntu Linux container — base operating system for development and testing',
    'weaviate': 'Open-source vector database for AI-powered semantic search applications',
    'wordpress': 'World\'s most popular content management system — powers 40%+ of the web',
    'xwiki': 'Advanced open-source enterprise wiki and collaboration platform',
    'znc': 'IRC bouncer — stays connected to IRC networks and delivers messages when you reconnect'
  };

  return knownDescs[templateId] || `${name} — self-hosted via Docker Compose`;
}

// ── README generator ──────────────────────────────────────────────────────

function generateReadme(templateId, name, upstreamUrl, upstreamName, composeData, envVars) {
  const { services, volumes } = composeData;
  const projectName = upstreamName || name || capitalize(templateId);

  // Description line
  const knownShort = {
    'adminer': 'Web-based database management tool',
    'backdrop': 'Open-source CMS — Drupal fork for simplicity',
    'caddy': 'Automatic-HTTPS web server',
    'couchdb': 'Document-oriented NoSQL database with replication',
    'databend': 'Cloud-native data warehouse',
    'docsgpt': 'AI-powered documentation assistant',
    'dokploy': 'Self-hosted deployment platform',
    'drupal': 'Open-source content management framework',
    'elasticsearch': 'Distributed search and analytics engine',
    'friendica': 'Decentralized social networking platform',
    'ghost': 'Modern publishing platform',
    'grafana': 'Open-source analytics and monitoring platform',
    'harness': 'AI-native software delivery platform',
    'joomla': 'Award-winning CMS',
    'matomo': 'Privacy-friendly web analytics',
    'mediawiki': 'Collaborative wiki platform',
    'minio': 'S3-compatible object storage',
    'monica': 'Personal relationship manager',
    'nextcloud': 'Self-hosted productivity platform',
    'nginx': 'High-performance HTTP server and reverse proxy',
    'parseable': 'Observability platform for logs',
    'phpmyadmin': 'Web-based MySQL/MariaDB administration',
    'prometheus': 'Open-source monitoring and alerting',
    'rabbitmq': 'Open-source message broker',
    'redis': 'In-memory data store and cache',
    'teamspeak': 'Voice communication platform',
    'tensorzero': 'AI agent evaluation and monitoring',
    'test-app': 'Test scaffold for Arcane build tools',
    'typesense': 'Typo-tolerant search engine',
    'ubuntu': 'Ubuntu Linux OS container',
    'weaviate': 'AI-native vector database',
    'wordpress': 'World\'s most popular CMS',
    'xwiki': 'Enterprise wiki platform',
    'znc': 'IRC bouncer'
  };
  const subtitle = knownShort[templateId] || `${projectName} — self-hosted via Docker Compose`;

  const mainService = services[0] || { name: templateId, image: '', ports: [] };
  const defaultPort = mainService.ports.length > 0 ? mainService.ports[0].default : '8080';
  const defaultPortVar = mainService.ports.length > 0 ? `$\{${mainService.ports[0].var}}` : '8080';

  let sections = [];

  // ── Architecture section ──
  let archSections = [];

  if (services.length > 0) {
    let svcTable = '| Service | Image | Purpose |\n|---------|-------|---------|\n';
    for (const s of services) {
      svcTable += `| \`${s.name}\` | \`${s.image}\` | ${inferServicePurpose(s.name)} |\n`;
    }
    archSections.push(`### Services\n\n${svcTable}`);
  }

  if (volumes.length > 0) {
    let volTable = '| Volume | Mount | Purpose |\n|--------|-------|---------|\n';
    for (const v of volumes) {
      volTable += `| \`${v}\` | (varies) | Persistent data storage |\n`;
    }
    archSections.push(`### Volumes\n\n${volTable}`);
  }

  // Health check section
  if (mainService.healthCheck) {
    const hc = mainService.healthCheck;
    archSections.push(`### Health Check\n\nThe container runs a health check every ${hc.interval}s (${hc.retries} retries, ${hc.startPeriod}s start period). Docker will report the container as unhealthy if the endpoint fails consistently.\n`);
  }

  archSections.push(`### Networks\n\nUses the default Docker bridge network. If you need to connect to other services (databases, APIs, reverse proxy), attach it to a shared Docker network.\n`);

  const architectureBlock = archSections.join('\n');

  // ── Quick Start ──
  const quickStart = `## Quick Start

### 1. Configure environment

\`\`\`bash
cp .env.example .env
# Edit .env with your configuration
\`\`\`

### 2. Start the service

\`\`\`bash
docker compose up -d
\`\`\`

### 3. Verify it's running

\`\`\`bash
docker compose ps
curl -s http://localhost:${defaultPort}/ | head -c 200
\`\`\`

### 4. Access the application

Open [http://localhost:${defaultPort}](http://localhost:${defaultPort}) in your browser.`;

  // ── Configuration Reference ──
  let envTable = '| Variable | Default | Description |\n|----------|---------|-------------|\n';
  if (envVars.length > 0) {
    for (const ev of envVars) {
      const desc = ev.comment || `${ev.var} configuration value`;
      envTable += `| \`${ev.var}\` | \`${ev.default || '—'}\` | ${desc} |\n`;
    }
  } else {
    envTable += '| (none) | — | No environment variables defined |\n';
  }

  const configBlock = `## Configuration Reference

### Environment Variables

Set these in your \`.env\` file (copy from \`.env.example\`):

${envTable}`;

  // ── Troubleshooting ──
  const troubleshooting = `## Troubleshooting

### Container won't start

Check the logs for error messages:

\`\`\`bash
docker compose logs
\`\`\`

### Port conflict

If the default port ${defaultPort} is already in use, change it in \`.env\` and restart:

\`\`\`bash
# Edit .env and change to an available port
docker compose down && docker compose up -d
\`\`\`

### Health check shows unhealthy

The container may need more time to start on first run or low-resource hosts. Check the logs:

\`\`\`bash
docker compose logs
\`\`\`

If needed, increase \`start_period\` in \`docker-compose.yml\`.

### Permission errors

Ensure the Docker user has write access to the data volume:

\`\`\`bash
docker compose exec ${mainService.name} ls -la /data 2>/dev/null || echo "Volume directory not accessible"
\`\`\``;

  // ── Backup & Recovery ──
  const firstVolName = volumes.length > 0 ? volumes[0] : `${templateId}_data`;

  const backup = `## Backup & Recovery

### Backup

Stop the service to ensure data consistency, then back up the data volume:

\`\`\`bash
docker compose down
docker run --rm -v ${firstVolName}:/data -v $(pwd):/backup alpine \\
  tar czf /backup/${templateId}-backup-\$(date +%Y%m%d).tar.gz -C /data .
docker compose up -d
\`\`\`

### Recovery

\`\`\`bash
docker compose down
docker run --rm -v ${firstVolName}:/data -v $(pwd):/backup alpine \\
  tar xzf /backup/${templateId}-backup-YYYYMMDD.tar.gz -C /data
docker compose up -d
\`\`\``;

  // ── Links section ──
  const linksBlock = `## Project Homepage

- **Project site:** [${projectName}](${upstreamUrl})
- **Docker Image:** \`${mainService.image}\`
- **Issues:** [GitHub Issues](${upstreamUrl.replace(/\/$/, '')}/issues)

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage`;

  // ── Assemble ──
  const readme = `# ${projectName}

${subtitle}

## Project Overview

[${projectName}](${upstreamUrl}) is a self-hosted deployment packaged as a Docker Compose template. This template provides everything needed to run ${projectName} in a containerized environment with persistent storage, health checks, and environment-based configuration.

## Architecture

${architectureBlock}
${quickStart}

${configBlock}

${troubleshooting}

${backup}

${linksBlock}
`;

  return readme;
}

// ── Write README and update arcane.json ──

function writeReadme(templateDir, readmeContent) {
  const readmePath = path.join(templateDir, 'README.md');
  fs.writeFileSync(readmePath, readmeContent, 'utf-8');
  return readmePath;
}

function updateArcaneJson(templateDir, templateId, name, upstreamUrl) {
  const arcanePath = path.join(templateDir, 'arcane.json');
  const data = readJson(arcanePath);
  if (!data) {
    console.error(`  ⚠ No arcane.json found at ${arcanePath}, skipping description update`);
    return;
  }

  // Update description to remove generic pattern
  const newDesc = inferDefaultDescription(templateId, name);
  if (data.description !== newDesc) {
    const oldDesc = data.description;
    data.description = newDesc;
    fs.writeFileSync(arcanePath, JSON.stringify(data, null, 2) + '\n', 'utf-8');
    console.log(`  ✓ Updated description: "${oldDesc.slice(50)}..." → "${newDesc.slice(50)}..."`);
  } else {
    console.log(`  - Description already correct`);
  }
}

// ── Self-verification ──

function verifyReadme(readmePath, upstreamUrl, envVarCount) {
  const content = fs.readFileSync(readmePath, 'utf-8');
  const issues = [];

  // Check section count (## headings)
  const sectionCount = (content.match(/^## /gm) || []).length;
  if (sectionCount < 6) {
    issues.push(`Only ${sectionCount} sections (expected >= 6)`);
  }

  // Check upstream URL is present
  if (!content.includes(upstreamUrl)) {
    issues.push(`Upstream URL "${upstreamUrl}" not found in README`);
  }

  // Check env var documentation
  if (envVarCount > 0 && content.includes('| `') === false) {
    issues.push('No environment variables documented in table');
  }

  return {
    issues,
    sectionCount,
    pass: issues.length === 0
  };
}

// ── Process a single template ──

function processTemplate(templateId, upstreamUrl, upstreamName) {
  const templateDir = path.join(TEMPLATES_DIR, templateId);

  if (!fs.existsSync(templateDir)) {
    console.error(`  ✗ Template directory not found: ${templateId}`);
    return false;
  }

  // Read template files
  const arcanePath = path.join(templateDir, 'arcane.json');
  const composePath = path.join(templateDir, 'docker-compose.yml');
  const envPath = path.join(templateDir, '.env.example');

  const arcane = readJson(arcanePath);
  const name = (arcane && arcane.name) || capitalize(templateId);

  if (!fs.existsSync(composePath)) {
    console.error(`  ✗ docker-compose.yml not found for ${templateId}`);
    return false;
  }

  // Parse compose and env
  const composeContent = fs.readFileSync(composePath, 'utf-8');
  const composeData = parseCompose(composeContent);

  const envContent = fs.existsSync(envPath) ? fs.readFileSync(envPath, 'utf-8') : '';
  const envVars = parseEnvExample(envContent);

  // Generate README
  const upstreamDisplayName = upstreamName || name;
  const readmeContent = generateReadme(templateId, name, upstreamUrl, upstreamDisplayName, composeData, envVars);

  // Write
  const readmePath = writeReadme(templateDir, readmeContent);
  console.log(`  ✓ README written: ${path.relative(process.cwd(), readmePath)}`);

  // Update arcane.json description
  updateArcaneJson(templateDir, templateId, name, upstreamUrl);

  // Verify
  const verification = verifyReadme(readmePath, upstreamUrl, envVars.length);
  if (verification.pass) {
    console.log(`  ✓ Self-verification passed (${verification.sectionCount} sections, ${envVars.length} env vars documented)`);
  } else {
    console.log(`  ⚠ Self-verification issues: ${verification.issues.join(', ')}`);
  }

  return verification.pass;
}

// ── Main ──

function main() {
  const opts = parseArgs();

  if (opts.help) {
    console.log(`
Usage: node scripts/rewrite-readme.js [options]

Options:
  --template <id>               Template ID to process (e.g. 2fauth)
  --upstream-url <url>          Upstream project URL (e.g. https://github.com/2fauth/2fauth)
  --upstream-name <name>        Upstream project display name (optional)
  --all                         Process all templates from a URL mapping file
  --upstream-url-file <path>    JSON file with template -> upstream URL mappings
  --help                        Show this help

Examples:
  node scripts/rewrite-readme.js --template adminer --upstream-url https://github.com/vrana/adminer --upstream-name Adminer
  node scripts/rewrite-readme.js --all --upstream-url-file ./upstream-map.json
`);
    process.exit(0);
  }

  if (opts.all) {
    if (!opts.upstreamUrlFile) {
      console.error('Error: --all requires --upstream-url-file <path>');
      process.exit(1);
    }

    const urlMap = readJson(opts.upstreamUrlFile);
    if (!urlMap) {
      console.error(`Error: Could not read upstream URL file: ${opts.upstreamUrlFile}`);
      process.exit(1);
    }

    const ids = Object.keys(urlMap);
    console.log(`Processing ${ids.length} templates...\n`);

    let passed = 0;
    let failed = 0;

    for (const id of ids) {
      const url = urlMap[id];
      // Object value could be a string or { url, name }
      const upstreamUrl = typeof url === 'string' ? url : url.url;
      const upstreamName = typeof url === 'object' ? url.name : undefined;

      console.log(`[${id}]`);
      const ok = processTemplate(id, upstreamUrl, upstreamName);
      if (ok) passed++;
      else failed++;
      console.log();
    }

    console.log(`\nDone. ${passed} succeeded, ${failed} failed.`);
    process.exit(failed > 0 ? 1 : 0);

  } else if (opts.template && opts.upstreamUrl) {
    const ok = processTemplate(opts.template, opts.upstreamUrl, opts.upstreamName);
    process.exit(ok ? 0 : 1);

  } else {
    console.error('Error: Provide --template + --upstream-url, or --all + --upstream-url-file');
    console.error('Run with --help for usage.');
    process.exit(1);
  }
}

main();
