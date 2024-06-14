#!/usr/bin/env python3

import argparse
import csv
import requests
import time


def get_team_id(org, team_name, token):
    url = f"https://api.github.com/orgs/{org}/teams"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    response = requests.get(url, headers=headers)
    teams = response.json()
    for team in teams:
        if team["name"] == team_name:
            return team["id"]
    return None


def main(csv_list, org, token, team_names=None):
    # read the CSV file as dict
    with open(csv_list, newline="", encoding="utf8") as f:
        reader = csv.DictReader(f)
        members = list(reader)

    team_ids = (
        [get_team_id(org, team_name, token) for team_name in team_names]
        if team_names
        else []
    )

    # If None is included in team_ids, output an error and exit
    if None in team_ids:
        team_name_failed = team_names[team_ids.index(None)]
        print(f"Failed to get team ID of {team_name_failed}. Check the team name.")
        return

    for member in members:
        url = f"https://api.github.com/orgs/{org}/invitations"
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        data = {
            "email": member["email"],
            "role": "direct_member",
            "team_ids": team_ids if team_ids else [],
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            print(f"Invited {member['name']} ({member['email']}) to {org}")
        else:
            print(
                f"Failed to Invite {member['name']} ({member['email']}) to {org} \n"
                f"Status code: {response.status_code}\n"
                f"Message: {response.json()['message']}\n"
                f"Errors: {response.json()['errors']}"
            )
        time.sleep(0.5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Invite members to GitHub organization"
    )
    parser.add_argument("csv_list", help="CSV file containing members' email addresses")
    parser.add_argument("org", help="GitHub organization name")
    parser.add_argument("token", help="GitHub personal access token")
    parser.add_argument(
        "-t",
        "--team",
        nargs="+",
        help="Team names to invite members to.",
    )
    args = parser.parse_args()
    main(args.csv_list, args.org, args.token, args.team)
