import React, { Component } from "react";
import { Row, Col } from "react-bootstrap";

class Title extends Component{
    render() {
        return(
            <Row>
                <Col md={12}>
                    <h1 className='display-1 title'><span className="title-symbols">&lt;</span> SAML VALIDATOR <span className="title-symbols">&gt;</span></h1>
                </Col>
            </Row>
        )
    }
}

export default Title;