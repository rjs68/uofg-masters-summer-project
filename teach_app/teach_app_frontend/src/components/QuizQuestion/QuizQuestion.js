import React, { Component } from 'react';

class QuizQuestion extends Component {
    constructor(props){
        super(props);
    }

    render() {
        return (
            <div>
                {this.props.question}
                {this.props.answers}
            </div>
        )
    }
}

export default QuizQuestion;