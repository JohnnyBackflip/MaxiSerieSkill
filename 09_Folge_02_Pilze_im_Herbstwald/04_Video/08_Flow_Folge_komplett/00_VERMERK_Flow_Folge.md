# Folge 02 „Pilze im Herbstwald“ – komplette Flow-Fassung v001 (2026-11-05)

- `Folge_02_Pilze_im_Herbstwald_Flow_v001.mp4` (109 s, 3 s Titelkarte + 26 Einstellungen), dieselbe Datei mit zuschaltbarer deutscher Untertitelspur: `…_mit_Untertitelspur.mp4`, Untertitel einzeln: `.srt`.
- Quellen: `06_Flow_Szenenvideos_r6` (SH010–SH051) und `07_Flow_Szenenvideos_Rest_r7` (SH060–SH220).
- Schnitt mit `flow_clips_schneiden.py` (Spracherkennung large-v3-turbo + VAD): Anfang bleibt, Ende = Ende des Sprachabschnitts mit dem letzten Wort + 0,5 s; Mindestlänge 2,5 s. Schnittliste: `…_Schnittliste.md`.
- Kontrolle: alle geschnittenen Teile erneut abgeschrieben und mit dem Original verglichen → kein Wort abgeschnitten (SH200 nur „Mh“-Brummen unterschiedlich erkannt, Clip ungeschnitten).
- Offen: Wer spricht (Stimmlage) erkennt die Software nicht – bitte anhören.

## v002 (2026-11-05, Kritik zu v001)
- SH040: Veo hatte ~0,6 s Musik vor Karls Szene → Clip ab 0,6 s (`--start SH040=0.6`, im Spektrogramm geprüft: Tonlinien weg).
- SH060: Bäume standen auf der Landstraße (Blockout: Baum_062/063/065 auf/an der Fahrbahn → an den Rand verschoben, Backup `Herbstwald_Blockout_vor_Strassenfix_2026-11-05.blend`) → Mockup, Flow-Bild und Flow-Video neu (altes Video in `07_…/rejected/`).
- Serien-Intro vorangestellt (siehe `00_Intro_Maxi_Cartoons/00_VERMERK_Intro.md`), danach Titelkarte „Folge 02 – Pilze im Herbstwald“.
- Dateien: `Folge_02_Pilze_im_Herbstwald_Flow_v002.mp4` (112,6 s), `…_v002_mit_Untertitelspur.mp4`.
- **Musiktest** (Original unverändert, Prüfsumme kontrolliert): `…_v002_MUSIKTEST.mp4` – Gemini-Track „Leaves and Tiny Treasures“ unter SH060–SH150 (36,9–82,6 s), „Shared Plates and Smiles“ unter SH190–SH220 (94,35–112,6 s), je −9 dB, mit Ducking beim Sprechen, 1,5 s Blenden; Werkzeug `musik_unterlegen.py`.

## v003 (2026-11-05): neues Intro, Einblenden, Musik zum Start
- Intro v3 (4,54 s, endet mit Maxis Sprung, Musik stoppt dort). **Titelkarte entfällt.**
- SH010 wird 1,0 s aus Schwarz eingeblendet (Bild; Ton unverändert).
- Musik zum Start: `Musik_01_Herbstwald_Leaves_and_Tiny_Treasures.mp3` von 4,54 s bis 13,5 s (unter SH010 + SH011), −9 dB, Ducking, 1,5 s Blenden. Die Musiktest-Cues aus v002 (SH060–SH150, SH190–SH220) sind NICHT enthalten.
- Gebaut aus den geschnittenen Teilen von v002 (keine neue Spracherkennung): `…_v003_teile/` (Intro + SH010 neu, Rest als Verknüpfung auf `…_v002_teile/`; ein älterer, unvollständiger v003-Teile-Ordner wurde dabei ersetzt).
- Dateien: `Folge_02_Pilze_im_Herbstwald_Flow_v003.mp4` (108,1 s), `…_v003_mit_Untertitelspur.mp4`, `…_v003.srt` (v002-Untertitel um −4,474 s verschoben), Zwischenstand ohne Musik `…_v003_ohne_Musik.mp4`.

## v004 (2026-11-05): Startmusik 1 s nach vorne
- Kritik: Ton der Startmusik verschoben. Ursache: `Musik_01_…mp3` beginnt mit ~1,2 s Stille. Cue jetzt `…@4.54-13.5:ab=1.0:laut=-9` (Lied ab Sekunde 1,0), sonst wie v003.
- Dateien: `Folge_02_Pilze_im_Herbstwald_Flow_v004.mp4`, `…_v004_mit_Untertitelspur.mp4`, `…_v004.srt` (= v003).

## v005 (2026-11-06): neues Intro + Wald-/Küchenmusik wieder drin
- Kritik: Intro hat sich geändert (Schwarzblende am Ende, Ton wie v2); Musik aus dem Musiktest fehlte. **Ursache:** v003/v004 wurden nur mit dem Start-Cue gebaut, die Musiktest-Cues aus v002 (SH060–SH150, SH190–SH220) waren dabei bewusst draußen geblieben und wurden danach nicht wieder eingesetzt.
- Intro: aktuelles `00_Intro_Maxi_Cartoons/Maxi_Cartoons_Intro.mp4` (4,542 s, gleiche Länge wie vorher → alle Zeiten und Untertitel unverändert). Teile: `…_v005_teile/` (Intro neu, SH010 aus v003 mit Einblendung, Rest als Verknüpfung).
- Musik (`musik_unterlegen.py`, `--ducking --fade 1.5`, je −9 dB):
  - `Musik_01_Herbstwald…mp3@4.54-13.5:ab=1.0` (Folgenanfang, SH010–SH011)
  - `Musik_01_Herbstwald…mp3@32.414-78.123` (SH060–SH150, wie Musiktest v002)
  - `Musik_02_Kueche_Abend…mp3@89.88-108.116` (SH190–SH220, wie Musiktest v002)
- Kontrolle: Musik-Restsignal (mit − ohne Musik) in allen drei Abschnitten deutlich über dem Grundrauschen; Intro-Bild = neue Fassung mit Schwarzblende.
- Dateien: `Folge_02_Pilze_im_Herbstwald_Flow_v005.mp4` (108,1 s), `…_v005_mit_Untertitelspur.mp4`, `…_v005.srt` (= v004), `…_v005_ohne_Musik.mp4`.

## v006 (2026-11-06): Stimmen-Ausreißer am Anfang von SH051 entfernt
- Kritik: bei ~28 s (SH051, Mama „Lass ihn reden“) ganz kurz eine kaputte Stimme. Ursache: Veo-Clip `06_…_r6/SH051_Mama_Lass_ihn_reden.mp4` hat in den ersten 0,075 s einen Tonfetzen (−21…−26 dB), dann Stille, Mamas Satz ab 0,52 s.
- Änderung: Teil `…_v006_teile/007_SH051.mp4` – Bild unverändert (Stream-Copy), Ton 0–0,4 s stumm, 0,05 s Einblendung. Keine Zeitverschiebung → Musik-Cues und Untertitel wie v005.
- Kontrolle: Pegel 28,5–28,9 s vorher −26 dB, jetzt still; Sprache ab ~29,0 s pegelgleich mit v005.
- Dateien: `Folge_02_Pilze_im_Herbstwald_Flow_v006.mp4`, `…_v006_mit_Untertitelspur.mp4`, `…_v006.srt` (= v005), `…_v006_ohne_Musik.mp4`.
