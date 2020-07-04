import React, { useState, useEffect, useRef } from 'react';
import socketIOClient from 'socket.io-client';
const ENDPOINT = 'http://127.0.0.1:5000/';

const socket = socketIOClient(ENDPOINT);

const ChatBox = () => {
    const [message, setMessage] = useState('');
    const [receivedMsgs, setAllMessages] = useState([]);

    useEffect(() => {
        socket.on('connect', function () {
            socket.send('User has connected!');
        });
        socket.on('message', (msg) => {
            // whatever is received put it to state
            setAllMessages([...receivedMsgs, msg]);
        });
    }, [receivedMsgs]);

    // disconnect socket once unmounted
    useEffect(() => {
        return () => {
            console.log('socket closed');
            socket.close();
        };
    }, []);

    const sendMessageHandler = () => {
        socket.emit('message', message);
        setMessage('');
    };

    return (
        <div>
            <div id="messages">
                {/* It's <time dateTime={response}>{response}</time> */}
                {receivedMsgs.map((elem, ind) => {
                    return <p key={ind}>{elem}</p>;
                })}
            </div>
            <input
                type="text"
                id="myMessage"
                value={message}
                onChange={(e) => {
                    setMessage(e.target.value);
                }}
            />
            <button onClick={sendMessageHandler} id="sendbutton">
                Send
            </button>
        </div>
    );
};

export default ChatBox;
