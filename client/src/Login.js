import React from 'react';
import Button from '@material-ui/core/Button';

export const Login = (props) => {
    return (
        <div className="App">
            <header className="App-header">
                <img
                    src="book-open-flat.png"
                    // className="App-logo"
                    alt="logo"
                />
                <p>Welcom to the Reader App</p>
                <Button
                    variant="contained"
                    color="info"
                    onClick={props.loginHandler}
                    // target="_blank"
                    // href="http://localhost:5000/goodreads/login"
                >
                    Login to Goodreads
                </Button>
            </header>
        </div>
    );
};
