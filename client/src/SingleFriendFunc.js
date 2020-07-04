import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Avatar from '@material-ui/core/Avatar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import ChatBox from './ChatBox';

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    paper: {
        padding: theme.spacing(3),
        textAlign: 'center',
        color: theme.palette.text.secondary,
        margin: '10px',
        height: '30%',
    },
    chat: {
        padding: theme.spacing(3),
        textAlign: 'center',
        color: theme.palette.text.secondary,
        margin: '10px',
        height: '75%',
    },
    large: {
        width: theme.spacing(10),
        height: theme.spacing(10),
    },
    extend: {
        height: '100%',
    },
}));

const SingleFriendFunc = () => {
    const classes = useStyles();
    const [loadClient, setLoadClient] = useState(true);
    return (
        // <div className={classes.root}>
        <Grid container spacing={3} className={classes.extend}>
            <Grid item xs={8} direction="column">
                <Paper className={classes.paper}>
                    <Grid container spacing={2} justify="center">
                        <Grid item xs={6}>
                            <Avatar
                                alt="Remy Sharp"
                                src="/static/images/avatar/1.jpg"
                                className={classes.large}
                            />
                        </Grid>
                        <Grid item xs={4}>
                            Details
                        </Grid>
                    </Grid>
                </Paper>
                <Paper className={classes.paper}>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            Top Books List
                        </Grid>
                    </Grid>
                </Paper>
            </Grid>
            <Grid item xs={4} direction="column">
                <Paper className={classes.chat}>
                    <Typography variant="h6"> Chat About Books!</Typography>
                    {loadClient ? <ChatBox /> : <div>No Chatting For You</div>}
                    <Button
                        variant="contained"
                        color="secondary"
                        onClick={() => setLoadClient((prevState) => !prevState)}
                    >
                        Close Chat
                    </Button>
                </Paper>
            </Grid>
        </Grid>
        // </div>
    );
};

export default SingleFriendFunc;
