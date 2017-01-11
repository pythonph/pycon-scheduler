from flask import Blueprint, Flask, render_template, request

from .board import (filter_by_label, filter_by_list, get_board, get_cards,
                    get_lists)

root = Blueprint("root", __name__)


@root.route("/")
def index():
    context = {}
    label = request.args.get("label")
    if label:
        confirmed_cards = get_confirmed_cards()
        context["cards"] = filter(filter_by_label(label), confirmed_cards)
    return render_template("index.html", **context)


def get_confirmed_cards():
    board = get_board()
    cards = get_cards(board)
    return filter(filter_by_label("Confirmed"), cards)


def create_app(**config):
    app = Flask(__name__)
    app.config.update(**config)
    app.register_blueprint(root)
    return app

