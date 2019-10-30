import React, { Component } from 'react';
import "../index.css";
import axios from "axios";
import Table from "../components/Table";
import MappedCard from "../components/MappedCard";
import DestinationCard from "./DestinationCard";
import AssertionCard from "./AssertionCard";

class Form extends Component {

    state = {
        saml_file: null,
        idp_name: "",
        data: [],
        // description: ""
    }

    handleInputChange = event => {
        const { name, value } = event.target;
        this.setState({
            [name]: value
        });
    }

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
            if (res.data) {
                // res.data[0] =
                this.setState({data: res.data})

                // console.log("ARR BELOW")
                // console.log(arr)
                // Object.entries(this.state.data).map(([key, value]) =>{
                //     return(
                //     <div>{key} : {value}</div>
                //     )
                // })
            }
        }, (err)=> {
            console.log(err)
        })
    }

    render() {
        let keyArr = [];
        let errorArr = [];
        let jsonData = this.state.data;

        for (let key in jsonData) {
            if (jsonData.hasOwnProperty(key) && key !== "assertion_attributes" && !("errors_found" in jsonData[key])) {
                keyArr.push(key);
            } else if (jsonData.hasOwnProperty(key) && key !== "assertion_attributes" && ("errors_found" in jsonData[key])) {
                errorArr.push(key);
            }
        }
        const mappedKeys = keyArr.map((key) =>
            <div className="card">
                <div className="card-body">
                    <h5 className="card-title">{key}</h5>
                    <p className="card-text">{jsonData[key].description}</p>
                    <p className="card-text">{jsonData[key].value}</p>
                </div>
            </div>
        );
        const errorKeys = errorArr.map((key) =>
            <div className="card error-card">
                <div className="card-body">
                    <h5 className="card-title error-title">{key}</h5>
                    <p className="card-text">{jsonData[key].description}</p>
                    <p className="card-text">{jsonData[key].value}</p>
                    <p className="card-text">{jsonData[key].errors_found.description}</p>
                    <p className="card-text">{jsonData[key].errors_found.hint}</p>
                    <a href={jsonData[key].errors_found.link} className="card-text">{jsonData[key].errors_found.link}</a>
                </div>
            </div>
        );


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
                        <AssertionCard res={this.state.data} />
                        {/*<MappedCard res={this.state.data}/>*/}
                        <li>{errorKeys}</li>
                        <li>{mappedKeys}</li>

                        {/*<li>{arr.map(item => <MappedCard description={item.description} value={item.value} />)}</li>*/}
                        {/*<table className="table borderless results-table col-9 mx-auto">{arr.map(item => <Table key={item.label} description={item.description} value={item.value} />)}</table>*/}
                    </div>
                </form>
            </div>
        )
    }
}

export default Form;