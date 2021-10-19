import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./Home.css";
import MypageLogo from "../../assets/mypage.png";
import HighlightsLogo from "../../assets/highlights.png";
import ReportLogo from "../../assets/report.png";
import FadeInOut from "../../components/FadeInOut/FadeInOut";

const Home = () => {
  const [show] = useState(true);
  return (
    <div className="Home__container">
      <FadeInOut show={show} duration={600}>
        <h1 className="Home__title">어서오세요.</h1>
        <div className="Home__menu-buttons-row">
          <Link
            to="/MyPage"
            className="Home__menu-button"
            style={{ textDecoration: "none" }}
          >
            <div className="Home__menu-button-text">마이페이지</div>
            <img className="Home__menu-button-logo" alt="" src={MypageLogo} />
          </Link>
          <Link
            to="/Highlights"
            className="Home__menu-button"
            style={{ textDecoration: "none" }}
          >
            <div className="Home__menu-button-text">하이라이트</div>
            <img
              className="Home__menu-button-logo"
              alt=""
              src={HighlightsLogo}
            />
          </Link>
          <Link
            to="/Report"
            className="Home__menu-button"
            style={{ textDecoration: "none" }}
          >
            <div className="Home__menu-button-text">학대의심신고</div>
            <img className="Home__menu-button-logo" alt="" src={ReportLogo} />
          </Link>
        </div>
      </FadeInOut>
    </div>
  );
};

export default Home;
