const fs = require('fs');
const https = require('https');

const existing = new Set(
  fs.readdirSync('templates/').filter(f => fs.statSync('templates/' + f).isDirectory())
);

function normalize(name) {
  return name.toLowerCase().replace(/[^a-z0-9]/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '');
}

function getUrl(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'Arcane-Audit/1.0' } }, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => resolve(d));
    }).on('error', reject);
  });
}

(async () => {
  const all = new Map(); // normalized -> {name, source, description, link, stars}

  function add(name, source, desc, link, stars) {
    const n = normalize(name);
    if (!n || n.length < 2 || existing.has(n) || all.has(n)) return;
    // Skip common non-serviceable names
    const skips = ['test-', 'example-', 'template-', '(container)', '(stack)'];
    for (const s of skips) if (n.includes(s)) return;
    if (n.startsWith('test-')) return;
    
    all.set(n, {
      name: n,
      originalName: name,
      source: source,
      description: (desc || '').slice(0, 120).replace(/```/g, '').replace(/`/g, ''),
      link: link || '',
      stars: stars || 0
    });
  }

  // 1. Portainer templates
  console.log('Fetching Portainer templates...');
  const portainerRaw = await getUrl('https://raw.githubusercontent.com/Lissy93/portainer-templates/main/templates.json');
  const portainer = JSON.parse(portainerRaw);
  for (const t of (portainer.templates || [])) {
    const name = t.title || t.name || '';
    if (!name || name.includes('(container)') || name.includes('(stack)')) continue;
    const imgs = t.image || (t.images && Array.isArray(t.images) ? t.images.map(i => i.image || i).filter(Boolean).join(', ') : '');
    add(name, 'Portainer', `${t.description || ''}${imgs ? ' | image: ' + imgs.slice(0, 60) : ''}`, '');
  }

  // 2. Awesome-selfhosted
  console.log('Fetching awesome-selfhosted...');
  const awesomeRaw = await getUrl('https://raw.githubusercontent.com/awesome-selfhosted/awesome-selfhosted/master/README.md');
  for (const line of awesomeRaw.split('\n')) {
    const match = line.match(/^\s*-\s*\[([^\]]+)\]\((https?:\/\/[^)]+)\)\s*-\s*(.+)$/);
    if (!match) continue;
    if (!line.includes('`Docker`') && !line.includes('`docker`')) continue;
    add(match[1].trim(), 'awesome-selfhosted', match[3].replace(/`[^`]*`/g, '').trim(), match[2], 0);
  }

  // 3. Umbrel app store
  console.log('Fetching Umbrel apps...');
  const umbrelTree = await getUrl('https://api.github.com/repos/getumbrel/umbrel-apps/git/trees/master?recursive=1');
  const umbrelJson = JSON.parse(umbrelTree);
  if (umbrelJson.tree) {
    const ymls = umbrelJson.tree.filter(t => t.path.endsWith('/umbrel-app.yml'));
    for (const entry of ymls) {
      const appName = entry.path.replace('/umbrel-app.yml', '');
      add(appName, 'Umbrel', '', `https://github.com/getumbrel/umbrel-apps/tree/master/${appName}`, 0);
    }
  }

  // 3b. YunoHost apps
  console.log('Fetching YunoHost apps...');
  try {
    const yunohostRaw = await getUrl('https://raw.githubusercontent.com/YunoHost/apps/master/apps.toml');
    for (const line of yunohostRaw.split('\n')) {
      const m = line.match(/^\[([^\]]+)\]/);
      if (m) {
        add(m[1].trim(), 'YunoHost', 'App from YunoHost catalog', `https://apps.yunohost.org/app/${m[1].trim()}`, 0);
      }
    }
  } catch(e) {
    console.log('YunoHost not available:', e.message);
  }

  // 4. GitHub search candidates
  const githubCandidates = [
    ['uptime-kuma', 'https://github.com/louislam/uptime-kuma', 86067, 'Fancy self-hosted monitoring tool'],
    ['Stirling-PDF', 'https://github.com/Stirling-Tools/Stirling-PDF', 78017, 'PDF editor - edit PDFs on any device anywhere'],
    ['coolify', 'https://github.com/coollabsio/coolify', 54429, 'Self-hostable PaaS alternative to Vercel, Heroku, Netlify'],
    ['plane', 'https://github.com/makeplane/plane', 48565, 'Open-source Jira/Linear alternative - project management'],
    ['mastodon', 'https://github.com/mastodon/mastodon', 49893, 'Self-hosted microblogging community'],
    ['gogs', 'https://github.com/gogs/gogs', 47503, 'Painless self-hosted Git service'],
    ['outline', 'https://github.com/outline/outline', 38338, 'Fastest knowledge base for growing teams - wiki'],
    ['ToolJet', 'https://github.com/ToolJet/ToolJet', 37819, 'Open-source low-code platform for internal tools and AI agents'],
    ['Sunshine', 'https://github.com/LizardByte/Sunshine', 36554, 'Self-hosted game stream host for Moonlight'],
    ['harness', 'https://github.com/harness/harness', 35400, 'Developer platform with SCM, CI/CD, Environments'],
    ['trivy', 'https://github.com/aquasecurity/trivy', 34785, 'Vulnerability, misconfig, secrets scanner for containers'],
    ['CasaOS', 'https://github.com/IceWhaleTech/CasaOS', 33746, 'Simple open-source Personal Cloud system'],
    ['dokploy', 'https://github.com/Dokploy/dokploy', 33630, 'Open source alternative to Vercel, Netlify and Heroku'],
    ['one-api', 'https://github.com/songquanpeng/one-api', 32751, 'LLM API management and redistribution proxy for 20+ providers'],
    ['dokku', 'https://github.com/dokku/dokku', 31870, 'Docker-powered PaaS - heroku-like'],
    ['AstrBot', 'https://github.com/AstrBotDevs/AstrBot', 31057, 'AI Agent Assistant integrating IM platforms, LLMs, plugins'],
    ['llm-app-pathway', 'https://github.com/pathwaycom/llm-app', 59872, 'Ready-to-run cloud templates for RAG, AI pipelines, enterprise search'],
    ['TrendRadar', 'https://github.com/sansan0/TrendRadar', 55897, 'AI-driven opinion and trend monitor with RSS aggregation'],
    ['chatwoot', 'https://github.com/chatwoot/chatwoot', 28952, 'Open-source live-chat, email support, omni-channel desk'],
    ['colima', 'https://github.com/abiosoft/colima', 28575, 'Container runtimes on macOS and Linux with minimal setup'],
    ['authelia', 'https://github.com/authelia/authelia', 27661, 'SSO Multi-Factor portal for web apps'],
    ['watchtower', 'https://github.com/containrrr/watchtower', 24602, 'Automating Docker container base image updates'],
    ['firefly-iii', 'https://github.com/firefly-iii/firefly-iii', 23113, 'Personal finances manager'],
    ['slimtoolkit', 'https://github.com/slimtoolkit/slim', 23169, 'Minify container images by up to 30x and make them secure'],
    ['jina-serve', 'https://github.com/jina-ai/serve', 21876, 'Build multimodal AI applications with cloud-native stack'],
    ['beszel', 'https://github.com/henrygd/beszel', 21473, 'Lightweight server monitoring with docker stats and alerts'],
    ['vulhub', 'https://github.com/vulhub/vulhub', 20612, 'Pre-Built Vulnerable Environments based on Docker-Compose'],
    ['RustScan', 'https://github.com/bee-san/RustScan', 19698, 'The Modern Port Scanner'],
    ['docker-elk', 'https://github.com/deviantony/docker-elk', 18337, 'The Elastic stack (ELK) powered by Docker and Compose'],
    ['ctop', 'https://github.com/bcicen/ctop', 17716, 'Top-like interface for container metrics'],
    ['ory-hydra', 'https://github.com/ory/hydra', 17104, 'OAuth2.0 and OpenID Connect provider - trusted by OpenAI'],
    ['rook', 'https://github.com/rook/rook', 13480, 'Storage Orchestration for Kubernetes'],
    ['FlareSolverr', 'https://github.com/FlareSolverr/FlareSolverr', 13707, 'Proxy server to bypass Cloudflare protection'],
    ['bentopdf', 'https://github.com/alam00000/bentopdf', 13004, 'The Privacy First PDF Toolkit'],
    ['bunkerweb', 'https://github.com/bunkerity/bunkerweb', 10372, 'Open-source cloud-native Web Application Firewall'],
    ['laradock', 'https://github.com/laradock/laradock', 12667, 'Full PHP development environment for Docker'],
    ['mailcow', 'https://github.com/mailcow/mailcow-dockerized', 12657, 'Mail server suite - dockerized'],
    ['grype', 'https://github.com/anchore/grype', 12112, 'Vulnerability scanner for container images and filesystems'],
    ['sftpgo', 'https://github.com/drakkan/sftpgo', 11994, 'Full-featured SFTP, HTTP/S, FTP/S and WebDAV server'],
    ['whoogle-search', 'https://github.com/benbusby/whoogle-search', 11495, 'Self-hosted ad-free privacy-respecting metasearch engine'],
    ['nginx-ui', 'https://github.com/0xJacky/nginx-ui', 11097, 'WebUI for Nginx with Lets Encrypt, MCP server'],
    ['bytebot', 'https://github.com/bytebot-ai/bytebot', 10977, 'Self-hosted AI desktop agent in containerized Linux desktop'],
    ['gatus', 'https://github.com/TwiN/gatus', 10802, 'Automated status page with alerting and incident support'],
    ['openebs', 'https://github.com/openebs/openebs', 9726, 'Container Native Storage for Stateful Apps on K8s'],
    ['cog', 'https://github.com/replicate/cog', 9407, 'Containers for machine learning (by Replicate)'],
    ['sentry-selfhosted', 'https://github.com/getsentry/self-hosted', 9317, 'Sentry packaged for low volume deployments'],
    ['tpotce', 'https://github.com/telekom-security/tpotce', 9124, 'T-Pot All In One Multi Honeypot Platform'],
    ['kata-containers', 'https://github.com/kata-containers/kata-containers', 7832, 'Lightweight VMs that feel like containers'],
    ['CompreFace', 'https://github.com/exadel-inc/CompreFace', 7904, 'Leading free open-source face recognition system'],
    ['Wallos', 'https://github.com/ellite/Wallos', 7752, 'Self-hostable personal subscription tracker'],
    ['Woodpecker', 'https://github.com/woodpecker-ci/woodpecker', 6910, 'Simple yet powerful CI/CD engine'],
    ['flagsmith', 'https://github.com/Flagsmith/flagsmith', 6328, 'Open source feature flagging and remote config service'],
    ['matrix-server', 'https://github.com/spantaleev/matrix-docker-ansible-deploy', 6332, 'Matrix server setup with Ansible and Docker'],
    ['pachyderm', 'https://github.com/pachyderm/pachyderm', 6298, 'Data-Centric Pipelines and Data Versioning'],
    ['komga', 'https://github.com/gotson/komga', 6192, 'Media server for comics, mangas, BDs, eBooks'],
    ['mailu', 'https://github.com/Mailu/Mailu', 7182, 'Email distribution - mail server as Docker images'],
    ['telepresence', 'https://github.com/telepresenceio/telepresence', 7195, 'Local dev against remote Kubernetes cluster'],
    ['microsandbox', 'https://github.com/superradcompany/microsandbox', 5900, 'Secure local programmable sandboxes for AI agents'],
    ['ufw-docker', 'https://github.com/chaifeng/ufw-docker', 6502, 'Fix Docker and UFW security flaw'],
    ['dockprom', 'https://github.com/stefanprodan/dockprom', 6507, 'Docker monitoring with Prometheus, Grafana, cAdvisor'],
    ['photoview', 'https://github.com/photoview/photoview', 6408, 'Photo gallery for self-hosted personal servers'],
    ['Pulse', 'https://github.com/rcourtman/Pulse', 5542, 'Real-time monitoring with AI-powered insights'],
    ['music-tag-web', 'https://github.com/xhongc/music-tag-web', 5654, 'Music tag editor for local music file metadata'],
    ['libreddit', 'https://github.com/libreddit/libreddit', 5192, 'Private front-end for Reddit'],
    ['Yuxi', 'https://github.com/xerrors/Yuxi', 5059, 'Multi-tenant Agent Harness with LightRAG, Neo4j, MCP'],
    ['sun-panel', 'https://github.com/hslr-s/sun-panel', 5104, 'Server/NAS navigation panel and browser homepage'],
    ['wgcloud', 'https://github.com/tianshiyeben/wgcloud', 5130, 'Linux monitoring tool'],
    ['uncloud', 'https://github.com/psviderski/uncloud', 5128, 'Deploy and manage containerised apps across Docker hosts'],
    ['RedInk', 'https://github.com/HisMax/RedInk', 5201, 'Image-and-text generator (Xiaohongshu style)'],
    ['Calibre-Web-Automated', 'https://github.com/crocodilestick/Calibre-Web-Automated', 5495, 'Calibre-Web Automated with new features'],
    ['YunoHost', 'https://github.com/YunoHost/yunohost', 0, 'Server OS aiming to make self-hosting accessible to everyone'],
    ['databasus', 'https://github.com/databasus/databasus', 6628, 'Database backup tool (PostgreSQL, MySQL, MongoDB)'],
    ['pytorch-serve', 'https://github.com/pytorch/serve', 4360, 'Serve, optimize and scale PyTorch models in production'],
    ['ezbookkeeping', 'https://github.com/mayswind/ezbookkeeping', 4721, 'Lightweight self-hosted personal finance app'],
    ['Streamer-Sales', 'https://github.com/PeterH0323/Streamer-Sales', 3684, 'AI livestream sales LLM with TTS, digital human, RAG'],
    ['planka', 'https://github.com/plankanban/planka', 11917, 'Kanban-style project mastering tool - Trello alternative'],
    ['zipline', 'https://github.com/diced/zipline', 3113, 'ShareX/file upload server with gallery'],
    ['speedtest-tracker', 'https://github.com/alexjustesen/speedtest-tracker', 5591, 'Self-hosted internet performance monitoring'],
    ['docker-ipsec-vpn', 'https://github.com/hwdsl2/docker-ipsec-vpn-server', 7060, 'IPsec VPN server as Docker image'],
    ['xiaomusic', 'https://github.com/hanxi/xiaomusic', 9796, 'XiaoAi speaker music player with yt-dlp'],
    ['neko', 'https://github.com/m1k1o/neko', 20723, 'Self hosted virtual browser using WebRTC'],
    ['shynet', 'https://github.com/milesmcc/shynet', 3133, 'Privacy-friendly web analytics without cookies or JS'],
    ['tianji', 'https://github.com/msgbyte/tianji', 3034, 'Website analytics, uptime monitor, server status'],
    ['parseable', 'https://github.com/parseablehq/parseable', 2365, 'Observability datalake built from first principles'],
    ['harbor-llm', 'https://github.com/av/harbor', 2890, 'One command brings complete pre-wired LLM stack'],
    ['cc-gateway', 'https://github.com/motiful/cc-gateway', 2724, 'AI API identity gateway - privacy-preserving reverse proxy'],
    ['Misago', 'https://github.com/rafalp/Misago', 2721, 'Modern Django forum application'],
    ['docker-flare', 'https://github.com/soulteary/docker-flare', 2133, 'Lightweight self-hosted navigation/bookmark page'],
    ['oras', 'https://github.com/oras-project/oras', 2241, 'OCI registry client for artifacts, images, packages'],
    ['NoteDiscovery', 'https://github.com/gamosoft/NoteDiscovery', 2465, 'Self-hosted knowledge base (Evernote alternative)'],
    ['opengist', 'https://github.com/thomiceli/opengist', 3108, 'Self-hosted pastebin powered by Git (Gist alternative)'],
    ['gonic', 'https://github.com/sentriz/gonic', 2370, 'Music streaming server (Subsonic API)'],
    ['mirotalksfu', 'https://github.com/miroslavpejic85/mirotalksfu', 2954, 'Self-hosted WebRTC video conferencing platform'],
    ['sismics-docs', 'https://github.com/sismics/docs', 2545, 'Lightweight document management system'],
  ];
  for (const [name, link, stars, desc] of githubCandidates) {
    add(name, 'GitHub', desc, link, stars);
  }

  console.log('\n=== FINAL SUMMARY ===');
  console.log(`Total unique candidates: ${all.size}`);
  console.log('Sources: ' + Array.from(new Set(Array.from(all.values()).map(e => e.source))).join(', '));

  // Write CANDIDATES.md organized by tags/categories
  const entries = Array.from(all.values()).sort((a, b) => (b.stars || 0) - (a.stars || 0));
  
  let md = '# Arcane Template Candidates\n\n';
  md += `**Total: ${all.size} candidates** found across Portainer (524 templates), awesome-selfhosted, Umbrel (328 apps), and GitHub search.\n\n`;
  md += `Cross-referenced against **${existing.size} existing templates** — duplicates and already-existing templates are excluded.\n\n`;
  md += `<details>\n<summary>Source breakdown</summary>\n\n`;
  const bySrc = {};
  for (const e of entries) bySrc[e.source] = (bySrc[e.source] || 0) + 1;
  for (const [s, c] of Object.entries(bySrc).sort((a, b) => b[1] - a[1])) {
    md += `- **${s}**: ${c}\n`;
  }
  md += `</details>\n\n---\n\n`;
  
  // Write full list
  entries.forEach((e, i) => {
    md += `${i + 1}. **${e.originalName}** (${e.source})${e.stars ? ' — ' + e.stars.toLocaleString() + '\u2605' : ''} — ${e.description || '(no description)'}${e.link ? `\n   ${e.link}` : ''}\n`;
    if (i < 10 || e.stars > 5000) { } // all get printed
  });
  // Actually, write all
  // (The .md file will have all entries)
  fs.writeFileSync('CANDIDATES.md', md);
  
  // Also write deduplicated JSON for programmatic use
  const jsonOut = entries.map(e => ({ name: e.name, originalName: e.originalName, source: e.source, stars: e.stars, description: e.description, link: e.link }));
  fs.writeFileSync('CANDIDATES.json', JSON.stringify(jsonOut, null, 2));
  
  console.log('\nWritten to CANDIDATES.md and CANDIDATES.json');
})();
