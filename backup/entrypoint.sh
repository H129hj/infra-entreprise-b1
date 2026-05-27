#!/bin/sh
set -e
echo "Service de sauvegarde demarre. Planification : ${BACKUP_CRON}"

# Installer la tache planifiee (busybox crond)
echo "${BACKUP_CRON} /backup.sh >> /var/log/backup.log 2>&1" > /etc/crontabs/root

# Attendre que la base soit prete puis premiere sauvegarde
sleep 30
/backup.sh >> /var/log/backup.log 2>&1 || echo "Premiere sauvegarde reportee (base pas encore prete)"

# Lancer le planificateur au premier plan + suivre le journal
crond -b -l 8
exec tail -F /var/log/backup.log
