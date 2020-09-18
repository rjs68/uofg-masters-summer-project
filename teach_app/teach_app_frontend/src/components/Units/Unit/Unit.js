import React from 'react';

import classes from './Unit.module.css';

const unit = (props) => {
    //creates a box that displays information about a unit
    const teacherEmail = props.unit['teacher'];
    const mailToString = "mailto:" + teacherEmail;
    return(
        <div className={classes.Unit}>
            <h1>{props.unit['unit_name']}</h1>
            <div>
                <h2>Teacher:</h2>
                <a href={mailToString}>{teacherEmail}</a> 
            </div>
            
        </div>
    )
}

export default unit;