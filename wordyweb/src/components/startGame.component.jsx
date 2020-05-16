import React, { Component } from "react";

export default class StartGame extends Component {
    startGame() {
        console.log("creating game");
    };
    render() {
        return (
            <React.Fragment><button onClick={this.startGame()}>START GAME</button></React.Fragment>
        );
    };
}
