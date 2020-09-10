import React, { Component } from 'react';

class PreLectureScreen extends Component {
    constructor(props){
        super(props);
        this.state = {
            newQuestions: {},
            newAnswers: {}
        };

        this.onQuestionChange = this.onQuestionChange.bind(this);
    }

    onQuestionChange(event) {
        const questionIndex = event.target.name;
        const newQuestion = event.target.value;
        const newQuestions = this.state.newQuestions;
        newQuestions[questionIndex] = newQuestion;
        this.setState({
            newQuestions: newQuestions
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
                const questions = Object.keys(this.props.quizData)
                for(const questionNumber in this.props.quizData){
                    const question = questions[questionNumber];
                    const inputName = "question " + questionNumber;
                    const editQuestionInput = <input onChange={this.onQuestionChange}
                                                    key={questionNumber}
                                                    type="text" 
                                                    name={questionNumber}
                                                    value={question} />
                    editQuizContent.push(editQuestionInput);
                }
            }
            const nextQuestionNumber = this.props.quizData ? Object.keys(this.props.quizData).length : 0;
            const inputName = "question " + nextQuestionNumber;
            const addQuestionInput = <input onChange={this.onQuestionChange}
                                            key={nextQuestionNumber}
                                            type="text" 
                                            name={nextQuestionNumber}
                                            placeholder="Add question" />
            editQuizContent.push(addQuestionInput);
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