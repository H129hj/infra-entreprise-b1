#!/bin/sh
# Restauration de la base depuis une sauvegarde.
# Usage : docker exec infra-backup /restore.sh /backups/db_AAAA-MM-JJ_HHMMSS.sql.gz
set -e
DUMP="$1"
[ -z "$DUMP" ] && { echo "Usage: restore.sh <fichier_db_*.sql.gz>"; ls -1 /backups/db_*.sql.gz 2>/dev/null; exit 1; }
[ -f "$DUMP" ] || { echo "Fichier introuvable: $DUMP"; exit 1; }

echo "[$(date)] Restauration de $DUMP vers $DB_NAME ..."
gunzip -c "$DUMP" | mysql -h "$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME"
echo "[$(date)] Restauration terminee."
