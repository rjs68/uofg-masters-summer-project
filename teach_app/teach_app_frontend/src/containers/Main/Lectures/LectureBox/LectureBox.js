import React from 'react';

import classes from './LectureBox.module.css';

const lectureBox = (props) => (
    <div className={classes.LectureBox}>
        {props.lecture['unit']}-{props.lecture['lecture_name']}
    </div>
)

export default lectureBox;