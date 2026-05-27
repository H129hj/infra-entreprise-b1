#!/bin/sh
# Routeur / pare-feu de demonstration inter-segments (Etape 1).
# Ce conteneur est multi-homed (dmz, lan_tech, lan_data) et illustre
# le filtrage entre zones avec nftables. Les regles s'appliquent dans
# la pile reseau du conteneur uniquement (aucun impact sur l'hote).
set -e
apk add --no-cache nftables iproute2 iputils >/dev/null 2>&1 || true

echo "=== Interfaces / adresses du routeur ==="
ip -brief addr

echo "=== Politique de filtrage inter-zones (exemple entreprise) ==="
nft -f - <<'EOF'
flush ruleset
table inet zones {
  chain forward {
    type filter hook forward priority 0; policy drop;
    ct state established,related accept
    # RH et Compta peuvent atteindre les serveurs applicatifs (lan_tech)
    iifname "eth1" oifname "eth0" accept
    # La zone data (db) ne doit pas initier de trafic vers la DMZ
    iifname "eth2" oifname "eth0" drop
    counter
  }
}
EOF
echo "Regles nftables chargees :"
nft list ruleset

echo "=== Tests de joignabilite depuis le routeur ==="
echo -n "reverse-proxy (172.30.10.10): "; ping -c1 -W1 172.30.10.10 >/dev/null 2>&1 && echo OK || echo KO
echo -n "db (172.30.20.10)          : "; ping -c1 -W1 172.30.20.10 >/dev/null 2>&1 && echo OK || echo KO

echo "Routeur/pare-feu actif. (logs ci-dessus)"
exec tail -f /dev/null
