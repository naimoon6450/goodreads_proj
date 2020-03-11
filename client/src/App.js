import React from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';

class App extends React.Component {
  constructor() {
    super();
    this.state = {
      ids: [],
    };
  }

  componentDidMount() {
    axios.get('http://127.0.0.1:5000/friends').then(({ data }) => {
      this.setState({ ids: data.friends });
    });
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
          <div>
            {this.state.ids
              ? this.state.ids.map(elem => {
                  return <p>{elem}</p>;
                })
              : ''}
          </div>
        </header>
      </div>
    );
  }
}

export default App;
