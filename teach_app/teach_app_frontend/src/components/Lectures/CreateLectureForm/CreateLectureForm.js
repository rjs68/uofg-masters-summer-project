import React, { Component } from 'react';
import axios from 'axios';

import {Dropdown} from 'reactjs-dropdown-component';
import TextField from '@material-ui/core/TextField';
import Button from '../../UI/Button/Button';
import classes from './CreateLectureForm.module.css';

class CreateLectureForm extends Component {
    constructor(props) {
        super(props);
        this.state = {};

        axios.defaults.headers.post['X-CSRFToken'] = this.props.cookies.get('csrftoken');

        this.handleInputChange = this.handleInputChange.bind(this);
        this.getUnits = this.getUnits.bind(this);
        this.resetThenSet = this.resetThenSet.bind(this);
        this.createLectureHandler = this.createLectureHandler.bind(this);
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
              //map units to objects in form required for Dropdown menu
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
        //deselects all units then selects new unit
        const temp = JSON.parse(JSON.stringify(this.state.units));
        temp.forEach(item => item.selected = false);
        temp[id].selected = true;
        this.setState({
          units: temp,
          unit: temp[id]['unit']
        });
    }

    createLectureHandler() {
        axios.post("/create-lecture/", {
            unitCode: this.state.unit['unit_code'],
            lectureName: this.state.lectureName,
            time: this.state.time
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
            /*
                Dropdown menu component obtained from 
                //https://github.com/dbilgili/Custom-ReactJS-Dropdown-Components
            */
            unitDropdown = <Dropdown searchable={["Search for Unit", "No matching unit"]}
                                        title="Select Unit"
                                        list={this.state.units}
                                        resetThenSet={this.resetThenSet}
                                        />
        }

        //editable input fields for teacher to set lecture information
        return (
            <div className={classes.CreateLectureForm}>
                {unitDropdown}
                <input onChange={this.handleInputChange}
                                type="text" 
                                name="lectureName" 
                                placeholder="Lecture Name" />
                <TextField onChange={this.handleInputChange}
                                type="datetime-local"
                                name="time" 
                                label="Lecture Time"
                                defaultValue="2020-12-31T00:00" 
                                InputLabelProps={{
                                    shrink: true,
                                  }} />
                <Button clicked={this.createLectureHandler}>Create</Button>
            </div>
        )
    }
}

export default CreateLectureForm;