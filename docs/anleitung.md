# ToneSeq — Anleitung

ToneSeq ist ein **Schritt-Sequenzer**: Du setzt ein Muster in ein Raster, das
Werkzeug läuft die Schritte der Reihe nach ab und spielt dabei Klänge. Es gibt zwei
Spuren-Ebenen — **Drums** (Schlagzeug) und **Notes** (Töne) — und eine **Graph**-Ansicht,
in der gespeicherte Muster als Knoten erscheinen.

Alles läuft im Browser. Es gibt kein Konto, keine Anmeldung, und das Werkzeug
speichert nichts auf einem Server.

## 1. Losspielen

1. `https://toneseq.mekotools.de` öffnen.
2. Auf **▶ Play** drücken. Der Takt läuft.
3. Im Raster (**Drums**) die Felder anklicken, in denen ein Schlag erklingen soll.
4. Wieder **■ Stop** drücken, um anzuhalten.

Das Raster hat **16 Schritte** (vier Zählzeiten zu vier Schlägen). Ist ein Feld
gesetzt, klingt die zugehörige Stimme in diesem Schritt.

## 2. Tempo und Takt

* **BPM**: das Tempo in Schlägen pro Minute. Kleiner Wert = langsam, großer Wert = schnell.
* **Click**: der Klick zum Mitüben (Metronom) — ein- und ausschaltbar.
* **Fwd / Rev / Ping**: die **Laufrichtung** des Rasters.
  *Fwd* läuft vorwärts, *Rev* rückwärts, *Ping* hin und zurück. Drums und Notes
  können unterschiedlich laufen; **Link** lässt die Drums der Richtung der Notes folgen.

## 3. Die Notes-Spur (Töne)

* In der Klavier-Roll (**piano-roll**) setzt du Töne über mehrere Schritte.
* Unten liegt eine kleine Klaviatur (C bis B) — damit hörst du einen Ton einzeln.
* **−** und **+** verschieben die Oktave (also die Tonhöhe insgesamt nach oben oder unten).
* **M**, **Rnd**, **Clr**, **Save** gelten jeweils für die Notes-Spur:
  stumm schalten, zufälliges Muster würfeln, leeren, speichern.

## 4. Klang einstellen (Controls)

Hinter **⚙ Controls** liegen die Regler für die Ton-Spur:

* **Welle**: Sine (weich), Square (voll/hohl), Saw (scharf) — die Grundform des Tons.
* **Hüllkurve (ADSR)**: Attack (Anschlag), Decay (Abklingen), Sustain (Halten),
  Release (Ausklang). Kurz gesagt: wie ein Ton beginnt, steht und endet.
* **Filter** mit **LP** (Tiefpass: hohe Anteile weg, dumpfer) und **HP**
  (Hochpass: tiefe Anteile weg, dünner), dazu die Flankensteilheit/Resonanz (Q)
  und die Grenzfrequenz.
* **Hall**: Anteil (Send) und Nachhallzeit (Decay).
* **Vol**: Gesamtlautstärke.

## 5. Speichern und weitergeben

* **Save** legt das aktuelle Muster als Knoten in der **Graph**-Ansicht ab
  (unten der Bereich *Graph*). So kannst du mehrere Muster nebeneinanderstellen.
* **Link / Copy** erzeugt einen **Link, der das Muster enthält** — er wird in die
  Adresszeile gelegt und in die Zwischenablage kopiert. Diesen Link kannst du
  weitergeben; wer ihn öffnet, sieht dasselbe Muster.
* **✕ Clear All** leert alles.

> **Wichtig:** Dein Muster steht **nur in der Adresse** und im Speicher der Seite.
> Es wird nichts auf einen Server geschickt und nichts dauerhaft im Browser abgelegt.
> Wenn du die Seite schließt, ohne den Link gespeichert zu haben, ist das Muster weg.
> Also: **erst kopieren, dann schließen.**

## 6. Datenschutz und Technik

* Das Werkzeug lädt **keine** fremden Inhalte: keine Zählwerke, keine Schriften von
  außen, keine Werbung. Die Regel dafür steht als Content-Security-Policy auf dem Server.
* Ton wird ausschließlich im Browser erzeugt. Es wird **nichts aufgenommen**; ein
  Mikrofon wird nicht benutzt.
* Die sechs Schlagzeugklänge sind freie Aufnahmen (CC0); ihre Herkunft steht in jeder
  Datei und in `klang/manifest.json` (siehe `NOTICE`).

## 7. Wenn etwas nicht klingt

1. **Es bleibt still, obwohl Play läuft:** Der Browser lässt Ton erst nach einer
   eigenen Handlung zu. Einmal auf **▶ Play** klicken (das ist diese Handlung).
   Bei Kopfhörern prüfen, ob der Browser-Tab stumm geschaltet ist.
2. **Kein Ton auf dem Tablet:** Lautstärke des Geräts prüfen; manche Geräte schalten
   den Ton im Energiesparmodus ab.
3. **Muster verschwunden:** Die Seite wurde neu geladen, ohne dass der Link gespeichert
   war (siehe Abschnitt 5). Das ist keine Störung, sondern so gebaut.
4. **Seite lädt nicht:** kurze Wartezeit und Neuladen; das Werkzeug läuft auf unserem
   eigenen Server, der bei einer Aktualisierung für wenige Sekunden nicht erreichbar sein kann.

## 8. Grenzen

* Das Werkzeug ist auf **Maus/Tastatur und Tablet** ausgelegt; ein sehr kleines
  Handydisplay macht das Raster unübersichtlich.
* Es gibt **keine** Aufnahmefunktion und **keinen** Ausdruck. Wer das Ergebnis
  sichern will, teilt den Link (Abschnitt 5) oder nimmt den Bildschirm auf.
* Die Graph-Ansicht ist eine Spielwiese, kein Notensatz.
