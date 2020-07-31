import React from 'react';

import classes from './StudentSubmission.module.css';

const studentSubmission = props => (
    <div className={classes.StudentSubmission}>
        <div className={classes.Email}>{props.studentEmail}</div>
        <a href={props.submissionPath} download>Download Submission</a>
        <div className={classes.Grade}>{props.grade}</div>
    </div>
)

export default studentSubmission;