import React from 'react';

import blackboard from '../../../assets/images/blackboard.jpg';
import classes from './BlackboardBackground.css';

const background = props => (
    <div className={classes.BlackboardBackground}>
        <img src={blackboard} alt="Image of blackboard filling background" />
    </div>
)

export default background;