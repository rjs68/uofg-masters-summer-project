import React from 'react';

import NextLectureBox from '../../../components/Home/NextLectureBox/NextLectureBox';
import NextAssignmentBox from '../../../components/Home/NextAssignmentBox/NextAssignmentBox';
import classes from '../PageContent.module.css';

const home = props => (
    //container for home screen displaying next lecture and assignment
    <div className={classes.PageContent}>
        <NextLectureBox email={props.email}
                        cookies={props.cookies}/>
        <NextAssignmentBox email={props.email}
                            cookies={props.cookies}/>
    </div>
)

export default home;