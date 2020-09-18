import React, { Component } from 'react';
import axios from 'axios';

import classes from './QuizResults.module.css';

class QuizResults extends Component {
    constructor(props){
        super(props);

        this.state={};

        this.getQuizResults = this.getQuizResults.bind(this);
        this.getAverageScore = this.getAverageScore.bind(this);
    }

    getQuizResults() {
        axios.post('/quiz-results/', {
            unitCode: this.props.unitCode,
            lectureName: this.props.lectureName
        })
        .then((response) => {
            this.setState({
                quizResults: response.data
            });
            this.getAverageScore();
        });
    }

    getAverageScore() {
        const numberOfUsers = Object.keys(this.state.quizResults).length
        var cumulativeScore = 0;
        for(const result in this.state.quizResults){
            const resultScore = this.state.quizResults[result];
            cumulativeScore += resultScore;
        }
        const averageScore = Math.round(cumulativeScore/numberOfUsers);
        this.setState({
            averageScore: averageScore
        });
    }

    componentDidMount() {
        this.getQuizResults();
    }

    render() {
        var quizResults;
        if(this.state.quizResults){
            if(this.props.userType==="teacher"){
                const userScores = [];
                for(const user in this.state.quizResults){
                    userScores.push(
                        <p key={user}>{user}: {this.state.quizResults[user]}</p>
                    )
                }
                quizResults = <div>
                                    <h1>Average Score: {this.state.averageScore}</h1>
                                    {userScores}
                            </div>
            }else{
                quizResults = <div>
                                    <h1>Average Score: {this.state.averageScore}</h1>
                                    <h1>Your Score: {this.state.quizResults[this.props.userEmail]}</h1>
                            </div>
            }
        }

        return (
            <div className={classes.QuizResults}>
                {quizResults}
            </div>
        )
    }
}

export default QuizResults;