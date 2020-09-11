import React, { Component } from 'react';

import QuestionEditor from '../QuestionEditor/QuestionEditor';

class PreLectureScreen extends Component {
    constructor(props){
        super(props);
        this.state = {};

        this.onQuestionChange = this.onQuestionChange.bind(this);
    }

    onQuestionChange(event) {
        var newQuizData;
        if(this.state.newQuizData){
            newQuizData = {...this.state.newQuizData};
        }else{
            newQuizData = {...this.props.quizData};
        }
        const questions = Object.keys(newQuizData);
        const questionIndex = event.target.name;
        const oldQuestion = questions[questionIndex];
        const answers = newQuizData[oldQuestion];
        const newQuestion = event.target.value;

        delete newQuizData[oldQuestion];
        newQuizData[newQuestion] = answers;
        this.setState({
            newQuizData: newQuizData
        });
    }

    render() {
        const lectureTime = new Date(this.props.lectureTime);
        const currentTime = new Date();
        var timeDifference = (lectureTime - currentTime)/1000/60;

        var lectureMinutes = lectureTime.getMinutes();
        if(lectureMinutes<10){
            lectureMinutes = '0' + lectureMinutes;
        }

        var lectureTimeDisplay;
        if(timeDifference>=60*24){
            timeDifference=(timeDifference/60)/24;
            lectureTimeDisplay = lectureTime.toDateString() + " - " + lectureTime.getHours() + ":" 
                                + lectureMinutes + " (" + Math.round(timeDifference) + " days to go)";
        }else if(timeDifference>=60){
            timeDifference=timeDifference/60;
            lectureTimeDisplay = "Today at " + lectureTime.getHours() + ":" + lectureMinutes
                                + lectureMinutes + " (" + Math.round(timeDifference) + " hours to go";
        }else{
            lectureTimeDisplay = "Today at " + lectureTime.getHours() + ":" + lectureMinutes
                                +  " (" + Math.round(timeDifference) + " minutes to go";
        }

        var editQuizContent=[];
        if(this.props.userType==="teacher"){
            if(this.props.quizAvailable){
                var quizData;
                if(this.state.newQuizData){
                    quizData = this.state.newQuizData;
                }else{
                    quizData = this.props.quizData;
                }
                const questions = Object.keys(quizData);
                for(const question in quizData){
                    const questionEditor = <QuestionEditor key={question}
                                                            question={question}
                                                            answers={quizData[question]}/>
                    editQuizContent.push(questionEditor);
                }
            }
            // const nextQuestionNumber = this.props.quizAvailable && this.state.newQuizData ? 
            //                                 Object.keys(this.state.newQuizData).length : 
            //                                     this.props.quizAvailable ? Object.keys(this.props.quizData).length : 0;
            // const addQuestionInput = <input onChange={this.onQuestionChange}
            //                                 key={nextQuestionNumber}
            //                                 type="text" 
            //                                 name={nextQuestionNumber}
            //                                 placeholder="Add question" />
            // editQuizContent.push(addQuestionInput);
        }

        return (
            <div>
                <h1>The lecture hasn't started yet</h1>
                <p>{lectureTimeDisplay}</p>
                {editQuizContent}
            </div>
        )
    }
}

export default PreLectureScreen;