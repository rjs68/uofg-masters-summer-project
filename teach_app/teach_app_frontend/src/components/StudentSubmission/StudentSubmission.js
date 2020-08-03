import React, { Component } from 'react';

import classes from './StudentSubmission.module.css';
import Button from '../UI/Button/Button';
import Modal from '../UI/Modal/Modal';
import GradeEditor from '../GradeEditor/GradeEditor';
import FeedbackEditor from '../FeedbackEditor/FeedbackEditor';

class StudentSubmission extends Component {
    constructor(props) {
        super(props);
        this.state = {
            showGradeModal: false,
            showFeedbackModal: false
        };

        this.handleGradeEditorStatus = this.handleGradeEditorStatus.bind(this);
        this.handleFeedbackEditorStatus = this.handleFeedbackEditorStatus.bind(this);
    };

    handleGradeEditorStatus() {
        var showGradeModal;
        if(this.state.showGradeModal === true){
            showGradeModal = false;
        }else{
            showGradeModal = true;
        };
        this.setState({
            showGradeModal: showGradeModal
        });
    }

    handleFeedbackEditorStatus() {
        var showFeedbackModal;
        if(this.state.showFeedbackModal === true){
            showFeedbackModal = false;
        }else{
            showFeedbackModal = true;
        };
        this.setState({
            showFeedbackModal: showFeedbackModal
        });
    }

    render() {
        var submissionTimeString;
        var plusIndex;
        var submissionTimeObject;
        var submittedDiv;
        if(this.props.submissionTime){
            submissionTimeString = this.props.submissionTime;
            submissionTimeString.replace(' ', 'T');
            plusIndex = submissionTimeString.indexOf('+');
            submissionTimeString = submissionTimeString.substring(0, plusIndex);
            submissionTimeObject = new Date(submissionTimeString);
            submittedDiv = <div>Submitted: {submissionTimeObject.toDateString()}</div>;
        }
        
        return (
            <div className={classes.StudentSubmission}>
                <Modal show={this.state.showGradeModal}>
                    <GradeEditor assignment={this.props.assignment}
                                studentEmail={this.props.studentEmail}
                                grade={this.props.grade}/>
                </Modal>
                <Modal show={this.state.showFeedbackModal}>
                    <FeedbackEditor assignment={this.props.assignment}
                                    studentEmail={this.props.studentEmail}
                                    feedback={this.props.feedback}/>
                </Modal>
                <div>
                    <div className={classes.Email}>{this.props.studentEmail}</div>
                    <a href={this.props.submissionPath} download>Download Submission</a>
                    <div className={classes.Grade}>{this.props.grade}</div>
                    {submittedDiv}
                </div>
                <div>
                    <Button clicked={this.handleGradeEditorStatus}>Edit Grade</Button>
                    <Button clicked={this.handleFeedbackEditorStatus}>Edit Feedback</Button>
                </div> 
            </div>
        )
    };
} 

export default StudentSubmission;