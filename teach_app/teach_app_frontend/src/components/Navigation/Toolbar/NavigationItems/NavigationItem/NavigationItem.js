import React from 'react';

import classes from './NavigationItem.module.css';

const navigationItem = (props) => (
    //creates display for a single navigation tab
    <div onClick={props.clicked} className={classes.NavigationItem}>
        {props.name}
    </div>
)

export default navigationItem;