from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# Get Ballchasing API token from environment variable
API_TOKEN = os.environ.get("BALLCHASING_API_TOKEN")
PLAYER_ID = "steam:76561198330826708"  # Replace with your ID

headers = {"Authorization": API_TOKEN}

playlists = {
    "1v1": "ranked-duels",
    "2v2": "ranked-doubles",
    "3v3": "ranked-standard"
}

@app.route("/ranks", methods=["GET"])
def get_ranks():
    rank_data = {}

    for mode, playlist in playlists.items():
        url = f"https://ballchasing.com/api/replays?player={PLAYER_ID}&count=10&playlist={playlist}"
        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            rank_data[mode] = f"Error {res.status_code}"
            continue

        replays = res.json().get("list", [])
        if not replays:
            rank_data[mode] = "No replays found"
            continue

        most_recent = sorted(replays, key=lambda r: r["created"], reverse=True)[0]
        replay_id = most_recent["id"]
        replay_url = f"https://ballchasing.com/api/replays/{replay_id}"
        replay = requests.get(replay_url, headers=headers).json()

        # Find player in replay
        player_data = None
        for team in ["blue", "orange"]:
            for p in replay[team]["players"]:
                if p["id"]["id"] == PLAYER_ID.split(":")[1]:
                    player_data = p
                    break
            if player_data:
                break

        rank_name = player_data.get("rank", {}).get("name", "Rank not available") if player_data else "Player not found"
        rank_data[mode] = rank_name

    return jsonify(rank_data)

@app.route("/", methods=["GET"])
def home():
    return "RankBot API is running! Visit /ranks"
