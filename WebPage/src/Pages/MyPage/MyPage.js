import React, { useState } from "react";
import FadeInOut from "../../components/FadeInOut/FadeInOut";
import "./MyPage.css";
import ProfileImage from "../../assets/profile.png";
import MypageDummy from "../../assets/mypage_dummy.png";

const MyPage = () => {
  const [show] = useState(true);
  return (
    <div className="MyPage__container">
      <FadeInOut show={show} duration={650}>
        <h1 className="MyPage__title">마이페이지</h1>
        <div className="MyPage__item-container">
          <div className="MyPage__item-column">
            {/* <img src={ProfileImage} alt="" className="MyPage__profile-image" /> */}
            <img src={MypageDummy} alt="" />
          </div>
          {/* <div className="MyPage__item-column">
            <div className="MyPage__item-row">
              <div className-="MyPage__text">유저명</div>
            </div>
            <div className="MyPage__item-row">
              <div className-="MyPage__text">유저명</div>
            </div>
            <div className="MyPage__item-row">
              <div className-="MyPage__text">유저명</div>
            </div>
          </div> */}
        </div>
      </FadeInOut>
    </div>
  );
};
export default MyPage;
