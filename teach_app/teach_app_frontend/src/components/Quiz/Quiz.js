import React, { Component } from 'react';

import QuizQuestion from '../QuizQuestion/QuizQuestion';

class Quiz extends Component {
    constructor(props){
        super(props);
        this.state = {
            question: 0,
            numberOfQuestions: Object.keys(this.props.quizData).length
        };

        this.nextQuestion = this.nextQuestion.bind(this);
    }

    nextQuestion() {
        const nextQuestion = this.state.question + 1;
        console.log(nextQuestion);
        if(nextQuestion<this.state.numberOfQuestions){
            this.setState({
                question: nextQuestion
            });
        }
    }

    render() {
        const questionKeys = Object.keys(this.props.quizData);
        const question = questionKeys[this.state.question];
        const answers = Object.keys(this.props.quizData[question]);

        return (
            <div>
                <QuizQuestion question={question}
                                answers={answers}
                                unitCode={this.props.unitCode}
                                lectureName={this.props.lectureName}
                                userEmail={this.props.userEmail}
                                userType={this.props.userType} 
                                nextQuestion={this.nextQuestion} />
            </div>
        )
    }
}

export default Quiz;