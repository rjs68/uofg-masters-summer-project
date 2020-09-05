import React from 'react';

import classes from './QuizAnswer.module.css';

const quizAnswer = props => {
    var styleClass = classes.QuizAnswer;
    if(props.selected){
        styleClass = classes.SelectedAnswer;
    };

    return (
        <div className={styleClass}
                onClick={() => props.clicked(props.id)}>
            {props.answer}
        </div>
    )
}

export default quizAnswer;