import React, { Component } from 'react';

import axios from 'axios';
import classes from './CreateUnitForm.module.css';
import Button from '../UI/Button/Button';

class CreateUnitForm extends Component {
    constructor(props) {
        super(props);
        this.state = {};

        this.handleInputChange = this.handleInputChange.bind(this);
        this.createUnitHandler = this.createUnitHandler.bind(this);
    }
    
    handleInputChange(event) {
        this.setState({[event.target.name]: event.target.value});
    }

    createUnitHandler() {
        axios.post('/create-unit/', {
            unitCode: this.state.unitCode,
            unitName: this.state.unitName,
            teacher: this.props.email,
            unitEnrolmentKey: this.state.unitEnrolmentKey,
            numberOfCredits: this.state.numberOfCredits
          })
          .then((response) => {
            console.log(response);
          }, (error) => {
            console.log(error);
          });
    }
    
    render() {
        return (
            <div className={classes.CreateUnitForm}>
                <input onChange={this.handleInputChange}
                                type="text" 
                                name="unitCode" 
                                placeholder="Unit Code" />
                <input onChange={this.handleInputChange}
                                type="text" 
                                name="unitName" 
                                placeholder="Unit Name" />
                <input onChange={this.handleInputChange}
                                type="text" 
                                name="unitEnrolmentKey" 
                                placeholder="Unit Enrolment Key" />
                <input onChange={this.handleInputChange}
                                type="text" 
                                name="numberOfCredits" 
                                placeholder="Number of Credits" />
                <Button clicked={this.createUnitHandler}>Create</Button>
            </div>
        )
    }
}

export default CreateUnitForm;