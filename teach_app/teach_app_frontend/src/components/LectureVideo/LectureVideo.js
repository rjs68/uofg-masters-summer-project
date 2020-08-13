import React, { Component } from 'react';

class LectureVideo extends Component {
    constructor(props){
        super(props);
        this.state = {
            configuration: {'iceServers': [{'urls': 'stun:eu-turn3.xirsys.com'}]}
        }

        this.getLocalVideoStream = this.getLocalVideoStream.bind(this);
        this.getRemoteMediaStream = this.getRemoteMediaStream.bind(this);
        this.handleConnection = this.handleConnection.bind(this);
        this.getOtherPeer = this.getOtherPeer.bind(this);
        this.getPeerName = this.getPeerName.bind(this);
        this.getPeerConnections = this.getPeerConnections.bind(this);
        this.createdOffer = this.createdOffer.bind(this);
        this.createdAnswer = this.createdAnswer.bind(this);
    }

    getLocalVideoStream() {
        const constraints = { audio: true, video: true };
        navigator.mediaDevices.getUserMedia(constraints)
            .then(stream => {
                this.setState({
                    localStream: stream
                })
                console.log('Got MediaStream:', stream);
                const video = document.getElementById('localVideo');
                video.srcObject = stream;
                video.onloadedmetadata = () => {
                    video.play();
                };
                this.getPeerConnections();
            })
            .catch(error => {
                console.error('Error accessing media devices.', error);
            });
    }

    //https://github.com/googlecodelabs/webrtc-web/blob/master/step-02/js/main.js
    getRemoteMediaStream(event) {
        const remoteStream = event.stream;
        this.setState({
            remoteStream: remoteStream
        })
        const video = document.getElementById('remoteVideo');
        video.srcObject = remoteStream;
    }

    handleConnection(event) {
        const peerConnection = event.target;
        const iceCandidate = event.candidate;
      
        if (iceCandidate) {
          const newIceCandidate = new RTCIceCandidate(iceCandidate);
          const otherPeer = this.getOtherPeer(peerConnection);
      
          otherPeer.addIceCandidate(newIceCandidate)
            .then(() => {
                console.log(`${this.getPeerName(peerConnection)} addIceCandidate success.`);
            }).catch((error) => {
                console.log(`${this.getPeerName(peerConnection)} failed to add ICE Candidate:\n`+
                    `${error.toString()}.`);
            });
      
          console.log(`${getPeerName(peerConnection)} ICE candidate:\n` +
                `${event.candidate.candidate}.`);
        }
    }

    getOtherPeer(peerConnection) {
        return (peerConnection === this.state.localPeerConnection) ?
            this.state.remotePeerConnection : this.state.localPeerConnection;
    }

    getPeerName(peerConnection) {
        return (peerConnection === this.state.localPeerConnection) ?
            'localPeerConnection' : 'remotePeerConnection';
    }

    createdOffer(description){
        console.log("Offer:" + description);
        const localPeerConnection = this.state.localPeerConnection;
        localPeerConnection.setLocalDescription(description);
        const remotePeerConnection = this.state.remotePeerConnection;
        remotePeerConnection.setRemoteDescription(description);
        remotePeerConnection.createAnswer()
            .then(this.createdAnswer);
    }

    createdAnswer(description){
        console.log("Answer:" + description);
        const remotePeerConnection = this.state.remotePeerConnection;
        remotePeerConnection.setLocalDescription(description);
        const localPeerConnection = this.state.localPeerConnection;
        localPeerConnection.setRemoteDescription(description);
    }

    getPeerConnections() {
        const localPeerConnection = new RTCPeerConnection(this.state.configuration);
        localPeerConnection.addEventListener('icecandidate', this.handleConnection);
        localPeerConnection.addStream(this.state.localStream);
        console.log(localPeerConnection);

        const remotePeerConnection = new RTCPeerConnection(this.state.configuration);
        remotePeerConnection.addEventListener('icecandidate', this.handleConnection);
        remotePeerConnection.addEventListener('addstream', this.getRemoteMediaStream);
        console.log(remotePeerConnection);

        this.setState({
            localPeerConnection: localPeerConnection,
            remotePeerConnection: remotePeerConnection
        });

        const offerOptions = {
            offerToReceiveAudio: true,
            offerToReceiveVideo: true
        }
        localPeerConnection.createOffer(offerOptions)
            .then(this.createdOffer);
    }


    componentDidMount(){
        this.getLocalVideoStream();
    }

    render() {
        return (
            <div>
                <video autoPlay={true} id="localVideo" controls></video>
                <video autoPlay={true} id="remoteVideo" controls></video>
            </div>
        )
    }
}

export default LectureVideo;