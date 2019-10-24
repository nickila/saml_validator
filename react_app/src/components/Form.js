import React, { Component } from 'react';
import "../index.css";
import axios from "axios"

class Form extends Component {

    state = {
        saml_file: null,
        idp_name: ""
    }

    handleInputChange = event => {
        const { name, value } = event.target;
        this.setState({
            [name]: value
        });
        console.log(this.state.idp_name)
    }

    handleFile(e) {
        let file = e.target.files[0]
        this.setState({file: file})
    }

    handleUpload(e) {
        let file = this.state.file
        let idp_name = this.state.idp_name
        let formdata = new FormData()
        formdata.append('saml_file', file)
        formdata.append('idp_name', idp_name)
        console.log('handleUpload')
        console.log(file)

        axios({
            url: "/upload",
            method: "POST",
            headers: {
            authorization: 'your token'
            },
            data: formdata
        }).then((res)=> {
            console.log('res')
            console.log(res)
        }, (err)=> {
            console.log(err)
        })
    }

    render() {
        return (
            <div className="container">
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
                                        <label className="custom-file-label" htmlFor="inputGroupFile01">Choose XML file...</label>

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
                            <option value="SecureAuth">SecureAuth</option>
                            <option value="adfs">AD FS</option>
                            <option value="PingFederate">PingFederate</option>
                            <option value="Other">Other</option>
                            </select>
                        </div>
                        <div className={"col field"}>
                            <button type="button" className="btn btn-warning mb-2" onClick={(e)=>this.handleUpload(e)}>SUBMIT</button>
                        </div>
                    </div>
                </form>
            </div>
        )
    }
}

export default Form;