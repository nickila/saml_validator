import React, { Component } from "react";
import "../index.css";

class Table extends Component {
    render() {
        if(this.props.res.assertion_attributes) {
            let jsonData = this.props.res;
            let assertionValues = "";
            let jsonArr = [];

            for (let attribute in jsonData) {
                if (jsonData.hasOwnProperty(attribute) && attribute === "assertion_attributes") {
                    for (let keys in jsonData[attribute].value) {
                        if (jsonData[attribute].value.hasOwnProperty(keys))
                            assertionValues += keys + " : " + jsonData[attribute].value[keys] + "\n";
                    }
                jsonData[attribute].value = assertionValues;
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
                <div className={'container'}>
                    <div className={"row"}>
                        <table className={"table-bordered"}>
                            <thead>
                            <tr>
                                <th scope="col" className={"attribute-header"}>Attribute</th>
                                <th scope="col" className={"value-header"}>Value</th>
                                <th scope="col" className={"description-header"}>Description</th>
                                <th scope="col" className={"error-header"}>Error Message</th>
                            </tr>
                            </thead>
                            <tbody>
                            {jsonArr.map(key =>
                                {return "errors_found" in key ?
                                    <tr className="error-row">
                                        <td className="error"><b>{key.name}</b></td>
                                        <td className="error">{key.value}</td>
                                        <td className="error">{key.description}</td>
                                        <td className="error">
                                            {key.errors_found.description}
                                            <p className="error-hint">({key.errors_found.hint})</p>
                                            <p><a href={key.errors_found.link} className="error-link">{key.errors_found.link}</a></p>
                                        </td>
                                    </tr>
                                        :
                                    <tr>
                                        <td><b>{key.name}</b></td>
                                        <td className="value">{key.value}</td>
                                        <td className={"description"}>{key.description}</td>
                                        <td> </td>
                                    </tr>
                                }
                            )}
                            </tbody>
                        </table>
                    </div>
                </div>
            )
        } else {
            return(
                <div></div>
            )
        }
    }
}

export default Table;