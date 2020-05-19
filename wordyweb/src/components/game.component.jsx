import React, { Component } from "react";
import Axios from 'axios';
import ShareGame from './shareGame.component'
import PlayersSideBar from './playersSideBar.component'
import LetterTiles from './letterTiles.component'

export default class Game extends Component {
    state = {
        players: [],
        gameId: this.props.location.state.gameId
    };

    componentDidMount() {
        Axios.get(`http://localhost:5000/api/v1/games/${this.state.gameId}/players`) //move to playersSideBar.component
            .then(res => {
                this.setState({ players: res.data });
            });
    }
    
    render() {
        return (
            <React.Fragment>
                <ShareGame gameId={this.state.gameId}></ShareGame>
                
                <LetterTiles gameId={this.state.gameId}></LetterTiles>
                <PlayersSideBar players={this.state.players}> </PlayersSideBar>
            </React.Fragment>
        );
    }
}