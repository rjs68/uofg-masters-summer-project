import React, { Component } from 'react';
import axios from 'axios';

import QuestionEditor from './QuestionEditor/QuestionEditor';
import classes from './PreLectureScreen.module.css';

class PreLectureScreen extends Component {
    constructor(props){
        super(props);
        this.state = {};

        this.updateQuestion = this.updateQuestion.bind(this);
    }

    updateQuestion(oldQuestion, newQuestion, newAnswers){
        //updates quiz data in the database
        axios.post('/update-quiz/', {
            unitCode: this.props.unitCode,
            lectureName: this.props.lecture,
            oldQuestion: oldQuestion,
            newQuestion: newQuestion,
            newAnswers: newAnswers
        })
        .then((response) => {
            //obtain updated data and render on screen
            this.props.updateQuizData();
            this.render();
        });
    }

    render() {
        const lectureTime = new Date(this.props.lectureTime);
        const currentTime = new Date();
        var timeDifference = (lectureTime - currentTime)/1000/60;

        var lectureMinutes = lectureTime.getMinutes();
        //ensure display of minutes less than 10 retains 2 digits
        if(lectureMinutes<10){
            lectureMinutes = '0' + lectureMinutes;
        }

        //logic to display how long is left until lecture starts
        var lectureTimeDisplay;
        if(timeDifference>=60*24){
            timeDifference=(timeDifference/60)/24;
            lectureTimeDisplay = lectureTime.toDateString() + " - " + lectureTime.getHours() + ":" 
                                + lectureMinutes + " (" + Math.round(timeDifference) + " days to go)";
        }else if(timeDifference>=60){
            timeDifference=timeDifference/60;
            lectureTimeDisplay = "Today at " + lectureTime.getHours() + ":" + lectureMinutes
                                + lectureMinutes + " (" + Math.round(timeDifference) + " hours to go)";
        }else{
            lectureTimeDisplay = "Today at " + lectureTime.getHours() + ":" + lectureMinutes
                                +  " (" + Math.round(timeDifference) + " minutes to go)";
        }

        //components allow teachers to update and add quiz questions
        var editQuizContent=[];
        if(this.props.userType==="teacher"){
            if(this.props.quizAvailable){
                const quizData = this.props.quizData;
                for(const question in quizData){
                    const questionEditor = <QuestionEditor key={question}
                                                            question={question}
                                                            answers={quizData[question]}
                                                            updateQuestion={this.updateQuestion} />
                    editQuizContent.push(questionEditor);
                }
            }
            const addQuestion = <QuestionEditor key="addQuestion"
                                                    question="Add Question"
                                                    updateQuestion={this.updateQuestion} />
            editQuizContent.push(addQuestion);
        }

        return (
            <div className={classes.PreLectureScreen}>
                <h1>The lecture hasn't started yet</h1>
                <p>{lectureTimeDisplay}</p>
                {editQuizContent}
            </div>
        )
    }
}

export default PreLectureScreen;