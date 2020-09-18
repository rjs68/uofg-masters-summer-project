import React, { Component } from 'react';
import axios from 'axios';

import QuizAnswer from '../QuizAnswer/QuizAnswer';
import Button from '../../../../UI/Button/Button';
import classes from './QuizQuestion.module.css';

class QuizQuestion extends Component {
    constructor(props){
        super(props);
        this.state={};

        this.selectAnswer = this.selectAnswer.bind(this);
        this.getNextQuestion = this.getNextQuestion.bind(this);
        this.submitAnswer = this.submitAnswer.bind(this);
    }

    selectAnswer(answerId){
        if(this.props.userType==="student"){
            //set selected answer for styling in QuizAnswer
            this.setState({
                selectedAnswer: answerId
            });
        };
    }

    getNextQuestion(){
        //allows student to move forward through the quiz
        if(this.props.userType==="student"){
            this.submitAnswer();
        }else{
            //answers aren't submitted for teachers
            if(this.props.isLastQuestion){
                this.props.finishQuiz();
            }else{
                this.props.nextQuestion();
            }
        }
    }

    submitAnswer(){
        if(this.state.selectedAnswer){
            axios.post('/submit-answer/', {
                unitCode: this.props.unitCode,
                lectureName: this.props.lectureName,
                question: this.props.question,
                answer: this.props.answers[this.state.selectedAnswer],
                userEmail: this.props.userEmail
            })
            .then((response) => {
                if(response.data==="Answer Submitted"){
                    this.setState({
                        selectedAnswer: null
                    })
                    //only moves to next question if previous answers is submitted successfully
                    if(this.props.isLastQuestion){
                        this.props.finishQuiz();
                    }else{
                        this.props.nextQuestion();
                    }
                }else{
                    console.log(response.data);
                }
            });
        };
    }

    render() {
        const quizAnswers = []
        for(const answer in this.props.answers){
            var answerSelected = false;
            if(answer===this.state.selectedAnswer){
                answerSelected = true;
            };

            const answerComponent = <QuizAnswer key={answer}
                                                id={answer}
                                                answer={this.props.answers[answer]}
                                                selected={answerSelected}
                                                clicked={this.selectAnswer}/>
            quizAnswers.push(answerComponent);
        }

        //button text changes for last question in the quiz
        var buttonText = "Next";
        if(this.props.isLastQuestion){
            buttonText = "Finish Quiz";
        }

        return (
            <div className={classes.QuizQuestion}>
                <div>
                    {this.props.question}
                </div>
                <div>
                    {quizAnswers}
                </div>
                <Button clicked={this.getNextQuestion}>{buttonText}</Button>
            </div>
        )
    }
}

export default QuizQuestion;