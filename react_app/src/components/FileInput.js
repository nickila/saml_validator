import React from "react";

const FileInput = (props) => {
    return(
        <div className="input-group mb-3 field">
            <div className="input-group-prepend">
                <span className="input-group-text">XML</span>
            </div>
            <div className="custom-file">
                <input
                    type={props.type}
                    name={props.name}
                    className={props.className}
                    id="inputGroupFile01"
                    onChange={props.onChange}
                />
                <label className="custom-file-label" htmlFor="inputGroupFile01">{props.label}</label>
            </div>
        </div>
    )
};

export default FileInput;
