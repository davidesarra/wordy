import React, { Component } from "react";
import PlayersSideBar from './playersSideBar.component'
import Axios from 'axios';
export default class Game extends Component {
    state = {
        players: []
    };
    componentDidMount(){
        Axios.get("http://localhost:5000/api/v1/games/0/players")
            .then(res => {
                this.setState({players:res.data});
            });
    }
    render(){
        return (
            <React.Fragment>
                <PlayersSideBar players={this.state.players}> </PlayersSideBar>
            </React.Fragment>
        );
    }
}