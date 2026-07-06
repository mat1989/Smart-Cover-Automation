🪟 Cover Klima-/Zeitsteuerung mit Sonnenlogik
Home Assistant Blueprint (Dachfenster & Lamellenstoren)
Automatisiert die Steuerung von Covers (Dachfenster, Rollläden, Lamellenstoren) basierend auf:

🌡️ Wettervorhersage (Temperatur)
☀️ Sonnenstand (Azimut + Elevation)
🕒 Tageszeiten (morgen / mittag / abend)
🪟 optionalem Fenstersensor
⛔ globalem „Do not move“-Schalter


✨ Features
✅ Intelligente Morgensteuerung (werktags & Wochenende getrennt)
✅ Hitzeschutz basierend auf Wetter + Sonnenposition
✅ Teilöffnung (Dachfenster) oder Kippstellung (Lamellen)
✅ Automatische Mittagsruhe inkl. Rückkehrlogik
✅ Automatisches Schließen am Abend
✅ Optionaler Fenstersensor (z. B. Fenster offen → Position anpassen)
✅ Globaler Override (input_boolean.cover_do_not_move)

🧠 Funktionsweise
🌅 Morgens

Prüft die Tageshöchsttemperatur
Prüft optional:

Ist die Sonne relevant für das Fenster? (Azimut + Höhe)


Verhalten:






















ZustandErgebnisNicht heißCover vollständig öffnenHeiß + Sonne auf FassadeTeilöffnung / KippstellungHeiß + keine Sonnevollständig öffnen

🌞 Mittagsruhe

Zur definierten Zeit → Cover schließen
Für definierte Dauer geschlossen halten
Danach:

gleiche Logik wie morgens anwenden




🌙 Abends

Zur definierten Zeit → Cover schließen
Bleibt geschlossen bis zum nächsten Morgen


🪟 Fenstersensor (optional)

















EreignisVerhaltenFenster öffnetCover auf Teilöffnung / KippstellungFenster schließtCover wieder schließen

⛔ Do-Not-Move
Wenn gesetzt:
YAMLinput_boolean.cover_do_not_move = onWeitere Zeilen anzeigen
👉 Alle automatischen Bewegungen werden unterdrückt

☀️ Sonnenlogik (Azimut + Elevation)
Der Blueprint nutzt die sun.sun Entity:

azimuth → Richtung (0–360°)
elevation → Höhe über Horizont

Beispiel Werte





















AusrichtungAzimut BereichOst45 – 135Süd135 – 225West225 – 315
Zusätzlich:
Plain TextMindesthöhe der Sonne (z. B. 10°)Weitere Zeilen anzeigen
👉 verhindert Reaktion bei tiefstehender oder keine Sonne

⚙️ Voraussetzungen

Home Assistant ≥ 2024.6
aktivierte Integration:

sun
weather


vorhandene Helper:

input_number (Positionen / Schwellwerte)
input_datetime (Zeiten)
input_boolean (Control)




📦 Installation

Datei speichern unter:

/config/blueprints/automation/<dein_name>/cover_klima_zeitsteuerung.yaml


In Home Assistant:

Einstellungen → Automationen & Szenen → Blueprints
