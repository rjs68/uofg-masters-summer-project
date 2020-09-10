import React from 'react';

import classes from './LectureBox.module.css';

const lectureBox = (props) => {
    const lectureDate = new Date(props.lecture['lecture_time']);
    const currentDate = new Date();
    var timeDifference = (lectureDate - currentDate)/1000/60;
    const lectureStarted = timeDifference<=0 && timeDifference>=-120;
    const lecturePassed = timeDifference<=-120;
    var lectureDateDisplay;
    if(lecturePassed){
        lectureDateDisplay = "This lecture has finshed";
    }else if(lectureStarted){
        lectureDateDisplay = "This lecture has already started";
    }else{
        var lectureMinutes = lectureDate.getMinutes();
        if(lectureMinutes<10){
            lectureMinutes = '0' + lectureMinutes;
        }
        if(timeDifference>=60*24){
            timeDifference=(timeDifference/60)/24;
            lectureDateDisplay = lectureDate.toDateString() + " - " + lectureDate.getHours() + ":" 
                                + lectureMinutes + " (" + timeDifference + " days to go)";
        }else if(timeDifference>=60){
            timeDifference=timeDifference/60;
            lectureDateDisplay = "Today at " + lectureDate.getHours() + ":" + lectureMinutes
                                + lectureMinutes + " (" + timeDifference + " hours to go";
        }else{
            lectureDateDisplay = "Today at " + lectureDate.getHours() + ":" + lectureMinutes
                                + lectureMinutes + " (" + timeDifference + " minutes to go";
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