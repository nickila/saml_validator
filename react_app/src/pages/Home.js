import React, { Component } from "react";
import UploadForm from "../components/UploadForm"
import Title from "../components/Title";
import ResultTable from "../components/ResultTable";
import Container from "react-bootstrap/Container";

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
            <Container fluid>
                <Title />
                <UploadForm callback={this.formData.bind(this)} />
                <ResultTable res={this.state.data} />
            </Container>
        )
    }
}

export default Home