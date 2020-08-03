import React, { Component } from 'react';

import classes from './StudentSubmission.module.css';
import Button from '../UI/Button/Button';
import Modal from '../UI/Modal/Modal';
import GradeEditor from '../GradeEditor/GradeEditor';

class StudentSubmission extends Component {
    constructor(props) {
        super(props);
        this.state = {
            showGradeModal: false,
            showFeedbackModal: false
        };
        
        this.handleGradeEditorStatus = this.handleGradeEditorStatus.bind(this);
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

    render() {
        return (
            <div className={classes.StudentSubmission}>
                <Modal show={this.state.showGradeModal}>
                    <GradeEditor assignment={this.props.assignment}
                                studentEmail={this.props.studentEmail}
                                grade={this.props.grade}/>
                </Modal>
                <div className={classes.Email}>{this.props.studentEmail}</div>
                <a href={this.props.submissionPath} download>Download Submission</a>
                <div className={classes.Grade}>{this.props.grade}</div>
                <Button clicked={this.handleGradeEditorStatus}>Edit Grade</Button>
                <Button>Edit Feedback</Button>
            </div>
        )
    };
} 

export default StudentSubmission;