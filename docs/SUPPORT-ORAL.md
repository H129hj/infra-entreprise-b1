# Support d'oral — Infrastructure d'entreprise sécurisée (15 min)

**Groupe 3 : Hugo BERTON & Shakil KHALDI** — B1 INFRA — Oral final 15 min + 5 min Q/R

> Trame de présentation alignée sur la grille (réseau, client-serveur, admin,
> virtualisation, sécurité, doc). Objectif : montrer du **fonctionnel** + justifier les choix.

## Plan (≈15 min)

### 1. Contexte & besoin client (1 min)
Siège social d'entreprise en croissance : segmenter le réseau, héberger plusieurs
applications web en sécurité, garantir la sauvegarde des données, et permettre un
accès distant sécurisé aux ressources internes.

### 2. Architecture globale (2 min) — *montrer le schéma*
- 3 zones réseau cloisonnées : DMZ, LAN technique, LAN data (isolé).
- Point d'entrée web unique (reverse proxy TLS), accès distant via VPN.
- Tout virtualisé (Docker Compose), reproductible et versionné (Git).

### 3. Étape 1 — Réseau & sécurité (3 min) — *démo live*
- `docker logs infra-router-fw` : interfaces multi-zones + règles **nftables** + tests.
- Insister : LAN data `internal` → base de données **sans accès Internet** (réduction de surface).
- Plan d'adressage (tableau).

### 4. Étape 2 — Serveur web multi-apps (3 min) — *démo live*
- Navigateur : `https://wordpress.entreprise.local:18443` (WordPress) et
  `https://app.entreprise.local:18443` (Node) → **2 apps, 2 sous-domaines, 1 serveur, HTTPS**.
- Montrer le certificat (CA interne) et le `Caddyfile` (routage par sous-domaine).

### 5. Étape 3 — Sauvegarde automatisée (2 min) — *démo live*
- `docker exec infra-backup ls -lh /backups` : archives horodatées (DB + fichiers).
- Lancer une restauration : `docker exec infra-backup /restore.sh /backups/db_<TS>.sql.gz`.
- Insister : stockage **isolé**, rétention, planification cron.

### 6. Accès distant — VPN (2 min) — *démo live*
- Activer le tunnel WireGuard sur le poste, ouvrir `http://10.13.13.1` (ressource interne).
- Couper le VPN → la ressource devient injoignable. Authentification : clé + PSK par utilisateur.

### 7. Bilan & ouverture (1 min)
- Ce qui marche, sécurité, et pistes : load balancing, Let's Encrypt (domaine réel),
  annuaire LDAP + partage Samba (bonus), monitoring.

## Répartition binôme (proposition)
- **Hugo** : architecture, étape 1 (réseau/sécurité), VPN.
- **Shakil** : étape 2 (web multi-apps), étape 3 (sauvegarde).
- Les deux : Q/R.

## Questions probables du jury (préparer les réponses)
- *Pourquoi Docker plutôt que pfSense/Packet Tracer ?* → maquette reproductible, acceptée
  par la grille ; la segmentation logique et le filtrage sont démontrés ; pfSense aurait été
  une alternative VM si L2/VLAN réels requis.
- *Vos certificats sont auto-signés, et en prod ?* → Let's Encrypt avec un vrai domaine.
- *Comment isolez-vous vraiment la base ?* → réseau `internal` (pas de gateway Internet) + pare-feu.
- *Que se passe-t-il si le VPS tombe ?* → sauvegardes restaurables ailleurs ; stack redéployable
  en une commande (`docker compose up`).
- *Sécurité des secrets ?* → ici démo ; en prod : secrets Docker / variables d'env / coffre.

## Checklist avant l'oral
- [ ] Stack démarrée (`docker compose ps` = 7 Up).
- [ ] Entrées `/etc/hosts` sur la machine de démo (sous-domaines).
- [ ] Tunnel VPN importé et testé.
- [ ] Schéma réseau imprimé/affiché.
- [ ] Une sauvegarde récente présente + test de restauration répété une fois.
