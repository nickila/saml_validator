import React, { Component } from 'react';
import "../index.css";
import axios from "axios";

class TestGet extends Component {

    state = {
        data: []
    };


    componentDidMount() {
        axios({
            url: "/upload",
            method: "GET"
        }).then((res)=> {
            console.log("************** DATA **************")
                // this.setState({data: res.data})
            console.log(res)
            console.log("************** DATA **************")

        }, (err)=> {
            console.log(err)
        })
    }



    render() {
        return (
                <div className={"row"}>
                    {/*<h1>{this.state.data}</h1>*/}
                </div>
        )
    }
}

export default TestGet;