import React, { Component } from 'react';
import "../index.css";
import Button from "../components/Button";
import API from "../utils/API";
import PropTypes from "prop-types";
import Select from "../components/Select";

class Form extends Component {
    constructor(props) {
        super(props);

        this.state = {
            saml_file: null,
            idp_name: "",
            data: [],
            file: null,
            idpOptions: ["adfs", "azure", "google", "shibboleth", "wso2", "okta", "other"],
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
         
                        <form>
                            <div className="form-row justify-content-md-center">
                                <div className="col-5">
                                    <div className="input-group mb-3 field">
                                        <div className="input-group-prepend">
                                            <span className="input-group-text">XML</span>
                                        </div>
                                        <div className="custom-file">
                                            <input
                                                type="file"
                                                name="file"
                                                className="custom-file-input mb-5"
                                                id="inputGroupFile01"
                                                onChange={(e)=>this.handleFile(e)}
                                            />
                                                <label className="custom-file-label" htmlFor="inputGroupFile01">{this.state.file !== null ? this.state.file.name : "Choose an XML file..."}</label>
                                        </div>
                                    </div>
                                </div>

                                <div className="col-2 field">
                                    <Select title={"idp"}
                                       name={"idp_name"}
                                       options = {this.state.idpOptions}
                                       value={this.state.idp_name}
                                       placeholder={"Select IDP..."}
                                       handleChange={this.handleInputChange}
                                       className="form-control mb-2"
                                    />
                                </div>
                                <div className={"col-2 field"}>
                                    <Button title={"SUBMIT"}
                                        action={(e)=>this.handleUpload(e)}
                                        className="btn btn-warning mb-2"
                                    />
                                </div>
                            </div>
                        </form>
             
        )
    }

    
}
Form.protoTypes = {
    callback : PropTypes.func,
}

export default Form;