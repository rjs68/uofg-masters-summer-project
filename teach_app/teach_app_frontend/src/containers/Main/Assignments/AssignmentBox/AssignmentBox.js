import React from 'react';

import classes from './AssignmentBox.module.css';

const assignment = (props) => (
    <div className={classes.AssignmentBox}
            onClick={() => {props.clicked(props.index)}}>
        {props.assignment['assignment_name']}
    </div>
)

export default assignment;