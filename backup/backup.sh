#!/bin/sh
# Sauvegarde automatisee : dump de la base + archive des fichiers WordPress
# vers le stockage isole /backups. (Etape 3)
set -e
TS=$(date +%F_%H%M%S)
DEST=/backups
mkdir -p "$DEST"

echo "[$(date)] Debut sauvegarde $TS"

# 1) Base de donnees
mysqldump -h "$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" 2>/dev/null | gzip > "$DEST/db_${TS}.sql.gz"
echo "  - base sauvegardee : db_${TS}.sql.gz"

# 2) Fichiers applicatifs (montes en lecture seule)
if [ -d /data/wp_files ]; then
  tar czf "$DEST/wpfiles_${TS}.tar.gz" -C /data/wp_files . 2>/dev/null
  echo "  - fichiers sauvegardes : wpfiles_${TS}.tar.gz"
fi

# 3) Retention : conserver les 10 dernieres sauvegardes de chaque type
ls -1t "$DEST"/db_*.sql.gz 2>/dev/null      | tail -n +11 | xargs -r rm -f
ls -1t "$DEST"/wpfiles_*.tar.gz 2>/dev/null | tail -n +11 | xargs -r rm -f

echo "[$(date)] Sauvegarde $TS terminee. Contenu du stockage :"
ls -lh "$DEST"
