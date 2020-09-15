import React from 'react';

import NextLectureBox from './NextLectureBox/NextLectureBox';
import NextAssignmentBox from './NextAssignmentBox/NextAssignmentBox';
import classes from '../PageContent.module.css';

const home = props => (
    <div className={classes.PageContent}>
        <NextLectureBox email={props.email}
                        cookies={props.cookies}/>
        <NextAssignmentBox email={props.email}
                            cookies={props.cookies}/>
    </div>
)

export default home;