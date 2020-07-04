import React from 'react';
import { withRouter } from 'react-router';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import ButtonBase from '@material-ui/core/ButtonBase';

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    paper: {
        padding: theme.spacing(2),
        // margin: 'auto',
        maxWidth: 500,
    },
    image: {
        width: 128,
        height: 128,
    },
    img: {
        margin: 'auto',
        display: 'block',
        maxWidth: '100%',
        maxHeight: '100%',
    },
}));

const Friends = (props) => {
    const classes = useStyles();
    const { friendArr, history } = props;
    console.log(friendArr);

    return (
        // <div className={classes.root}>
        <Grid container spacing={3}>
            {friendArr.map((friend) => {
                return (
                    <Grid item xs={3}>
                        <Paper className={classes.paper}>
                            <Grid container spacing={3}>
                                <Grid item>
                                    <ButtonBase className={classes.image}>
                                        <img
                                            className={classes.img}
                                            alt="complex"
                                            src={
                                                friend.user_image.includes(
                                                    'nophoto'
                                                )
                                                    ? 'reader.png'
                                                    : friend.user_image
                                            }
                                            onClick={() => {
                                                // console.log(history);
                                                history.push(
                                                    `/friend/${friend.goodreads_id}`
                                                );
                                            }}
                                        />
                                    </ButtonBase>
                                </Grid>
                                <Grid item xs={12} sm container>
                                    <Grid
                                        item
                                        xs
                                        container
                                        direction="column"
                                        spacing={2}
                                    >
                                        <Grid item xs>
                                            <Typography
                                                gutterBottom
                                                variant="subtitle1"
                                            >
                                                {friend.name}
                                            </Typography>
                                            <Typography
                                                variant="body2"
                                                gutterBottom
                                            >
                                                Friends: {friend.friends}
                                            </Typography>
                                            <Typography
                                                variant="body2"
                                                color="textSecondary"
                                            >
                                                Profile: {friend.profile_link}
                                            </Typography>
                                        </Grid>
                                    </Grid>
                                </Grid>
                            </Grid>
                        </Paper>
                    </Grid>
                );
            })}
        </Grid>
        // </div>
    );
};

export default withRouter(Friends);
