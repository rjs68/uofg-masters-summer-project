import React, { Component } from 'react';
import axios from 'axios';

import classes from './Assignment.module.css';
import Aux from '../../hoc/Auxiliary/Auxiliary';
import Button from '../UI/Button/Button';

class Assignment extends Component{
    constructor(props) {
        super(props);
        this.state = {
            specificationUploaded: false,
            specificationName: "specification-"+this.props.assignment['unit_code']
                                +"-"+this.props.assignment['assignment_name']+".pdf"
        };

        this.getAssignmentSpecification = this.getAssignmentSpecification.bind(this);
        this.handleSpecificationUpload = this.handleSpecificationUpload.bind(this);
        this.uploadSpecificationHandler = this.uploadSpecificationHandler.bind(this);
    }

    getAssignmentSpecification(){
        axios.post('/assignment-specification/', {
            unitCode: this.props.assignment['unit_code'],
            assignmentName: this.props.assignment['assignment_name']
        })
            .then((response) => {
                if(response.data === "Specification found"){
                    this.setState({specificationUploaded: true});
                }else if(response.data === "Specification not found"){
                    this.setState({specificationUploaded: false});
                }
            });
    }

    handleSpecificationUpload(event){
        const specification = event.target.files[0];
        Object.defineProperty(specification, 'name', {
            writable: true,
            value: event.target.name
        })
        this.setState({specification: specification});
    }

    uploadSpecificationHandler() {
        //https://www.geeksforgeeks.org/file-uploading-in-react-js/
        const formData = new FormData(); 
        formData.append( 
            "specification", 
            this.state.specification, 
            this.state.specification.name 
        ); 
        console.log(this.state.specification.name);
        axios.post('/upload-specification/', formData);
    }

    componentDidMount() {
        this.getAssignmentSpecification();
    }

    render() {
        var specification;
        if(this.state.specificationUploaded){
            const specificationPath = "/media/assignments/" + this.state.specificationName + "/";
            specification = <a  href={specificationPath} download> Download Specification </a>;
        }else if(this.props.userType === "teacher") { 
            specification = <Aux>
                                <p>Upload the specification here</p>
                                <input onChange={this.handleSpecificationUpload}
                                        type="file" 
                                        name={this.state.specificationName} />
                                <Button clicked={this.uploadSpecificationHandler}>Upload Assignment</Button>
                            </Aux>
        }else{
            specification = <p>
                                We couldn't find the specification. 
                                Please check that your lecturer has uploaded it.
                            </p>
        }

        return (
            <div className={classes.Assignment}>
                <h1>{this.props.assignment['unit']} - {this.props.assignment['assignment_name']}</h1>
                {specification}
            </div>
        )
    }
}

export default Assignment;