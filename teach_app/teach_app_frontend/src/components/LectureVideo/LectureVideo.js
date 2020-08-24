import React, { Component } from 'react';

class LectureVideo extends Component {
    constructor(props){
        super(props);
        this.state = {
            configuration: {'iceServers': [{'urls': 'stun:eu-turn3.xirsys.com'}]},
            ident: 'teach',
            secret: '2b07e9c8-da3b-11ea-ab22-0242ac150002',
            channel: 'Teach',
            username: this.props.userEmail,
            sendDisabled: true,
            peerConnections: {}
        }

        this.getToken = this.getToken.bind(this);
        this.getSocketServer = this.getSocketServer.bind(this);
        this.connectToSocket = this.connectToSocket.bind(this);
        this.onSocketMessage = this.onSocketMessage.bind(this);
        this.getIceCandidates = this.getIceCandidates.bind(this);
        this.onCreateOffer = this.onCreateOffer.bind(this);
        this.onCreateAnswer = this.onCreateAnswer.bind(this);
        this.onIceCandidate = this.onIceCandidate.bind(this);
        this.onDataChannel = this.onDataChannel.bind(this);
        this.onMessageChange = this.onMessageChange.bind(this);
        this.sendMessage = this.sendMessage.bind(this);
        this.onDataMessage = this.onDataMessage.bind(this);
        this.onDataChannelOpen = this.onDataChannelOpen.bind(this);
        this.callPeer = this.callPeer.bind(this);
        this.createNewPeerConnection = this.createNewPeerConnection.bind(this);
        this.setDataChannelHandlers = this.setDataChannelHandlers.bind(this);
        this.getUsernameByRemoteDescription = this.getUsernameByRemoteDescription.bind(this);
        this.getLocalVideoStream = this.getLocalVideoStream.bind(this);
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
        var f;
        var desc;
        var pc;
        var sender;
        switch (data.m.o) {
            case "peers":
                const users = data.p.users;
                for(var i=0; i < users.length; i++) {
                    console.log(users[i] + " is in the chat");
                }
                break;
            case "peer_connected":
                f = data.m.f.split("/");
                const joining = f[f.length-1];
                console.log(joining + " has joined the chat");
                this.callPeer(joining);
                break;
            case "message":
                switch(data.p.msg.type) {
                    case "offer":
                        desc = new RTCSessionDescription(data.p.msg);
                        f = data.m.f.split("/");
                        sender = f[f.length-1];
                        pc = this.createNewPeerConnection(sender);
                        pc.setRemoteDescription(desc);
                        pc.createAnswer().then(d => this.onCreateAnswer(d,sender));
                        break;
                    case "answer":
                        desc = new RTCSessionDescription(data.p.msg);
                        f = data.m.f.split("/");
                        sender = f[f.length-1];
                        this.state.peerConnections[sender].pc.setRemoteDescription(desc);
                        break;
                    case "candidate":
                        f = data.m.f.split("/");
                        sender = f[f.length-1];
                        console.log("candidate", sender, data, this.state.peerConnections);
                        var candidate = new RTCIceCandidate(data.p.msg);
                        this.state.peerConnections[sender].pc.addIceCandidate(candidate);
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
            }
        }
        xhr.open("PUT", "https://global.xirsys.net/_turn/Teach", true);
        xhr.setRequestHeader ("Authorization", "Basic " + btoa("teach:2b07e9c8-da3b-11ea-ab22-0242ac150002"));
        xhr.setRequestHeader ("Content-Type", "application/json");
        xhr.send();
    }

    onCreateOffer(description, peer) {
        this.state.peerConnections[peer].pc.setLocalDescription(description);
        var pkt = {
            t: "u", 
            m: {
                f: "Teach/" + this.state.username, 
                o: "message", 
                t: peer
            }, 
            p: {msg:description}};
        this.state.webSocket.send(JSON.stringify(pkt));
    }

    onCreateAnswer(description, peer) {
        this.state.peerConnections[peer].pc.setLocalDescription(description);
        var pkt = {
            t: "u", 
            m: {
                f: "Teach/" + this.state.username, 
                o: "message", 
                t: peer
            }, 
            p: {msg:description}};
        this.state.webSocket.send(JSON.stringify(pkt));
    }

    onIceCandidate(event) {
        var remoteUsername;
        if(event.target.remoteDescription){
            remoteUsername = this.getUsernameByRemoteDescription(event.target.remoteDescription.sdp);
        };
        const candidate = event.candidate;
        if (candidate != null && remoteUsername != null) {
            var cPkt = {
                type: "candidate",
                sdpMLineIndex: candidate.sdpMLineIndex,
                sdpMid: candidate.sdpMid,
                candidate: candidate.candidate
            };
            var pkt = {
                t: "u",
                m: {
                    f: "Teach/" + this.state.username,
                    o: "message",
                    t: remoteUsername
                },
                p: {msg:cPkt}
            };
            this.state.webSocket.send(JSON.stringify(pkt));
        }   
    }

    onDataChannel(event) {
        const dataChannel = event.channel;
        const keys = Object.keys(this.state.peerConnections);
        var comp;
        for(var i = 0; i < keys.length; i++) {
            comp = this.state.peerConnections[keys[i]];
            if(event.currentTarget.localDescription.sdp == comp.pc.localDescription.sdp) {
                comp.dc = dataChannel;
            }
        }
        this.setDataChannelHandlers(dataChannel);
    }

    setDataChannelHandlers(dc) {
        dc.onmessage = evt => this.onDataMessage(evt);
        dc.onopen = evt => this.onDataChannelOpen(evt);
    }       

    onMessageChange(event) {
        this.setState({
            message: event.target.value
        });
    }

    onDataChannelOpen(event) {
        this.setState({
            sendDisabled: false
        })
    }

    callPeer(peer) {
        if(peer!==this.state.username){
            var pc = this.createNewPeerConnection(peer);
            var dataChannel = pc.createDataChannel("data");
            this.state.peerConnections[peer].dc = dataChannel;
            this.setDataChannelHandlers(dataChannel);
            pc.createOffer().then(d => this.onCreateOffer(d, peer));
        };
    }
    
    sendMessage() {
        const message = this.state.message;
        console.log("You said " + message);
        const messagePacket = {
            f: this.state.username,
            msg: message
        };
        var dataChannel;
        const keys = Object.keys(this.state.peerConnections);
        var comp;
        for(var i = 0; i < keys.length; i++) {
            comp = this.state.peerConnections[keys[i]];
            dataChannel = comp.dc;
            dataChannel.send(JSON.stringify(messagePacket));
        }
    }

    onDataMessage(event) {
        const messagePacket = JSON.parse(event.data);
        console.log(messagePacket.f + " said: " + messagePacket.msg);
    }

    createNewPeerConnection(username){
        const pc = new RTCPeerConnection(this.state.iceCandidates);
        if(this.props.userType==="teacher"){
            pc.addStream(this.state.localStream);
        }else{
            pc.onaddstream = event => this.onAddStream(event);
        };
        pc.ondatachannel = event => this.onDataChannel(event);
        pc.onicecandidate = candidate => this.onIceCandidate(candidate);
        pc.oniceconnectionstatechange = event => console.log("iceconnection state ", event);
        this.state.peerConnections[username] = {pc: pc, dc: null};
        console.log("setting new peer connection: ", this.state.peerConnections);
        return pc;
    }
     
    getUsernameByRemoteDescription(sdp) {
        const keys = Object.keys(this.state.peerConnections);
        var pc;
        for(var i = 0; i < keys.length; i++) {
            pc = this.state.peerConnections[keys[i]].pc;
            if(pc.remoteDescription.sdp == sdp) {
                return keys[i];
            }
        }
        return null;
    }

    getLocalVideoStream() {
        const constraints = { audio: true, video: true };
        navigator.mediaDevices.getUserMedia(constraints)
            .then(stream => {
                this.setState({
                    localStream: stream
                })
                console.log('Got MediaStream:', stream);
                const video = document.querySelector('video');
                video.srcObject = stream;
                video.onloadedmetadata = () => {
                    video.play();
                };
            })
            .catch(error => {
                console.error('Error accessing media devices.', error);
            });
    }

    onAddStream(event) {
        const video = document.querySelector('video');
        video.srcObject = event.stream;
        console.log("Received media stream: " + event.stream);
        video.onloadedmetadata = () => {
            video.play();
        };
    }

    componentDidMount(){
        this.getToken();
        if(this.props.userType==="teacher"){
            this.getLocalVideoStream();
        };
    }

    render() {
        return (
            <div>
                {/* <button onClick={this.callPeer}>Call</button> */}
                <input onChange={this.onMessageChange}
                        type="text" 
                        name="message" 
                        placeholder="Message" />
                <button onClick={this.sendMessage}
                        disabled={this.state.sendDisabled}>Send</button>
                <video autoPlay={true} controls></video>
            </div>
        )
    }
}

export default LectureVideo;