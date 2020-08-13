import React, { Component } from 'react';
import axios from 'axios';

import LectureBox from './LectureBox/LectureBox';
import Lecture from './Lecture/Lecture';
import classes from '../PageContent.module.css';

class Lectures extends Component {
    constructor(props) {
        super(props);
        this.state = {
          lectures: {},
          lectureSelected: false
        };

        this.getLectures = this.getLectures.bind(this);
        this.selectLectureHandler = this.selectLectureHandler.bind(this);
    }

    getLectures() {
        axios.post('/lectures/', {
            email: this.props.email,
          })
          .then((response) => {
              this.setState({lectures: response.data});
          });
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
        var pageContent;

        if(this.state.lectureSelected){
            pageContent = <Lecture lecture={this.state.selectedLecture['lecture_name']} 
                                    userType={this.props.userType} />
        }else{
            pageContent = []
            if(this.state.lectures !== {}){
                var index = 0;
                for(const lecture in this.state.lectures){
                    pageContent.push(<LectureBox key={index}
                                                index={index} 
                                                lecture={this.state.lectures[lecture]} 
                                                clicked={this.selectLectureHandler} />);
                    index += 1;
                }
            }
        }

        return (
            <div className={classes.PageContent}>
                {pageContent}
            </div>
        );
    }
};

export default Lectures;