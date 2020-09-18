import React, { Component } from 'react';

class CountdownClock extends Component {
    constructor(props){
        super(props);
        this.state={
            minutes: this.props.quizLength,
            seconds: 0
        };
    }

    /*
        Methodology for countdown clock obtained from 
        https://medium.com/better-programming/building-a-simple-countdown-timer-with-react-4ca32763dda7
    */  

    componentDidMount() {
        //counts down in 1000 millisecond (1 second) intervals
        this.myInterval = setInterval(() => {
            const { seconds, minutes } = this.state;

            if (seconds > 0) {
                this.setState(({ seconds }) => ({
                    seconds: seconds - 1
                }))
            }
            if (seconds === 0) {
                if (minutes === 0) {
                    clearInterval(this.myInterval);
                    this.props.quizTimeUp();
                } else {
                    this.setState(({ minutes }) => ({
                        minutes: minutes - 1,
                        seconds: 59
                    }));
                };
            }; 
        }, 1000);
    }

    render(){
        //displays time remaining
        const {minutes, seconds} = this.state;

        return (
            <div>
                { minutes }:{ seconds < 10 ? `0${ seconds }` : seconds }
            </div>
        );
    }
}

export default CountdownClock;