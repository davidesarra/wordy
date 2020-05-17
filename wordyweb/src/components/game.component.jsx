import React, { Component } from "react";
import Axios from 'axios';
import ShareGame from './shareGame.component'
import PlayersSideBar from './playersSideBar.component'
import LetterTiles from './letterTiles.component'

export default class Game extends Component {
    state = {
        players: []
    };
    componentDidMount() {
        Axios.get(`http://localhost:5000/api/v1/games/${this.props.location.state.gameId}/players`)
            .then(res => {
                this.setState({ players: res.data });
            });
    }
    render() {
        return (
            <React.Fragment>
                <ShareGame gameId={this.props.location.state.gameId}></ShareGame>
                <LetterTiles></LetterTiles>
                <PlayersSideBar players={this.state.players}> </PlayersSideBar>
            </React.Fragment>
        );
    }
}