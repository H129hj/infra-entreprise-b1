# Infrastructure d'entreprise sécurisée — Projet B1 INFRA

**Groupe 3 — Hugo BERTON & Shakil KHALDI** · SUJET FINAL (3 étapes + sécurité/VPN)

Stack Docker reproductible déployable sur n'importe quel hôte Linux avec Docker.

## Étapes couvertes
1. **Réseau & segmentation** — réseaux Docker cloisonnés (`dmz`, `lan_tech`, `lan_data` *internal*),
   DNS/DHCP interne (`dns`, zone `entreprise.local`), routeur/pare-feu inter-zones (`router-fw`, nftables).
   *(Accès distant sécurisé = serveur VPN WireGuard, déployé à part — voir `../projet-infra-vpn/`.)*
2. **Serveur web multi-applications** — `wordpress` (PHP) + `nodeapp` (Node.js) derrière un
   **reverse proxy Caddy** avec **TLS** (CA interne) et **sous-domaines distincts**
   (`wordpress.entreprise.local`, `app.entreprise.local`).
3. **Sauvegarde automatisée** — service `backup` (cron) : dump MariaDB + archive des fichiers
   vers un **stockage isolé** (`backup_storage`), rétention 10, **restauration testée** (`restore.sh`).

## Démarrage
```bash
docker compose up -d --build
docker compose ps
```

Accès (depuis une machine ayant les entrées `/etc/hosts` ci-dessous ou via le DNS interne) :
- https://wordpress.entreprise.local:18443
- https://app.entreprise.local:18443

`/etc/hosts` pour la démo (remplacer `<IP>` par l'IP de l'hôte) :
```
<IP>  wordpress.entreprise.local app.entreprise.local
```

## Plan d'adressage (réseaux Docker)
| Zone | Sous-réseau | Hôtes |
|---|---|---|
| dmz | 172.30.0.0/24 | reverse-proxy, router-fw |
| lan_tech | 172.30.10.0/24 | reverse-proxy .10, wordpress .20, nodeapp .30, dns .53 |
| lan_data (internal) | 172.30.20.0/24 | db .10, backup |

## Sauvegarde / restauration
```bash
docker exec infra-backup /backup.sh                 # sauvegarde immédiate
docker exec infra-backup ls -lh /backups            # lister les sauvegardes
docker exec infra-backup /restore.sh /backups/db_<TS>.sql.gz   # restaurer
```

## Arrêt / nettoyage
```bash
docker compose down            # stoppe (conserve les volumes/données)
docker compose down -v         # + supprime les volumes (données effacées)
```

Voir `docs/` pour la documentation technique détaillée et le support d'oral.
