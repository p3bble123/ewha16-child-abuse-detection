import React from "react";
import { Route } from "react-router-dom";
import "./App.css";
import NavBar from "./components/NavBar/NavBar";
import Footer from "components/Footer/Footer";
import Home from "Pages/Home/Home";
import MyPage from "Pages/MyPage/MyPage";
import Highlights from "Pages/Highlights/Highlights";
import Report from "Pages/Report/Report";

function App() {
  return (
    <div className="App__container">
      <header>
        <NavBar />
      </header>
      <Route path="/" exact={true} component={Home} />
      <Route path="/MyPage" exact={true} component={MyPage} />
      <Route path="/Highlights" exact={true} component={Highlights} />
      <Route path="/Report" exact={true} component={Report} />
      <footer>
        <Footer />
      </footer>
    </div>
  );
}

export default App;
