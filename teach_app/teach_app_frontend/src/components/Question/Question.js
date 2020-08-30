import React from 'react';

import classes from './Question.module.css';

const question = props => (
    <div className={classes.Question}>
        <h1>{props.username} asks:</h1>
        <p>{props.question}</p>
    </div>
);

export default question;