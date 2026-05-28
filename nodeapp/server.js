// Service Node.js de demonstration (Application 2 du serveur web multi-apps)
const http = require('http');
const os = require('os');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(`<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>App Node - Infra Entreprise</title>
<style>body{font-family:system-ui,sans-serif;max-width:680px;margin:60px auto;padding:0 20px;color:#1a1a2e}
h1{color:#0f3460}code{background:#eee;padding:2px 6px;border-radius:4px}</style></head>
<body>
<h1>Application Node.js</h1>
<p>Servie via le reverse proxy sur le sous-domaine <code>app.entreprise.local</code>.</p>
<ul>
<li>Hote conteneur : <code>${os.hostname()}</code></li>
<li>Heure serveur : <code>${new Date().toISOString()}</code></li>
<li>Chemin demande : <code>${req.url}</code></li>
</ul>
<p>Projet B1 INFRA - Groupe 3 (Hugo BERTON, Shakil KHALDI & Mathéo AMOUROUX).</p>
</body></html>`);
});

server.listen(3000, () => console.log('Node app sur le port 3000'));
