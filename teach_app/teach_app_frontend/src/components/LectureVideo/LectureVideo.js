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
            callMade: false
        }

        this.getToken = this.getToken.bind(this);
        this.getSocketServer = this.getSocketServer.bind(this);
        this.connectToSocket = this.connectToSocket.bind(this);
        this.onSocketMessage = this.onSocketMessage.bind(this);
        this.getIceCandidates = this.getIceCandidates.bind(this);
        this.createPeerConnection = this.createPeerConnection.bind(this);
        this.createdOffer = this.createdOffer.bind(this);
        this.createdAnswer = this.createdAnswer.bind(this);
        this.onIceCandidate = this.onIceCandidate.bind(this);
        this.onDataChannel = this.onDataChannel.bind(this);
        this.onMessageChange = this.onMessageChange.bind(this);
        this.sendMessage = this.sendMessage.bind(this);
        this.onDataMessage = this.onDataMessage.bind(this);
        this.onDataChannelOpen = this.onDataChannelOpen.bind(this);
        this.callPeer = this.callPeer.bind(this);
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
                        var desc = new RTCSessionDescription(data.p.msg);
                        console.log(desc);
                        var pc = this.state.peerConnection;
                        pc.setRemoteDescription(desc);
                        pc.ondatachannel = event => this.onDataChannel(event);
                        pc.createAnswer().then(description => this.createdAnswer(description));
                        break;
                    case "answer":
                        desc = new RTCSessionDescription(data.p.msg);
                        console.log(desc);
                        pc = this.state.peerConnection;
                        pc.setRemoteDescription(desc);
                        break;
                    case "candidate":
                        console.log("You are receiving a candidate");
                        var candidate = new RTCIceCandidate(data.p.msg);
                        pc = this.state.peerConnection;
                        pc.addIceCandidate(candidate);
                            
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
        pc.onicecandidate = event => this.onIceCandidate(event);
        this.setState({
            peerConnection: pc,
        });
        // pc.createOffer().then(description => this.createdOffer(description));
    }

    createdOffer(description){
        const pc = this.state.peerConnection;
        pc.setLocalDescription(description);
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

    createdAnswer(description){
        const pc = this.state.peerConnection;
        pc.setLocalDescription(description);
        var pkt = {
            t: "u", 
            m: {
                f: "Teach/" + this.state.username, 
                o: "message", 
                t: null
            },  
            p: {msg:description}
        };
        this.state.webSocket.send(JSON.stringify(pkt));
    }

    onIceCandidate(event) {
        console.log("You are sending a candidate");
        const candidate = event.candidate;
        if (event.candidate != null) {
            var cPkt = {type: "candidate",
            sdpMLineIndex: candidate.sdpMLineIndex,
            sdpMid: candidate.sdpMid,
            candidate: candidate.candidate
        };
        const pkt = {
            t: "u",
            m: {
                f: "SampleAppChannel/" + this.state.username,
                o: 'message'
                },
            p: {msg:cPkt}
        }
        this.state.webSocket.send(JSON.stringify(pkt));
        }
    }

    onDataChannel(event) {
        const dc = event.channel;
        dc.onmessage = event => this.onDataMessage(event);
        dc.onopen = event => this.onDataChannelOpen(event);
        dc.onreadystatechange = event => console.log("Status Changed");
        this.setState({
            dataChannel: dc
        })
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

    callPeer() {
        console.log("You are calling");
        const pc = this.state.peerConnection;
        const dc = pc.createDataChannel("data"); 
        dc.onmessage = event => this.onDataMessage(event);
        dc.onopen = event => this.onDataChannelOpen(event);
        dc.onreadystatechange = event => console.log("Status Changed");
        this.setState({
            dataChannel: dc
        })
        pc.createOffer().then(d => this.createdOffer(d));
    }
    
    sendMessage() {
        const message = this.state.message;
        console.log("You said " + message);
        const messagePacket = {
            f: this.state.username,
            msg: message
        }
        const dc = this.state.dataChannel;
        dc.send(JSON.stringify(messagePacket));
    }

    onDataMessage(event) {
        const messagePacket = JSON.parse(event.data);
        console.log(messagePacket.f + " said: " + messagePacket.msg);
    }

    componentDidMount(){
        this.getToken();
    }

    render() {
        return (
            <div>
                <button onClick={this.callPeer}>Call</button>
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