import React from 'react';

import NavigationItem from './NavigationItem/NavigationItem';
import classes from './NavigationItems.module.css';

const navigationItems = (props) => (
    <div className={classes.NavigationItems}>
        <NavigationItem clicked={() => props.navigation("units")} name="Units" />
        <NavigationItem clicked={() => props.navigation("assignments")} name="Assignments" />
        <NavigationItem clicked={() => props.navigation("grades")} name="Grades" />
    </div>
)

export default navigationItems;