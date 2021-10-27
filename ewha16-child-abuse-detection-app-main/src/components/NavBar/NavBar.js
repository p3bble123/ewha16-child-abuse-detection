import React, { Component } from "react";
import logo from "../../assets/logo.png";
import { MenuItems } from "./MenuItems";
import "./NavBar.css";
import { Button } from "./Button";

class NavBar extends Component {
  state = { clicked: false };
  handleClick = () => {
    this.setState({ clicked: !this.state.clicked });
  };

  render() {
    return (
      <div className="NavBar_items">
        <h2 className="NavBar_title">Kidow</h2>
        <img className="NavBar_logo" alt="" src={logo} />
        <div className="NavBar_menuIcon" onClick={this.handleClick}>
          <i className={this.state.clicked ? "fas fa-times" : "fas fa-bars"} />
        </div>
        <ul
          className={this.state.clicked ? "NavBar_menu active" : "NavBar_menu"}
        >
          {MenuItems.map((item, index) => {
            return (
              <li key={index}>
                <a className={item.cName} href={item.url}>
                  {item.title}
                </a>
              </li>
            );
          })}
        </ul>
        <Button className="NavBar_Button">로그아웃</Button>
      </div>
    );
  }
}

export default NavBar;
