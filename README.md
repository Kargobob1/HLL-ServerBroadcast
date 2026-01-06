# HLL Stats Bot 🎮

Automatischer Stats-Bot für Hell Let Loose CRCON Server. Zeigt die Top 3 Spieler in Offense, Defense und Support als Auto-Broadcast Nachricht an.

## Features

- ✅ Automatische Anzeige der besten Spieler
- ✅ Startet ab einer konfigurierbaren Spieleranzahl (Standard: 20)
- ✅ Entfernt die Nachricht automatisch bei zu wenig Spielern
- ✅ Aktualisiert sich kontinuierlich (Standard: jede Minute)
- ✅ Minimale Server-Last durch intelligente Updates

## Voraussetzungen

- Python 3.7 oder höher
- Hell Let Loose CRCON API Zugang
- `requests` Library

## Installation

1. **Repository klonen**
```bash
git clone https://github.com/Kargobob1/HLL-ServerBroadcast.git
cd hll-stats-bot
```

2. **Dependencies installieren**
```bash
pip install requests
```

3. **Konfiguration anpassen**

Öffne `stats_bot.py` und trage deine Daten ein:
```python
API_URL = "http://127.0.0.1/api"        # Deine CRCON URL
API_TOKEN = "12345678910abcdefg"        # Dein API Token
```

## Konfiguration

| Variable | Standard | Beschreibung |
|----------|----------|--------------|
| `API_URL` | `http://127.0.0.1/api` | URL zu deiner CRCON API |
| `API_TOKEN` | - | Dein CRCON API Token |
| `MIN_PLAYERS` | `20` | Mindestanzahl Spieler für Stats-Anzeige |
| `STATS_DURATION` | `60` | Anzeigedauer der Nachricht (Sekunden) |
| `UPDATE_INTERVAL` | `60` | Update-Intervall (Sekunden) |

## Verwendung

### Manuell starten
```bash
python stats_bot.py
```

### Als Hintergrundprozess (Linux)

**Mit screen:**
```bash
screen -S statsbot
python stats_bot.py
# Ctrl+A dann D zum Detachen
```

**Mit tmux:**
```bash
tmux new -s statsbot
python stats_bot.py
# Ctrl+B dann D zum Detachen
```

**Mit systemd Service:**

Erstelle `/etc/systemd/system/hll-statsbot.service`:
```ini
[Unit]
Description=HLL Stats Bot
After=network.target

[Service]
Type=simple
User=deinuser
WorkingDirectory=/pfad/zum/hll-stats-bot
ExecStart=/usr/bin/python3 stats_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Dann:
```bash
sudo systemctl enable hll-statsbot
sudo systemctl start hll-statsbot
sudo systemctl status hll-statsbot
```

### Als Hintergrundprozess (Windows)

**Mit Batch-Datei:**

Erstelle `start_bot.bat`:
```batch
@echo off
python stats_bot.py
pause
```

**Als Windows Service mit NSSM:**
```bash
nssm install HLLStatsBot "C:\Python39\python.exe" "C:\pfad\zum\stats_bot.py"
nssm start HLLStatsBot
```

## Ausgabe

Das Script zeigt dir Status-Updates in der Konsole:
```
HLL STATS BOT
Update alle 60s | Min. Spieler: 20
--------------------------------------------------
[14:30:15] Stats aktualisiert - 45 Spieler
[14:31:15] Keine Änderung - 45 Spieler
[14:32:15] Stats entfernt - zu wenig Spieler
```

## Beispiel-Nachricht im Server
```
Top Offense: PlayerOne (156), PlayerTwo (142), PlayerThree (138) - Top Defense: DefenderA (89), DefenderB (76), DefenderC (71) - Top Support: SupportX (112), SupportY (98), SupportZ (87)
```

## Troubleshooting

### Bot startet nicht
- Prüfe ob Python installiert ist: `python --version`
- Prüfe ob requests installiert ist: `pip show requests`

### Keine Stats werden angezeigt
- Prüfe ob `MIN_PLAYERS` erreicht ist
- Prüfe API URL und Token in der Config
- Schaue in die Console für Fehlermeldungen

### API Fehler
```
Fehler beim Laden: 401 Unauthorized
```
→ API Token ist falsch oder abgelaufen
```
Fehler beim Laden: Connection refused
```
→ API URL ist falsch oder CRCON nicht erreichbar

## Lizenz

MIT License - siehe [LICENSE](LICENSE)

## Credits

Entwickelt für die Hell Let Loose Community 🎖️

## Support

Bei Fragen oder Problemen öffne ein [Issue](https://github.com/deinusername/hll-stats-bot/issues)
