import React from 'react';

import classes from './LectureBox.module.css';

const lectureBox = (props) => {
    //displays information about individual lectures

    //logic determines status of the lecture
    const lectureDate = new Date(props.lecture['lecture_time']);
    const currentDate = new Date();
    var timeDifference = (lectureDate - currentDate)/1000/60;
    //lectures assumed to have a maximum time of 2 hours
    const lectureStarted = timeDifference<=0 && timeDifference>=-120;
    const lecturePassed = timeDifference<=-120;
    var lectureDateDisplay;
    if(lecturePassed){
        lectureDateDisplay = "This lecture has finshed";
    }else if(lectureStarted){
        lectureDateDisplay = "This lecture has already started";
    }else{
        //calculates how long until the lecture starts
        var lectureMinutes = lectureDate.getMinutes();
        //ensures minutes are displayed with 2 digits
        if(lectureMinutes<10){
            lectureMinutes = '0' + lectureMinutes;
        }
        if(timeDifference>=60*24){
            timeDifference=(timeDifference/60)/24;
            lectureDateDisplay = lectureDate.toDateString() + " - " + lectureDate.getHours() + ":" 
                                + lectureMinutes + " (" + Math.round(timeDifference) + " days to go)";
        }else if(timeDifference>=60){
            timeDifference=timeDifference/60;
            lectureDateDisplay = "Today at " + lectureDate.getHours() + ":" + lectureMinutes
                                +  " (" + Math.round(timeDifference) + " hours to go)";
        }else{
            lectureDateDisplay = "Today at " + lectureDate.getHours() + ":" + lectureMinutes
                                +  " (" + Math.round(timeDifference) + " minutes to go)";
        }
    }

    return (
        <div className={classes.LectureBox} onClick={() => props.clicked(props.index)}>
            <h1>{props.lecture['unit']} - {props.lecture['lecture_name']}</h1>
            <h2>{lectureDateDisplay}</h2>
        </div>
    )
}   

export default lectureBox;