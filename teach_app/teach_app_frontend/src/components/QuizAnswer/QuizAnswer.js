import React from 'react';

import classes from './QuizAnswer.module.css';

const quizAnswer = props => (
    <div className={classes.QuizAnswer}>
        {props.answer}
    </div>
);

export default quizAnswer;