def test_create_game(client):
    # when
    response = client.post("/api/v1/games")

    # then
    assert response.status_code == 200
    assert response.json.keys() == {"game"}
    assert response.json["game"].keys() == {"id"}


def test_get_game(client):
    # given
    response = client.post("/api/v1/games")
    assert response.status_code == 200
    game_id = response.json["game"]["id"]

    # when
    response = client.get(f"/api/v1/games/{game_id}")

    # then
    assert response.status_code == 200
    assert response.json.keys() == {"game"}
    assert response.json["game"].keys() == {"id"}
    assert response.json["game"]["id"] == game_id


def test_create_player(client):
    # given
    response = client.post("/api/v1/games")
    assert response.status_code == 200
    game_id = response.json["game"]["id"]
    player_name = "Davide"

    # when
    response = client.post(
        f"/api/v1/games/{game_id}/players", json={"name": player_name}
    )

    # then
    assert response.status_code == 200
    assert response.json.keys() == {"player"}
    assert response.json["player"].keys() == {"id", "name"}
    assert response.json["player"]["name"] == player_name


def test_create_player_twice(client):
    # given
    response = client.post("/api/v1/games")
    assert response.status_code == 200
    game_id = response.json["game"]["id"]
    player1_name = "Davide"
    response = client.post(
        f"/api/v1/games/{game_id}/players", json={"name": player1_name}
    )
    assert response.status_code == 200
    player2_name = "Davide"

    # when
    response = client.post(
        f"/api/v1/games/{game_id}/players", json={"name": player2_name}
    )

    # then
    assert response.status_code == 400
    assert response.json.keys() == {"message"}


def test_create_player_with_invalid_game_id(client):
    # given
    player_name = "Davide"
    invalid_game_id = "invalid-game-id"

    # when
    response = client.post(
        f"/api/v1/games/{invalid_game_id}/players", json={"name": player_name}
    )

    # then
    assert response.status_code == 404


def test_get_player(client):
    # given
    response = client.post("/api/v1/games")
    assert response.status_code == 200
    game_id = response.json["game"]["id"]
    player_name = "Davide"
    response = client.post(
        f"/api/v1/games/{game_id}/players", json={"name": player_name}
    )
    assert response.status_code == 200
    player_id = response.json["player"]["id"]

    # when
    response = client.get(f"/api/v1/games/{game_id}/players/{player_id}")

    # then
    assert response.status_code == 200
    assert response.json.keys() == {"player"}
    assert response.json["player"].keys() == {"id", "name"}
    assert response.json["player"]["name"] == player_name
    assert response.json["player"]["id"] == player_id


def test_get_player_with_invalid_player_id(client):
    # given
    response = client.post("/api/v1/games")
    assert response.status_code == 200
    game_id = response.json["game"]["id"]
    player_id = "invalid-player-id"

    # when
    response = client.get(f"/api/v1/games/{game_id}/players/{player_id}")

    # then
    assert response.status_code == 404


def test_get_player_with_invalid_game_id(client):
    # given
    response = client.post("/api/v1/games")
    assert response.status_code == 200
    game_id = response.json["game"]["id"]
    player_name = "Davide"
    response = client.post(
        f"/api/v1/games/{game_id}/players", json={"name": player_name}
    )
    assert response.status_code == 200
    player_id = response.json["player"]["id"]
    invalid_game_id = "invalid-game-id"

    # when
    response = client.get(f"/api/v1/games/{invalid_game_id}/players/{player_id}")

    # then
    assert response.status_code == 404


def test_get_players(client):
    # given
    response = client.post("/api/v1/games")
    assert response.status_code == 200
    game_id = response.json["game"]["id"]
    player1_name = "Cherry"
    response = client.post(
        f"/api/v1/games/{game_id}/players", json={"name": player1_name}
    )
    assert response.status_code == 200
    player2_name = "Davide"
    response = client.post(
        f"/api/v1/games/{game_id}/players", json={"name": player2_name}
    )
    assert response.status_code == 200

    # when
    response = client.get(f"/api/v1/games/{game_id}/players")

    # then
    assert response.status_code == 200
    assert response.json.keys() == {"players"}
    players = sorted(response.json["players"], key=lambda player: player["name"])
    assert players[0].keys() == {"name"}
    assert players[0]["name"] == player1_name
    assert players[1].keys() == {"name"}
    assert players[1]["name"] == player2_name


def test_get_players_with_invalid_game_id(client):
    # given
    invalid_game_id = "invalid-game-id"

    # when
    response = client.get(f"/api/v1/games/{invalid_game_id}/players")

    # then
    assert response.status_code == 404
