import React from "react";
import "../index.css";

function DestinationCard(props) {
    // console.log("Destination Card")
    // console.log(props.res.destination)
    if (props.res.destination) {
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
                        <td>{props.res.destination.description}</td>
                        <td>{props.res.destination.value}</td>
                    </tr>
                    </tbody>
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

export default DestinationCard;