# Flow-Szenenvideos Runde 7 – SH060 bis SH220 (2026-11-05)

- Ein-Sprecher-Regel: SH130 → SH130 (Mama) + SH131 (Maxi); SH190 → SH190 (Mama) + SH191 (Papa).
- Startbilder: wo der Sprecher groß/frontal war, vorhandenes A- oder B-Bild (SH070B, SH080B, SH130B für SH131, SH170A für SH160, SH170B für SH170); sonst NEUE Sprecher-Einstellungen
  SH090S, SH120S, SH130S, SH190S, SH191S, SH200S (Blender-Mockups in `build_folge02_szenen_AB.py`, Flow-Bilder `make_jobs_11_runde7.py`).
- Flow: Veo 3.1 Fast, Frames nur Startbild, 720p, 4/6/8 s; 21 Läufe (19 + 2 Wiederholungen) à 10 Punkte.
- Zwei Fehlschläge „Fehler bei der Audiogenerierung“ bei Zeilen, die NUR aus einem Laut bestanden (SH170 „Bäääääh!“, SH180 „Hä?!“) → Zeilen um echte Wörter ergänzt: „Bäh! Wir haben ganz viele!“, „Hä? Was war das denn?“.
- Prompts: `flow_video_prompts_r7.json` / `SHxxx_prompt.txt`; Spracherkennung: `00_Spracherkennung_r7.md`.
