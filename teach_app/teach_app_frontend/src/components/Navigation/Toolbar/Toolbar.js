import React from 'react';

import classes from './Toolbar.module.css';
import Logo from '../../UI/Logo/Logo';
import NavigationItems from './NavigationItems/NavigationItems';

const toolbar = (props) => (
    //creates a toolbar to be display across the top of the page
    <header className={classes.Toolbar}>
        <div className={classes.Logo}>
            <Logo navigation={props.navigation} />
        </div>
        <NavigationItems navigation={props.navigation}/>
    </header>
);

export default toolbar;