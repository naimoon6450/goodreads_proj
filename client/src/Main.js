import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import axios from 'axios';

import Home from './Home';

class Main extends Component {
    constructor() {
        super();
        this.state = {
            friends: [],
        };
    }

    componentDidMount() {
        axios
            .get('http://localhost:5000/friends')
            .then((resp) => {
                this.setState({ friends: resp.data });
            })
            .catch((e) => {
                return e;
            });
    }

    render() {
        return (
            <Home friends={this.state.friends} history={this.props.history} />
        );
    }
}

export default Main;
