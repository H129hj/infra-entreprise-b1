# Documentation technique — Infrastructure d'entreprise sécurisée

**Projet UF B1 INFRA — SUJET FINAL** · **Groupe 3 : Hugo BERTON, Shakil KHALDI & Mathéo AMOUROUX**
Hôte : VPS Contabo `144.91.126.51` (Ubuntu 24.04 LTS) · Orchestration : Docker Compose
Dépôt : https://github.com/H129hj/infra-entreprise-b1

---

## 1. Vue d'ensemble

Le projet déploie l'infrastructure complète d'un siège social d'entreprise,
sécurisée et résiliente, couvrant les trois étapes imposées + l'accès distant sécurisé :

| Étape | Réalisation |
|---|---|
| 1. Routeur & segmentation réseau | Réseaux cloisonnés (DMZ / LAN technique / LAN data isolé), DNS + DHCP internes, routeur/pare-feu nftables inter-zones |
| 2. Serveur web multi-applications | WordPress + application Node.js derrière un reverse proxy Caddy, TLS (CA interne), 2 sous-domaines distincts |
| 3. Sauvegarde automatisée | Service planifié (cron) : dump base + archive fichiers vers un stockage isolé, rétention, restauration testée |
| Sécurité / accès distant | Serveur VPN WireGuard (projet `projet-infra-vpn`) : accès chiffré depuis l'extérieur |

Tout est conteneurisé et **isolé de la production** co-hébergée (brandyze, immo, kezify) :
ports publics sur plages hautes `18080/18443`, aucune modification des services existants,
réversible via `docker compose down -v`.

## 2. Architecture

```
                          Internet
                             │
        ┌────────────────────┼─────────────────────────┐
        │ 144.91.126.51:18080/18443      :51820/udp     │
        ▼                                       ▼
  ┌───────────────┐                       ┌─────────────┐
  │ Reverse proxy │  (DMZ 172.30.0.0/24)  │  VPN        │
  │ Caddy + TLS   │                       │ WireGuard   │
  └──────┬────────┘                       │ 10.13.13.0/24│
         │ lan_tech 172.30.10.0/24        └─────────────┘
    ┌────┴───────────────┬──────────────┐
    ▼                    ▼              ▼
 WordPress(.20)     Node app(.30)   DNS/DHCP(.53)     Router/FW (multi-zones)
    │
    │ lan_data 172.30.20.0/24  (internal: pas d'Internet)
    ▼
 MariaDB(.10) ───── Backup ──→ stockage isolé (volume backup_storage)
```

## 3. Plan d'adressage

| Zone (réseau Docker) | Sous-réseau | Hôtes | Rôle |
|---|---|---|---|
| DMZ | 172.30.0.0/24 | reverse-proxy, router-fw | Exposition contrôlée |
| LAN technique | 172.30.10.0/24 | reverse-proxy .10, wordpress .20, nodeapp .30, dns .53 | Serveurs applicatifs |
| LAN data (*internal*) | 172.30.20.0/24 | db .10, backup | Données — **aucun accès Internet sortant** |
| VPN | 10.13.13.0/24 | serveur .1, hugo .2, shakil .3, matheo .4 | Accès distant chiffré |
| DHCP (démo) | 172.30.10.100-150 | — | Distribution dynamique sur le LAN technique |

## 4. Choix techniques & justifications

| Composant | Techno | Justification |
|---|---|---|
| Orchestration | Docker Compose | Maquette reproductible et versionnée (acceptée par la grille « maquette »). |
| Segmentation | Réseaux bridge + `internal` | Isolement logique des zones ; le LAN data n'a aucune route Internet. |
| Routeur/pare-feu | conteneur Alpine + nftables | Démonstration du filtrage inter-zones ; règles dans le netns du conteneur. |
| DNS/DHCP | dnsmasq | Résolution de la zone `entreprise.local` + plage DHCP. |
| Reverse proxy / TLS | Caddy (`tls internal`) | Certificats auto-signés via CA locale, routage par sous-domaine, simple et robuste. |
| App 1 | WordPress (PHP/Apache) | Application web « legacy » typique. |
| App 2 | Node.js | Seconde techno, démontre l'unification multi-langages. |
| Base de données | MariaDB | Standard, isolée en zone data. |
| Sauvegarde | Alpine + mariadb-client + cron | Léger, scripté, planifié, restaurable. |
| Accès distant | WireGuard | VPN moderne, chiffrement fort, clés + PSK. |

## 5. Étape 1 — Segmentation & routeur/pare-feu

- Trois zones cloisonnées (voir plan d'adressage). Le LAN data est `internal: true`
  → la base et le service de sauvegarde **ne peuvent pas sortir sur Internet**.
- `router-fw` est multi-homed (une interface par zone) et charge un jeu de règles
  **nftables** (politique `forward` = `drop` par défaut, autorisation par flux).
- `dns` fournit la résolution interne (`entreprise.local`) et une plage DHCP.
- Vérification : `docker logs infra-router-fw` montre les interfaces, les règles et les
  tests de joignabilité inter-zones.

## 6. Étape 2 — Serveur web multi-applications

- `reverse-proxy` (Caddy) termine le TLS (CA interne) et route selon le sous-domaine :
  - `wordpress.entreprise.local` → conteneur `wordpress:80`
  - `app.entreprise.local` → conteneur `nodeapp:3000`
- Accès : `https://wordpress.entreprise.local:18443` et `https://app.entreprise.local:18443`
  (entrée `/etc/hosts` ou DNS interne ; SNI requis pour le bon certificat).
- WordPress installé (site « Entreprise Demo - Infra B1 »), base sur MariaDB en zone data.
- *Optionnel non réalisé : load balancing actif (extension possible avec plusieurs nodeapp + `reverse_proxy` multi-upstream Caddy).*

## 7. Étape 3 — Sauvegarde automatisée

- Service `backup` : à intervalle régulier (`*/30 * * * *`), il réalise :
  1. `mysqldump` de la base WordPress → `db_<horodatage>.sql.gz`
  2. archive des fichiers WordPress → `wpfiles_<horodatage>.tar.gz`
  3. rétention des 10 dernières sauvegardes de chaque type.
- Stockage **isolé** : volume Docker dédié `backup_storage` (zone data, sans Internet).
- **Restauration testée** : `restore.sh <fichier>` réinjecte un dump via `mysql`.

```bash
docker exec infra-backup /backup.sh                # sauvegarde immédiate
docker exec infra-backup ls -lh /backups           # inventaire
docker exec infra-backup /restore.sh /backups/db_<TS>.sql.gz   # restauration
```

## 7bis. Bonus — Annuaire LDAP + partage de fichiers Samba

- **Annuaire central** : `ldap` (OpenLDAP, base `dc=entreprise,dc=local`). Les unités
  d'organisation (`people`, `groups`) et les utilisateurs (hugo, shakil, matheo) sont
  créés au démarrage via `bonus/ldap/bootstrap.ldif`. Service interne (389/636, non exposé).
- **Serveur de fichiers** : `samba` (Samba), partages `partage-entreprise` et `technique`,
  utilisateurs gérés et journalisation des accès (`docker logs infra-samba`).
  Non exposé publiquement → accès via le réseau interne ou le VPN.
- **Gestion des utilisateurs** :
```bash
docker logs infra-ldap        # import des comptes (custom ldif)
docker exec infra-ldap ldapsearch -x -b dc=entreprise,dc=local "(objectClass=inetOrgPerson)"
docker logs infra-samba       # comptes Samba + accès (logs)
```
- Accès au partage depuis un poste (via VPN) : `smb://<hôte>/partage-entreprise`
  (Finder macOS : Aller → Se connecter au serveur).
- *Piste d'amélioration : authentification Samba directement adossée à LDAP (back-end ldapsam).*

## 8. Sécurité

- **Cloisonnement réseau** : 3 zones, LAN data sans accès Internet (`internal`).
- **Filtrage** : pare-feu nftables inter-zones (politique deny par défaut).
- **TLS** partout sur le web (CA interne Caddy).
- **Exposition minimale** : seuls 3 ports publics (18080/18443 web, 51820/udp VPN).
- **Accès distant** : VPN WireGuard (clé par peer + PresharedKey = authentification forte).
- **Secrets** : mots de passe de démo ; en production → variables d'environnement/secrets.
- **Isolation hôte** : tout en conteneurs, production co-hébergée intacte.

## 9. Procédure de déploiement (reproductible)

```bash
git clone https://github.com/H129hj/infra-entreprise-b1.git
cd infra-entreprise-b1
docker compose up -d --build
docker compose ps          # 7 services "Up"
```

## 10. Tests de validation réalisés

| Test | Résultat |
|---|---|
| 7 conteneurs démarrés | ✅ `docker compose ps` |
| WordPress servi en HTTPS via sous-domaine | ✅ HTTP 200, titre « Entreprise Demo - Infra B1 » |
| App Node servie en HTTPS via sous-domaine | ✅ page HTML rendue |
| Routeur multi-zones + nftables | ✅ logs `infra-router-fw` |
| Zone data isolée (pas d'Internet) | ✅ réseau `internal` |
| Sauvegarde auto (DB + fichiers) | ✅ archives horodatées dans `backup_storage` |
| Restauration | ✅ `restore.sh` |
| VPN externe + ressource interne VPN-only | ✅ (voir `projet-infra-vpn`) |

## 11. Couverture de la grille (note technique, coef. 3)

| Compétence (pond.) | Preuve dans le projet |
|---|---|
| Réseau simple (4) | 3 sous-réseaux, plan d'adressage, DNS/DHCP, routage inter-zones |
| Infra client-serveur (4) | reverse proxy + 2 apps + DB + clients (navigateur, VPN) |
| Administration système (4) | Docker/Linux, services persistants, scripts Bash (backup/restore, firewall) |
| Virtualisation / maquette (3) | Stack Docker Compose fidèle au besoin client |
| Sécurisation (3) | segmentation, nftables, TLS, VPN WireGuard, exposition minimale |
| Documentation (3) | ce document + READMEs + support d'oral + dépôt Git |
