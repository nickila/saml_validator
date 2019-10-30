import React from "react";
import "../index.css";

function AssertionCard(props) {

    if (props.res.assertion_attributes) {
        let link = props.res.assertion_attributes.errors_found.link;
        let description = props.res.assertion_attributes.description;
        let keyArr = [];
        let values = props.res.assertion_attributes.value;
        for (let key in values) {
            if(values.hasOwnProperty(key)) {
                keyArr.push(key)
            }
        }
         const assertKeys = keyArr.map((key) =>
            <li>{key} : {values[key]}</li>
        );

        if (props.res.assertion_attributes.errors_found) {
            let errors = props.res.assertion_attributes.errors_found;
            let errorArr = [];
            for (let key in errors) {
                if (errors.hasOwnProperty(key)) {
                    errorArr.push(key)
                }
            }
            const assertErrors = errorArr.map((key) =>
                <li>{errors[key]}</li>
            )

            return (
            <div className="card error-card">
                <div className="card-body">
                    <h5 className="card-title error-title">Assertion Attributes</h5>
                    <p className="card-text">{description}</p>
                    <p className="card-text">{assertKeys}</p>
                    <p className="card-text">{assertErrors}</p>
                    <a href={link} className="card-link">{link}</a>
                </div>
            </div>
        );
        }

        return (
            <div className="card">
                <div className="card-body">
                    <h5 className="card-title">Assertion Attributes</h5>
                    <p className="card-text">{description}</p>
                    <p className="card-text">{assertKeys}</p>
                    <a href={link} className="card-link">{link}</a>
                </div>
            </div>
        );
    } else {
        return(
            <div>

            </div>
        )
    }



}

export default AssertionCard;