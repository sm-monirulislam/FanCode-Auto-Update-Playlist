import requests
import json
from datetime import datetime

API_URL = "https://raw.githubusercontent.com/IPTVFlixBD/Fancode-BD/refs/heads/main/data.json"

# Output files
OUT_JSON = "FanCode_data.json"
OUT_M3U = "FanCode.m3u"

OWNER = "Monirul Islam"
TELEGRAM = "https://t.me/monirul_Islam_SM"

def main():
    response = requests.get(API_URL, timeout=15)
    data = response.json()

    matches = data.get("matches", [])

    all_matches = []
    live_matches = []

    for m in matches:
        match_data = {
            "event_category": m.get("event_category"),
            "title": m.get("title"),
            "event_name": m.get("event_name"),
            "match_name": m.get("match_name"),
            "team_1": m.get("team_1"),
            "team_2": m.get("team_2"),
            "status": m.get("status"),
            "match_id": m.get("match_id"),
            "startTime": m.get("startTime"),
            "logo": m.get("src"),
            "stream_url": m.get("hls_url")
        }

        all_matches.append(match_data)

        if m.get("status", "").upper() == "LIVE":
            live_matches.append(match_data)

    now_time = datetime.now().strftime("%I:%M:%S %p %d-%m-%Y")

    # ===== JSON OUTPUT =====
    json_output = {
        "name": "Fancode Live Matches Data in Json",
        "owner": OWNER,
        "telegram": TELEGRAM,
        "channels_amount": len(live_matches),
        "last update time": now_time,
        "matches": all_matches
    }

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(json_output, f, ensure_ascii=False, indent=2)

    # ===== M3U OUTPUT =====
    with open(OUT_M3U, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write("#=================================\n")
        f.write(f"# 🖥️ Developed by: {OWNER}\n")
        f.write(f"# 🔗 Telegram: {TELEGRAM}\n")
        f.write(f"# 🕒 Last Updated: {now_time} (BD Time)\n")
        f.write(f"# 📺 Channels Count: {len(live_matches)}\n")
        f.write("#=================================\n\n")

        for m in live_matches:
            f.write(
                f'#EXTINF:-1 tvg-id="{m["match_id"]}" '
                f'tvg-logo="{m["logo"]}" '
                f'group-title="{m["event_category"]}",{m["match_name"]}\n'
            )
            f.write(f'{m["stream_url"]}\n')

    print("✅ FanCode_data.json created")
    print("✅ FanCode.m3u created")

if __name__ == "__main__":
    main()
