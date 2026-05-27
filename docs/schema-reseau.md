# Schéma réseau

```mermaid
flowchart TB
    NET([Internet]):::ext

    subgraph VPS["VPS Contabo — 144.91.126.51 (Ubuntu 24.04, Docker)"]
        direction TB

        subgraph DMZ["DMZ — 172.30.0.0/24"]
            RP["Reverse proxy Caddy<br/>TLS interne<br/>:18080 / :18443"]
            FW["Routeur / Pare-feu<br/>nftables (multi-zones)"]
        end

        subgraph TECH["LAN technique — 172.30.10.0/24"]
            WP["WordPress<br/>.20"]
            NODE["App Node.js<br/>.30"]
            DNS["DNS + DHCP<br/>dnsmasq .53"]
            LDAP["Annuaire LDAP<br/>.60"]
            SMB["Samba partages<br/>.70"]
        end

        subgraph DATA["LAN data — 172.30.20.0/24 (internal, sans Internet)"]
            DB[("MariaDB<br/>.10")]
            BK["Backup cron<br/>+ stockage isolé"]
        end

        subgraph VPNZONE["VPN — 10.13.13.0/24"]
            WG["Serveur WireGuard<br/>.1 :51820/udp<br/>+ ressource interne VPN-only"]
        end
    end

    REMOTE["Collaborateur distant<br/>(client WireGuard)"]:::ext

    NET -->|HTTPS 18443| RP
    NET -->|UDP 51820| WG
    REMOTE -.tunnel chiffré.-> WG
    RP -->|wordpress.entreprise.local| WP
    RP -->|app.entreprise.local| NODE
    WP --> DB
    BK --> DB
    DNS -. résolution .- TECH
    FW -. filtrage .- DMZ
    FW -. filtrage .- TECH
    FW -. filtrage .- DATA

    classDef ext fill:#0f3460,color:#fff;
```

## Légende
- **DMZ** : exposition contrôlée (reverse proxy + routeur/pare-feu).
- **LAN technique** : serveurs applicatifs + services réseau (DNS/DHCP).
- **LAN data** : base + sauvegarde, réseau `internal` (aucune route Internet sortante).
- **VPN** : accès distant chiffré ; la ressource interne n'est joignable que par le tunnel.
- Seuls 3 ports sont exposés sur Internet : `18080/tcp`, `18443/tcp`, `51820/udp`.
