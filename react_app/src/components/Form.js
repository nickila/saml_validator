import React, { Component } from 'react';
import "../index.css";
import axios from "axios"
import Table from "../components/Table";
import ErrorTable from "../components/ErrorTable";

class Form extends Component {

    state = {
        saml_file: null,
        idp_name: "",
        data: [],
        description: ""
    }

    handleInputChange = event => {
        const { name, value } = event.target;
        this.setState({
            [name]: value
        });
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

        axios({
            url: "/upload",
            method: "POST",
            data: formdata
        }).then((res)=> {
            // console.log(res)
            if (res.data) {
                // res.data[0] =
                this.setState({data: res.data})
                let jsonData = this.state.data
                for (let key in jsonData) {
                    if (jsonData.hasOwnProperty(key)) {
                        // console.log(key + " description: " + JSON.stringify(jsonData[key].description));
                        // console.log(key + " value: " + JSON.stringify(jsonData[key].value));
                        // console.log(key + " errors: " + JSON.stringify(jsonData[key]["errors_found"]))
                    }
                }
                // Object.entries(this.state.data).map(([key, value]) =>{
                //     return(
                //     <div>{key} : {value}</div>
                //     )
                // })
            }

            // this.setState({description: res.data.assertion_attributes.description})
            //     console.log(this.state.description)

        }, (err)=> {
            console.log(err)
        })

    }

    render() {

        let json = this.state.data;
        let arr = [];
        let valueArr = [];
        let errorArr = [];
        let simpleArr = [];
            Object.keys(json).forEach(function(key) {
                arr.push(json[key])

            })
            for (let i=0; i < arr.length; i++) {
                if ("errors_found" in arr[i]) {
                    Object.keys(arr[i]).forEach(function (key) {
                        errorArr.push(arr[i][key])
                        if (typeof arr[i][key] === "object") {
                            console.log(arr)
                            console.log("==========================")

                        }
                    })
                }
            }
            console.log(arr)
            console.log("==========================")
        //         if (typeof arr[i].value === "object") {
        //             console.log(arr[i])
        //             Object.keys(arr[i]).forEach(function (key) {
        //                 valueArr.push(arr[i][key])
        //                 console.log(valueArr)
        //             })
        //         } else {
        //             Object.keys(arr[i]).forEach(function (key) {
        //                 simpleArr.push(json[key])
        //             });
        //         }
        //     }
        //     console.log("arr")
        //     console.log(arr)
            // console.log("************** ERROR ARRAY **************")
            // console.log(errorArr)
            // console.log("*****************************************")
            // console.log("************** SIMPLE ARRAY **************")
            // console.log(simpleArr)
            // console.log("*****************************************")
            // console.log("************** VALUE ARRAY **************")
            // console.log(valueArr)
            // console.log("*****************************************")
            // console.log("************** ALL ARRAY **************")
            // console.log(arr)
            // console.log("*****************************************")

        // THE FOLLOWING CODE WILL GRAB ALL NESTED KEYS AND VALUES AND CONSOLE LOG THEM

        // const group = (obj, fn) => {
        //     const values = Object.values(obj)
        //     const keys = Object.keys(obj)
        //
        //     values.forEach(val =>
        //     val && typeof val === "object" ? group(val, fn) : fn(val))
        //     keys.forEach(key =>
        //     key && typeof key === "object" ? group(key, fn) : fn(key))
        // }
        //
        // const print = (val) => console.log(val)
        // console.log("+++++++++++++++++++++++++++++++++++")
        // group(this.state.data, print)
        // console.log("+++++++++++++++++++++++++++++++++++")





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
                        <table className="table borderless results-table col-9 mx-auto">{errorArr.map(item => <ErrorTable key={item.label} hint={item["hint"]} description={item.description} link={item.link} />)}</table>
                        <table className="table borderless results-table col-9 mx-auto">{arr.map(item => <Table key={item.label} description={item.description} value={item.value} />)}</table>
                    </div>
                </form>
            </div>
        )
    }
}

export default Form;