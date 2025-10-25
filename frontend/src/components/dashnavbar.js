import React from "react";
import { Navbar, Container, Nav } from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'; 
import '../styles/dashnavbar.css'; 

export default function DashNav(){
    return (
        <div className="dash-navigation-container">
            <Navbar className="dash-nav-body flex-column align-items-start">
                <Navbar.Brand href="/" className="dash-nav-brand mb-4">Phisherman</Navbar.Brand>
                <br />
                <br />
                <Nav className="flex-column w-100" style={{flex: 1}}>
                    <Nav.Link className="dash-nav-link" href="/admin">Dashboard</Nav.Link>
                    <Nav.Link className="dash-nav-link" href="/campaign">Campaigns</Nav.Link>
                    <Nav.Link className="dash-nav-link" href="/organization">Your Organization</Nav.Link>
                    <div style={{flex: 1}}></div>
                    <Nav.Link className="dash-nav-link mt-auto" href="/">Logout</Nav.Link>
                </Nav>
            </Navbar>
        </div>
    )
}