import React, { Component } from 'react';
import axios from 'axios';

import classes from '../PageContent.module.css';
import Aux from '../../../hoc/Auxiliary/Auxiliary';
import AssignmentBox from '../../../components/Assignments/AssignmentBox/AssignmentBox';
import Assignment from '../../../components/Assignments/Assignment/Assignment';
import Button from '../../../components/UI/Button/Button';
import Modal from '../../../components/UI/Modal/Modal';
import Backdrop from '../../../components/UI/Backdrop/Backdrop';
import CreateAssignmentForm from '../../../components/Assignments/CreateAssignmentForm/CreateAssignmentForm';

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
        this.handleAssignmentSelectedStatus = this.handleAssignmentSelectedStatus.bind(this);
    }

    getAssignments() {
        axios.defaults.headers.post['X-CSRFToken'] = this.props.cookies.get('csrftoken');
        axios.post('/assignments/', {
            email: this.props.email,
          })
          .then((response) => {
              this.setState({assignments: response.data});
          }, (error) => {
            if(error.response.status===403){
                window.location.reload(false);
            }else{
                console.log(error);
            }
          });
    }

    handleChangeStatus() {
        if(this.state.createAssignmentHandling === true){
            this.setState({createAssignmentHandling: false});
            this.getAssignments();
        }else{
            this.setState({createAssignmentHandling: true});
        }
    }

    handleAssignmentSelectedStatus(index) {
        if(this.state.assignmentSelected){
            this.setState({
                assignmentSelected: false,
                selectedAssignment: null
            })
        }else{
            this.setState({
                assignmentSelected: true,
                selectedAssignment: this.state.assignments[index]
            })
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
                            <CreateAssignmentForm email={this.props.email}
                                                    closeForm={this.handleChangeStatus}
                                                    cookies={this.props.cookies} />
                        </Modal>
                        <div>
                            <Button clicked={this.handleChangeStatus}>Create Assignment</Button>
                        </div>
                    </Aux>;
        }

        var assignments = []
        if(this.state.assignments !== {}){
            var index = 0;
            for(const assignment in this.state.assignments){
                assignments.push(<AssignmentBox key={index} 
                                                index={index}
                                                assignment={this.state.assignments[assignment]} 
                                                clicked={this.handleAssignmentSelectedStatus}/>);
                index += 1;
            }
        }

        var selectedAssignment;
        if(this.state.assignmentSelected){
            selectedAssignment = <Modal show={this.state.assignmentSelected}>
                                        <Assignment assignment={this.state.selectedAssignment} 
                                                    userType={this.props.userType} 
                                                    email={this.props.email} />
                                    </Modal>
        }

        var showBackdrop = false;
        var backdropClicked;
        if(this.state.createAssignmentHandling){
            showBackdrop = true;
            backdropClicked = this.handleChangeStatus;
        }else if(this.state.assignmentSelected){
            showBackdrop = true;
            backdropClicked = this.handleAssignmentSelectedStatus;
        };

        return (
            <div className={classes.PageContent}>
                <Backdrop show={showBackdrop} clicked={backdropClicked}/>
                {form}
                {selectedAssignment}
                {assignments}
            </div>
        )
    }
} 

export default Assignments;