import React, { Component } from 'react';

class LectureVideo extends Component {
    constructor(props){
        super(props);
        this.state = {
            configuration: {'iceServers': [{'urls': 'stun:eu-turn3.xirsys.com'}]},
            ident: 'teach',
            secret: '2b07e9c8-da3b-11ea-ab22-0242ac150002',
            channel: 'Teach',
            username: this.props.userEmail
        }

        this.getToken = this.getToken.bind(this);
        this.getSocketServer = this.getSocketServer.bind(this);
        this.connectToSocket = this.connectToSocket.bind(this);
        this.onSocketMessage = this.onSocketMessage.bind(this);
        this.getIceCandidates = this.getIceCandidates.bind(this);
        this.createPeerConnection = this.createPeerConnection.bind(this);


        // this.getLocalVideoStream = this.getLocalVideoStream.bind(this);
        // this.getRemoteMediaStream = this.getRemoteMediaStream.bind(this);
        // this.handleConnection = this.handleConnection.bind(this);
        // this.getOtherPeer = this.getOtherPeer.bind(this);
        // this.getPeerName = this.getPeerName.bind(this);
        // this.getPeerConnections = this.getPeerConnections.bind(this);
        // this.createdOffer = this.createdOffer.bind(this);
        // this.createdAnswer = this.createdAnswer.bind(this);
    }

    getToken() {
        const xhr = new XMLHttpRequest();
        xhr.onreadystatechange = ($evt) => {
            if(xhr.readyState == 4 && xhr.status == 200){
                let res = JSON.parse(xhr.responseText);
                console.log("token response: ",res);
                this.setState({
                    token: res['v']
                });
                this.getSocketServer();
            }
        }
        xhr.open("PUT", "https://global.xirsys.net/_token/Teach?k="+this.state.username, true);
        xhr.setRequestHeader ("Authorization", "Basic " + btoa("teach:2b07e9c8-da3b-11ea-ab22-0242ac150002") );
        xhr.setRequestHeader ("Content-Type", "application/json");
        xhr.send();
    }

    getSocketServer() {
        const xhr = new XMLHttpRequest();
        xhr.onreadystatechange = ($evt) => {
            if(xhr.readyState == 4 && xhr.status == 200){
                let res = JSON.parse(xhr.responseText);
                console.log("server response: ",res);
                this.setState({
                    server: res['v']
                });
                this.connectToSocket();
            }
        }
        xhr.open("GET", "https://global.xirsys.net/_host/Teach?type=signal&k="+this.state.username, true);
        xhr.setRequestHeader ("Authorization", "Basic " + btoa("teach:2b07e9c8-da3b-11ea-ab22-0242ac150002") );
        xhr.setRequestHeader ("Content-Type", "application/json");
        xhr.send();
    }

    connectToSocket() {
        const serverUrl = this.state.server+"/v2/"+this.state.token;
        var ws = new WebSocket(serverUrl);
        console.log(ws);
        ws.onopen = () => {
            ws.addEventListener('message', this.onSocketMessage);
            this.setState({
                webSocket: ws
            });
            this.getIceCandidates();
        }
    }

    onSocketMessage(event) {
        const data = JSON.parse(event.data);
        switch (data.m.o) {
            case "peers":
                const users = data.p.users;
                for(var i=0; i < users.length; i++) {
                    console.log(users[i] + " is in the chat");
                }
                break;
            case "peer_connected":
                const f = data.m.f.split("/");
                const joining = f[f.length-1];
                    console.log(joining + " has joined the chat");
                break;
            case "message":
                switch(data.p.msg.type) {
                    case "offer":
                        const desc = new RTCSessionDescription(data.p.msg);
                        console.log(desc);
                        const pc = this.state.peerConnection;
                        pc.setRemoteDescription(desc);
                        this.setState({
                            peerConnection: pc
                        });
                        break;
                }
        }
    }

    getIceCandidates() {
        const xhr = new XMLHttpRequest();
        xhr.onreadystatechange = ($evt) => {
            if(xhr.readyState == 4 && xhr.status == 200){
                let res = JSON.parse(xhr.responseText);
                console.log("ice candidates: ",res);
                this.setState({
                    iceCandidates: res['v']
                });
                this.createPeerConnection();
            }
        }
        xhr.open("PUT", "https://global.xirsys.net/_turn/Teach", true);
        xhr.setRequestHeader ("Authorization", "Basic " + btoa("teach:2b07e9c8-da3b-11ea-ab22-0242ac150002"));
        xhr.setRequestHeader ("Content-Type", "application/json");
        xhr.send();
    }

    createPeerConnection(){
        const pc = new RTCPeerConnection(this.state.iceCandidates);
        this.setState({
            peerConnection: pc
        });
        pc.createOffer().then(description => this.createdOffer(description));
    }

    createdOffer(description){
        const pc = this.state.peerConnection;
        pc.setLocalDescription(description);
        this.setState({
            peerConnection: pc
        });
        var pkt = {
            t: "u",
            m: {
                f: "Teach/" + this.state.username,
                o: "message"
            },
            p: {msg:description}
            };
        this.state.webSocket.send(JSON.stringify(pkt));
    }

    // getLocalVideoStream() {
    //     const constraints = { audio: true, video: true };
    //     navigator.mediaDevices.getUserMedia(constraints)
    //         .then(stream => {
    //             this.setState({
    //                 localStream: stream
    //             })
    //             console.log('Got MediaStream:', stream);
    //             const video = document.querySelector('video');
    //             video.srcObject = stream;
    //             video.onloadedmetadata = () => {
    //                 video.play();
    //             };
    //             this.getPeerConnections();
    //         })
    //         .catch(error => {
    //             console.error('Error accessing media devices.', error);
    //         });
    // }

    // //https://github.com/googlecodelabs/webrtc-web/blob/master/step-02/js/main.js
    // getRemoteMediaStream(event) {
    //     console.log("Got remote stream");
    //     const remoteStream = event.stream;
    //     this.setState({
    //         remoteStream: remoteStream
    //     })
    //     if(this.props.userType==="student"){
    //         const video = document.getElementById('remoteVideo');
    //         video.srcObject = remoteStream;
    //     }
    // }

    // handleConnection(event) {
    //     const peerConnection = event.target;
    //     const iceCandidate = event.candidate;
      
    //     if (iceCandidate) {
    //       const newIceCandidate = new RTCIceCandidate(iceCandidate);
    //       const otherPeer = this.getOtherPeer(peerConnection);
      
    //       otherPeer.addIceCandidate(newIceCandidate)
    //         .then(() => {
    //             console.log(`${this.getPeerName(peerConnection)} addIceCandidate success.`);
    //         }).catch((error) => {
    //             console.log(`${this.getPeerName(peerConnection)} failed to add ICE Candidate:\n`+
    //                 `${error.toString()}.`);
    //         });
      
    //       console.log(`${this.getPeerName(peerConnection)} ICE candidate:\n` +
    //             `${event.candidate.candidate}.`);
    //     }
    // }

    // getOtherPeer(peerConnection) {
    //     return (peerConnection === this.state.localPeerConnection) ?
    //         this.state.remotePeerConnection : this.state.localPeerConnection;
    // }

    // getPeerName(peerConnection) {
    //     return (peerConnection === this.state.localPeerConnection) ?
    //         'localPeerConnection' : 'remotePeerConnection';
    // }

    // createdAnswer(description){
    //     console.log("Answer:" + description);
    //     const remotePeerConnection = this.state.remotePeerConnection;
    //     remotePeerConnection.setLocalDescription(description);
    //     const localPeerConnection = this.state.localPeerConnection;
    //     localPeerConnection.setRemoteDescription(description);
    // }

    // getPeerConnections() {
    //     const localPeerConnection = new RTCPeerConnection(this.state.configuration);
    //     localPeerConnection.addEventListener('icecandidate', this.handleConnection);
    //     if(this.props.userType==="teacher"){
    //         localPeerConnection.addStream(this.state.localStream);
    //     }
    //     console.log(localPeerConnection);

    //     const remotePeerConnection = new RTCPeerConnection(this.state.configuration);
    //     remotePeerConnection.addEventListener('icecandidate', this.handleConnection);
    //     remotePeerConnection.addEventListener('addstream', this.getRemoteMediaStream);
    //     console.log(remotePeerConnection);

    //     this.setState({
    //         localPeerConnection: localPeerConnection,
    //         remotePeerConnection: remotePeerConnection
    //     });

    //     const offerOptions = {
    //         offerToReceiveAudio: true,
    //         offerToReceiveVideo: true
    //     }
    //     localPeerConnection.createOffer(offerOptions)
    //         .then(this.createdOffer);
    // }


    componentDidMount(){
        // if(this.props.userType==="teacher"){
        //     this.getLocalVideoStream();
        // }else{
        //     this.getPeerConnections();
        // }
        this.getToken();
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