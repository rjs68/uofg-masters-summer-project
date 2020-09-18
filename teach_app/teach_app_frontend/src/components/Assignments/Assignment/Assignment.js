import React, { Component } from 'react';
import { Alert } from 'react-alert';
import axios from 'axios';

import classes from './Assignment.module.css';
import Aux from '../../../hoc/Auxiliary/Auxiliary';
import Button from '../../UI/Button/Button';
import StudentSubmission from './StudentSubmission/StudentSubmission';

class Assignment extends Component{
    constructor(props) {
        super(props);
        //set specification and submission names for internal file handling
        this.state = {
            specificationUploaded: false,
            specificationName: "specification-"+this.props.assignment['unit_code']
                                +"-"+this.props.assignment['assignment_name']+".",
            submissionUploaded: false,
            submissionName: this.props.email+"-"+this.props.assignment['unit_code']
                            +"-"+this.props.assignment['assignment_name']+".",
        };

        this.getAssignmentSpecification = this.getAssignmentSpecification.bind(this);
        this.getAssignmentSpecificationName = this.getAssignmentSpecificationName.bind(this);
        this.handleSpecificationUpload = this.handleSpecificationUpload.bind(this);
        this.uploadSpecificationHandler = this.uploadSpecificationHandler.bind(this);
        this.getSubmission = this.getSubmission.bind(this);
        this.getStudentSubmissions = this.getStudentSubmissions.bind(this);
        this.handleSubmissionUpload = this.handleSubmissionUpload.bind(this);
        this.uploadSubmissionHandler = this.uploadSubmissionHandler.bind(this);
    }

    getAssignmentSpecification(){
        axios.post('/assignment-specification/', {
            unitCode: this.props.assignment['unit_code'],
            assignmentName: this.props.assignment['assignment_name']
        })
            .then((response) => {
                if(response.data === "Specification found"){
                    this.setState({specificationUploaded: true});
                    this.getAssignmentSpecificationName();
                }else if(response.data === "Specification not found"){
                    this.setState({specificationUploaded: false});
                }
            });
    }

    getAssignmentSpecificationName(){
        //get actual specification name including extension to retrieve files
        axios.post('/specification-name/', {
            unitCode: this.props.assignment['unit_code'],
            assignmentName: this.props.assignment['assignment_name']
        })
            .then((response) => {
                this.setState({specificationName: response.data});
            });
    }

    handleSpecificationUpload(event){
        //retrieve file extension
        const specification = event.target.files[0];
        const specificationNameSplit = specification.name.split('.');
        const specificationExtension = specificationNameSplit.pop();
        //add file extension to specification name
        const previousSpecificationName = this.state.specificationName.split('.');
        const specificationName = previousSpecificationName[0] + '.' + specificationExtension;
        //override file 'name' property to make it writable
        Object.defineProperty(specification, 'name', {
            writable: true,
            value: specificationName
        })
        this.setState({specification: specification});
    }

    uploadSpecificationHandler() {
        /* 
            Code to send files in POST request obtained from
            https://www.geeksforgeeks.org/file-uploading-in-react-js/
        */
        const formData = new FormData(); 
        //add file and filename to form data
        formData.append( 
            "specification", 
            this.state.specification, 
            this.state.specification.name 
        ); 
        axios.post('/upload-specification/', formData)
            .then((response) => {
                if(response.data === "Upload Successful"){
                    alert("The specification has been uploaded!")
                }else{
                    alert("Something went wrong... please try again")
                }
            });
    }

    getSubmission(){
        axios.post('/submission/', {
            userEmail: this.props.email,
            unitCode: this.props.assignment['unit_code'],
            assignmentName: this.props.assignment['assignment_name']
        })
            .then((response) => {
                if(response.data === "Submission not found"){
                    this.setState({submissionUploaded: false});
                }else{
                    this.setState({
                        submissionUploaded: true,
                        submissionData: response.data
                    });
                } 
            });
    }

    getSubmissionName(){
        //get actual submission name including extension to retrieve files
        axios.post('/submission-name/', {
            userEmail: this.props.email,
            unitCode: this.props.assignment['unit_code'],
            assignmentName: this.props.assignment['assignment_name']
        })
            .then((response) => {
                this.setState({submissionName: response.data});
            });
    }

    getStudentSubmissions(){
        axios.post('/student-submissions/', {
            unitCode: this.props.assignment['unit_code'],
            assignmentName: this.props.assignment['assignment_name']
        })
            .then((response) => {
                this.setState({studentSubmissions: response.data});
            });
    }

    handleSubmissionUpload(event){
        //retrieve file extension
        const submission = event.target.files[0];
        const submissionNameSplit = submission.name.split('.');
        const submissionExtension = submissionNameSplit.pop();
        //add file extension to specification name
        const submissionName = this.props.email+"-"+this.props.assignment['unit_code']+"-"
                                +this.props.assignment['assignment_name']+"."+ submissionExtension;
        //override file 'name' property to make it writable
        Object.defineProperty(submission, 'name', {
            writable: true,
            value: submissionName
        })
        this.setState({
            submission: submission,
            submissionName: submissionName
        });
    }

    uploadSubmissionHandler() {
        const formData = new FormData(); 
        //add file and filename to form data
        formData.append( 
            "submission", 
            this.state.submission, 
            this.state.submission.name 
        ); 
        axios.post('/upload-submission/', formData)
            .then((response) => {
                if(response.data==="Upload Successful"){
                    alert("Your submission has been uploaded!")
                }else{
                    alert("Something went wrong... please try again")
                }
                //make requests to get new submission and update screen
                this.getSubmission();
                this.getSubmissionName();
            });
    }

    componentDidMount() {
        this.getAssignmentSpecification();
        if(this.props.userType === "student"){
            this.getSubmission();
            this.getSubmissionName();
        }else{
            //user is teacher so retrieve all student submissions
            this.getStudentSubmissions();
        }
    }

    render() {
        var specification = [];
        //logic to determine display depending on a specification being available
        if(this.state.specificationUploaded){
            const specificationPath = "/media/assignments/" + this.state.specificationName + "/";
            specification.push(<a  key='download' href={specificationPath} download> Download Specification </a>);
            if(this.props.userType === "teacher"){
                specification.push(<div key='edit specification'>
                                        <input onChange={this.handleSpecificationUpload}
                                                type="file" 
                                                name={this.state.specificationName} />
                                        <Button clicked={this.uploadSpecificationHandler}>Edit Specification</Button>
                                    </div>)
            }
        }else if(this.props.userType === "teacher") { 
            specification.push(<div key='upload specification'>
                                    <p>Upload the specification here</p>
                                    <input onChange={this.handleSpecificationUpload}
                                            type="file" 
                                            name={this.state.specificationName} />
                                    <Button clicked={this.uploadSpecificationHandler}>Upload Assignment</Button>
                                </div>)
        }else{
            specification.push(<p key='no specification'>
                                    We couldn't find the specification. 
                                    Please check that your lecturer has uploaded it.
                                </p>)
        }

        var submission;
        //logic to determine display of assignment submissions depending on available data
        if(this.props.userType === "student"){
            if(this.state.submissionUploaded){
                const submissionName = this.state.submissionName.replace('@', '').replace(' ', '_');
                const submissionPath = "media/submissions/" + submissionName + "/";
                submission = <Aux>
                                <a href={submissionPath} download> Download Submission </a>
                                <p>You can change your submission here</p>
                                <input onChange={this.handleSubmissionUpload}
                                        type="file" 
                                        name={this.state.submissionName} />
                                <Button clicked={this.uploadSubmissionHandler}>Edit Submission</Button>
                                <p>Grade: {this.state.submissionData['grade']}</p>
                                <p>Feedback: {this.state.submissionData['feedback']}</p>
                            </Aux>;
            }else if(this.state.specificationUploaded){
                submission = <Aux>
                                <p>Upload your submission here</p>
                                <input onChange={this.handleSubmissionUpload}
                                        type="file" 
                                        name={this.state.submissionName} />
                                <Button clicked={this.uploadSubmissionHandler}>Upload Submission</Button>
                            </Aux>;
            }
        }else{
            if(this.state.studentSubmissions){
                submission = [];
                for(const studentSubmission in this.state.studentSubmissions){
                    const studentEmail = this.state.studentSubmissions[studentSubmission]['user'];
                    const submissionName = this.state.studentSubmissions[studentSubmission]['submission_name'];
                    const submissionPath = "media/submissions/" + submissionName + "/";
                    var grade = this.state.studentSubmissions[studentSubmission]['grade'];
                    if(grade === null){
                        grade = "N/A";
                    };
                    submission.push(<StudentSubmission key={studentSubmission}
                                                        submissionPath={submissionPath}
                                                        studentEmail={studentEmail}
                                                        grade={grade}
                                                        feedback={this.state.studentSubmissions[studentSubmission]['feedback']}
                                                        assignment={this.props.assignment}
                                                        submissionTime={this.state.studentSubmissions[studentSubmission]['submission_time']}
                                                        getStudentSubmissions={this.getStudentSubmissions}/>)
                }
            }
        }

        return (
            <div className={classes.Assignment}>
                <h1>{this.props.assignment['unit']} - {this.props.assignment['assignment_name']}</h1>
                <div className={classes.SpecificationDiv}>
                    {specification}
                </div>
                <br />
                {submission}
            </div>
        )
    }
}

export default Assignment;