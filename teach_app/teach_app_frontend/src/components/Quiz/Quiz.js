import React, { Component } from 'react';

import QuizQuestion from '../QuizQuestion/QuizQuestion';

class Quiz extends Component {
    constructor(props){
        super(props);
        this.state = {
            question: 0
        };
    }

    render() {
        const questionKeys = Object.keys(this.props.quizData);
        const question = questionKeys[this.state.question];
        const answers = Object.keys(this.props.quizData[question]);

        return (
            <div>
                <QuizQuestion question={question}
                                answers={answers}/>
            </div>
        )
    }
}

export default Quiz;