import React, { Component } from 'react';
import axios from 'axios';

import classes from '../PageContent.module.css';
import Aux from '../../../hoc/Auxiliary/Auxiliary';
import AssignmentBox from './AssignmentBox/AssignmentBox';
import Assignment from '../../../components/Assignment/Assignment';
import Button from '../../../components/UI/Button/Button';
import Modal from '../../../components/UI/Modal/Modal';
import CreateAssignmentForm from '../../../components/CreateAssignmentForm/CreateAssignmentForm';

class Assignments extends Component {
    constructor(props) {
        super(props);
        this.state = {
          assignments: {},
          createAssignmentHandling: false,
          assignmentSelected: false
        };

        this.getAssignments = this.getAssignments.bind(this);
        this.handleChangeStatus = this.handleChangeStatus.bind(this);
        this.handleAssignmentSelected = this.handleAssignmentSelected.bind(this);
    }

    getAssignments() {
        axios.post('/assignments/', {
            email: this.props.email,
          })
          .then((response) => {
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

    handleAssignmentSelected(index) {
        console.log(index);
        console.log(this.state.assignments[index]);
        this.setState({
            assignmentSelected: true,
            selectedAssignment: this.state.assignments[index]
        })
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
                assignments.push(<AssignmentBox key={index} 
                                                index={index}
                                                assignment={this.state.assignments[assignment]} 
                                                clicked={this.handleAssignmentSelected}/>);
                index += 1;
            }
        }

        var selectedAssignment;
        if(this.state.assignmentSelected){
            selectedAssignment = <Modal show={this.state.assignmentSelected}>
                                        <Assignment assignment={this.state.selectedAssignment} 
                                                    userType={this.props.userType} />
                                    </Modal>
        }

        return (
            <div className={classes.PageContent}>
                {form}
                {selectedAssignment}
                {assignments}
            </div>
        )
    }
} 

export default Assignments;