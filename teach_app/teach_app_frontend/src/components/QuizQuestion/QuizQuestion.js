import React, { Component } from 'react';

import QuizAnswer from '../QuizAnswer/QuizAnswer';
import classes from './QuizQuestion.module.css';

class QuizQuestion extends Component {
    constructor(props){
        super(props);
    }

    render() {
        const quizAnswers = []
        for(const answer in this.props.answers){
            const answerComponent = <QuizAnswer key={answer}
                                                answer={this.props.answers[answer]}/>
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
            </div>
        )
    }
}

export default QuizQuestion;