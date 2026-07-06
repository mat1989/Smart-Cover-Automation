# 🪟 Cover Klima-/Zeitsteuerung mit Sonnenlogik
### Home Assistant Blueprint (Dachfenster & Lamellenstoren)

Automatisiere deine Covers intelligent basierend auf:
- 🌡️ Wetter (Temperatur-Prognose)
- ☀️ Sonnenstand (Azimut & Elevation)
- 🕒 Tageszeiten (Morgen / Mittag / Abend)
- 🪟 optionalem Fenstersensor
- ⛔ globalem "Do not move"-Schalter

---

## ✨ Features

✅ Unterschiedliche Öffnungszeiten (Wochentag / Wochenende)  
✅ Temperatur-basierter Hitzeschutz  
✅ Sonnenorientierte Steuerung (nur wenn Sonne relevant ist)  
✅ Teilöffnung für Dachfenster  
✅ Kippstellung für Lamellenstoren  
✅ Mittagsruhe mit automatischer Wiederöffnung  
✅ Automatisches Schließen am Abend  
✅ Unterstützung für Fenstersensoren  
✅ Globaler Override-Schalter  

---

## 🧠 Funktionsweise

### 🌅 Morgens

- Prüft die Tageshöchsttemperatur
- Prüft optional:
  - Ob die Sonne auf die Fassade scheint

| Bedingung | Verhalten |
|-----------|----------|
| Nicht heiß | vollständig öffnen |
| Heiß + Sonne trifft Fassade | Teilöffnung / Kippstellung |
| Heiß + keine Sonne | vollständig öffnen |

---

### 🌞 Mittagsruhe

- Zur definierten Zeit:
  - Cover schließen
- Für definierte Dauer geschlossen halten
- Danach:
  - gleiche Logik wie morgens anwenden

---

### 🌙 Abends

- Zur definierten Zeit:
  - Cover schließen
- Bleibt geschlossen bis zum nächsten Morgen

---

### 🪟 Fenstersensor (optional)

| Ereignis | Verhalten |
|----------|----------|
| Fenster öffnet | Teilöffnung / Kippstellung |
| Fenster schließt | Cover schließen |

---

### ⛔ Do-Not-Move

Wenn aktiv:

```yaml
input_boolean.cover_do_not_move = on
