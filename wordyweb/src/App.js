import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom'
import './App.css';
import JoinGame from './components/joinGame.component'
import Game from './components/game.component';

function App() {
  return (
    <Router>
      <Route
      path="/game"
      render={(props) => <Game {...props}/>}
      />
      <Route
      path="/"
      render={() => <JoinGame />}
      />
  </Router>
  ); 
}

export default App;
