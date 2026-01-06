import requests
import time
from datetime import datetime

# === DEINE EINSTELLUNGEN ===
API_URL = "http://127.0.0.1/api"
API_TOKEN = "12345678910abcdefg"  # Hier deinen Token eintragen

MIN_PLAYERS = 20
STATS_DURATION = 60
UPDATE_INTERVAL = 60

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def get_player_count():
    try:
        response = requests.get(f"{API_URL}/get_gamestate", headers=HEADERS)
        response.raise_for_status()
        data = response.json().get("result", {})
        return data.get("num_axis_players", 0) + data.get("num_allied_players", 0)
    except Exception as e:
        print(f"Fehler beim Laden: {e}")
        return 0

def get_stats():
    try:
        response = requests.get(f"{API_URL}/get_live_game_stats", headers=HEADERS)
        response.raise_for_status()
        return response.json().get("result", {}).get("stats", [])
    except:
        return []

def format_top_players(stats, category, limit=3):
    sorted_players = sorted(stats, key=lambda x: x.get(category, 0), reverse=True)
    result = []

    for player in sorted_players[:limit]:
        score = player.get(category, 0)
        if score > 0:
            result.append(f"{player.get('player', 'Unbekannt')} ({score})")

    return ", ".join(result) if result else "Keine"

def run_update():
    get_url = f"{API_URL}/get_auto_broadcasts_config"
    set_url = f"{API_URL}/set_auto_broadcasts_config"

    try:
        player_count = get_player_count()

        resp = requests.get(get_url, headers=HEADERS)
        resp.raise_for_status()
        config = resp.json().get("result", {})

        if not config or "messages" not in config:
            print("Config konnte nicht geladen werden")
            return

        current_messages = config["messages"]

        if player_count < MIN_PLAYERS:
            new_messages = [msg for msg in current_messages
                          if not ("Top Offense:" in msg.get("message", "")
                          and "Top Defense:" in msg.get("message", ""))]

            if len(new_messages) < len(current_messages):
                config["messages"] = new_messages
                requests.post(set_url, headers=HEADERS, json={"config": config, "by": "StatsBot"})
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Stats entfernt - zu wenig Spieler")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {player_count} Spieler - Stats inaktiv")
            return

        stats = get_stats()

        stats_text = (
            f"Top Offense: {format_top_players(stats, 'offense', 3)} - "
            f"Top Defense: {format_top_players(stats, 'defense', 3)} - "
            f"Top Support: {format_top_players(stats, 'support', 3)}"
        )

        new_messages = []
        found = False
        changed = False

        for msg in current_messages:
            if "Top Offense:" in msg.get("message", "") and "Top Defense:" in msg.get("message", ""):
                if msg["message"] != stats_text:
                    changed = True
                new_messages.append({
                    "time_sec": STATS_DURATION,
                    "message": stats_text
                })
                found = True
            else:
                new_messages.append(msg)

        if not found:
            new_messages.append({
                "time_sec": STATS_DURATION,
                "message": stats_text
            })
            changed = True

        if changed:
            config["messages"] = new_messages
            requests.post(set_url, headers=HEADERS, json={"config": config, "by": "StatsBot"})
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Stats aktualisiert - {player_count} Spieler")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Keine Änderung - {player_count} Spieler")

    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    print("HLL STATS BOT")
    print(f"Update alle {UPDATE_INTERVAL}s | Min. Spieler: {MIN_PLAYERS}")
    print("-" * 50)

    while True:
        run_update()
        time.sleep(UPDATE_INTERVAL)