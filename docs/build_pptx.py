#!/usr/bin/env python3
"""Génération du diaporama PowerPoint (16:9) pour l'oral B1 INFRA."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pathlib import Path

# ---- Charte graphique ----
BG       = RGBColor(0x0D, 0x11, 0x17)   # fond
CARD     = RGBColor(0x16, 0x1B, 0x22)   # cartes
LINE     = RGBColor(0x30, 0x36, 0x3D)   # bords
INK      = RGBColor(0xE6, 0xED, 0xF3)   # texte principal
MUT      = RGBColor(0x8B, 0x94, 0x9E)   # texte secondaire
ACC      = RGBColor(0x58, 0xA6, 0xFF)   # accent bleu
OK       = RGBColor(0x3F, 0xB9, 0x50)   # vert
WARN     = RGBColor(0xD2, 0x99, 0x22)   # orange
BAD      = RGBColor(0xF8, 0x51, 0x49)   # rouge

W = Inches(13.333)    # 16:9 widescreen
H = Inches(7.5)

GROUP_FOOTER = "Hugo BERTON · Shakil KHALDI · Mathéo AMOUROUX  —  Groupe 3"

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H
blank = prs.slide_layouts[6]   # layout vide

DOCS = Path(__file__).parent
ROOT = DOCS.parent

def add_bg(slide, color=BG):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, H)
    bg.line.fill.background()
    bg.fill.solid(); bg.fill.fore_color.rgb = color
    bg.shadow.inherit = False
    return bg

def add_text(slide, x, y, w, h, text, size=18, bold=False, color=INK, align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP, font="Inter"):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Pt(0)
    tf.margin_top = tf.margin_bottom = Pt(2)
    lines = text.split("\n") if isinstance(text, str) else text
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        runs = line if isinstance(line, list) else [(line, {})]
        for run_text, fmt in runs:
            r = p.add_run()
            r.text = run_text
            r.font.name = font
            r.font.size = Pt(fmt.get("size", size))
            r.font.bold = fmt.get("bold", bold)
            r.font.color.rgb = fmt.get("color", color)
    return tb

def add_rect(slide, x, y, w, h, fill=CARD, border=LINE, border_w=0.75, radius=True):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE, x, y, w, h
    )
    if radius:
        try: shape.adjustments[0] = 0.06
        except Exception: pass
    shape.fill.solid(); shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = border
    shape.line.width = Pt(border_w)
    shape.shadow.inherit = False
    return shape

def add_chip(slide, x, y, text, color=MUT):
    """Pill / chip en haut des slides."""
    tw = Inches(2.6); th = Inches(0.35)
    pill = add_rect(slide, x, y, tw, th, fill=BG, border=LINE, border_w=0.75)
    add_text(slide, x, y, tw, th, text, size=11, color=color,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

def add_footer(slide, num, total=12):
    add_text(slide, Inches(0.4), H - Inches(0.4), Inches(8), Inches(0.3),
             f"Projet B1 INFRA · {GROUP_FOOTER}", size=10, color=MUT)
    add_text(slide, W - Inches(1.6), H - Inches(0.4), Inches(1.2), Inches(0.3),
             f"{num} / {total}", size=10, color=MUT, align=PP_ALIGN.RIGHT)

def add_title(slide, text, sub=None):
    add_text(slide, Inches(0.7), Inches(0.45), Inches(12), Inches(0.7),
             text, size=30, bold=True, color=ACC, font="Inter")
    if sub:
        add_text(slide, Inches(0.7), Inches(1.15), Inches(12), Inches(0.5),
                 sub, size=14, color=MUT)

# =====================================================================
# Slide 1 — Titre
# =====================================================================
s = prs.slides.add_slide(blank); add_bg(s)
add_chip(s, Inches(0.7), Inches(0.6), "UF B1 INFRA · Ynov Informatique")
# Bloc titre
add_text(s, Inches(0.7), Inches(2.0), Inches(12), Inches(2.6),
         [
            [("Conception & déploiement", {"size": 54, "bold": True, "color": INK})],
            [("d'une infrastructure", {"size": 54, "bold": True, "color": INK})],
            [("d'entreprise ", {"size": 54, "bold": True, "color": INK}),
             ("sécurisée", {"size": 54, "bold": True, "color": ACC})],
         ])
add_text(s, Inches(0.7), Inches(5.4), Inches(12), Inches(0.5),
         "Hugo BERTON · Shakil KHALDI · Mathéo AMOUROUX — Groupe 3",
         size=18, color=INK)
add_text(s, Inches(0.7), Inches(5.95), Inches(12), Inches(0.4),
         "Oral final — 29 mai 2026", size=14, color=MUT)
add_footer(s, 1)

# =====================================================================
# Slide 2 — Contexte & besoin
# =====================================================================
s = prs.slides.add_slide(blank); add_bg(s)
add_title(s, "Contexte & besoin client")
add_text(s, Inches(0.7), Inches(1.7), Inches(12), Inches(0.5),
         "Siège social d'une PME en croissance — l'équipe doit :",
         size=17, color=INK)
needs = [
    ("Segmenter", " le réseau interne (RH, Compta, Technique) pour réduire la surface d'attaque."),
    ("Héberger plusieurs applications web", " (PHP + Node) sur un même serveur, en HTTPS, avec sous-domaines distincts."),
    ("Sauvegarder", " automatiquement les données critiques et restaurer rapidement."),
    ("Permettre l'accès distant", " sécurisé aux ressources internes (télétravail)."),
    ("Bonus", " : partage de fichiers et annuaire centralisé."),
]
y = Inches(2.3)
for h_, rest in needs:
    bullet = add_rect(s, Inches(0.8), y + Inches(0.18), Inches(0.12), Inches(0.12), fill=ACC, border=ACC, radius=False)
    add_text(s, Inches(1.1), y, Inches(11.5), Inches(0.5),
             [[(h_, {"size": 16, "bold": True, "color": INK}),
               (rest, {"size": 16, "color": INK})]])
    y += Inches(0.55)

# 3 KPI cards
kpis = [("4 axes", "réseau · web · sauvegarde · accès distant"),
        ("9 services", "conteneurisés et reproductibles"),
        ("3 ports", "exposés sur Internet seulement")]
for i, (k, sub) in enumerate(kpis):
    x = Inches(0.7 + i * 4.0); w = Inches(3.7); h_ = Inches(0.95)
    add_rect(s, x, Inches(5.85), w, h_)
    add_text(s, x + Inches(0.2), Inches(5.95), w, Inches(0.4),
             k, size=22, bold=True, color=ACC)
    add_text(s, x + Inches(0.2), Inches(6.4), w, Inches(0.5),
             sub, size=11, color=MUT)

add_footer(s, 2)

# =====================================================================
# Slide 3 — Architecture (image)
# =====================================================================
s = prs.slides.add_slide(blank); add_bg(s)
add_title(s, "Architecture — vue d'ensemble")
schema = DOCS / "schema-reseau.png"
if schema.exists():
    # 1180 x 469 environ -> fit dans Inches(12) x Inches(5)
    from PIL import Image
    iw, ih = Image.open(schema).size
    avail_w, avail_h = Inches(12.3), Inches(5.5)
    # ratio
    r = min(avail_w / iw * 96, avail_h / ih * 96, 1.2)
    # simpler: use add_picture and size manually
    pw = Inches(12.3)
    ph = int(pw * ih / iw)
    if ph > avail_h:
        ph = avail_h; pw = int(ph * iw / ih)
    x = (W - pw) // 2; y = Inches(1.7)
    s.shapes.add_picture(str(schema), x, y, width=pw, height=ph)
add_footer(s, 3)

# =====================================================================
# Slide 4 — Plan d'adressage (table)
# =====================================================================
s = prs.slides.add_slide(blank); add_bg(s)
add_title(s, "Plan d'adressage")
headers = ["Zone", "Sous-réseau", "Hôtes", "Particularité"]
rows = [
    ["DMZ", "172.30.0.0/24", "Reverse proxy · Routeur/pare-feu", "Exposition contrôlée"],
    ["LAN technique", "172.30.10.0/24", "WordPress .20 · Node .30 · DNS .53 · LDAP .60 · Samba .70", "Serveurs applicatifs"],
    ["LAN data", "172.30.20.0/24", "MariaDB .10 · Backup", "internal — sans Internet sortant"],
    ["VPN", "10.13.13.0/24", "WireGuard .1 · hugo .2 · shakil .3 · matheo .4", "Tunnel chiffré 51820/udp"],
]
tbl = s.shapes.add_table(len(rows) + 1, 4, Inches(0.7), Inches(1.8), Inches(12), Inches(4.5)).table
widths = [Inches(1.7), Inches(2.0), Inches(5.4), Inches(2.9)]
for i, w in enumerate(widths): tbl.columns[i].width = w
# header
for j, h_ in enumerate(headers):
    cell = tbl.cell(0, j)
    cell.fill.solid(); cell.fill.fore_color.rgb = CARD
    tf = cell.text_frame; tf.clear()
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = h_
    r.font.bold = True; r.font.size = Pt(13); r.font.color.rgb = MUT
for i, row in enumerate(rows, start=1):
    for j, val in enumerate(row):
        cell = tbl.cell(i, j)
        cell.fill.solid(); cell.fill.fore_color.rgb = BG
        tf = cell.text_frame; tf.clear()
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = val
        r.font.size = Pt(13); r.font.color.rgb = INK
        if j == 0:
            r.font.bold = True

add_text(s, Inches(0.7), Inches(6.4), Inches(12), Inches(0.4),
         "Ports publics : 18080/tcp · 18443/tcp (web) · 51820/udp (VPN). Tout le reste est interne.",
         size=12, color=MUT)
add_footer(s, 4)

# =====================================================================
# Helper : 3 cartes côte à côte
# =====================================================================
def three_cards(slide, items, top=Inches(1.85), card_h=Inches(4.6)):
    """items: list of (title, lines) where lines is list of (text, fmt|None)."""
    n = len(items); gap = Inches(0.35)
    total = W - Inches(1.4)
    cw = int((total - gap * (n - 1)) / n)
    for i, (t, lines) in enumerate(items):
        x = Inches(0.7) + i * (cw + gap)
        add_rect(slide, x, top, cw, card_h)
        add_text(slide, x + Inches(0.3), top + Inches(0.2), cw - Inches(0.6), Inches(0.4),
                 t.upper(), size=12, bold=True, color=ACC)
        y = top + Inches(0.75)
        for line, fmt in lines:
            tb = add_text(slide, x + Inches(0.3), y, cw - Inches(0.6), Inches(0.5),
                          line, size=14, color=INK)
            y += Inches(0.5)

# =====================================================================
# Slide 5 — Étape 1 réseau
# =====================================================================
s = prs.slides.add_slide(blank); add_bg(s)
add_title(s, "Étape 1 — Réseau & segmentation")
three_cards(s, [
    ("Cloisonnement", [
        ("• Trois zones isolées par défaut", None),
        ("• LAN data internal :", None),
        ("   la base n'a aucune route sortante", None),
        ("• DNS + DHCP internes (dnsmasq,", None),
        ("   zone entreprise.local)", None),
    ]),
    ("Routeur / pare-feu", [
        ("• Conteneur multi-homed (3 interfaces)", None),
        ("• Règles nftables", None),
        ("   politique forward = drop", None),
        ("• Filtrage explicite par flux + compteurs", None),
    ]),
    ("Démo", [
        ("docker logs infra-router-fw", None),
        ("→ interfaces, règles, et tests", None),
        ("   de joignabilité inter-zones (OK)", None),
    ]),
])
add_footer(s, 5)

# =====================================================================
# Slide 6 — Étape 2 web multi-apps
# =====================================================================
s = prs.slides.add_slide(blank); add_bg(s)
add_title(s, "Étape 2 — Serveur web multi-applications")
# 2 cartes (gauche large, droite normale)
add_rect(s, Inches(0.7), Inches(1.85), Inches(7.0), Inches(4.6))
add_text(s, Inches(1.0), Inches(2.05), Inches(6.5), Inches(0.4),
         "REVERSE PROXY + TLS", size=12, bold=True, color=ACC)
for i, line in enumerate([
    "• Caddy termine le TLS (CA interne)",
    "• Routage par sous-domaine (SNI)",
    "• 2 applications, 2 sous-domaines,",
    "   1 entrée HTTPS unique",
]):
    add_text(s, Inches(1.0), Inches(2.55 + i*0.5), Inches(6.5), Inches(0.5),
             line, size=15, color=INK)
# mini grille services
labels = [("Caddy","18080/18443"),("WordPress",":80 PHP"),("Node.js",":3000"),("MariaDB","data zone")]
for i,(n,sub) in enumerate(labels):
    x = Inches(1.0 + (i%2)*3.0); y = Inches(4.8 + (i//2)*0.85)
    add_rect(s, x, y, Inches(2.8), Inches(0.75), fill=BG, border=LINE)
    add_text(s, x, y + Inches(0.06), Inches(2.8), Inches(0.32),
             n, size=12, bold=True, color=ACC, align=PP_ALIGN.CENTER)
    add_text(s, x, y + Inches(0.38), Inches(2.8), Inches(0.32),
             sub, size=11, color=MUT, align=PP_ALIGN.CENTER)

add_rect(s, Inches(8.0), Inches(1.85), Inches(4.7), Inches(4.6))
add_text(s, Inches(8.3), Inches(2.05), Inches(4.2), Inches(0.4),
         "DÉMO", size=12, bold=True, color=ACC)
for i, line in enumerate([
    "https://wordpress.entreprise.local:18443",
    "https://app.entreprise.local:18443",
    "",
    "Certificats émis par la CA",
    "Caddy locale. En production :",
    "Let's Encrypt + domaine réel.",
]):
    add_text(s, Inches(8.3), Inches(2.55 + i*0.5), Inches(4.2), Inches(0.5),
             line, size=13, color=INK if i<2 else MUT)
add_footer(s, 6)

# =====================================================================
# Slide 7 — Étape 2 preuve visuelle (capture WordPress)
# =====================================================================
s = prs.slides.add_slide(blank); add_bg(s)
add_title(s, "Étape 2 — preuve : WordPress en HTTPS via sous-domaine")
img = DOCS / "screenshots/02-wordpress-site.png"
if img.exists():
    from PIL import Image
    iw, ih = Image.open(img).size
    pw = Inches(11); ph = int(pw * ih / iw)
    if ph > Inches(5.2): ph = Inches(5.2); pw = int(ph * iw / ih)
    x = (W - pw) // 2; y = Inches(1.7)
    # Cadre
    add_rect(s, x - Inches(0.1), y - Inches(0.1), pw + Inches(0.2), ph + Inches(0.2),
             fill=CARD, border=LINE, radius=False)
    s.shapes.add_picture(str(img), x, y, width=pw, height=ph)
add_footer(s, 7)

# =====================================================================
# Slide 8 — Étape 3 sauvegarde
# =====================================================================
s = prs.slides.add_slide(blank); add_bg(s)
add_title(s, "Étape 3 — Sauvegarde automatisée")
three_cards(s, [
    ("Mécanisme", [
        ("• Planification cron */30 * * * *", None),
        ("• mysqldump de la base WordPress", None),
        ("• tar.gz des fichiers du site", None),
        ("• Rétention : 10 dernières sauvegardes", None),
    ]),
    ("Stockage isolé", [
        ("• Volume dédié backup_storage", None),
        ("• Hébergé en zone data", None),
        ("   (sans Internet sortant)", None),
        ("• Aucun port exposé", None),
    ]),
    ("Restauration testée", [
        ("/restore.sh /backups/db_<TS>.sql.gz", None),
        ("", None),
        ("Dernier dump :", None),
        ("18,9 Ko (SQL) + 25,9 Mo (fichiers)", None),
    ]),
])
add_footer(s, 8)

# =====================================================================
# Slide 9 — Sécurité / VPN
# =====================================================================
s = prs.slides.add_slide(blank); add_bg(s)
add_title(s, "Sécurité & accès distant — VPN WireGuard")
three_cards(s, [
    ("Chiffrement & authentification", [
        ("• WireGuard (ChaCha20-Poly1305)", None),
        ("• Clé par peer + PresharedKey unique", None),
        ("   = authentification forte", None),
        ("• Exposition minimale : 51820/udp", None),
    ]),
    ("Ressource interne VPN-only", [
        ("• Service whoami sur 10.13.13.1:80", None),
        ("• Jamais exposé publiquement", None),
        ("• Démo : VPN actif → page OK,", None),
        ("   VPN coupé → injoignable", None),
    ]),
    ("Posture globale", [
        ("• 3 ports publics seulement", None),
        ("• TLS interne sur tout le web", None),
        ("• Zone data sans Internet sortant", None),
        ("• Production cohabitée intacte", None),
    ]),
])
add_footer(s, 9)

# =====================================================================
# Slide 10 — Bonus
# =====================================================================
s = prs.slides.add_slide(blank); add_bg(s)
add_title(s, "Bonus — Annuaire LDAP & partage de fichiers")
# 2 cartes
add_rect(s, Inches(0.7), Inches(1.85), Inches(6.0), Inches(4.6))
add_text(s, Inches(1.0), Inches(2.05), Inches(5.5), Inches(0.4),
         "OPENLDAP", size=12, bold=True, color=ACC)
for i, line in enumerate([
    "• Base : dc=entreprise,dc=local",
    "• OU people · groups",
    "• 3 comptes provisionnés :",
    "   hugo, shakil, matheo",
    "• Gestion centralisée des identités",
]):
    add_text(s, Inches(1.0), Inches(2.55 + i*0.55), Inches(5.5), Inches(0.5),
             line, size=15, color=INK)
add_rect(s, Inches(7.1), Inches(1.85), Inches(5.6), Inches(4.6))
add_text(s, Inches(7.4), Inches(2.05), Inches(5.0), Inches(0.4),
         "SAMBA", size=12, bold=True, color=ACC)
for i, line in enumerate([
    "• 2 partages :",
    "   partage-entreprise · technique",
    "• Utilisateurs & permissions explicites",
    "• Journalisation des accès",
    "• Non exposé publiquement",
    "   (accès interne / via VPN)",
]):
    add_text(s, Inches(7.4), Inches(2.55 + i*0.5), Inches(5.0), Inches(0.5),
             line, size=14, color=INK)
add_footer(s, 10)

# =====================================================================
# Slide 11 — Couverture grille (table)
# =====================================================================
s = prs.slides.add_slide(blank); add_bg(s)
add_title(s, "Couverture de la grille (note technique · coef. 3)")
grille = [
    ("Mise en œuvre d'un réseau simple", "4", "3 sous-réseaux, plan d'adressage, DNS/DHCP, routage"),
    ("Infrastructure client-serveur", "4", "Reverse proxy + 2 apps + DB + clients (web, VPN, Samba)"),
    ("Administration d'un système", "4", "Docker/Linux, services persistants, scripts Bash"),
    ("Virtualisation & maquette", "3", "Stack Docker Compose fidèle au besoin client"),
    ("Sécurisation (pare-feu, segmentation, VPN)", "3", "nftables, TLS, VPN, exposition minimale, zone data isolée"),
    ("Documentation technique", "3", "Doc + READMEs + support oral + dépôt Git public"),
]
tbl = s.shapes.add_table(len(grille) + 1, 3, Inches(0.7), Inches(1.85), Inches(12), Inches(4.7)).table
tbl.columns[0].width = Inches(4.5); tbl.columns[1].width = Inches(1.0); tbl.columns[2].width = Inches(6.5)
for j, h_ in enumerate(["Compétence", "Pond.", "Couverture"]):
    cell = tbl.cell(0, j); cell.fill.solid(); cell.fill.fore_color.rgb = CARD
    tf = cell.text_frame; tf.clear()
    p = tf.paragraphs[0]; r = p.add_run(); r.text = h_
    r.font.bold = True; r.font.size = Pt(13); r.font.color.rgb = MUT
for i, row in enumerate(grille, start=1):
    for j, val in enumerate(row):
        cell = tbl.cell(i, j); cell.fill.solid(); cell.fill.fore_color.rgb = BG
        tf = cell.text_frame; tf.clear()
        p = tf.paragraphs[0]
        if j == 1: p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = val
        r.font.size = Pt(13); r.font.color.rgb = INK
        if j in (0, 1): r.font.bold = True
        if j == 1: r.font.color.rgb = ACC
add_footer(s, 11)

# =====================================================================
# Slide 12 — Merci
# =====================================================================
s = prs.slides.add_slide(blank); add_bg(s)
add_text(s, Inches(0.7), Inches(2.4), Inches(12), Inches(1.4),
         "Merci.", size=64, bold=True, color=INK, align=PP_ALIGN.CENTER)
add_text(s, Inches(0.7), Inches(3.9), Inches(12), Inches(0.6),
         "Questions ?", size=24, color=MUT, align=PP_ALIGN.CENTER)
add_text(s, Inches(0.7), Inches(5.4), Inches(12), Inches(0.5),
         "Dépôt : github.com/H129hj/infra-entreprise-b1",
         size=14, color=MUT, align=PP_ALIGN.CENTER)
add_text(s, Inches(0.7), Inches(5.85), Inches(12), Inches(0.4),
         GROUP_FOOTER, size=14, color=MUT, align=PP_ALIGN.CENTER)
add_footer(s, 12)

# ----
out = DOCS / "Presentation-Oral.pptx"
prs.save(out)
print(f"Fichier généré : {out}  ({out.stat().st_size//1024} Ko, {len(prs.slides)} slides)")
