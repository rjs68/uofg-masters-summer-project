import React from 'react';

import NextLectureBox from './NextLectureBox/NextLectureBox';
import classes from '../PageContent.module.css';

const home = props => (
    <div className={classes.PageContent}>
        <NextLectureBox email={props.email}
                        cookies={props.cookies}/>
    </div>
)

export default home;