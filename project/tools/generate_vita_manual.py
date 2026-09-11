#!/usr/bin/env python3
"""Generate FEARVita's original Vita Bubble manual pages (960x544 PNG)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 960, 544
BG = (17, 20, 24)
RED = (190, 36, 58)
PINK = (238, 147, 160)
WHITE = (242, 244, 246)
TEXT = (196, 202, 208)
MUTED = (132, 140, 148)
LINE = (57, 64, 71)

FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def wrap_px(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        test = word if not cur else cur + " " + word
        if draw.textbbox((0, 0), test, font=fnt)[2] <= width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def base_page(num, title, kicker="FEARVITA · HANDBUCH"):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 11, H), fill=RED)
    d.text((42, 28), kicker, font=font(18, True), fill=PINK)
    d.text((42, 61), title, font=font(35, True), fill=WHITE)
    d.line((42, 111, 918, 111), fill=LINE, width=2)
    d.line((42, 500, 918, 500), fill=LINE, width=1)
    d.text((42, 510), "FEARVita 0.02 · M29AW", font=font(13), fill=MUTED)
    d.text((860, 508), f"{num:02d}/05", font=font(15, True), fill=PINK)
    return im, d


def paragraph(d, text, y, size=20, width=840, x=54, leading=8, fill=TEXT, bold=False):
    f = font(size, bold)
    for line in wrap_px(d, text, f, width):
        d.text((x, y), line, font=f, fill=fill)
        y += size + leading
    return y


def bullet(d, title, body, y):
    d.ellipse((54, y + 8, 62, y + 16), fill=PINK)
    d.text((76, y), title, font=font(19, True), fill=WHITE)
    y += 28
    return paragraph(d, body, y, size=17, width=800, x=76, leading=6) + 10


def save_pages(outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)

    im, d = base_page(1, "Willkommen")
    y = 138
    y = paragraph(d, "FEARVita bringt F.E.A.R., Extraction Point und Perseus Mandate in einer Vita-Anwendung zusammen.", y, 21)
    y += 18
    y = bullet(d, "Frontend", "Alle drei Retail-Menüs, Menüvideos, Musik und UI-Sounds sind integriert.", y)
    y = bullet(d, "Sprache", "Die Vita-Systemsprache steuert die FEARVita-Oberfläche. Fehlende Retail-Lokalisierung wird nicht als Originalübersetzung ausgegeben.", y)
    y = bullet(d, "Aktueller Meilenstein", "Singleplayer-Weltstart, Server-/ObjectDLL-Runtime und Gameplay werden schrittweise aktiviert.", y)
    im.save(outdir / "001.png", optimize=True)

    im, d = base_page(2, "Spieldaten")
    y = 138
    y = paragraph(d, "Kopiere deine legal erworbenen PC-Spieldaten nach ux0:data/FEARVita/data/. FEARVita enthält keine Retail-Archive.", y, 20)
    y += 18
    y = bullet(d, "F.E.A.R.", "Basisarchive liegen direkt im data-Ordner.", y)
    y = bullet(d, "Extraction Point", "Expansion-Dateien liegen unter data/FEARXP/.", y)
    y = bullet(d, "Perseus Mandate", "Expansion-Dateien liegen unter data/FEARXP2/.", y)
    y = bullet(d, "Steam-Hinweis", "Die aktuelle Steam-Fassung von F.E.A.R. liefert die Spieloberfläche auf Englisch. Deutsche Vita-Texte sind deshalb teilweise FEARVita-Fallbacks.", y)
    im.save(outdir / "002.png", optimize=True)

    im, d = base_page(3, "Spielauswahl & Menüs")
    y = 138
    y = bullet(d, "Touch", "Ein Tap markiert ein Spiel mit Rahmen. Ein zweiter Tap auf das markierte Spiel startet es.", y)
    y = bullet(d, "Tasten", "Steuerkreuz wählt, X bestätigt, Kreis geht zurück. START öffnet bzw. schließt später das Pausenmenü.", y)
    y = bullet(d, "Original-Sounds", "Auswahl und Bestätigung verwenden die Retail-Menüsounds des Spiels.", y)
    y = bullet(d, "Standard", "Unter Steuerung > Standard wiederherstellen wird immer das FEARVita-Vita-Profil geladen – in allen drei Kampagnen.", y)
    im.save(outdir / "003.png", optimize=True)

    im, d = base_page(4, "Logs & Tests")
    y = 138
    y = paragraph(d, "Bei Tests bitte den passenden Log sichern. Die Kampagnen überschreiben sich nicht mehr gegenseitig.", y, 20)
    y += 18
    logs = [
        ("Launcher", "ux0:data/FEARVita/fear_launcher.log"),
        ("F.E.A.R.", "ux0:data/FEARVita/fear_fear.log"),
        ("Extraction Point", "ux0:data/FEARVita/fear_ep.log"),
        ("Perseus Mandate", "ux0:data/FEARVita/fear_pm.log"),
    ]
    for name, path in logs:
        d.text((54, y), name, font=font(18, True), fill=WHITE)
        d.text((260, y), path, font=font(16), fill=TEXT)
        y += 48
    y += 8
    paragraph(d, "Bei einem Crash zusätzlich den neuen Core-Dump sichern. Ein Log direkt nach dem Fehler ist am wertvollsten.", y, 18)
    im.save(outdir / "004.png", optimize=True)

    im, d = base_page(5, "Steuerung · Standardprofil")
    left = [
        ("Linker Stick", "Bewegen"), ("Rechter Stick", "Umsehen"),
        ("R", "Feuern"), ("L", "Zielen"), ("X", "Springen"),
        ("Kreis", "Ducken"), ("Quadrat", "Nachladen"),
        ("Dreieck", "Benutzen / Aktivieren"),
    ]
    right = [
        ("St.-Kreuz ↑", "SlowMo"), ("St.-Kreuz ↓", "Granate"),
        ("St.-Kreuz ←/→", "Vorherige / nächste Waffe"),
        ("SELECT", "Missionsziele"), ("START", "Menü"),
        ("Touch vorn links", "Taschenlampe"),
        ("Touch vorn Mitte", "Nahkampf"),
        ("Touch vorn rechts", "Nächste Waffe"),
    ]

    def col(items, x, y):
        for key, action in items:
            d.text((x, y), key, font=font(16, True), fill=WHITE)
            d.text((x + 184, y), action, font=font(16), fill=TEXT)
            y += 38

    col(left, 54, 136)
    col(right, 492, 136)
    d.rounded_rectangle((54, 450, 906, 486), radius=7, outline=LINE, width=1)
    d.text((68, 458), "Touchpad hinten: doppeltippen + zweiten Kontakt halten = Sprint", font=font(16, True), fill=PINK)
    im.save(outdir / "005.png", optimize=True)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    save_pages(here.parent / "sce_sys" / "manual")
