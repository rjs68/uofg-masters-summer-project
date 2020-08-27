import React, { Component } from 'react';

import Button from '../UI/Button/Button';

class SubmitQuestion extends Component {
    constructor(props){
        super(props);

        this.onQuestionChange = this.onQuestionChange.bind(this);
        this.submitQuestion = this.submitQuestion.bind(this);
    }

    onQuestionChange(event){
        this.setState({
            question: event.target.value
        });
    }

    submitQuestion() {
        const question = this.state.question;
        const questionPacket = {
            username: this.props.username,
            question: question
        };
        var dataChannel;
        const keys = Object.keys(this.props.peerConnections);
        var peer;
        for(var i = 0; i < keys.length; i++) {
            peer = this.props.peerConnections[keys[i]];
            dataChannel = peer.dc;
            dataChannel.send(JSON.stringify(questionPacket));
        }
        this.props.addLocalQuestion(questionPacket);
    }

    render() {
        return (
            <div>
                <input onChange={this.onQuestionChange}
                        type="text" 
                        name="question" 
                        placeholder="Ask a question" />
                <Button clicked={this.submitQuestion}>Submit Question</Button>
            </div>
        )
    }
}

export default SubmitQuestion;