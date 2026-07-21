# Smart-Cover-Automation

Eine universelle Home-Assistant-Automation zur intelligenten Steuerung von **Dachfenstern** und **Lamellenstoren** basierend auf:

- Wetterprognose
- Sonnenstand (Azimut / Elevation)
- Tageszeit
- Fenstersensoren
- Benutzerdefinierten Sperrzeiten
- Simulations- und Loggingmodus

Der Blueprint optimiert automatisch den Sonnenschutz und die Lüftung, ohne unnötige Fahrbewegungen auszuführen.

---

# Features

✅ Unterstützung für Dachfenster und Lamellenstoren

✅ Temperaturabhängiger Hitzeschutz

✅ Sonnenstandsabhängiger Sonnenschutz

✅ Werktag-/Wochenend-Morgentrigger

✅ Mittagssperrzeit

✅ Nachtsperrzeit

✅ Schliessen bei Sonnenuntergang oder Bettgehzeit

✅ Optionaler Fenstersensor

✅ Do-Not-Move-Schalter

✅ Simulationsmodus

✅ Ausführliches Logging

✅ Verhindert unnötige Fahrbewegungen

---

# Funktionsweise

Die Automation entscheidet zwischen vier Zuständen:

| Zustand | Bedeutung |
|----------|------------|
| `close` | Cover schliessen |
| `open` | Cover vollständig öffnen |
| `heat_protection` | Hitzeschutzstellung |
| `none` | Keine Aktion |

---

# Entscheidungslogik

```text
                       Trigger
                          │
                          ▼

                   Do Not Move?
                          │
             JA ──────────┴─────────► STOP

                          │ NEIN
                          ▼

                 Sperrzeit aktiv?
                          │
              JA ─────────┴────────► Keine Aktion

                          │ NEIN
                          ▼

                   Heisser Tag?
                          │
             NEIN ────────┴────────► Öffnen

                          │ JA
                          ▼

                 Sonne auf Fassade?
                          │
             NEIN ────────┴────────► Öffnen

                          │ JA
                          ▼

                    Hitzeschutz
```

---

# Wetterauswertung

Die Tages-Maximaltemperatur wird aus der Wettervorhersage ermittelt.

```text
MaxTemp Heute >= Temperatur-Schwelle
```

Beispiel:

```text
MaxTemp Heute = 27°C
Schwellenwert = 23°C

27 >= 23

→ Heisser Tag
```

---

# Sonnenstandsprüfung

Zusätzlich kann geprüft werden, ob die Sonne überhaupt auf die entsprechende Fassade scheint.

## Azimut

```text
0°   = Norden
90°  = Osten
180° = Süden
270° = Westen
```

Beispiel:

```text
Azimut Minimum = 135°
Azimut Maximum = 225°
```

Aktiver Bereich:

```text
                  N
                 0°

 W 270° ◄────────┼────────► 90° O

                 ▼
               180°
                S
```

```text
135° ─────────────────── 225°
       Sonne auf Fassade
```

Zusätzlich muss die Sonne höher als die minimale Elevation stehen.

---

# Verhalten bei Hitzeschutz

## Dachfenster

Das Dachfenster fährt auf eine definierte Teilöffnung.

Beispiel:

```text
Teilöffnung = 20 %
```

```text
┌─────────────┐
│             │
│             │
└─────╱───────┘
      20 %
```

---

## Lamellenstoren

Die Storen bleiben unten und werden auf die konfigurierte Kippstellung gesetzt.

Beispiel:

```text
Kippstellung = 50 %
```

```text
/////
\\\\\
/////
```

---

# Tagesablauf

## Morgens

Zur definierten Öffnungszeit:

- Werktags
- Wochenende

wird die Tagesprognose bewertet.

```text
07:15 Werktags
07:30 Wochenende
```

Anschliessend wird entschieden:

```text
Öffnen
oder
Hitzeschutz
```

---

## Regelmässige Prüfung

Alle 15 Minuten erfolgt eine Neubewertung.

```text
00
15
30
45
```

Beispiel:

```text
08:00
08:15
08:30
08:45
```

Dadurch kann die Automation auf veränderte Wetterbedingungen reagieren.

---

# Mittagssperrzeit

Während der Mittagssperrzeit werden keine automatischen Anpassungen vorgenommen.

Beispiel:

```text
11:50 ────────────────── 14:15
       Mittagsblock
```

Optional kann das Cover zu Beginn geschlossen werden.

```text
11:50
  ▼
Schliessen
```

Nach Ende der Sperrzeit wird die normale Logik wieder aktiviert.

---

# Nachtsperrzeit

Zwischen Abend und Morgen werden automatische Bewegungen unterdrückt.

```text
18:40 ────────────────── 07:15
        Nachtblock
```

Dies verhindert unerwartete Bewegungen während der Nacht.

---

# Abendverhalten

Es stehen drei Modi zur Verfügung:

| Modus | Verhalten |
|---------|------------|
| Aus | Keine Aktion |
| Bettgehzeit | Schliessen zur definierten Uhrzeit |
| Sonnenuntergang | Schliessen bei Sunset |

---

## Bettgehzeit

```text
18:40
  ▼
Schliessen
```

---

## Sonnenuntergang

```text
Sunset
  ▼
Schliessen
```

---

# Fenstersensor

Optional kann ein Fenstersensor eingebunden werden.

## Fenster geöffnet

Wenn das Cover geschlossen ist:

```text
Fenster auf
      │
      ▼
Cover geschlossen
      │
      ▼
Hitzeschutzstellung
```

### Dachfenster

```text
geschlossen
     ▼
20 % öffnen
```

### Lamellenstoren

```text
geschlossen
     ▼
50 % Kippstellung
```

---

## Fenster geschlossen

Beim Schliessen des Fensters wird die gesamte Logik neu berechnet.

```text
Temperatur
+
Sonne
+
Sperrzeiten
+
Abendmodus
```

---

# Do Not Move

Globale Sperre für sämtliche Bewegungen.

```text
Do Not Move = EIN
```

Dann gilt:

```text
Automation startet
       │
       ▼
Do Not Move?
       │
      JA
       ▼
      STOP
```

Die Automation läuft weiter, bewegt jedoch keinerlei Aktoren.

---

# Simulationsmodus

Im Simulationsmodus werden keine Covers bewegt.

Die komplette Entscheidungslogik wird trotzdem ausgeführt.

```text
Entscheidung berechnen
          │
          ▼
Logging schreiben
          │
          ▼
Keine Bewegung
```

Ideal zum Testen neuer Konfigurationen.

---

# Logging

Optional können detaillierte Logbucheinträge erstellt werden.

Beispiel:

```text
Trigger=periodic_check
TargetAction=heat_protection
HotToday=true
SunMatches=true
BlockedTime=false
```

Dadurch kann jederzeit nachvollzogen werden:

- warum eine Bewegung ausgelöst wurde
- warum keine Bewegung erfolgte
- welche Parameter zur Entscheidung geführt haben

---

# Unterstützte Covertypen

| Covertyp | Verhalten |
|------------|------------|
| Dachfenster | Teilöffnung |
| Lamellenstoren | Kippstellung |

---

# Empfohlene Helper

| Typ | Beispiel |
|------|-----------|
| input_number | Temperatur Schwellenwert |
| input_number | Teilöffnung Dachfenster |
| input_number | Kippstellung Storen |
| input_datetime | Öffnungszeiten |
| input_datetime | Mittagssperrzeit |
| input_datetime | Bettgehzeit |
| input_boolean | Do Not Move |

---

# Beispielkonfiguration

```text
Temperatur Schwellenwert: 23°C

Teilöffnung Dachfenster: 20 %

Kippstellung Storen: 50 %

Öffnen Werktags: 07:15

Öffnen Wochenende: 07:30

Mittag Start: 11:50

Mittag Ende: 14:15

Bettgehzeit Abend: 18:40
```

---

# Zusammenfassung

Die Smart-Cover-Automation kombiniert Wetterprognose, Sonnenstand, Tageszeit und Gebäudestatus, um Dachfenster und Storen automatisch zu steuern.

Ziel ist:

- maximaler Komfort
- automatischer Hitzeschutz
- minimale manuelle Eingriffe
- keine unnötigen Fahrbewegungen
- nachvollziehbares Verhalten durch Logging