import React, { Component } from "react";

export default class Game extends Component {
    createPlayersListElement() {
        if (this.props.players.length > 0){
            console.log(this.props.players)
            let p = this.props.players
            return p.map(player => <li key={player.name}>{player.name}</li>);
        }
    }
    render() {
        console.log(this.props)
        const players = this.createPlayersListElement();
        return (
            <div className="playersSideBar">
                {players}
            </div>
        );
    }
}