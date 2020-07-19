import React, { Component } from 'react';
import axios from 'axios';

import classes from '../PageContent.module.css';
import Assignment from './Assignment/Assignment';

class Assignments extends Component {
    constructor(props) {
        super(props);
        this.state = {
          assignments: {},
        };
    }

    getAssignments() {
        axios.post('/assignments/', {
            email: this.props.email,
          })
          .then((response) => {
              console.log(response);
              this.setState({assignments: response.data});
          });
    }

    componentDidMount(){
        this.getAssignments();
    }

    render() {
        var assignments = []
        if(this.state.assignments !== {}){
            var index = 0;
            for(const assignment in this.state.assignments){
                assignments.push(<Assignment key={index} 
                                    assignment={this.state.assignments[assignment]} />);
                index += 1;
            }
        }

        return (
            <div className={classes.PageContent}>
                {assignments}
            </div>
        )
    }
} 

export default Assignments;