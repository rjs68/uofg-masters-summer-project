import React, {Component} from 'react';

import classes from '../PageContent.module.css';
import axios from 'axios';

class Units extends Component {
    getUnits() {
        axios.post('/units/', {
            email: this.props.email,
          })
          .then((response) => {
              console.log(response.data);
          });
    }

    componentDidMount(){
        this.getUnits();
    }

    render() {
        return (
            <div className={classes.PageContent}>
                Units
            </div>
        )
    }
} 

export default Units;