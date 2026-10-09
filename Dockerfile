# ToneSeq für MekoTools — Abbild, das auf jedem Server gleich aussieht.
#
# Fassung: fester Quelltext-Abzug (keine schwimmende Marke), damit dasselbe
# Ergebnis reproduzierbar ist. ToneSeq braucht keinen Bauschritt: die Dateien
# werden entpackt, die sechs Klänge ersetzt, Adressen gesetzt, dann kopiert.
#
# Erste Stufe: zubereiten (Werkzeuge bleiben hier und landen NICHT im Abbild).
#
# FALLE: Ein ARG, das in einer FROM-Zeile benutzt wird, muss VOR dem ersten FROM
# stehen (globaler Gültigkeitsbereich). Steht es zwischen zwei FROM-Zeilen, gilt es
# nur für die Stufe, in der es deklariert ist — die zweite Stufe erbt es NICHT und
# der Bau scheitert mit "base name (${...}) should not be blank".
ARG BASIS_ALPINE=alpine:3.20
ARG BASIS_NGINX=nginx:alpine-slim

FROM ${BASIS_ALPINE} AS zubereiten

ARG QUELLE_DATEI=https://github.com/joedickey/ToneSeq/archive/9c70c513fa01cd828c70c9dd503974145feccadf.tar.gz

RUN apk add --no-cache curl tar python3

WORKDIR /web
RUN curl -fsSL "$QUELLE_DATEI" | tar xz --strip-components=1 \
 && test -f index.html && test -f app.js && test -f vendor/Tone.js \
 && test "$(ls audio/*.mp3 | wc -l)" = "6"

COPY klang /klang
COPY scripts/klange-setzen.py /klange-setzen.py
RUN python3 /klange-setzen.py /web /klang \
 && test "$(ls audio/*.mp3 | wc -l)" = "6" \
 && ! grep -rq "toneseq\.com" . \
 && ! grep -rqiE "goatcounter|gtag|google-analytics|plausible|matomo" index.html app.js \
 && grep -q "mt-hinweis" index.html \
 && grep -q "toneseq.mekotools.de" index.html

# Zweite Stufe: nur der Webserver und die fertigen Dateien.
FROM ${BASIS_NGINX}

COPY --from=zubereiten /web/ /usr/share/nginx/html/
COPY config/default.conf /etc/nginx/conf.d/default.conf

RUN nginx -t

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1/gesundheit || exit 1
