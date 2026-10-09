#!/usr/bin/env python3
"""Setzt die freien Klänge in den festgeschriebenen Quelltext-Abzug von ToneSeq ein,
setzt die Adressangaben auf unsere Auslieferung und kennzeichnet die geänderte Fassung.

ToneSeq hat KEINEN Bauschritt (reines HTML/JS) — hier wird nur kopiert und geprüft.
Jede Abweichung bricht ab: lieber kein Abbild als ein falsches.

Aufruf: klange-setzen.py <quelle> <klangverzeichnis>
"""
import json
import re
import shutil
import sys
from pathlib import Path

NOTIZ = ("Angepasste Fassung für MekoTools: die sechs Klänge wurden durch freie Aufnahmen "
         "(CC0) ersetzt. Alles läuft im Browser.")
ADRESSE = "https://toneseq.mekotools.de"
ANZ = 6


def anker(bedingung, text):
    if not bedingung:
        sys.exit(f"ANKER: {text}")


def mp3_format(datei):
    """MP3-Kopfdaten ohne Fremdwerkzeug lesen (das Bauabbild hat kein ffprobe)"""
    d = datei.read_bytes()
    id3 = d[:3] == b"ID3"
    i = 0
    if id3 and len(d) > 10:
        groesse = ((d[6] & 0x7F) << 21) | ((d[7] & 0x7F) << 14) | ((d[8] & 0x7F) << 7) | (d[9] & 0x7F)
        i = 10 + groesse
    while i < len(d) - 4:
        if d[i] == 0xFF and (d[i + 1] & 0xE0) == 0xE0:
            b1, b2, b3 = d[i + 1], d[i + 2], d[i + 3]
            version = (b1 >> 3) & 0x03
            schicht = (b1 >> 1) & 0x03
            bitraten = (0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320)
            raten = {3: [44100, 48000, 32000], 2: [22050, 24000, 16000], 0: [11025, 12000, 8000]}
            return {"id3": id3, "mpeg": version, "layer": schicht,
                    "rate": raten.get(version, [0])[(b2 >> 2) & 0x03],
                    "kanaele": 1 if ((b3 >> 6) & 0x03) == 3 else 2,
                    "kbit": bitraten[(b2 >> 4) & 0x0F]}
        i += 1
    return {"id3": id3, "mpeg": 0, "layer": 0, "rate": 0, "kanaele": 0, "kbit": 0}


def main():
    quelle, klang = Path(sys.argv[1]), Path(sys.argv[2])

    # 1. Gestalt des Abzugs
    for datei in ("index.html", "app.js", "style.css", "vendor/Tone.js"):
        anker((quelle / datei).is_file(), f"{datei} fehlt")
    seite = quelle / "index.html"
    text = seite.read_text()
    if ADRESSE not in text:
        anker("toneseq.com" in text, "Adressangabe toneseq.com nicht gefunden")

    # 2. Plan und Zieldateien
    plan = json.loads((klang / "manifest.json").read_text())
    anker(len(plan) == ANZ, f"Manifest hat {len(plan)} statt {ANZ} Einträge")
    for e in plan:
        ziel = quelle / "audio" / e["ziel"]
        anker(ziel.is_file(), f"Zieldatei fehlt: {e['ziel']}")
        neu = klang / e["ziel"]
        anker(neu.is_file(), f"neuer Klang fehlt: {e['ziel']}")
        ziel.write_bytes(neu.read_bytes())

    # 3. genau ANZ Klangdateien, Namen wie im Plan
    dateien = sorted(p.name for p in (quelle / "audio").glob("*.mp3"))
    anker(len(dateien) == ANZ, f"{len(dateien)} Klangdateien statt {ANZ}")
    anker(dateien == sorted(e["ziel"] for e in plan), "Dateiliste weicht vom Plan ab")

    # 4. Format der neuen Dateien
    for e in plan:
        f = mp3_format(quelle / "audio" / e["ziel"])
        anker(f["id3"], f"{e['ziel']}: keine ID3-Kennung (Herkunft fehlt)")
        anker(f["mpeg"] == 3 and f["layer"] == 1, f"{e['ziel']}: kein MPEG-1 Layer III")
        anker(f["rate"] == 44100, f"{e['ziel']}: {f['rate']} Hz statt 44100")
        anker(f["kanaele"] == 1, f"{e['ziel']}: {f['kanaele']} Kanäle statt 1")
    print(f"Formprüfung: {ANZ} Dateien, 44,1 kHz, mono, ID3 vorhanden")

    # 5. Adressangaben auf unsere Auslieferung
    for alt, neu in (("https://toneseq.com/sitemap.xml", f"{ADRESSE}/sitemap.xml"),
                     ("https://toneseq.com/og-image.png", f"{ADRESSE}/og-image.png"),
                     ("https://toneseq.com", ADRESSE)):
        text = text.replace(alt, neu)
    anker("toneseq.com" not in text, "fremde Adresse noch in index.html")
    seite.write_text(text)
    for datei, alt, neu in (("robots.txt", "https://toneseq.com/sitemap.xml", f"{ADRESSE}/sitemap.xml"),
                            ("sitemap.xml", "https://toneseq.com/", f"{ADRESSE}/")):
        p = quelle / datei
        if p.is_file():
            t = p.read_text().replace(alt, neu)
            p.write_text(t)
    # Nicht zur Anwendung gehörende Beigaben des Originals entfernen: sie liegen sonst
    # im Wurzelverzeichnis des Webservers und werden mit ausgeliefert. CNAME gehört zu
    # GitHub Pages, README.md und .claude/ sind Beigaben zur Entwicklung.
    entfernt = []
    for beigabe in ("CNAME", "README.md", ".claude"):
        p = quelle / beigabe
        if p.is_dir():
            shutil.rmtree(p)
            entfernt.append(beigabe)
        elif p.is_file():
            p.unlink()
            entfernt.append(beigabe)
    print("Beigaben entfernt: " + (", ".join(entfernt) if entfernt else "keine"))

    # 6. Kennzeichnung der Änderung sichtbar in der Fußzeile
    if NOTIZ not in text:
        anker('<nav class="info-links">' in text, "Fußzeile (info-links) nicht gefunden")
        text = seite.read_text()
        text = text.replace(
            "<footer id=\"info-bar\">",
            "<footer id=\"info-bar\">\n    <p class=\"mt-hinweis\">" + NOTIZ + "</p>", 1)
        anker('class="mt-hinweis"' in text, "Hinweis nicht eingesetzt")
        seite.write_text(text)
        css = quelle / "style.css"
        c = css.read_text()
        if ".mt-hinweis" not in c:
            c += ("\n.mt-hinweis {\n  margin: 0.15rem 0 0.35rem;\n  text-align: center;\n"
                  "  font-size: 0.68rem;\n  opacity: 0.8;\n}\n")
            css.write_text(c)
        print("Fußzeile: MekoTools-Hinweis ergänzt")
    else:
        print("Fußzeile: Hinweis war schon vorhanden")

    # 7. Gegenprobe über den ganzen Baum: keine fremde Adresse darf übrig bleiben.
    fremde = []
    for p in quelle.rglob("*"):
        if p.is_file() and p.suffix.lower() in (".html", ".js", ".css", ".json", ".txt", ".xml", ".md", ".svg"):
            if "toneseq.com" in p.read_text(errors="ignore"):
                fremde.append(str(p.relative_to(quelle)))
    anker(not fremde, "fremde Adresse noch in: " + ", ".join(fremde))
    print("Gegenprobe: keine fremde Adresse im Baum")


if __name__ == "__main__":
    main()
