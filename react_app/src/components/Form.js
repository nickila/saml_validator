import React, { Component } from 'react';
import "../index.css";
import axios from "axios";
import MapCards from "../components/MappedCard";
import Table from "../components/Table";
class Form extends Component {

    state = {
        saml_file: null,
        idp_name: "",
        data: [],
        file: null
    };

    handleInputChange = event => {
        const { name, value } = event.target;
        this.setState({
            [name]: value
        });
    };

    handleFile(e) {
        let file = e.target.files[0];
        this.setState({file: file})
    }

    handleUpload(e) {
        let file = this.state.file;
        let idp_name = this.state.idp_name;
        let formdata = new FormData();
        formdata.append('saml_file', file);
        formdata.append('idp_name', idp_name);

        axios({
            url: "/upload",
            method: "POST",
            data: formdata
        }).then((res)=> {
            // if (res.data) {
                // res.data[0] =
                this.setState({data: res.data})
            // }
        }, (err)=> {
            // Show error
            console.log(err)
        })
    }

    render() {
        return (
                <div className={"row"}>
                    <div className={"col-md-10 mx-auto"}>
                            <form>
                                <div className="form-row">
                                    <div className="col-7">
                                        <div className="input-group mb-3 field">
                                            <div className="input-group-prepend">
                                                <span className="input-group-text">XML</span>
                                            </div>
                                            <div className="custom-file">
                                                <input
                                                    type="file"
                                                    name="file"
                                                    className="custom-file-input"
                                                    id="inputGroupFile01"
                                                    onChange={(e)=>this.handleFile(e)}
                                                />
                                                    <label className="custom-file-label" htmlFor="inputGroupFile01">{this.state.file !== null ? this.state.file.name : "Choose an XML file..."}</label>
                                            </div>
                                        </div>
                                    </div>

                                    <div className="col-3 field">
                                        <select
                                            className="form-control"
                                            name="idp_name"
                                            value={this.state.idp_name}
                                            onChange={this.handleInputChange}
                                        >
                                        <option className={"grey-text"}>Select IDP...</option>
                                        <option value="adfs">AD FS</option>
                                        <option value="azure">Azure</option>
                                        <option value="shibboleth">Shibboleth</option>
                                        <option value="google">Google</option>
                                        <option value="wso2">WSO2</option>
                                        <option value="okta">Okta</option>
                                        <option value="other">Other</option>
                                        </select>
                                    </div>
                                    <div className={"col field"}>
                                        <button type="button" className="btn btn-warning mb-2" onClick={(e)=>this.handleUpload(e)}>SUBMIT</button>
                                    </div>
                                </div>
                            </form>
                        </div>
                    <Table res={this.state.data} />
                </div>
        )
    }
}

export default Form;