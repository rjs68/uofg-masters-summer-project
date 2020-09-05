import React, { Component } from 'react';
import axios from 'axios';

import {Dropdown} from 'reactjs-dropdown-component';
import TextField from '@material-ui/core/TextField';
import Button from '../UI/Button/Button';
import classes from './CreateAssignmentForm.module.css';

class CreateAssignmentForm extends Component {
    constructor(props) {
        super(props);
        this.state = {};

        this.handleInputChange = this.handleInputChange.bind(this);
        this.getUnits = this.getUnits.bind(this);
        this.resetThenSet = this.resetThenSet.bind(this);
        this.createAssignmentHandler = this.createAssignmentHandler.bind(this);
    }

    handleInputChange(event) {
        this.setState({[event.target.name]: event.target.value});
    }

    getUnits() {
        axios.post('/units/', {
            email: this.props.email,
          })
          .then((response) => {
              var index = 0;
              var units = response.data.map(unit => {
                  const id = index;
                  index++;
                  return {
                      id: id,
                      unit: unit,
                      title: unit['unit_name'],
                      selected: false,
                      key: 'unit'
                  }
              })
              this.setState({units: units});
          });
    }

    resetThenSet(id) {
        const temp = JSON.parse(JSON.stringify(this.state.units));
        temp.forEach(item => item.selected = false);
        temp[id].selected = true;
        this.setState({
          units: temp,
          unit: temp[id]['unit']
        });
    }

    createAssignmentHandler() {
        axios.post("/create-assignment/", {
            unitCode: this.state.unit['unit_code'],
            assignmentName: this.state.assignmentName,
            deadline: this.state.deadline,
            weight: this.state.weight
        })
          .then((response) => {
            console.log(response);
            this.props.closeForm();
          }, (error) => {
            console.log(error);
          });
    }

    componentDidMount(){
        this.getUnits();
    }

    render() {
        var unitDropdown;
        if(this.state.units){
            //https://github.com/dbilgili/Custom-ReactJS-Dropdown-Components
            unitDropdown = <Dropdown searchable={["Search for Unit", "No matching unit"]}
                                        title="Select Unit"
                                        list={this.state.units}
                                        resetThenSet={this.resetThenSet}
                                        />
        }

        return (
            <div className={classes.CreateAssignmentForm}>
                {unitDropdown}
                <input onChange={this.handleInputChange}
                                type="text" 
                                name="assignmentName" 
                                placeholder="Assignment Name" />
                <TextField onChange={this.handleInputChange}
                                type="datetime-local"
                                name="deadline" 
                                label="Deadline"
                                defaultValue="2020-12-31T00:00" 
                                InputLabelProps={{
                                    shrink: true,
                                  }} />
                <input onChange={this.handleInputChange}
                                type="number" 
                                name="weight" 
                                placeholder="Assignment Weight" />
                <Button clicked={this.createAssignmentHandler}>Create</Button>
            </div>
        )
    }
}

export default CreateAssignmentForm;