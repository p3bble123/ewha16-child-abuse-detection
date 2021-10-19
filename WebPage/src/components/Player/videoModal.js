import React, { Component } from "react";
import ModalVideo from "react-modal-video";
import "./modal-video.scss";

export class videoModal extends Component {
  constructor() {
    super();
    this.state = {
      isOpen: false,
      customUrl:
        "https://midtermpresentation.s3.ap-northeast-2.amazonaws.com/midterm-demo.mp4",
    };
    this.openModal = this.openModal.bind(this);
  }

  openModal() {
    this.setState({ isOpen: true });
  }
  render() {
    return (
      <div>
        <div>
          <ModalVideo
            channel="custom"
            isOpen={this.state.isOpen}
            url={this.state.customUrl}
            onClose={() => this.setState({ isOpen: false })}
          />
          <button onClick={this.openModal}> View </button>
        </div>
      </div>
    );
  }
}

export default videoModal;
