import React, { Component } from 'react';

import classes from './LectureVideo.module.css';

class LectureVideo extends Component {
    componentDidMount() {
        const video = document.querySelector('video');
        video.srcObject = this.props.lectureStream;
        video.onloadedmetadata = () => {
            video.play();
        };
    }

    render() {
        return (
            <div className={classes.LectureVideo}>
                <video autoPlay={true} controls></video>
            </div>
        )
    }
}

export default LectureVideo;