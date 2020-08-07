import React, { Component } from 'react';
import axios from 'axios';

import LectureBox from './LectureBox/LectureBox';
import classes from '../PageContent.module.css';

class Lectures extends Component {
    constructor(props) {
        super(props);
        this.state = {
          lectures: {}
        };

        this.getLectures = this.getLectures.bind(this);
    }

    getLectures() {
        axios.post('/lectures/', {
            email: this.props.email,
          })
          .then((response) => {
              this.setState({lectures: response.data});
          });
    }

    componentDidMount(){
        this.getLectures();
    }

    render() {
        var lectures = []
        if(this.state.lectures !== {}){
            var index = 0;
            for(const lecture in this.state.lectures){
                lectures.push(<LectureBox key={index} 
                                            lecture={this.state.lectures[lecture]} />);
                index += 1;
            }
        }

        return (
            <div className={classes.PageContent}>
                {lectures}
            </div>
        );
    }
};

export default Lectures;