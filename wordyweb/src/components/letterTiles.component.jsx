import React, { Component } from "react";
import Axios from "axios";

export default class letterTiles extends Component {
    constructor(props) {
        super(props); //is this needed?
        this.state = {
            letters: []
        }
        this.startRound = this.startRound.bind(this);
    }

    startRound() {
        console.log(this.props.gameId);
        Axios.post(`http://localhost:5000/api/v1/games/${this.props.gameId}/draw`)
            .then(res => {
                console.log(res.data)
                this.setState({letters: res.data})
            });
    }

    renderTiles() {
        let tilesElements = [];
        for(const letter in this.state.letters) {
            const letterCount = this.state.letters[letter]['count']
            for(let i=0;i<letterCount;i++){
                let letterPoints = this.state.letters[letter]['points'];
                tilesElements.push(this.renderTile(letter, letterPoints));
            }
        }
        return tilesElements;
    }

    renderTile(letter, points) {
        return ( 
                <div className="letter-tile">
                    <div className="letter-tile__points">{points}</div>
                    <div className="letter-tile__letter">{letter}</div>
                </div>
        );
    }

    render() {
        return (
            <React.Fragment>
                <button onClick={this.startRound}>Start Round</button>
                <div className="letter-tiles-container">
                    {this.renderTiles()}
                </div>
            </React.Fragment>
        );
    }
}