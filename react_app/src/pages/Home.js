import React, { Component } from "react";
import Form from "../components/Form"
import Title from "../components/Title";
import Table from "../components/Table";

class Home extends Component {
    constructor() {
        super();
        this.state = {
            data: ""
        }
    }

    formData(params) {
        this.setState({
            data : params
        })
    }
    render() {
        return (
            <div className={"container-fluid"}>
                <Title />
                <Form callback={this.formData.bind(this)} />
                <Table res={this.state.data} />
            </div>
        )
    }
}

export default Home