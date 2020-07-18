import React from 'react';

import classes from './Unit.module.css';

const unit = (props) => (
    <div className={classes.Unit}>
        {props.unit['unit_name']}
    </div>
)

export default unit;