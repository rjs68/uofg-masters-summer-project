import React, { Component } from 'react';

import Button from '../UI/Button/Button';
import classes from './QuestionEditor.module.css';

class QuestionEditor extends Component {
    constructor(props){
        super(props);
        
        var correctAnswer;
        var correctAnswerIndex;
        var index=0;
        for(const answer in props.answers){
            if(props.answers[answer]){
                correctAnswer = answer;
                correctAnswerIndex = index;
            };
            index++;
        };

        this.state = {
            oldQuestion: props.question,
            newQuestion: props.question,
            newAnswers: props.answers,
            correctAnswer: correctAnswer,
            correctAnswerIndex: correctAnswerIndex
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
        if(oldAnswer===this.state.correctAnswer){
            newAnswers[newAnswer] = true;
            this.setState({
                correctAnswer: newAnswer
            });
        }else{
            newAnswers[newAnswer] = false;
        }
        
        this.setState({
            newAnswers: newAnswers
        })
    }

    render() {
        const editAnswers = [];
        var index = 0;
        for(const answer in this.props.answers){
            var style;
            if(index===this.state.correctAnswerIndex){
                style=classes.CorrectAnswer;
            }else{
                style=null;
            }
            const editAnswer = <div className={style} key={index}>
                                    <input index={index}
                                            onChange={this.onAnswerChange}
                                            type="text" 
                                            name={answer}
                                            placeholder={answer} />
                                </div>
            editAnswers.push(editAnswer);
            index++;
        };
        const addAnswer = <div key={index}>
                                <input index={index}
                                        onChange={this.onAnswerChange}
                                        type="text" 
                                        name="addAnswer"
                                        placeholder="Add Answer" />
                            </div>
        editAnswers.push(addAnswer);

        return (
            <div className={classes.QuestionEditor}>
                <input onChange={this.onQuestionChange}
                        type="text" 
                        name="question"
                        placeholder={this.props.question} />
                <div>
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