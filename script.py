import requests
import json

API_URL = "https://raw.githubusercontent.com/IPTVFlixBD/Fancode-BD/refs/heads/main/data.json"

OUT_JSON = "matches_all.json"
OUT_M3U = "live_matches.m3u"

def main():
    data = requests.get(API_URL, timeout=15).json()

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

    # save all matches json
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_matches, f, ensure_ascii=False, indent=2)

    # create live playlist
    with open(OUT_M3U, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for m in live_matches:
            f.write(
                f'#EXTINF:-1 tvg-id="{m["match_id"]}" '
                f'tvg-logo="{m["logo"]}" '
                f'group-title="{m["event_category"]}",{m["match_name"]}\n'
            )
            f.write(f'{m["stream_url"]}\n')

    print("✅ matches_all.json created")
    print("✅ live_matches.m3u created")

if __name__ == "__main__":
    main()
