import React, { Component } from 'react';

import Button from '../UI/Button/Button';

class QuestionEditor extends Component {
    constructor(props){
        super(props);
        this.state = {
            oldQuestion: props.question,
            newQuestion: props.question,
            newAnswers: props.answers
        };

        this.onQuestionChange = this.onQuestionChange.bind(this);
        this.onAnswerChange = this.onAnswerChange.bind(this);
    }

    onQuestionChange(event) {
        this.setState({
            newQuestion: event.target.value
        });
    }

    onAnswerChange(event) {
        var newAnswers;
        if(this.state.newAnswers){
            newAnswers = {...this.state.newAnswers};
        }else{
            newAnswers = {...this.props.answers};
        };

        const oldAnswer = event.target.name;
        const newAnswer = event.target.value;
        event.target.name = newAnswer;
        delete newAnswers[oldAnswer];
        newAnswers[newAnswer] = false;
        this.setState({
            newAnswers: newAnswers
        })
    }

    render() {
        const editAnswers = [];
        var index = 0;
        for(const answer in this.props.answers){
            const editAnswer = <input key={index}
                                        index={index}
                                        onChange={this.onAnswerChange}
                                        type="text" 
                                        name={answer}
                                        placeholder={answer} />
            editAnswers.push(editAnswer);
            index++;
        };

        return (
            <div>
                <label htmlFor={this.props.question}>Question</label>
                <input onChange={this.onQuestionChange}
                        id={this.props.question}
                        type="text" 
                        name="question"
                        placeholder={this.props.question} />
                <label htmlFor="answers">Answers</label>
                <div id="answer">
                    {editAnswers}
                </div>
                <Button clicked={() => {this.props.updateQuestion(this.state.oldQuestion, this.state.newQuestion, this.state.newAnswers)}}>
                    Update Question
                </Button>
            </div>
        )
    }
}

export default QuestionEditor;