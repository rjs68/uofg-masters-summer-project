import React, { Component } from 'react';
import axios from 'axios';

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
        return (
            <div>
                Lectures
            </div>
        );
    }
};

export default Lectures;