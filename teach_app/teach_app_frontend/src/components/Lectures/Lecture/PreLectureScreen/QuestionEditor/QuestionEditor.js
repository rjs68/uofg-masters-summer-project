import React, { Component } from 'react';

import Button from '../../../../UI/Button/Button';
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
        //retrieve all the current answers
        if(this.state.newAnswers){
            newAnswers = {...this.state.newAnswers};
        }else{
            newAnswers = {...this.props.answers};
        };

        const oldAnswer = event.target.name;
        const newAnswer = event.target.value;
        event.target.name = newAnswer;
        //delete old answer from the list
        delete newAnswers[oldAnswer];
        //add new answer to the list
        if(oldAnswer===this.state.correctAnswer || this.props.question==="Add Question"){
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
        //provides input fields to edit questions and answers
        //correct answers are highlighted 
        const editAnswers = [];
        var index = 0;
        var style;
        for(const answer in this.props.answers){
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
        if(this.props.question==="Add Question"){
            style=classes.CorrectAnswer;
        }else{
            style=null;
        }
        const addAnswer = <div key={index} className={style}>
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