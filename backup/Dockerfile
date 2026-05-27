FROM alpine:3.20
RUN apk add --no-cache mariadb-client tar gzip busybox-suid tzdata
COPY backup.sh /backup.sh
COPY restore.sh /restore.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /backup.sh /restore.sh /entrypoint.sh && mkdir -p /var/log && touch /var/log/backup.log
ENTRYPOINT ["/entrypoint.sh"]
