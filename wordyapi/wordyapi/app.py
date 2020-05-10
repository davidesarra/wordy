#!flask/bin/python
from flask import Flask, abort, jsonify, request

from wordyapi import games


app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/api/v1/games", methods=["POST"])
def create_game():
    game_id = games.create_game()
    return get_game(game_id=game_id)


@app.route("/api/v1/games/<string:game_id>", methods=["GET"])
def get_game(game_id):
    try:
        games.get_game(game_id=game_id)
        return jsonify({"game": {"id": game_id}})
    except KeyError:
        return abort(404)


@app.route("/api/v1/games/<string:game_id>/players", methods=["GET"])
def get_players(game_id):
    try:
        game = games.get_game(game_id=game_id)
        player_names = game.players
        players = {"players": [{"name": player_name} for player_name in player_names]}
        return jsonify(players)
    except KeyError:
        return abort(404)


@app.route("/api/v1/games/<string:game_id>/players", methods=["POST"])
def create_player(game_id):
    if not request.json or "name" not in request.json:
        abort(400)
    player_name = request.json["name"]
    try:
        player_id = games.create_player(game_id=game_id, player_name=player_name)
    except KeyError:
        return abort(404)
    except ValueError as error:
        bad_response = jsonify({"description": str(error)})
        bad_response.status_code = 400
        return bad_response
    return get_player(game_id=game_id, player_id=player_id)


@app.route("/api/v1/games/<string:game_id>/players/<string:player_id>", methods=["GET"])
def get_player(game_id, player_id):
    try:
        player_name = games.get_player(game_id=game_id, player_id=player_id)
        return jsonify({"player": {"id": player_id, "name": player_name}})
    except KeyError:
        return abort(404)


if __name__ == "__main__":
    app.run()
