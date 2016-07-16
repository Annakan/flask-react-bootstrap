import React from 'react'
import { render } from 'react-dom'

// First we import some components...
import { Router, Route, Link } from 'react-router'
import { Input, Panel, Button, Navbar, NavBrand, Nav, NavItem, NavDropdown, MenuItem } from 'react-bootstrap';


import  '../styles/app.less'

var jQuery = require('jquery');
var io = require('socket.io-client');
console.log("io.connect :" + 'http://' + document.domain + ':' + location.port)
var socket = io.connect('http://' + document.domain + ':' + location.port);
console.log("io.connected : " + 'http://' + document.domain + ':' + location.port)

var connections = [];

// Then we delete a bunch of code from App and
// add some <Link> elements...
const App = React.createClass({
    getInitialState(){
	return {stdout: []};
    },
    askForConsole(){
        console.log("ask for ping " + (new Date()).toUTCString());
        console.log("io.connect" + 'http://' + document.domain + ':' + location.port)
        socket.emit('publisher_spawn', {date: (new Date()).toUTCString});
    },
    render() {
        console.log("render");
        // socket.emit("hello", {connection_attempt: connections.length});
        socket.on('connect', function(){
            // console.log("Hello connect");
            socket.emit("hello", {connection_attempt: connections.length});
            socket.emit("zeromq");
            // console.log("Hello connect end");
        });
        socket.on('ready', function(data){
            jQuery("#recv").append("Socket.IO connected to Flask at "+ data.ready);
            console.log("READY");
        });
        socket.on('zeromq', function(response){
            // console.log("zeromq message /  response : ", response);
            var data = response.data;
            // console.log("Extracted data packet :", data);
            switch (response.topic) {
                case "in":
                    // console.log("zeromq message IN TYPE ");
                    var parts = [
                        "[from client: ", data.client_id, "]",
                        " ",
                        data.message
                    ];
                    jQuery("#zeromq-in-container").prepend(parts.join("") + "\n");
                    break;

                case "out":
                    // console.log("zeromq message OUT TYPE ");
                    var parts = [
                        "[from server: ", data.server_id, "]",
                        " ",
                        data.message
                    ];
                    jQuery("#zeromq-out-container").prepend(parts.join("") + "\n");
                    break;
                case "msg":
                    jQuery("#zeromq-default-container").append(data);
                default:
                    // console.log("zeromq message ninout");
                    jQuery("#zeromq-default-container").append(JSON.stringify(data));
            }
        });

        socket.on('shell', this.onShellReceived);
        return (
            <div className="container-fluid">
                <Navbar>
                    <NavBrand>Flask ReactJS [Got SHELL !!]</NavBrand>
                    <Nav>
                        <NavItem eventKey={1} href="#">with a hint of Socket.IO and ZeroMQ</NavItem>
                    </Nav>
                </Navbar>

                <div className="row">
                    <div className="col-md-6">
                        <Panel header="monitor in" bsStyle="success">
                            <pre id="zeromq-in-container"></pre>
                        </Panel>
                    </div>
                    <div className="col-md-6">
                        <Panel header="monitor out" bsStyle="danger">
                            <pre id="zeromq-out-container"></pre>
                        </Panel>
                    </div>
                    <div className="col-md-12">
                        <Panel header="monitor extra" bsStyle="info" >
                            <pre id="zeromq-default-container"></pre>
                            <pre id="recv">zooom</pre>
                        </Panel>
                    </div>
                </div>
            </div>
        )
    }
})

    jQuery(function(){
        render((
            <Router>
                <Route path="/" component={App}>
                </Route>
            </Router>
        ), document.getElementById('app-container'))
    })
