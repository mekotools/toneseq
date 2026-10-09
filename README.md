# ToneSeq — Auslieferung für MekoTools

Dieses Verzeichnis enthält **alles, was zum Bauen und Ausliefern der MekoTools-Fassung
von ToneSeq nötig ist** — nicht den Quelltext selbst. Der Quelltext wird beim Bauen aus
dem amtlichen Archiv geholt, auf eine **feste Fassung** festgeschrieben:

> `joedickey/ToneSeq`, Fassung `9c70c513fa01cd828c70c9dd503974145feccadf` (02.03.2026)

Damit ist jedes gebaute Abbild reproduzierbar, und ein späterer Wechsel im Original
verändert unsere Fassung nicht.

## Was wir ändern — und warum

| Änderung | Grund |
| --- | --- |
| Die sechs Klänge (`audio/*.mp3`) ersetzt | Das Original nannte für **keine** Datei eine Herkunft (keine Kennzeichnung im Klangkopf, im Projekt kein Klangpaket genannt). Ein Werkzeug, das wir weitergeben, darf keine Klänge ohne belegte Herkunft enthalten. Die Ersatzklänge sind freie Aufnahmen (CC0), belegt in `klang/manifest.json` **und** im Klangkopf jeder Datei. |
| Adressangaben auf `toneseq.mekotools.de` gesetzt | Kanonische Adresse, Vorschaubild, Sitemap und strukturierte Daten zeigten sonst auf die Seite des Autors. |
| Hinweis in der Fußzeile ergänzt | Kennzeichnung der geänderten Fassung (bei CC BY verlangt) — sichtbar, nicht nur im Quelltext. |
| `CNAME` entfernt | Die Datei gehört zu GitHub Pages und hat auf unserem Server keine Bedeutung. |
| Fremdaufrufe verboten (CSP) | `default-src 'self'`, `connect-src 'self'` — das Werkzeug kann keinen fremden Server erreichen. Belegt: der Quelltext enthält außer einem Spenden-Verweis und einem Feedback-Verweis (beide nur Klickziele) keine fremden Adressen. |

## Bauen

Auf dem Zielrechner wird **nicht** gebaut. Der Bau läuft bei GitHub
(`.github/workflows/abbild-bauen.yml`) und legt das Abbild in der Registry ab:

```
ghcr.io/mekotools/toneseq:latest
ghcr.io/mekotools/toneseq:<Commit>
```

ToneSeq hat **keinen Bauschritt** (reines HTML/JS): im Bauabbild wird der Quelltext
entpackt, `scripts/klange-setzen.py` setzt die Klänge und Adressen, dann wird kopiert.
Die erste Stufe (`alpine`) enthält Python und bleibt im fertigen Abbild **nicht** enthalten;
was ausgeliefert wird, ist `nginx:alpine-slim` plus die Dateien.

Lokal nachbauen (ohne Abbild, nur die Dateien):

```
cp -r <geklonter-toneseq> /tmp/web
python3 scripts/klange-setzen.py /tmp/web ./klang
```

Das Skript ist **wiederholbar**: ein zweiter Lauf ändert nichts mehr. Jede Abweichung
bricht ab — lieber kein Abbild als ein falsches.

## Prüfungen, die der Bau selbst erzwingt

* Gestalt des Quelltext-Abzugs (Dateien vorhanden)
* genau sechs Klangdateien, Namen wie im Manifest
* jede Datei MPEG-1 Layer III, 44,1 kHz, mono, mit ID3-Kennung
* keine fremde Adresse mehr im Quelltext
* kein Zählwerk (goatcounter, gtag, Analytics, Matomo, Plausible)
* Hinweis in der Fußzeile vorhanden, Adresse gesetzt

## Ausliefern

```
ZIEL_HOST=root@192.168.1.20 ZIEL_PFAD=/poolio/docker/mekotools-web ...
```

(Die Auslieferung selbst läuft über das Skript im Werkzeug-Bestand; Einzelheiten im
Skill `mekotools-katalog`.)

## Herkunft und Lizenz

* Werk: ToneSeq, © Joe Dickey, **CC BY-NC 4.0** (Namensnennung, keine kommerzielle Nutzung).
* Unsere Fassung: dieselbe Lizenz; die Änderungen sind in `NOTICE` und auf der Seite selbst benannt.
* Eingebundene Programmbibliotheken: Tone.js, cytoscape.js, lz-string (alle MIT) —
  sie lagen bereits im Original bei (`vendor/`).
