#---------------------------------------------------------------------
# Slack Get Active Users and Compare to First Check who was Fired!
#
# Version      Date        Info
# 1.0          2025        Initial Version
#
# Made by Denis Astahov ADV-IT Copyleft (c) 2025
#---------------------------------------------------------------------
import requests
import json
import os
from datetime import datetime

# Test it in CLI:
# curl -X GET "https://slack.com/api/users.list" -H "Authorization: Bearer <TOKEN>"

# Slack API Config
SLACK_API_URL = "https://slack.com/api/users.list"
TOKEN         = "xoxp-2704744787926-your-user-token-7086d8c9477484166"

HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# Directory to store JSON files
DATA_DIR = "./slack_data"
os.makedirs(DATA_DIR, exist_ok=True)  # Ensure the directory exists


# Fetch active Slack users
def get_active_users():
    response = requests.get(SLACK_API_URL, headers=HEADERS, params={"include_deleted": "true"})
    data = response.json()

    if not data.get("ok"):
        print("Error fetching Slack users:", data.get("error"))
        return []

    # Filter only active users and extract full names
    active_users = [
        {
            "id": user["id"],
            "name": user["profile"].get("real_name", user["name"])  # Full name fallback to username
        }
        for user in data.get("members", [])
        if not user.get("deleted")             # Exclude deactivated users
        and not user.get("is_bot", False)      # Exclude bots
        and user.get("id") != "USLACKBOT"      # Exclude Slackbot
    ]

    return active_users


# Save users to a JSON file
def save_users_to_file(users, filename):
    with open(filename, "w") as f:
        json.dump(users, f, indent=4)


# Compare two files and print missing users
def compare_users(file1, file2):
    with open(file1, "r") as f1, open(file2, "r") as f2:
        users_start = json.load(f1)
        users_latest = json.load(f2)

    start_ids = {user["id"] for user in users_start}
    latest_ids = {user["id"] for user in users_latest}

    missing_users = [user for user in users_start if user["id"] not in latest_ids]

    if missing_users:
        print("Users missing in the new file compared to the START file:")
        for user in missing_users:
            print(f"- {user['name']} (ID: {user['id']})")
    else:
        print("No users are missing.")


def main():
    active_users = get_active_users()
    if not active_users:
        return

    num_users = len(active_users)
    today = datetime.now().strftime("%d-%m-%Y")

    # Look for an existing START file (created on first run)
    start_filename = None
    for file in os.listdir(DATA_DIR):
        if file.endswith("-START.json"):
            start_filename = os.path.join(DATA_DIR, file)
            break

    # If no START file exists, create one
    if start_filename is None:
        start_filename = os.path.join(DATA_DIR, f"slack_{num_users}_active_{today}-START.json")
        save_users_to_file(active_users, start_filename)
        print(f"Saved initial active users to {start_filename}")

    # Save today's file (without START suffix)
    latest_filename = os.path.join(DATA_DIR, f"slack_{num_users}_active_{today}.json")
    save_users_to_file(active_users, latest_filename)
    print(f"Saved latest active users to {latest_filename}")


    # Compare with START file
    compare_users(start_filename, latest_filename)

if __name__ == "__main__":
    main()