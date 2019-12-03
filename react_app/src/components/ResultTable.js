import React, { Component } from "react";
import "../index.css";
import Modal from "./Modal";
import {Col, Row, Table} from "react-bootstrap";

class ResultTable extends Component {
    render() {
        if (this.props.res) {
            console.log(this.props);
            let jsonData = this.props.res;
            let assertionValues = "";
            let jsonArr = [];
            let shortCert;
            let cert;
            let helpx;
        console.log(jsonData)
            for (let attribute in jsonData) {
                if (jsonData.hasOwnProperty(attribute) && attribute === "helpx") {
                    helpx = jsonData[attribute].helpx

                }
                if (jsonData.hasOwnProperty(attribute) && attribute === "assertion_attributes") {
                    for (let keys in jsonData[attribute].value) {
                        if (jsonData[attribute].value.hasOwnProperty(keys))
                            assertionValues += keys + " : " + jsonData[attribute].value[keys] + "\n";
                    }
                jsonData[attribute].value = assertionValues;
                }
                if (jsonData.hasOwnProperty(attribute) && attribute === "signing_cert") {
                    cert = jsonData[attribute].value;
                    shortCert = cert.slice(0, 100);
                    shortCert += "... ";
                    jsonData[attribute].value = shortCert;
                    jsonData[attribute].extraValue = "full value";
                    
                }
                if (jsonData.hasOwnProperty(attribute)) {
                    jsonData[attribute].name = attribute;
                    jsonArr.push(jsonData[attribute]);
                }
            }
            let timeSent = jsonArr[jsonArr.length-1];
            jsonArr.splice(8, 0, timeSent);
            jsonArr.pop();
            return (
                    <Row className="justify-content-md-center">
                        <Col md={10}>
                        <Table className="table-bordered">
                            <thead>
                            <tr>
                                <th scope="col" className={"attribute-header"}>Attribute</th>
                                <th scope="col" className={"value-header"}>Value</th>
                                <th scope="col" className={"description-header"}>Description</th>
                            </tr>
                            </thead>
                            <tbody>
                            {jsonArr.map(key =>
                                {
                                    return "errors_found" in key ?
                                        <tr className="error-row">
                                            <td className="error"><b>{key.name}</b></td>
                                            <td className="error">{key.value}</td>
                                            <td className="error">ERROR: {key.errors_found.description}
                                                {/*<p className="error-hint">({key.errors_found.hint})</p>*/}
                                                <p><a href={key.helpx + key.errors_found.link} className="error-link" target="_blank">{key.errors_found.hint}</a></p>
                                            </td>
                                        </tr>
                                            :
                                        <tr>
                                            <td><b>{key.name}</b></td>
                                            <td className="value">{key.value}<span data-toggle="modal" data-target="#fullValue" className="full-value-link">{key.extraValue}</span></td>
                                            <td className={"description"}>{key.description}</td>
                                        </tr>
                                }
                            )}
                            </tbody>
                        </Table>
                    </Col>
                    <Modal 
                        cert={cert}
                        id="fullValue"
                        name="signing_cert"
                    />
                </Row>
            )
        } else {
            return null;

        }
    }
}

export default ResultTable;