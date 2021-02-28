import time

import chess
import requests
from icecream import ic
from traceback_with_variables import activate_by_import


def get_json(fen):
    payload = [
        ("fen", fen),
        ("variant", "standard"),
        ("speeds[]", "blitz"), ("speeds[]", "rapid"), ("speeds[]", "classical"),
        ("ratings[]", 2000), ("ratings[]", 2200), ("ratings[]", 2500),
        ("moves", 20),
        ("topGames", 0), ("recentGames", 0)
    ]
    try:
        return requests.get("https://explorer.lichess.ovh/lichess", params=payload).json()
    except:
        print("rate limiting: sleep")
        time.sleep(2)
        return requests.get("https://explorer.lichess.ovh/lichess", params=payload).json()

def make_tree():
    parent = board.fen()
    for move in get_json(parent)["moves"]:
        halfdraws = move["draws"] / 2
        white = move["white"] + halfdraws
        black = move["black"] + halfdraws
        ngames = white + black
        board.push_san(move["san"])
        fen = board.fen()
        tree[fen] = {"parent": parent, "children": [], "ngames": ngames, "white": white, "black": black}
        tree[parent]["children"].append(fen)
        board.pop() if ngames < floor else make_tree()
    try: board.pop()
    except IndexError: return

tree: dict = {}
board = chess.Board()

floor = 10**7
parent = board.fen()
tree[parent] = {"children": []}

make_tree()
