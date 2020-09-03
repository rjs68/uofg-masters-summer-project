import React, { Component } from 'react';

import QuizQuestion from '../QuizQuestion/QuizQuestion';

class Quiz extends Component {
    constructor(props){
        super(props);
        this.state = {
            question: 0,
            numberOfQuestions: Object.keys(this.props.quizData).length,
            isLastQuestion: false,
            quizFinished: false
        };

        this.nextQuestion = this.nextQuestion.bind(this);
        this.finishQuiz = this.finishQuiz.bind(this);
    }

    nextQuestion() {
        const nextQuestion = this.state.question + 1;
        if(nextQuestion<this.state.numberOfQuestions-1){
            this.setState({
                question: nextQuestion
            });
        }else{
            this.setState({
                isLastQuestion: true
            });
        };
    }

    finishQuiz() {
        this.setState({
            quizFinished: true
        });
    }

    render() {
        var quizContent;
        if(this.state.quizFinished){
            quizContent = "Waiting for quiz to end";
        }else{
            const questionKeys = Object.keys(this.props.quizData);
            const question = questionKeys[this.state.question];
            const answers = Object.keys(this.props.quizData[question]);
            quizContent = <QuizQuestion question={question}
                                        answers={answers}
                                        unitCode={this.props.unitCode}
                                        lectureName={this.props.lectureName}
                                        userEmail={this.props.userEmail}
                                        userType={this.props.userType} 
                                        nextQuestion={this.nextQuestion} 
                                        isLastQuestion={this.state.isLastQuestion} 
                                        finishQuiz={this.finishQuiz} />
        }
        

        return (
            <div>
                {quizContent}
            </div>
        )
    }
}

export default Quiz;