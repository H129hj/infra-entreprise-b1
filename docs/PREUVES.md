# Preuves de réalisation (captures)

Captures à inclure dans le rendu final et à projeter à l'oral.

## Schéma d'architecture / flux complet
![Schéma réseau](schema-reseau.png)

## 1. Preuves techniques (réseau, conteneurs, sauvegarde, VPN)
![Preuves techniques](screenshots/01-preuves-techniques.png)

## 2. Application 1 — WordPress (HTTPS, sous-domaine `wordpress.entreprise.local`)
![Site WordPress](screenshots/02-wordpress-site.png)

## 3. Application 2 — Node.js (HTTPS, sous-domaine `app.entreprise.local`)
![App Node](screenshots/03-nodeapp.png)

## 4. Sécurité — accès administration WordPress (authentification)
![WordPress admin](screenshots/04-wordpress-admin-login.png)

---
*Les deux applications sont servies par le **même** reverse proxy Caddy en HTTPS (CA interne),
sur deux sous-domaines distincts — preuve du serveur web multi-applications (Étape 2).*
