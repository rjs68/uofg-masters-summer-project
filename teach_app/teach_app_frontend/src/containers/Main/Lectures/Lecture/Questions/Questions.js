import React from 'react';

import Question from '../../../../../components/Question/Question';

const questions = props => {
    const questionComponents = [];
    for(const question in props.questions){
        const questionComponent = <Question key={question}
                                            username={props.questions[question].username}
                                            question={props.questions[question].question} />
        questionComponents.push(questionComponent);
    }

    return(
        <div>
            {questionComponents}
        </div>
    )
}

export default questions;