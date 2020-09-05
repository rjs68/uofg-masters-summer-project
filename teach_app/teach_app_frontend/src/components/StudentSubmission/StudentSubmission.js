import React, { Component } from 'react';

import classes from './StudentSubmission.module.css';
import Button from '../UI/Button/Button';
import Modal from '../UI/Modal/Modal';
import Backdrop from '../UI/Backdrop/Backdrop';
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
        var submittedDiv;
        var submissionTimeObject;
        if(this.props.submissionTime){
            var submissionTimeString = this.props.submissionTime;
            submissionTimeObject = new Date(submissionTimeString);
            submittedDiv = <div>
                                Submitted: {submissionTimeObject.toLocaleTimeString()} {submissionTimeObject.toDateString()}
                            </div>;
        }

        var deadlineComparisonDiv;
        if(this.props.assignment['deadline'] && submissionTimeObject){
            var assignmentTimeString = this.props.assignment['deadline'];
            const assignmentTimeObject = new Date(assignmentTimeString);
            var timeDifference = ((assignmentTimeObject.getTime() - submissionTimeObject.getTime())/1000)/60;
            var timeUnit = " minutes"
            const submittedOnTime = timeDifference>=0;
            var earlyOrLate;
            if(!submittedOnTime){
                timeDifference = timeDifference*-1;
                earlyOrLate = " late";
            }else{
                earlyOrLate = " early";
            }
            if(timeDifference>=60*24){
                timeDifference=(timeDifference/60)/24;
                timeUnit = " days";
            }else if(timeDifference>=60){
                timeDifference=timeDifference/60;
                timeUnit = " hours";
            }
            deadlineComparisonDiv = <div>
                                {Math.round(timeDifference)} {timeUnit} {earlyOrLate}
                            </div>;
        }

        var showBackdrop = false;
        var backdropClicked;
        if(this.state.showFeedbackModal){
            showBackdrop = true;
            backdropClicked = this.handleFeedbackEditorStatus;
        }else if(this.state.showGradeModal){
            showBackdrop = true;
            backdropClicked = this.handleGradeEditorStatus;
        }
        
        return (
            <div className={classes.StudentSubmission}>
                <Backdrop show={showBackdrop} clicked={backdropClicked}/>
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
                    {submittedDiv}
                </div>
                <div>
                    <div className={classes.Grade}>Grade: {this.props.grade}</div>
                    <Button clicked={this.handleGradeEditorStatus}>Edit Grade</Button>
                    <Button clicked={this.handleFeedbackEditorStatus}>Edit Feedback</Button>
                    {deadlineComparisonDiv}
                </div> 
            </div>
        )
    };
} 

export default StudentSubmission;