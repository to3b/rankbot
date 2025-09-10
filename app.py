import requests

API_TOKEN = "YOUR_API_KEY"
PLAYER_ID = "steam:76561198330826708"

def get_recent_replays(player_id, playlist):
    url = f"https://ballchasing.com/api/replays?player={player_id}&count=10&playlist={playlist}"
    headers = {"Authorization": API_TOKEN}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        return None

replays = get_recent_replays(PLAYER_ID, "ranked-doubles")
print(replays)
