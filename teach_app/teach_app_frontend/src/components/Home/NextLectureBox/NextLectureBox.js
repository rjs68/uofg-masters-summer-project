import React, { Component } from 'react';
import axios from 'axios';

import classes from './NextLectureBox.module.css';

class NextLectureBox extends Component {
    constructor(props){
        super(props);
        this.state = {
            nextLecture: null
        }

        axios.defaults.headers.post['X-CSRFToken'] = this.props.cookies.get('csrftoken');

        this.getNextLecture = this.getNextLecture.bind(this);
    }

    getNextLecture() {
        axios.post('/next-lecture/', {
            email: this.props.email,
        })
            .then((response) => {
                    this.setState({nextLecture: response.data});
                }, (error) => {
                    if(error.response.status===403){
                        window.location.reload(false);
                    }else{
                        console.log(error);
                    } 
            });
    }

    componentDidMount() {
        this.getNextLecture();
    }

    render() {
        var pageContent = <h1>No Lectures Scheduled</h1>;

        if(this.state.nextLecture){
            const lectureDate = new Date(this.state.nextLecture['lecture_time']);
            const currentDate = new Date();
            var timeDifference = (lectureDate - currentDate)/1000/60;
            const lectureStarted = timeDifference<=0 && timeDifference>=-120;
            var lectureDateDisplay;
            if(lectureStarted){
                lectureDateDisplay = "This lecture has already started";
            }else{
                var lectureMinutes = lectureDate.getMinutes();
                if(lectureMinutes<10){
                    lectureMinutes = '0' + lectureMinutes;
                }
                if(timeDifference>=60*24){
                    timeDifference=(timeDifference/60)/24;
                    lectureDateDisplay = lectureDate.toDateString() + " - " + lectureDate.getHours() + ":" 
                                        + lectureMinutes + " (" + Math.round(timeDifference) + " days to go)";
                }else if(timeDifference>=60){
                    timeDifference=timeDifference/60;
                    lectureDateDisplay = "Today at " + lectureDate.getHours() + ":" + lectureMinutes
                                        +  " (" + Math.round(timeDifference) + " hours to go)";
                }else{
                    lectureDateDisplay = "Today at " + lectureDate.getHours() + ":" + lectureMinutes
                                        +  " (" + Math.round(timeDifference) + " minutes to go)";
                }
            }
            pageContent = <div> 
                                <h1>Next Lecture</h1>
                                <h2>{this.state.nextLecture['unit']} - {this.state.nextLecture['lecture_name']}</h2>
                                <p>{lectureDateDisplay}</p>
                        </div>
        }

        return(
            <div className={classes.NextLectureBox}>
                {pageContent}
            </div>
        )
    }
}

export default NextLectureBox;