import React from 'react';

import classes from './Button.module.css';

const button = (props) => (
    //creates a custom button component for improved styling
    <button
        className={classes.Button}
        onClick={props.clicked}>{props.children}</button>
);

export default button;