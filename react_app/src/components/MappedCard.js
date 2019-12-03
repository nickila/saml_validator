import React from "react";
import "../index.css";

/**
 * @return {null}
 */
function MapCards(props) {
    if (props.res.assertion_attributes) {
        console.log(props.res);
        let keyArr = [];
        let errorArr = [];
        let jsonData = props.res;
        let certValue = props.res.signing_cert.value;
        let certDesc = props.res.signing_cert.description;

        for (let key in jsonData) {
            if (jsonData.hasOwnProperty(key) && key === "assertion_attributes") {
                jsonData[key].value = JSON.stringify(jsonData[key].value);
                jsonData[key].value = jsonData[key].value.replace(/,/g, ",\n");
                jsonData[key].value = jsonData[key].value.replace(/{/, "");
                jsonData[key].value = jsonData[key].value.replace(/}/, "");
            }
            if (jsonData.hasOwnProperty(key) && !("errors_found" in jsonData[key]) && key !== "signing_cert") {
                keyArr.push(key);
            } else if (jsonData.hasOwnProperty(key) && ("errors_found" in jsonData[key])) {
                errorArr.push(key);
            }
        }
        const errorKeys = errorArr.map((key) =>
            <div className="card" key={key.id}>
                <div className="card-header error-header">{key}</div>
                <div className="card-body">
                    <p className="card-text value">{jsonData[key].value}</p>
                    <p className="card-text description">{jsonData[key].description}</p>
                    <p className="card-text error-description">{jsonData[key].errors_found.description}<span
                        className={"error-hint"}> ({jsonData[key].errors_found.hint})</span>
                        <a href={jsonData[key].errors_found.link}
                           className="card-text error-link">{jsonData[key].errors_found.link}</a>
                    </p>
                </div>
            </div>
        );
        const mappedKeys = keyArr.map((key) =>
            <div className="card">
                <div className="card-header">{key}</div>
                <div className="card-body">
                    <p className="card-text value">{jsonData[key].value}</p>
                    <p className="card-text description">{jsonData[key].description}</p>
                </div>
            </div>
        );
        const certCard =
            <div className="card cert-card">
                <div className="card-header">
                    signing_cert
                </div>
                <div className="card-body">
                    <p className="card-text value">{certValue}</p>
                    <p className="card-text description">{certDesc}</p>
                </div>
            </div>;

        return (
            <div>
                <div className={"row"}>
                    {errorKeys}
                    {mappedKeys}
                </div>
                <div className={"row"}>
                    {certCard}
                </div>
            </div>
        )
    }
    return null;
}

export default MapCards;