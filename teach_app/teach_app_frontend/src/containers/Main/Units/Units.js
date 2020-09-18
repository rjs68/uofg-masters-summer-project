import React, {Component} from 'react';

import classes from '../PageContent.module.css';
import axios from 'axios';
import Unit from '../../../components/Units/Unit/Unit';
import Button from '../../../components/UI/Button/Button';
import Modal from '../../../components/UI/Modal/Modal';
import Backdrop from '../../../components/UI/Backdrop/Backdrop';
import CreateUnitForm from '../../../components/Units/CreateUnitForm/CreateUnitForm';
import UnitEnrolmentForm from '../../../components/Units/UnitEnrolmentForm/UnitEnrolmentForm';

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
          }, (error) => {
            if(error.response.status===403){
                //reloads window to update csrf token
                window.location.reload(false);
            }else{
                console.log(error);
            } 
          });
    }

    //determines if unit form should be displayed
    handleChangeStatus() {
        if(this.state.unitChangeHandling === true){
            this.setState({unitChangeHandling: false});
            this.getUnits();
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

        //teacher form creates unit and student form enrols in a unit
        if(this.props.userType === "teacher"){
            button = "Create Unit";
            form = <CreateUnitForm email={this.props.email} />;
        }else{
            button = "Enrol in a Unit";
            form = <UnitEnrolmentForm email={this.props.email} 
                                        handleChangeStatus={this.handleChangeStatus} />;
        }

        //creates a list of available units
        var units = []
        if(this.state.units !== {}){
            for(const unit in this.state.units){
                units.push(<Unit key={this.state.units[unit]['unit_code']} unit={this.state.units[unit]} />);
            }
        }

        //determines if backdrop should be shown
        var showBackdrop = false;
        var backdropClicked;
        if(this.state.unitChangeHandling){
            showBackdrop = true;
            backdropClicked = this.handleChangeStatus;
        };

        return (
            <div className={classes.PageContent}>
                <Backdrop show={showBackdrop} clicked={backdropClicked}/>
                <Modal show={this.state.unitChangeHandling}>{form}</Modal>
                <div>
                    <Button clicked={this.handleChangeStatus}>{button}</Button>
                </div>
                {units}
            </div>
        )
    }
} 

export default Units;