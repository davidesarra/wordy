def test_create_game(client):
    # when
    response = client.post("/api/v1/games")

    # then
    assert response.status_code == 200
    assert response.json.keys() == {"id"}


def test_get_game(client):
    # given
    response = client.post("/api/v1/games")
    game_id = response.json["id"]

    # when
    response = client.get(f"/api/v1/games/{game_id}")

    # then
    assert response.status_code == 200
    assert response.json.keys() == {"id"}


def test_create_player(client):
    # given
    response = client.post("/api/v1/games")
    game_id = response.json["id"]
    player_name = "Davide"

    # when
    response = client.post(
        f"/api/v1/games/{game_id}/players", json={"name": player_name}
    )

    # then
    assert response.status_code == 200
    assert response.json.keys() == {"id", "name"}
    assert response.json["name"] == player_name


def test_create_player_twice(client):
    # given
    response = client.post("/api/v1/games")
    game_id = response.json["id"]
    player1_name = "Davide"
    response = client.post(
        f"/api/v1/games/{game_id}/players", json={"name": player1_name}
    )
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
    game_id = response.json["id"]
    player_name = "Davide"
    response = client.post(
        f"/api/v1/games/{game_id}/players", json={"name": player_name}
    )
    player_id = response.json["id"]

    # when
    response = client.get(f"/api/v1/games/{game_id}/players/{player_id}")

    # then
    assert response.status_code == 200
    assert response.json.keys() == {"id", "name"}
    assert response.json["name"] == player_name
    assert response.json["id"] == player_id


def test_get_player_with_invalid_player_id(client):
    # given
    response = client.post("/api/v1/games")
    game_id = response.json["id"]
    player_id = "invalid-player-id"

    # when
    response = client.get(f"/api/v1/games/{game_id}/players/{player_id}")

    # then
    assert response.status_code == 404


def test_get_player_with_invalid_game_id(client):
    # given
    response = client.post("/api/v1/games")
    game_id = response.json["id"]
    player_name = "Davide"
    response = client.post(
        f"/api/v1/games/{game_id}/players", json={"name": player_name}
    )
    player_id = response.json["id"]
    invalid_game_id = "invalid-game-id"

    # when
    response = client.get(f"/api/v1/games/{invalid_game_id}/players/{player_id}")

    # then
    assert response.status_code == 404


def test_get_players(client):
    # given
    response = client.post("/api/v1/games")
    game_id = response.json["id"]
    player1_name = "Cherry"
    response = client.post(
        f"/api/v1/games/{game_id}/players", json={"name": player1_name}
    )
    player2_name = "Davide"
    response = client.post(
        f"/api/v1/games/{game_id}/players", json={"name": player2_name}
    )

    # when
    response = client.get(f"/api/v1/games/{game_id}/players")

    # then
    assert response.status_code == 200
    assert len(response.json) == 2
    players = sorted(response.json, key=lambda player: player["name"])
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


def test_create_draw(client):
    # given
    response = client.post("/api/v1/games")
    game_id = response.json["id"]
    player_name = "Davide"
    client.post(f"/api/v1/games/{game_id}/players", json={"name": player_name})

    # when
    response = client.post(f"/api/v1/games/{game_id}/draw")

    # then
    assert response.status_code == 200
    for letter_data in response.json.values():
        assert letter_data.keys() == {"count", "points"}


def test_create_draw_with_invalid_game_id(client):
    # given
    response = client.post("/api/v1/games")
    game_id = response.json["id"]
    player_name = "Davide"
    client.post(f"/api/v1/games/{game_id}/players", json={"name": player_name})
    invalid_game_id = "invalid-game-id"

    # when
    response = client.post(f"/api/v1/games/{invalid_game_id}/draw")

    # then
    assert response.status_code == 404


def test_get_draw(client):
    # given
    response = client.post("/api/v1/games")
    game_id = response.json["id"]
    player_name = "Davide"
    client.post(f"/api/v1/games/{game_id}/players", json={"name": player_name})
    client.post(f"/api/v1/games/{game_id}/draw")

    # when
    response = client.get(f"/api/v1/games/{game_id}/draw")

    # then
    assert response.status_code == 200
    for letter_data in response.json.values():
        assert letter_data.keys() == {"count", "points"}


def test_get_draw_with_invalid_game_id(client):
    # given
    response = client.post("/api/v1/games")
    game_id = response.json["id"]
    player_name = "Davide"
    client.post(f"/api/v1/games/{game_id}/players", json={"name": player_name})
    client.post(f"/api/v1/games/{game_id}/draw")
    invalid_game_id = "invalid-game-id"

    # when
    response = client.get(f"/api/v1/games/{invalid_game_id}/draw")

    # then
    assert response.status_code == 404
