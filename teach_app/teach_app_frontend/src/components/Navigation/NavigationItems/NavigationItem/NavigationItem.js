import React from 'react';

import classes from './NavigationItem.module.css';

const navigationItem = (props) => (
    <div onClick={props.clicked} className={classes.NavigationItem}>
        {props.name}
    </div>
)

export default navigationItem;