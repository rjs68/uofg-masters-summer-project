import React, { Component } from 'react';

import Button from '../../../UI/Button/Button';

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
            type: "question",
            username: this.props.username,
            question: question
        };
        const keys = Object.keys(this.props.peerConnections);
        for(var i = 0; i < keys.length; i++) {
            //sends student question to all peer connections
            const peer = this.props.peerConnections[keys[i]];
            const dataChannel = peer.dc;
            dataChannel.send(JSON.stringify(questionPacket));
        }
        //adds question to own user's screen
        this.props.addLocalQuestion(questionPacket);
    }

    render() {
        //input fields allowing student to ask questions
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