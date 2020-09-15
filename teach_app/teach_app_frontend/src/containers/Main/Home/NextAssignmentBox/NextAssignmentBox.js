import React, { Component } from 'react';
import axios from 'axios';

import classes from './NextAssignmentBox.module.css';

class NextAssignmentBox extends Component {
    constructor(props){
        super(props);
        this.state = {
            nextAssignment: null
        }

        axios.defaults.headers.post['X-CSRFToken'] = this.props.cookies.get('csrftoken');

        this.getNextAssignment = this.getNextAssignment.bind(this);
    }

    getNextAssignment() {
        axios.post('/next-assignment/', {
            email: this.props.email,
        })
            .then((response) => {
                if(response.data!=="No assignment available"){
                    this.setState({nextAssignment: response.data});
                }
                }, (error) => {
                    if(error.response.status===403){
                        window.location.reload(false);
                    }else{
                        console.log(error);
                    } 
            });
    }

    componentDidMount() {
        this.getNextAssignment();
    }

    render() {
        var pageContent = <h1>No Assignments Scheduled</h1>;

        if(this.state.nextAssignment){
            const assignmentDate = new Date(this.state.nextAssignment['deadline']);
            const currentDate = new Date();
            var timeDifference = (assignmentDate - currentDate)/1000/60;
            var assignmentDateDisplay;
            var assignmentMinutes = assignmentDate.getMinutes();
            if(assignmentMinutes<10){
                assignmentMinutes = '0' + assignmentMinutes;
            }
            if(timeDifference>=60*24){
                timeDifference=(timeDifference/60)/24;
                assignmentDateDisplay = assignmentDate.toDateString() + " - " + assignmentDate.getHours() + ":" 
                                    + assignmentMinutes + " (" + Math.round(timeDifference) + " days to go)";
            }else if(timeDifference>=60){
                timeDifference=timeDifference/60;
                assignmentDateDisplay = "Today at " + assignmentDate.getHours() + ":" + assignmentMinutes
                                    +  " (" + Math.round(timeDifference) + " hours to go";
            }else{
                assignmentDateDisplay = "Today at " + assignmentDate.getHours() + ":" + assignmentMinutes
                                    +  " (" + Math.round(timeDifference) + " minutes to go";
            }
            pageContent = <div> 
                                <h1>Next Assignment</h1>
                                <h2>{this.state.nextAssignment['unit']} - {this.state.nextAssignment['assignment_name']}</h2>
                                <p>{assignmentDateDisplay}</p>
                        </div>
        }

        return(
            <div className={classes.NextAssignmentBox}>
                {pageContent}
            </div>
        )
    }
}

export default NextAssignmentBox;