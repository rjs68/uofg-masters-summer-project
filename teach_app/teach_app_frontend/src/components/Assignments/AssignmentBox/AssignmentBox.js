import React from 'react';

import classes from './AssignmentBox.module.css';

const assignment = (props) => {
    //component for displaying assignments

    //logic calculates time remaining before an assignment is due
    const deadline = new Date(props.assignment['deadline']);
    const currentDate = new Date();
    var timeDifference = (deadline - currentDate)/1000/60;
    var timeUnit = " minutes"
    const isTimeLeft = timeDifference>=0;
    var earlyOrLate;
    if(!isTimeLeft){
        timeDifference = timeDifference*-1;
        earlyOrLate = " late";
    }else{
        earlyOrLate = " left";
    }
    if(timeDifference>=60*24){
        timeDifference=(timeDifference/60)/24;
        timeUnit = " days";
    }else if(timeDifference>=60){
        timeDifference=timeDifference/60;
        timeUnit = " hours";
    }

    //ensures display of minutes looks correct
    var deadlineMinutes = deadline.getMinutes();
    if(deadlineMinutes<10){
        deadlineMinutes = '0' + deadlineMinutes;
    }

    return (<div className={classes.AssignmentBox}
                onClick={() => {props.clicked(props.index)}}>
                <h1>{props.assignment['unit']} - {props.assignment['assignment_name']}</h1>
                <h2>{deadline.toDateString()} - {deadline.getHours()}:{deadlineMinutes} ({Math.round(timeDifference)} {timeUnit} {earlyOrLate})</h2>
            </div>)
}

export default assignment;