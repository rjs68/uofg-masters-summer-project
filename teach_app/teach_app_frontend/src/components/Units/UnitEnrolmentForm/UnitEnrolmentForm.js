import React, { Component } from 'react';
import axios from 'axios';

import Button from '../../UI/Button/Button';
import classes from './UnitEnrolmentForm.module.css';

class UnitEnrolmentForm extends Component {
    constructor(props) {
        super(props);
        this.state = {};

        this.handleInputChange = this.handleInputChange.bind(this);
        this.unitEnrolmentHandler = this.unitEnrolmentHandler.bind(this);
    }
    
    handleInputChange(event) {
        this.setState({[event.target.name]: event.target.value});
    }

    unitEnrolmentHandler() {
        axios.post('/unit-enrol/', {
            unitCode: this.state.unitCode,
            unitEnrolmentKey: this.state.unitEnrolmentKey,
            email: this.props.email
          })
          .then((response) => {
            console.log(response);
            this.props.handleChangeStatus();
          }, (error) => {
            console.log(error);
          });
    }

    render() {
        //input fields that allow a student to enrol in a unit
        return (
            <div className={classes.UnitEnrolmentForm}>
                <input onChange={this.handleInputChange}
                                type="text" 
                                name="unitCode" 
                                placeholder="Unit Code" />
                <input onChange={this.handleInputChange}
                                type="text" 
                                name="unitEnrolmentKey" 
                                placeholder="Unit Enrolment Key" />
                <Button clicked={this.unitEnrolmentHandler}>Enrol</Button>
            </div>
        );
    }
}

export default UnitEnrolmentForm;