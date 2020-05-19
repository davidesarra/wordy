import React, { Component } from "react";

export default class PlayersSideBar extends Component {
    createPlayersListElement() {
        if (this.props.players.length > 0){
            let players = this.props.players;
            return players.map(player => <li key={player.name}>{player.name}</li>);
        }
    }
    render() {
        return (
            <div className="players-sideBar">
                Players:
                {this.createPlayersListElement()}
            </div>
        );
    }
}