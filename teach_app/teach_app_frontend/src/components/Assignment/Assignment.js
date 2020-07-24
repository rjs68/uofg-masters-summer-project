import React, { Component } from 'react';
import axios from 'axios';

class Assignment extends Component{
    constructor(props) {
        super(props);

        this.getAssignmentSpecification = this.getAssignmentSpecification.bind(this);
    }

    getAssignmentSpecification(){
        axios.post('/assignment-specification/', {
            unitCode: this.props.assignment['unit_code'],
            assignmentName: this.props.assignment['assignment_name']
        })
            .then((response) => {
                console.log(response);
            });
    }

    componentDidMount() {
        this.getAssignmentSpecification();
    }

    render() {
        return (
            <div>
                <h1>{this.props.assignment['unit']} - {this.props.assignment['assignment_name']}</h1>
            </div>
        )
    }
}

export default Assignment;