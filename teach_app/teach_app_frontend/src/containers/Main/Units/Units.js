import React, {Component} from 'react';

import classes from '../PageContent.module.css';
import axios from 'axios';
import Unit from './Unit/Unit';
import Button from '../../../components/UI/Button/Button';
import Modal from '../../../components/UI/Modal/Modal';
import CreateUnitForm from '../../../components/CreateUnitForm/CreateUnitForm';
import UnitEnrolmentForm from '../../../components/UnitEnrolmentForm/UnitEnrolmentForm';

class Units extends Component {
    constructor(props) {
        super(props);
        this.state = {
          units: {},
          unitChangeHandling: false
        };

        this.handleChangeStatus = this.handleChangeStatus.bind(this);
    }

    getUnits() {
        axios.defaults.headers.post['X-CSRFToken'] = this.props.cookies.get('csrftoken');
        axios.post('/units/', {
            email: this.props.email,
          })
          .then((response) => {
              this.setState({units: response.data});
          });
    }

    handleChangeStatus() {
        if(this.state.unitChangeHandling === true){
            this.setState({unitChangeHandling: false});
        }else{
            this.setState({unitChangeHandling: true});
        }
    }

    componentDidMount(){
        this.getUnits();
    }

    render() {
        var button;
        var form;

        if(this.props.userType === "teacher"){
            button = "Create Unit";
            form = <CreateUnitForm email={this.props.email} />;
        }else{
            button = "Enrol in a Unit";
            form = <UnitEnrolmentForm email={this.props.email} />;
        }

        var units = []
        if(this.state.units !== {}){
            for(const unit in this.state.units){
                units.push(<Unit key={this.state.units[unit]['unit_code']} unit={this.state.units[unit]} />);
            }
        }

        return (
            <div className={classes.PageContent}>
                <Modal show={this.state.unitChangeHandling}>{form}</Modal>
                <Button clicked={this.handleChangeStatus}>{button}</Button>
                {units}
            </div>
        )
    }
} 

export default Units;