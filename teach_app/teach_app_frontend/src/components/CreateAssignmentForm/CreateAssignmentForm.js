import React, { Component } from 'react';
import axios from 'axios';

import DropdownButton from 'react-bootstrap/DropdownButton';
import Dropdown from 'react-bootstrap/Dropdown';
import TextField from '@material-ui/core/TextField';
import Button from '../UI/Button/Button';

class CreateAssignmentForm extends Component {
    constructor(props) {
        super(props);
        this.state = {};

        this.handleInputChange = this.handleInputChange.bind(this);
        this.getUnits = this.getUnits.bind(this);
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
              this.setState({units: response.data});
          });
    }

    createAssignmentHandler() {
        console.log("Create Assignment");
        // axios.post('/create-unit/', {
        //     unitCode: this.state.unitCode,
        //     unitName: this.state.unitName,
        //     teacher: this.props.email,
        //     unitEnrolmentKey: this.state.unitEnrolmentKey,
        //     numberOfCredits: this.state.numberOfCredits
        //   })
        //   .then((response) => {
        //     console.log(response);
        //   }, (error) => {
        //     console.log(error);
        //   });
    }

    componentDidMount(){
        this.getUnits();
    }

    render() {
        var units = []
        if(this.state.units !== {}){
            for(const unit in this.state.units){
                units.push(<Dropdown.Item as="button">{this.state.units[unit]['unit_name']}</Dropdown.Item>);
            }
        }

        return (
            <div>
                <DropdownButton id="unitSelector" title="Unit">
                    {units}
                </DropdownButton>
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
                                type="file" 
                                name="specification" />
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