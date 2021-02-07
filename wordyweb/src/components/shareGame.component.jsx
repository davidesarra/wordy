import React, { Component } from "react";

export default class ShareGame extends Component {
    render() {
        return (
            <div className="shareGame">
                Invite other players to this game - Game ID {this.props.gameId}
            </div>
        );
    };
};
