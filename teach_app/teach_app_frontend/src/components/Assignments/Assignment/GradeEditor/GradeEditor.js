import React, { Component } from 'react';
import axios from 'axios';

import Button from '../../../UI/Button/Button';

class GradeEditor extends Component {
    constructor(props){
        super(props);
        this.state = {
            grade: this.props.grade
        };

        this.handleGradeChange = this.handleGradeChange.bind(this);
        this.editGradeHandler = this.editGradeHandler.bind(this);
    };

    handleGradeChange(event) {
        this.setState({
            grade: event.target.value
        })
    }

    editGradeHandler() {
        //saves updated student grade to the database
        axios.post('/student-grade/', {
            unitCode: this.props.assignment['unit_code'],
            assignmentName: this.props.assignment['assignment_name'],
            studentEmail: this.props.studentEmail,
            grade: this.state.grade
        })
            .then((response) => {
                //retrieves new values and updates the screen
                this.setState({studentSubmissions: response.data});
                this.props.handleGradeEditorStatus();
                this.props.getStudentSubmissions();
            });
    }

    render() {
        //number input to allow teachers to update grades
        return(
            <div>
                <input onChange={this.handleGradeChange}
                                type="number" 
                                name="grade" 
                                placeholder="Grade" />
                <Button clicked={this.editGradeHandler}>Submit Grade</Button>
            </div>
        )
    };
}

export default GradeEditor;