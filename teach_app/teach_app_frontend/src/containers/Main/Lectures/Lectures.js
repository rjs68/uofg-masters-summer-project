import React, { Component } from 'react';
import axios from 'axios';

import LectureBox from '../../../components/Lectures/LectureBox/LectureBox';
import Lecture from '../../../components/Lectures/Lecture/Lecture';
import CreateLectureForm from '../../../components/Lectures/CreateLectureForm/CreateLectureForm';
import classes from '../PageContent.module.css';
import Aux from '../../../hoc/Auxiliary/Auxiliary';
import Modal from '../../../components/UI/Modal/Modal';
import Button from '../../../components/UI/Button/Button';
import Backdrop from '../../../components/UI/Backdrop/Backdrop';

class Lectures extends Component {
    constructor(props) {
        super(props);
        this.state = {
          lectures: {},
          lectureSelected: false,
          createLectureHandling: false
        };

        this.getLectures = this.getLectures.bind(this);
        this.handleChangeStatus = this.handleChangeStatus.bind(this);
        this.selectLectureHandler = this.selectLectureHandler.bind(this);
    }

    getLectures() {
        axios.defaults.headers.post['X-CSRFToken'] = this.props.cookies.get('csrftoken');
        axios.post('/lectures/', {
            email: this.props.email,
          })
          .then((response) => {
              this.setState({lectures: response.data});
          }, (error) => {
            if(error.response.status===403){
                //reloads window to update csrf token
                window.location.reload(false);
            }else{
                console.log(error);
            } 
          });
    }

    handleChangeStatus() {
        //changes whether lecture creation form is displayed
        if(this.state.createLectureHandling === true){
            this.setState({createLectureHandling: false});
            this.getLectures();
        }else{
            this.setState({createLectureHandling: true});
        }
    }

    selectLectureHandler(index){
        //sets selected lecture
        this.setState({
            lectureSelected: true,
            selectedLecture: this.state.lectures[index]
        })
    }

    componentDidMount(){
        this.getLectures();
    }

    render() {
        var form;
        //create lecture form only available to teachers
        if(this.props.userType === "teacher" && !this.state.lectureSelected){
            form = <Aux>
                        <Modal show={this.state.createLectureHandling}>
                            <CreateLectureForm email={this.props.email}
                                                    closeForm={this.handleChangeStatus}
                                                    cookies={this.props.cookies} />
                        </Modal>
                        <div>
                            <Button clicked={this.handleChangeStatus}>Create Lecture</Button>
                        </div>
                    </Aux>;
        }

        //either displays lecture screen or list of available lectures
        var pageContent;
        if(this.state.lectureSelected){
            pageContent = <Lecture lecture={this.state.selectedLecture['lecture_name']} 
                                    lectureTime={this.state.selectedLecture['lecture_time']}
                                    unitCode={this.state.selectedLecture['unit_code']}
                                    userEmail={this.props.email}
                                    userType={this.props.userType} />
        }else{
            pageContent = []
            if(this.state.lectures !== {}){
                for(const lecture in this.state.lectures){
                    pageContent.push(<LectureBox key={lecture}
                                                index={lecture} 
                                                lecture={this.state.lectures[lecture]} 
                                                clicked={this.selectLectureHandler} />);
                }
            }
        }

        //determines if backdrop should be shown 
        var showBackdrop = false;
        var backdropClicked;
        if(this.state.createLectureHandling){
            showBackdrop = true;
            backdropClicked = this.handleChangeStatus;
        };

        return (
            <div className={classes.PageContent}>
                <Backdrop show={showBackdrop} clicked={backdropClicked}/>
                {form}
                {pageContent}
            </div>
        );
    }
};

export default Lectures;