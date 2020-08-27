import React, { Component } from 'react';

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
            <div>
                <video autoPlay={true} controls></video>
            </div>
        )
    }
}

export default LectureVideo;