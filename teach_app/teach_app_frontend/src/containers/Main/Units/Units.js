import React, {Component} from 'react';

import classes from '../PageContent.module.css';
import axios from 'axios';
import Unit from './Unit/Unit';

class Units extends Component {
    constructor(props) {
        super(props);
        this.state = {
          units: {}
        };
    }

    getUnits() {
        axios.post('/units/', {
            email: this.props.email,
          })
          .then((response) => {
              this.setState({units: response.data});
          });
    }

    componentDidMount(){
        this.getUnits();
    }

    render() {
        var units = []
        if(this.state.units !== {}){
            for(const unit in this.state.units){
                units.push(<Unit key={this.state.units[unit]['unit_code']} unit={this.state.units[unit]} />)
            }
        }
        return (
            <div className={classes.PageContent}>
                {units}
            </div>
        )
    }
} 

export default Units;