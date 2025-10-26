import React, {useState} from 'react'
import { Navbar, Container, Nav} from "react-bootstrap"
import 'bootstrap/dist/css/bootstrap.min.css'
import {Link} from 'react-scroll'
import '../styles/navbar.css'

export default function Navigation() {
    return(
        <div className="navigation">
            <Navbar collapseOnSelect expand='lg' className='nav-background'>
                <Container fluid>
                    <Navbar.Brand href='/' className='nav-logo'>Phisherman</Navbar.Brand>
                    <Navbar.Toggle className='toggler' aria-controls='responsive-navbar-nav'></Navbar.Toggle>
                    <Navbar.Collapse id='responsive-navbar-nav'>
                        <Nav className='ms-auto'>
                            <Nav.Link href='/login' className='navi'>Login</Nav.Link>
                            <Nav.Link href='/register' className='navi'>Register</Nav.Link>
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
        </div>
    )
}
