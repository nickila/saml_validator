import React from "react";
import "../index.css";

function ErrorTable(props) {
    return (
      <div className={'container'}>
          <div className={"row"}>
              <thead>
              <tr>
                <th scope="col">Attribute</th>
                <th scope="col">Value</th>
                <th scope="col">Message</th>
              </tr>
              </thead>
              <tbody>
              <tr>
                <td>{props.description}</td>
                <td>{props.hint}</td>
                <td>{props.link}</td>
              </tr>
              </tbody>
          </div>
      </div>
    );

}

export default ErrorTable;