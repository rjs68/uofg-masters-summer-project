import React, { Component } from 'react';
import axios from 'axios';

import classes from '../PageContent.module.css';
import Aux from '../../../hoc/Auxiliary/Auxiliary';
import Assignment from './Assignment/Assignment';
import Button from '../../../components/UI/Button/Button';
import Modal from '../../../components/UI/Modal/Modal';
import CreateAssignmentForm from '../../../components/CreateAssignmentForm/CreateAssignmentForm';

class Assignments extends Component {
    constructor(props) {
        super(props);
        this.state = {
          assignments: {},
          createAssignmentHandling: false
        };

        this.getAssignments = this.getAssignments.bind(this);
        this.handleChangeStatus = this.handleChangeStatus.bind(this);
    }

    getAssignments() {
        axios.post('/assignments/', {
            email: this.props.email,
          })
          .then((response) => {
              console.log(response);
              this.setState({assignments: response.data});
          });
    }

    handleChangeStatus() {
        if(this.state.createAssignmentHandling === true){
            this.setState({createAssignmentHandling: false});
        }else{
            this.setState({createAssignmentHandling: true});
        }
    }

    componentDidMount(){
        this.getAssignments();
    }

    render() {
        var form;

        if(this.props.userType === "teacher"){
            form = <Aux>
                        <Modal show={this.state.createAssignmentHandling}>
                            <CreateAssignmentForm email={this.props.email} />
                        </Modal>
                        <Button clicked={this.handleChangeStatus}>Create Assignment</Button>
                    </Aux>;
        }

        var assignments = []
        if(this.state.assignments !== {}){
            var index = 0;
            for(const assignment in this.state.assignments){
                assignments.push(<Assignment key={index} 
                                    assignment={this.state.assignments[assignment]} />);
                index += 1;
            }
        }

        return (
            <div className={classes.PageContent}>
                {form}
                {assignments}
            </div>
        )
    }
} 

export default Assignments;