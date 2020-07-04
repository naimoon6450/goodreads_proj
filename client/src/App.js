import React from 'react';
import { Route, Switch, Redirect } from 'react-router-dom';

import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import Button from '@material-ui/core/Button';

// components
import Main from './Main';
import SingleFriend from './SingleFriend';
import Friends from './Friends';
import Error404 from './Error404';
import { Login } from './Login';

class App extends React.Component {
    constructor() {
        super();
        this.state = {
            accessToken: '',
        };
        this.loginHandler = this.loginHandler.bind(this);
    }

    componentDidMount() {
        let search = window.location.search;
        let params = new URLSearchParams(search);
        let auth_token = params.get('oauth_token');
        this.setState({ accessToken: auth_token });
    }

    loginHandler() {
        window.location = 'http://localhost:5000/goodreads/login';
    }

    render() {
        return (
            <Switch>
                <Route
                    exact
                    path="/"
                    render={() => {
                        return <Login loginHandler={this.loginHandler} />;
                    }}
                />
                <Route
                    path="/home"
                    render={(history) => {
                        return this.state.accessToken ? (
                            <Main
                                token={this.state.accessToken}
                                history={history}
                            />
                        ) : (
                            <Error404 />
                        );
                    }}
                />
                <Route path="/friend/:id" component={SingleFriend} />
            </Switch>
        );
    }
}

export default App;
