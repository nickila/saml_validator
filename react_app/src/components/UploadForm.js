import React, { Component } from 'react';
import "../index.css";
import Button from "./Button";
import API from "../utils/API";
import PropTypes from "prop-types";
import Select from "./Select";
import FileInput from "./FileInput";
import { Col, Form } from "react-bootstrap";

class UploadForm extends Component {
    constructor(props) {
        super(props);

        this.state = {
            saml_file: null,
            idp_name: "",
            data: [],
            file: null,
            idpOptions: ["ADFS", "Azure", "Google", "Shibboleth", "WSO2", "Okta", "Other"]
        }
        this.handleUpload = this.handleUpload.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);

    }

    handleInputChange(event) {
        const {name, value} = event.target;
        this.setState(prevState => ({
            ...prevState.idp_name, [name]: value    
        }))
    }

    handleFile(e) {
        let file = e.target.files[0];
        this.setState({file: file})
    }

    handleUpload(e) {
        e.preventDefault();
        let file = this.state.file;
        let idp_name = this.state.idp_name;
        idp_name = idp_name.toLowerCase();
        let formdata = new FormData();
        formdata.append('saml_file', file);
        formdata.append('idp_name', idp_name);
        console.log(formdata);

        API.postData(formdata)
            .then((res)=> {
                this.setState({data: res.data});
                this.props.callback(this.state.data);
        }, (err)=> {
            console.log(err)
        })
    }
 
    render() {
        return (
         
            <Form>
                <Form.Row className="justify-content-md-center">
                    <Col md={5}>
                        <FileInput
                            name="file"
                            type="file"
                            className="custom-file-input mb-5"
                            onChange={(e)=>this.handleFile(e)}
                            label={this.state.file !== null ? this.state.file.name : "Choose an XML file..."}
                        />
                    </Col>
                    <Col md={2}>
                        <Select title={"idp"}
                            name={"idp_name"}
                            options = {this.state.idpOptions}
                            value={this.state.idp_name}
                            placeholder={"Select IDP..."}
                            handleChange={this.handleInputChange}
                            className="form-control mb-2"
                        />
                    </Col>
                    <Col md={1}>
                        <Button title={"SUBMIT"}
                            action={(e)=>this.handleUpload(e)}
                            className="btn btn-warning mb-2"
                        />
                    </Col>
                </Form.Row>
            </Form>
        )
    }

    
}
Form.protoTypes = {
    callback : PropTypes.func,
}

export default UploadForm;