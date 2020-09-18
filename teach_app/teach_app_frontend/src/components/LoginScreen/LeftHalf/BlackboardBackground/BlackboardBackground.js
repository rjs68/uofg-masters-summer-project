import React from 'react';

import blackboard from '../../../../../static/frontend/blackboard.jpg';
import classes from './BlackboardBackground.module.css';

const background = props => (
    <div className={classes.BlackboardBackground}>
        <img src={blackboard} alt="Blackboard filling background" />
    </div>
)

export default background;