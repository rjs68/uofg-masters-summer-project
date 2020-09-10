import React, { Component } from 'react';
import axios from 'axios';

import LectureBox from './LectureBox/LectureBox';
import Lecture from './Lecture/Lecture';
import CreateLectureForm from '../../../components/CreateLectureForm/CreateLectureForm';
import classes from '../PageContent.module.css';
import Aux from '../../../hoc/Auxiliary/Auxiliary';
import Modal from '../../../components/UI/Modal/Modal';
import Button from '../../../components/UI/Button/Button';

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
                window.location.reload(false);
            }else{
                console.log(error);
            } 
          });
    }

    handleChangeStatus() {
        if(this.state.createLectureHandling === true){
            this.setState({createLectureHandling: false});
            this.getLectures();
        }else{
            this.setState({createLectureHandling: true});
        }
    }

    selectLectureHandler(index){
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
        if(this.props.userType === "teacher"){
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

        var pageContent;
        if(this.state.lectureSelected){
            pageContent = <Lecture lecture={this.state.selectedLecture['lecture_name']} 
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

        return (
            <div className={classes.PageContent}>
                {form}
                {pageContent}
            </div>
        );
    }
};

export default Lectures;