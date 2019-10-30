// import React from "react";
// import "../index.css";
//
// function MappedCard(props) {
//     if(props.res) {
//
//         let description = ""
//         let keyArr = [];
//         let jsonData = props.res
//
//         for (let key in jsonData) {
//             console.log(key);
//             if (jsonData.hasOwnProperty(key) && key !== "assertion_attributes") {
//                 console.log("KEY BELOW");
//                 console.log(key);
//                 keyArr.push(key);
//             }
//         }
//         const mappedKeys = keyArr.map((key) =>
//             <li>{key} : {jsonData[key].description} &&& {jsonData[key].value}</li>
//         );
//
//         return (
//             <div className="card error-card">
//                 <div className="card-body">
//                     <h5 className="card-title error-title">Assertion Attributes</h5>
//                     <p className="card-text">{description}</p>
//                     <p className="card-text">{mappedKeys}</p>
//                 </div>
//             </div>
//         )
//     }
// }
//
//
//
//
//
// export default MappedCard;