import React from 'react';

import classes from './Backdrop.module.css';

const backdrop = props => {
    /*
    creates a clickable backdrop component that darkens the background to highlight 
    components in the foreground
    */
    if(props.show){
        return (
            <div className={classes.Backdrop} onClick={props.clicked}></div>
        )
    }
    return null;
};

export default backdrop;