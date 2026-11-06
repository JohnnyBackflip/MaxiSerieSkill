# Veo/Flow-Dialog-Regeln (STRIKT, aus den Veo/Flow-Guides + Folge 02, 2026-11-05)

Gilt schon beim Szenenplan, nicht erst beim Video.

## Szenenplan
1. **Eine Einstellung = EIN Sprecher.** Zwei Sätze von zwei Figuren → zwei Einstellungen (SH010 + SH011). Mehrsprecher-Szenen getrennt erzeugen und schneiden.
2. **Zeilen kurz:** max. ~8 Wörter, passt in ≤ 3 s.
3. **Sprechzeitfenster je Einstellung festlegen** (z. B. 0–1 s Aktion, 1–4 s Satz).
4. **Sprecher groß, halbnah oder nah, frontal zur Kamera** – kein Profil, kein Rücken, nicht klein im Hintergrund (sonst schlechte Lippensynchronität). Die anderen sind still im Bild.

## Prompt
5. **Zeitblöcke:** `[00:00-00:01] <Aktion> … [00:01-00:04] <Sprecher> says: <Zeile>`. Die Zeile muss in ihren Block passen (Überlänge → gehetzte oder abgeschnittene Sprache).
6. **Sprecher direkt vor der Zeile über sichtbares Merkmal + Bildposition benennen**, nicht nur mit Namen: „the woman in the yellow sweater on the left says: …“.
7. **Nur die Stimme der sprechenden Figur beschreiben** (z. B. „bright cheerful voice of a five-year-old boy“). Alle anderen ausdrücklich: „everyone else stays silent with closed mouths“. **Keine Stimmenliste aller Figuren** im gemeinsamen Stilblock (Fehler 2026-11-05: falsche Person sprach).
8. **Dialog nach dem Doppelpunkt ohne Anführungszeichen**, am Ende „(no subtitles)“.
9. **Keine Zeile nur aus einem Laut** („Hä?!“, „Bäääh!“) → Flow bricht mit „Fehler bei der Audiogenerierung“ ab. Immer echte Wörter ergänzen („Hä? Was war das denn?“).
10. **Off-Sprecher** (Figur nicht sichtbar, z. B. im fahrenden Auto) als „off-screen voice“ ausweisen.
11. Keine Musik verlangen; Veo setzt manchmal trotzdem einen Musikschnipsel an den Anfang → beim Schnitt prüfen und mit `--start` entfernen.

## Erzeugen
12. Frames → **nur Startbild** (ohne Endbild besser), Veo 3.1 Fast, 720p, Länge = Szenenlänge (4/6/8 s).
13. Startbild = Sprecher-Einstellung, in der der Sprecher groß und frontal ist (vorhandenes A/B-Bild oder eigenes `SHxxxS`).
14. **Notfall-Ausweg:** Clip ohne Dialog erzeugen, Stimme nachträglich anlegen.

## Prüfen
15. Jeden Clip mit `sprache_abschreiben.py` gegen die Prompt-JSON prüfen (Wortlaut, Zeitfenster) und **anhören, ob die richtige Stimme spricht** (Whisper kann keine Sprecher unterscheiden). Falsch → neu erzeugen.
