import React from "react";
import "../index.css";

function Table(props) {
    if(props.res.assertion_attributes) {
        let jsonData = props.res;
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
        // Splice out the signing cert and add it back into the array to get it to the end.
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
                                <tr>
                                    <td><b>{key.name}</b></td>
                                    <td className="error-value">{key.value}</td>
                                    <td className={"description"}>{key.description}</td>
                                    <td className="error-description">
                                        {key.errors_found.description}
                                        <p className={"error-hint"}>({key.errors_found.hint})</p>
                                        <p><a href={key.errors_found.link} className="error-link">{key.errors_found.link}</a></p>
                                    </td>
                                </tr>
                                    :
                                <tr>
                                    <td><b>{key.name}</b></td>
                                    <td className="value">{key.value}</td>
                                    <td className={"description"}>{key.description}</td>
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

export default Table;