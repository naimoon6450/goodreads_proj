import React, { Component } from 'react';
import axios from 'axios';
import SingleFriendFunc from './SingleFriendFunc';

class SingleFriend extends Component {
    constructor() {
        super();
        this.state = {
            friend: [],
        };
    }
    componentDidMount() {
        const goodreads_id = this.props.match.params.id;
        axios
            .post('http://localhost:5000/get_friend', { goodreads_id })
            .then((response) => {
                this.setState({ friend: response.data });
            });
    }
    render() {
        console.log(this.state.friend);
        // const { friendArr } = props;
        // console.log(friendArr);
        return <SingleFriendFunc />;
    }
}

export default SingleFriend;
