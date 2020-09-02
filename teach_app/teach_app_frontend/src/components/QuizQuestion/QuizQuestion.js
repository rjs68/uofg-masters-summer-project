import React, { Component } from 'react';
import axios from 'axios';

import QuizAnswer from '../QuizAnswer/QuizAnswer';
import Button from '../UI/Button/Button';
import classes from './QuizQuestion.module.css';

class QuizQuestion extends Component {
    constructor(props){
        super(props);
        this.state={};

        this.selectAnswer = this.selectAnswer.bind(this);
        this.submitAnswer = this.submitAnswer.bind(this);
    }

    selectAnswer(answerId){
        this.setState({
            selectedAnswer: answerId
        });
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
                    this.props.nextQuestion();
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

        return (
            <div className={classes.QuizQuestion}>
                <div>
                    {this.props.question}
                </div>
                <div>
                    {quizAnswers}
                </div>
                <Button clicked={this.submitAnswer}>Submit Answer</Button>
            </div>
        )
    }
}

export default QuizQuestion;