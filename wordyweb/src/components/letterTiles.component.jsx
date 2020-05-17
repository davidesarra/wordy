import React, { Component } from "react";

export default class letterTiles extends Component {
    constructor() {
        super();
        this.state = {
            letters: []
        }
    }
    componentDidMount() {
        this.setState({letters: ["a", "b", "c"]});
    }

    renderTiles(){
        return this.state.letters.map(letter =>  
                   <span className="letter-tile">{letter}</span>
                );
    }
    render() {
        if(this.state.letters.length === 0) return <div>No Tiles</div>;
        return (
            <React.Fragment>
                <div className="tile-container">
                    {this.renderTiles()}
                </div>
            </React.Fragment>
        );
    }
}