import os
import json
from pprint import pprint

import requests

TRELLO_BOARD_ID = os.environ["TRELLO_BOARD_ID"]
TRELLO_KEY = os.environ["TRELLO_KEY"]
TRELLO_TOKEN = os.environ["TRELLO_TOKEN"]
TRELLO_ENDPOINT = 'https://api.trello.com/1/'


def get_board(board_id):
    url = "{}/boards/{}".format(TRELLO_ENDPOINT, board_id)
    resp = requests.get(url, params={
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN,
        "lists": "open",
        "cards": "open",
        "card_attachments": "cover",
        "pluginData": "true",
        "card_pluginData": "true",
    })
    resp.raise_for_status()
    return resp.json()


def get_fields(board):
    fields = {}
    plugin_data = json.loads(board["pluginData"][0]["value"])
    for f in plugin_data["fields"]:
        field = {"name": f["n"]}
        if f.get("friendlyType") == "Dropdown List":
            options = {}
            for o in f["o"]:
                options[o["id"]] = o["value"]
            field["options"] = options
        fields[f["id"]] = field
    return fields


def main():
    board = get_board(TRELLO_BOARD_ID)
    fields = get_fields(board)
    # Get lists
    # Get cards
    # Render


if __name__ == "__main__":
    main()

