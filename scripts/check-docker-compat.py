"""Batch-check GitHub repos for Docker compatibility."""
import urllib.request, urllib.error, json, sys, re

REPOS = [
    # AI/Agent frameworks
    ("web-infra-dev/midscene", "AI-driven browser automation/testing"),
    ("microsoft/RD-Agent", "Research & development agent by Microsoft"),
    ("puckeditor/puck", "Visual editor for React (drag-drop page builder)"),
    ("neuml/txtai", "AI-powered semantic search and RAG platform"),
    ("pipecat-ai/pipecat", "Voice AI agent framework (real-time audio)"),
    ("Zackriya-Solutions/meetily", "Meeting transcription/assistant"),
    ("dataelement/bisheng", "Open-source LLM ops platform"),
    ("tensorzero/tensorzero", "A/B testing for LLM outputs"),
    ("kyegomez/OpenMythos", "Swarm intelligence agents framework"),
    ("wandb/wandb", "ML experiment tracking (CLI + Python)"),
    ("livekit/agents", "Voice agent framework for LiveKit"),
    ("replicate/cog", "Docker containers for ML models (tool)"),
    ("databendlabs/databend", "Cloud data warehouse (Rust)"),
    ("evilsocket/pwnagotchi", "Wi-Fi pentesting device (RPi)"),
    ("lencx/Noi", "AI-powered browser/desktop app (Tauri)"),
    ("topoteretes/cognee", "Cognitivie graph memory for AI"),
    ("khoj-ai/khoj", "AI second brain (desktop app)"),
    ("typesense/typesense", "Typo-tolerant search engine (C++)"),
    ("deepset-ai/haystack", "NLP framework (LLM pipelines)"),
    ("arc53/DocsGPT", "Docs chatbot with RAG"),
    ("weaviate/weaviate", "Vector database (Go)"),
    ("Tencent/WeKnora", "Knowledge graph platform"),
    ("triggerdotdev/trigger.dev", "Background jobs framework"),
    ("botpress/botpress", "Chatbot builder platform"),
    ("onyx-dot-app/onyx", "Enterprise search/knowledge platform"),
    ("mlflow/mlflow", "ML lifecycle platform"),
    ("elizaOS/eliza", "AI agent framework (TypeScript)"),
    ("agent0ai/agent-zero", "Autonomous AI coding agent"),
    ("SillyTavern/SillyTavern", "LLM chat interface (web app)"),
    ("assafelovic/gpt-researcher", "Autonomous research agent"),
    ("facefusion/facefusion", "Face fusion/synthesis (desktop app)"),
    ("simstudioai/sim", "AI agent simulation platform"),
    ("onlook-dev/onlook", "Visual editor for React apps"),
    ("sinaptik-ai/pandas-ai", "AI data analysis (Python library)"),
    ("charmbracelet/crush", "Terminal UI (TUI) chat app"),
    ("alibaba/page-agent", "Autonomous web agent"),
    ("alibaba/OpenSandbox", "Sandboxed code execution"),
    ("modular/modular", "Mojo programming language"),
    ("milvus-io/milvus", "Vector database (distributed)"),
    ("unum-cloud/USearch", "Vector search library"),
    ("zilliztech/knowhere", "Vector similarity engine"),
    ("logseq/logseq", "Knowledge management (desktop app)"),
    ("OpenSPG/KAG", "Knowledge-augmented generation"),
    ("go-vgo/robotgo", "Desktop automation (Go library)"),
    ("codota/TabNine", "Code completion (AI)"),
    # Binary analysis / RE tools
    ("We5ter/Scanners-Box", "Security scanner collection (list)"),
    ("cmu-sei/pharos", "Binary analysis framework"),
    ("redasm-dev/redasm", "Disassembler (desktop app)"),
    ("m4b/goblin", "Binary parsing library (Rust)"),
    ("dyninst/dyninst", "Binary instrumentation library"),
    ("GrammaTech/ddisasm", "Disassembler (Rust)"),
    ("zrax/pycdc", "Python decompiler"),
    ("rocky/python-uncompyle6", "Python decompiler library"),
    ("uxmal/reko", "Decompiler (.NET/Java)"),
    ("Jon-Becker/heimdall-rs", "EVM smart contract analyzer"),
    ("rizinorg/rz-ghidra", "Rizin + Ghidra integration"),
    ("binsync/binsync", "Binary analysis sync (plugin)"),
    ("joernio/joern", "Code analysis platform"),
    ("bethington/ghidra-mcp", "Ghidra MCP server"),
    ("symgraph/GhidrAssist", "AI assistant for Ghidra"),
    ("symgraph/GhidrAssistMCP", "MCP server for GhidrAssist"),
    ("sjkim1127/Fission", "Binary diffing tools"),
    ("toolCHAINZ/jingle", "Binary-related tool"),
    # Edge case / misc
    ("666ghj/MiroFish", "Unknown/personal project"),
    ("safishamsi/graphify", "Graph visualization tool"),
    ("TriliumNext/Trilium", "Note-taking app (fork)"),
    ("Lum1104/Understand-Anything", "Code understanding tool"),
    ("RyanCodrai/turbovec", "Vector search related"),
    ("MinishLab/vicinity", "Similarity search library"),
    ("sb-ai-lab/HypEx", "Hypothesis exploration"),
    ("yichuan-w/LEANN", "Research project"),
    ("AsyncFuncAI/deepwiki-open", "Personal knowledge base"),
    ("memvid/memvid", "Video generation from memories"),
    ("raymondmdzz123/agent-memory", "Agent memory experiments"),
    ("VectifyAI/PageIndex", "Web page indexing"),
    ("DayuanJiang/next-ai-draw-io", "AI drawing tool"),
    ("Fosowl/agenticSeek", "Agent search experiments"),
    ("jamiepine/voicebox", "Voice assistant"),
    ("iOfficeAI/AionUi", "AI office UI"),
    ("InsForge/InsForge", "Unknown project"),
    ("SylphAI-Inc/AdalFlow", "LLM workflow optimization"),
    ("TEN-framework/ten-framework", "Real-time voice AI framework"),
    ("ShaneBreazeale/rsleigh", "SLEIGH disassembler (Rust)"),
    ("naim94a/lumen", "Binary analysis tool"),
]

def check(repo):
    """Check a repo for Docker compatibility signals."""
    result = {"repo": repo, "exists": False, "has_df": False, "has_compose": False, 
              "has_df_in_docker": False, "desc": "", "is_list": False, "is_lib": False,
              "is_desktop": False, "is_cli": False, "needs_build": False}
    
    # Quick skip known types from the label
    known_label = KNOWN.get(repo, "")
    if known_label:
        result["known_type"] = known_label
    
    # Check repo exists
    try:
        u = urllib.request.urlopen(f"https://api.github.com/repos/{repo}", timeout=5)
        data = json.loads(u.read())
        result["exists"] = True
        result["desc"] = data.get("description", "")
    except:
        result["desc"] = "(API limit - using known info)"
        # Still try rawgit checks even if API fails
    
    # Check for Dockerfile
    for branch in ["main", "master"]:
        try:
            u = urllib.request.urlopen(f"https://raw.githubusercontent.com/{repo}/{branch}/Dockerfile", timeout=5)
            result["has_df"] = True
            break
        except:
            pass
    
    # Check docker-compose.yml
    for branch in ["main", "master"]:
        try:
            u = urllib.request.urlopen(f"https://raw.githubusercontent.com/{repo}/{branch}/docker-compose.yml", timeout=5)
            result["has_compose"] = True
            break
        except:
            pass
    
    # Check docker/Dockerfile
    for branch in ["main", "master"]:
        try:
            u = urllib.request.urlopen(f"https://raw.githubusercontent.com/{repo}/{branch}/docker/Dockerfile", timeout=5)
            result["has_df_in_docker"] = True
            break
        except:
            pass
    
    return result

def classify(r):
    """Classify a repo by Docker compatibility."""
    repo = r["repo"]
    name = repo.split("/")[1].lower()
    desc = r["desc"].lower() if r["desc"] else ""
    
    # Signal words
    cli_sig = any(w in desc + name for w in ["cli", "terminal", "tui", "command-line", "library", "sdk"])
    lib_sig = any(w in desc for w in ["library", "sdk for", "python package", "npm package", "crate"])
    desktop_sig = any(w in desc for w in ["desktop app", "electron", "tauri", "gui"])
    list_sig = any(w in desc for w in ["list", "collection", "awesome", "curated"])
    
    has_df = r["has_df"] or r["has_df_in_docker"]
    has_compose = r["has_compose"]
    
    if list_sig or name in ["awesome-langchain", "awesome-ai-apps", "scanners-box"]:
        return "📋 LIST/COLLECTION — not buildable"
    
    # Well-known project types
    known = r.get("known_type", "")
    
    cli_lib_desktop = ["replicate/cog", "wandb/wandb", "sinaptik-ai/pandas-ai", 
                       "charmbracelet/crush", "go-vgo/robotgo", "codota/TabNine",
                       "m4b/goblin", "rocky/python-uncompyle6", "zrax/pycdc",
                       "dyninst/dyninst", "unum-cloud/USearch", "zilliztech/knowhere",
                       "logseq/logseq", "lencx/Noi", "facefusion/facefusion",
                       "onlook-dev/onlook", "neuml/txtai", "assafelovic/gpt-researcher",
                       "typesense/typesense"]
    
    if repo in cli_lib_desktop:
        return "🔧 CLI/LIB/DESKTOP — low Docker suitability"
    
    # Has Dockerfile or docker-compose = natively Docker-compatible
    if has_df or has_compose:
        return "🐳 DOCKER-READY (has Dockerfile/compose in repo)"
    
    # Service-type projects that SHOULD be Dockerized
    services = ["milvus-io/milvus", "weaviate/weaviate", "typesense/typesense",
                "databendlabs/databend", "deepset-ai/haystack", "botpress/botpress",
                "livekit/agents", "ten-framework/ten-framework", "modular/modular",
                "pipecat-ai/pipecat", "elizaOS/eliza", "agent0ai/agent-zero"]
    
    if repo in services:
        return "🔧 SERVICE — Dockerizable, may have official image"
    
    return "🤷 UNCLEAR — needs deeper look"

# Known labels
KNOWN = {}
for name, label in [
    ("web-infra-dev/midscene", "AI browser automation — should be Dockerizable"),
    ("microsoft/RD-Agent", "Research dev agent — service?")]:
    KNOWN[name] = label

results = []
for repo, hint in REPOS:
    r = check(repo)
    r["hint"] = hint
    results.append(r)
    print(f"=== {repo} ===")
    print(f"  Desc: {r['desc'][:80] if r['desc'] else '(none)'}")
    print(f"  Has Dockerfile: {r['has_df']} | Has compose: {r['has_compose']} | In docker/: {r['has_df_in_docker']}")
    print(f"  Classify: {classify(r)}")
    print()
