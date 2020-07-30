import React from 'react';

const studentSubmission = props => (
    <div>
        <a href={props.submissionPath} download>{props.studentEmail}</a>
        <p>{props.grade}</p>
        <p>{props.feedback}</p>
    </div>
)

export default studentSubmission;