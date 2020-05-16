import React, { Component } from "react";

import axios from 'axios';

export default class JoinGame extends Component {
    constructor(props) {
        super(props)
        this.state = {
            gameId: "",
            playerName: "",
            playerId: null,
        };
        this.handlePlayerNameChange = this.handlePlayerNameChange.bind(this);
        this.handleGameIdChange = this.handleGameIdChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.joinExistingGame = this.joinExistingGame.bind(this);
        this.joinNewGame = this.joinNewGame.bind(this);
    };
    joinNewGame() {
        axios.post(`http://localhost:5000/api/v1/games`)
            .then(res => {
                this.setState({ gameId: res.data.id });
                axios.post(`http://localhost:5000/api/v1/games/${this.state.gameId}/players`, { "name": this.state.playerName })
                    .then(res => this.setState({ playerId: res.data.id }));
            });
    };
    joinExistingGame() {
        axios.post(`http://localhost:5000/api/v1/games/${this.state.gameId}/players`, { "name": this.state.playerName })
            .then(res => this.setState({ playerId: res.data.id }));
    };
    handlePlayerNameChange(event) {
        this.setState({ playerName: event.target.value });
    };
    handleGameIdChange(event) {
        this.setState({ gameId: event.target.value });
    };
    handleSubmit(event) {
        if (!this.state.gameId) {
            this.joinNewGame();
        } else {
            this.joinExistingGame();
        }
        event.preventDefault();
    };
    render() {
        return (
            <React.Fragment>
                <h1>WORDY</h1>
                To join a new a game, leave the Game ID field empty.
                <br></br>
                To join an existing game, paste the Game ID that was shared with you.
                <br></br>
                <br></br>
                <form onSubmit={this.handleSubmit}>
                    <label>
                        Name:
                    <textarea value={this.state.playerName} onChange={this.handlePlayerNameChange} />
                    </label>
                    <br></br>
                    <label>
                        Game ID:
                    <textarea value={this.state.gameId} onChange={this.handleGameIdChange} />
                    </label>
                    <br></br>
                    <input type="submit" value="Join" />
                </form>
            </React.Fragment>
        );
    };
};
