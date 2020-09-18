import React, { Component } from 'react';

import QuizQuestion from './QuizQuestion/QuizQuestion';
import QuizResults from './QuizResults/QuizResults';
import CountdownClock from './CountdownClock/CountdownClock';
import classes from './Quiz.module.css';

class Quiz extends Component {
    constructor(props){
        super(props);
        this.state = {
            question: 0,
            numberOfQuestions: Object.keys(this.props.quizData).length,
            isLastQuestion: false,
            quizFinished: false,
            timeUp: false
        };

        this.nextQuestion = this.nextQuestion.bind(this);
        this.finishQuiz = this.finishQuiz.bind(this);
        this.quizTimeUp = this.quizTimeUp.bind(this);
    }

    nextQuestion() {
        //moves screen display onto the next question
        const nextQuestion = this.state.question + 1;
        if(nextQuestion<this.state.numberOfQuestions){
            this.setState({
                question: nextQuestion
            });
            if(nextQuestion===this.state.numberOfQuestions-1){
                this.setState({
                    isLastQuestion: true
                });
            }
        }
    }

    finishQuiz() {
        //user confirms that they have finished the quiz
        this.setState({
            quizFinished: true
        });
    }

    quizTimeUp() {
        //called when quiz countdown reaches 0
        this.setState({
            timeUp: true
        });
    }

    render() {
        var quizContent;
        //displays quiz questions or results depending on time remaining
        if(this.state.timeUp){
            quizContent = <QuizResults unitCode={this.props.unitCode}
                                        lectureName={this.props.lectureName} 
                                        userType={this.props.userType}
                                        userEmail={this.props.userEmail} />
        }else{
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
        }

        return (
            <div className={classes.Quiz}>
                <CountdownClock quizLength={this.props.quizLength} 
                                quizTimeUp={this.quizTimeUp} />
                {quizContent}
            </div>
        )
    }
}

export default Quiz;