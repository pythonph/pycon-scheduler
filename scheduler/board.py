import json
import os

import requests

TRELLO_BOARD_ID = os.environ["TRELLO_BOARD_ID"]
TRELLO_KEY = os.environ["TRELLO_KEY"]
TRELLO_TOKEN = os.environ["TRELLO_TOKEN"]
TRELLO_ENDPOINT = "https://api.trello.com/1/"


def get_board():
    url = "{}/boards/{}".format(TRELLO_ENDPOINT, TRELLO_BOARD_ID)
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


def get_lists(board):
    return {
        l["name"]: l["id"] for l in board["lists"]
    }


def get_board_fields(board):
    plugin_data = json.loads(board["pluginData"][0]["value"])
    return {
        f["id"]: f["n"] for f in plugin_data["fields"]
    }


def get_card_fields(card, board_fields):
    if not len(card["pluginData"]):
        return {}
    plugin_data = json.loads(card["pluginData"][0]["value"])
    return {
        board_fields[field_id]: field_value
        for field_id, field_value in plugin_data["fields"].items()
        if field_id in board_fields
    }


def set_card_fields(cards, board_fields):
    for card in cards:
        card_fields = get_card_fields(card, board_fields)
        yield {
            **card,
            "fields": card_fields,
        }


def get_cards(board):
    board_fields = get_board_fields(board)
    return list(set_card_fields(board["cards"], board_fields))


def filter_by_list(list_id):
    return lambda c: c["idList"] == list_id


def filter_by_label(label):
    return lambda c: label in [
        l["name"] for l in c["labels"]
    ]

