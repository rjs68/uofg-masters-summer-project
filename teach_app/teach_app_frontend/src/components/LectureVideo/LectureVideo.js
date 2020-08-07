import React, { Component } from 'react';

class LectureVideo extends Component {
    constructor(props){
        super(props);
        this.state = {
            constraints : {
                'video': true,
                'audio': true
            }
        }
    }

    render() {
        navigator.mediaDevices.getUserMedia(this.state.constraints)
            .then(stream => {
                console.log('Got MediaStream:', stream);
            })
            .catch(error => {
                console.error('Error accessing media devices.', error);
            });
            
        return (
            <div>Video</div>
        );
    }
}

export default LectureVideo;