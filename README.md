# Smart-Cover-Automation

Home Assistant Blueprint zur intelligenten Steuerung von Dachfenstern und Lamellenstoren basierend auf Wetter, Temperatur, Sonnenstand, Zeitplänen und optionalen Fenstersensoren.

## Features

✅ Unterstützung für Dachfenster und Lamellenstoren

✅ Automatische Hitzeschutzfunktion

✅ Berücksichtigung der maximalen Tagestemperatur

✅ Optionale Sonnenstandserkennung (Azimut + Elevation)

✅ Separate Morgentrigger für Werktage und Wochenende

✅ Nacht-Sperrzeit

✅ Mittags-Sperrzeit

✅ Sollzustandsprüfung alle 15 Minuten

✅ Optionaler Fenstersensor

✅ Globaler "Do Not Move"-Schalter

✅ Konfigurierbare Teilöffnung und Kippstellung

---

## Unterstützte Cover-Typen

### Dachfenster

Bei aktivem Hitzeschutz wird das Fenster auf eine definierte Teilöffnung gefahren.

### Lamellenstoren

Bei aktivem Hitzeschutz werden die Lamellen auf eine definierte Kippstellung gesetzt.

---

## Entscheidungslogik

### Hitzeschutz aktiv

Der Hitzeschutz wird aktiviert wenn:

```text
Maximale Tagestemperatur >= Temperaturschwellenwert
```

und optional:

```text
Die Sonne befindet sich im definierten Azimut- und Elevationsbereich.
```

### Ergebnis

| Bedingung | Aktion |
|------------|---------|
| Hitzeschutz aktiv | Teilöffnung / Kippstellung |
| Hitzeschutz nicht aktiv | Cover öffnen |

---

## Tagesablauf

### Morgens

Zum definierten Morgentrigger:

- Werktage separat konfigurierbar
- Wochenenden separat konfigurierbar

Aktion:

- Hitzeschutz aktiv → Teilöffnung bzw. Kippstellung
- Hitzeschutz inaktiv → Öffnen

---

### Tagsüber

Alle 15 Minuten wird der Sollzustand geprüft.

Die Prüfung erfolgt nur ausserhalb der definierten Sperrzeiten.

---

### Mittagszeit

Optional kann das Cover zu Beginn der Mittags-Sperrzeit geschlossen werden.

Nach Ende der Sperrzeit wird der Sollzustand neu berechnet.

---

### Abend

Optional kann das Cover bei der definierten Bettgehzeit geschlossen werden.

Die Nacht-Sperrzeit endet automatisch beim nächsten Morgentrigger.

---

## Sonnenstand

Der Hitzeschutz kann optional auf Situationen beschränkt werden, in denen die Sonne tatsächlich auf die betreffende Fassade scheint.

Konfigurierbar:

- Azimut Minimum
- Azimut Maximum
- Mindesthöhe der Sonne

Beispiel:

```yaml
Azimut Minimum: 135°
Azimut Maximum: 225°
Mindesthöhe: 10°
```

---

## Fenstersensor (optional)

Wird ein Fenstersensor konfiguriert, reagiert der Blueprint auf Zustandsänderungen.

### Fenster geöffnet

Falls das Cover geschlossen ist:

- Dachfenster → Teilöffnung
- Lamellenstoren → Kippstellung

### Fenster geschlossen

Der Sollzustand wird neu ermittelt und die konfigurierten Sperrzeiten werden berücksichtigt.

---

## Do Not Move

Der Schalter

```yaml
input_boolean.cover_do_not_move
```

hat höchste Priorität.

Wenn dieser auf `on` steht:

```text
Keine automatische Bewegung des Covers.
```

---

## Benötigte Helfer

### Temperaturschwellenwert

```yaml
input_number.cover_temperatur_schwellenwert
```

---

### Teilöffnung Dachfenster

```yaml
input_number.external_cover_teiloffnung
```

---

### Kippstellung Lamellenstoren

```yaml
input_number.storren_kippstellung
```

---

### Do Not Move

```yaml
input_boolean.cover_do_not_move
```

---

### Zeit-Helfer

```yaml
input_datetime.cover_offnen_wochentags
input_datetime.cover_offnen_wochenende

input_datetime.cover_bett_geh_zeit_mittag_start
input_datetime.cover_bett_geh_zeit_mittag_ende

input_datetime.cover_bett_geh_zeit_abend
```

---

## Wetterdaten

Der Blueprint verwendet die Forecast-Daten der gewählten Wetter-Entity.

Aktuell wird die maximale Temperatur des ersten Forecast-Eintrags ausgewertet.

Beispiel:

```jinja
state_attr(weather_entity, 'forecast')[0].temperature
```

---

## Beispielkonfiguration

```yaml
cover_entity: cover.schlafzimmer
cover_type: dachfenster

weather_entity: weather.weather_at_9444

temperature_threshold_entity: input_number.cover_temperatur_schwellenwert

partial_open_entity: input_number.external_cover_teiloffnung

do_not_move_boolean: input_boolean.cover_do_not_move

weekday_morning_time: input_datetime.cover_offnen_wochentags
weekend_morning_time: input_datetime.cover_offnen_wochenende

midday_start_time: input_datetime.cover_bett_geh_zeit_mittag_start
midday_end_time: input_datetime.cover_bett_geh_zeit_mittag_ende

evening_close_time: input_datetime.cover_bett_geh_zeit_abend

close_before_midday: true
close_before_evening: true

enable_sun_condition: true

sun_azimuth_min: 135
sun_azimuth_max: 225
sun_min_elevation: 10
```

---

## Installation

### Import über GitHub

In Home Assistant:

```text
Einstellungen
→ Automatisierungen & Szenen
→ Blueprints
→ Blueprint importieren
```

Danach die Raw-GitHub-URL des Blueprint-Files einfügen.

Beispiel:

```text
https://raw.githubusercontent.com/<github-user>/<repository>/main/Smart-Cover-Automation.yaml
```

---

## Einschränkungen

- Die Wetterintegration muss Forecast-Daten bereitstellen.
- Nicht jedes Cover unterstützt Positionen oder Tilt-Werte.
- Für Lamellenstoren muss `cover.set_cover_tilt_position` unterstützt werden.
- Für Dachfenster muss `cover.set_cover_position` unterstützt werden.

---

## Getestet mit

- Home Assistant 2026.7.x
- Wetter-Entitäten mit Forecast-Unterstützung
- Dachfenstern mit Positionssteuerung
- Lamellenstoren mit Tilt-Unterstützung

---

## Autor

Matthias Rohner

---
