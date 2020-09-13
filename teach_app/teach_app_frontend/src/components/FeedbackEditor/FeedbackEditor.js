import React, { Component } from 'react';
import axios from 'axios';

import Button from '../UI/Button/Button';

class FeedbackEditor extends Component {
    constructor(props){
        super(props);
        this.state = {
            feedback: this.props.feedback
        };

        this.handleFeedbackChange = this.handleFeedbackChange.bind(this);
        this.editFeedbackHandler = this.editFeedbackHandler.bind(this);
    };

    handleFeedbackChange(event) {
        this.setState({
            feedback: event.target.value
        })
    }

    editFeedbackHandler() {
        axios.post('/student-feedback/', {
            unitCode: this.props.assignment['unit_code'],
            assignmentName: this.props.assignment['assignment_name'],
            studentEmail: this.props.studentEmail,
            feedback: this.state.feedback
        })
            .then((response) => {
                this.props.handleFeedbackEditorStatus();
                this.props.getStudentSubmissions();
            });
    }

    render() {
        return(
            <div>
                <textarea onChange={this.handleFeedbackChange}
                            name="feedback"
                            placeholder="Feedback"
                            rows={5}
                            columns={40}/>
                <Button clicked={this.editFeedbackHandler}>Submit Feedback</Button>
            </div>
        )
    };
}

export default FeedbackEditor;