import React, { useState } from "react";
import FadeInOut from "../../components/FadeInOut/FadeInOut";
import "./Report.css";

const Report = () => {
  const [show] = useState(true);
  return (
    <div className="Report__container">
      <FadeInOut show={show} duration={600}>
        <h1 className="Report__title">학대의심신고</h1>
        <p className="Report__law">
          누구든지 아동학대범죄를 알게 된 경우나 그 의심이 있는 경우에는
          특별시·광역시·특별자치시·도·특별자치도, 시·군·구 또는 수사기관에
          신고할 수 있습니다(「아동학대범죄의 처벌 등에 관한 특례법」
          제10조제1항).
        </p>
      </FadeInOut>
    </div>
  );
};
export default Report;
