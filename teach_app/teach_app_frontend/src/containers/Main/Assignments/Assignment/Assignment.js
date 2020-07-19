import React from 'react';

import classes from './Assignment.module.css';

const assignment = (props) => (
    <div className={classes.Assignment}>
        {props.assignment['assignment_name']}
    </div>
)

export default assignment;