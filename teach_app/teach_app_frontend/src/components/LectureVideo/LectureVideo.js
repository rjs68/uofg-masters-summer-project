import React, { Component } from 'react';

class LectureVideo extends Component {
    constructor(props){
        super(props);
        this.state = {}

        this.getVideoStream = this.getVideoStream.bind(this);
    }

    getVideoStream() {
        const constraints = { audio: true, video: true };
        navigator.mediaDevices.getUserMedia(constraints)
            .then(stream => {
                console.log('Got MediaStream:', stream);
                var video = document.querySelector('video');
                video.srcObject = stream;
                video.onloadedmetadata = () => {
                    video.play();
                };
            })
            .catch(error => {
                console.error('Error accessing media devices.', error);
            });
    }

    componentDidMount(){
        this.getVideoStream();
    }

    render() {
        return (
            <div>
                <video autoPlay={true} id='lectureVideo' controls></video>
            </div>
        )
    }
}

export default LectureVideo;