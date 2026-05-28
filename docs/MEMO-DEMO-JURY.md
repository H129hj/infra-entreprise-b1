# Mémo de démo — Oral B1 INFRA (Groupe 3)

> Pas-à-pas à suivre **devant le jury**. 15 min d'oral, 5 min Q/R.
> Suis l'ordre, lis les commandes, dis les phrases en gras à voix haute si besoin.

---

## ⏱️ T−15 min — Préparation (à faire AVANT d'entrer)

- [ ] **Sur ton Mac**, ajouter à `/etc/hosts` (sudo) :
      `144.91.126.51 wordpress.entreprise.local app.entreprise.local`
- [ ] **Activer le VPN** WireGuard (config `projet-infra-vpn/clients/hugo.conf`) → vérifier qu'il y a un handshake.
- [ ] **Ouvrir 3 onglets navigateur** prêts (sans charger) :
  - `https://wordpress.entreprise.local:18443`
  - `https://app.entreprise.local:18443`
  - `http://10.13.13.1` (ressource VPN-only)
- [ ] **Ouvrir 1 terminal** dans `~/Dev/Travail/infra-entreprise` (pour les commandes Docker).
- [ ] **Ouvrir** le PDF `docs/slides.pdf` (mode plein écran) et le PNG `docs/schema-reseau.png` à part.
- [ ] **Vérifier** que la stack tourne : la commande de la slide 5 (voir ci-dessous).

---

## 🎬 Déroulé minuté (15 min)

### ⌚ 0:00 — Slide 1 (titre)
> **« Bonjour, on est Hugo, Shakil et Mathéo, Groupe 3. Notre projet : concevoir et déployer une infrastructure d'entreprise sécurisée, couvrant les trois étapes imposées et le bonus. »**

### ⌚ 0:30 — Slide 2 (contexte)
> **« Le client est une PME en croissance. Quatre besoins : segmenter le réseau, héberger plusieurs apps web, sauvegarder automatiquement, et permettre le télétravail. Plus le bonus : partage de fichiers et annuaire. »**

### ⌚ 1:30 — Slide 3 (schéma) + Slide 4 (plan d'adressage) — *2 min*
> **« Voici l'architecture. Trois zones cloisonnées : DMZ, LAN technique, LAN data — cette dernière est en mode `internal`, c'est-à-dire que la base de données n'a aucune route Internet sortante. Tout est conteneurisé. Trois ports seulement sont exposés sur Internet. »**

### ⌚ 3:30 — Slide 5 + DÉMO Étape 1 — *2 min*

**Dans le terminal :**
```bash
ssh ubuntu@144.91.126.51 'docker logs infra-router-fw'
```

> **« Le routeur est multi-zones (3 interfaces). Les règles nftables ont une politique deny par défaut, on autorise explicitement les flux légitimes. Et les tests de joignabilité inter-zones sont OK. »**

### ⌚ 5:30 — Slide 6 + Slide 7 + DÉMO Étape 2 — *3 min*

**Dans le navigateur, ouvrir successivement :**
1. `https://wordpress.entreprise.local:18443` — *« Première application : WordPress, sous le sous-domaine wordpress.entreprise.local, en HTTPS. »*
2. `https://app.entreprise.local:18443` — *« Deuxième application : un service Node.js, sur app.entreprise.local. Même reverse proxy, même port d'entrée, deux apps, deux sous-domaines. »*
3. Cliquer sur le cadenas du navigateur → montrer que le certificat est émis par la **CA interne Caddy**.

> **« Le reverse proxy Caddy termine le TLS et route selon le SNI. En production on prendrait Let's Encrypt avec un vrai domaine — ici on a une CA locale pour la démo. »**

### ⌚ 8:30 — Slide 8 + DÉMO Étape 3 — *2 min*

**Dans le terminal :**
```bash
ssh ubuntu@144.91.126.51 'docker exec infra-backup ls -lh /backups'
ssh ubuntu@144.91.126.51 'docker exec infra-backup /backup.sh'
ssh ubuntu@144.91.126.51 'docker exec infra-backup ls -lh /backups'
```

> **« La sauvegarde tourne automatiquement toutes les 30 min : dump SQL + archive des fichiers, dans un volume isolé en zone data. On garde les 10 dernières. La restauration se fait avec `restore.sh <fichier>`. »**

**Test restauration (optionnel) :**
```bash
ssh ubuntu@144.91.126.51 'docker exec infra-backup ls /backups | head -1'
# puis :
ssh ubuntu@144.91.126.51 'docker exec infra-backup /restore.sh /backups/<FICHIER>'
```

### ⌚ 10:30 — Slide 9 + DÉMO VPN — *2 min*

1. **Désactiver le VPN** dans WireGuard → ouvrir `http://10.13.13.1` → **timeout** ✅
2. **Réactiver le VPN** → recharger `http://10.13.13.1` → page **whoami** s'affiche.

> **« Le serveur VPN écoute en UDP 51820. Chaque utilisateur a une clé privée + une PresharedKey unique — c'est notre authentification forte. La ressource interne n'est jamais exposée publiquement : elle n'est joignable que par le tunnel, je viens de le prouver. »**

### ⌚ 12:30 — Slide 10 + DÉMO Bonus — *1 min 30*

**Dans le terminal :**
```bash
ssh ubuntu@144.91.126.51 'docker logs infra-ldap 2>&1 | grep -iE "ldif|added|bootstrap"'
ssh ubuntu@144.91.126.51 'docker logs infra-samba'
```

**Dans Finder (Mac) :** Aller → Se connecter au serveur → `smb://10.13.13.1/partage-entreprise` → login `hugo` / `hugo_pass_2026`.

> **« Bonus : un annuaire OpenLDAP centralise les comptes (hugo, shakil, matheo). Et un serveur Samba expose deux partages, accessibles seulement en interne ou via VPN. »**

### ⌚ 14:00 — Slide 11 (couverture grille) + Slide 12 (merci) — *1 min*

> **« En résumé, on couvre les six compétences de la grille. Tout est versionné, reproductible avec `docker compose up`, et entièrement réversible. Merci, on prend vos questions. »**

---

## 🛡️ Questions probables du jury — réponses prêtes

| Question | Réponse |
|---|---|
| Pourquoi Docker plutôt que pfSense/Packet Tracer ? | La grille accepte explicitement Docker comme outil de maquette. Notre segmentation logique et notre filtrage nftables sont démontrés. pfSense aurait été l'alternative VM si on voulait des vrais VLAN niveau 2 ; ici on a privilégié une maquette reproductible et versionnée. |
| Certificats auto-signés, et en prod ? | Let's Encrypt sur un vrai domaine — Caddy le fait nativement. |
| Comment isolez-vous *vraiment* la base ? | Le réseau `lan_data` est `internal: true` dans Docker → pas de gateway Internet, et pare-feu nftables côté routeur. |
| Que se passe-t-il si le VPS tombe ? | Sauvegardes restaurables sur n'importe quel hôte Docker. `git clone` + `docker compose up` → la stack repart en 5 minutes. |
| Sécurité des secrets ? | Ici en clair pour la démo. En prod : Docker secrets / variables d'environnement chiffrées / coffre. |
| L'authentification Samba est-elle liée à LDAP ? | Pas dans cette version : Samba a ses propres comptes, alignés avec les UID LDAP. L'intégration `ldapsam` est notre piste d'évolution. |
| Pourquoi le port 18443 et pas 443 ? | Pour ne pas entrer en conflit avec les services co-hébergés sur le VPS. En infra dédiée, on prendrait 443. |
| Captive portal ? | Non implémenté (pas dans le scope final du sujet) — extension possible avec un service comme CoovaChilli. |

---

## 🧰 Commandes de secours (si quelque chose ne répond pas)

```bash
# Tout vérifier d'un coup
ssh ubuntu@144.91.126.51 'docker compose -f /home/ubuntu/infra-entreprise-b1/docker-compose.yml ps'

# Relancer la stack si besoin
ssh ubuntu@144.91.126.51 'docker compose -f /home/ubuntu/infra-entreprise-b1/docker-compose.yml up -d'

# Logs ciblés
ssh ubuntu@144.91.126.51 'docker logs --tail 20 infra-reverse-proxy'
ssh ubuntu@144.91.126.51 'docker logs --tail 20 infra-wordpress'
ssh ubuntu@144.91.126.51 'docker logs --tail 20 infra-backup'
```

## 📂 Fichiers à avoir sous la main
- `docs/slides.pdf` — diaporama
- `docs/schema-reseau.png` — schéma
- `docs/PREUVES.md` + `docs/screenshots/` — captures
- `docs/DOCUMENTATION-TECHNIQUE.md` — livrable
- `projet-infra-vpn/clients/hugo.conf` + `hugo-qr.png` — VPN
- Dépôt : `https://github.com/H129hj/infra-entreprise-b1` (à projeter au début si le jury veut voir le code)
