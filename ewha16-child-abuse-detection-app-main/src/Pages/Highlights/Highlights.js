import { React, useState } from "react";

import Table from "@material-ui/core/Table";
import { withStyles, makeStyles } from "@material-ui/styles";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableBody from "@material-ui/core/TableBody";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import Paper from "@material-ui/core/Paper";
import ModalVideo from "components/Player/videoModal";
import Player from "components/reactPlayer";

import Calendar from "components/Calendar/Calendar";
import FadeInOut from "components/FadeInOut/FadeInOut";
import thumbnail from "../../assets/video-thumbnail.png";
import "./Highlights.css";
import "components/Player/modal-video.scss";
import ReactPlayer from "react-player";

const StyledTableCell = withStyles((theme) => ({
  head: {},
  body: {
    fontSize: 14,
  },
}))(TableCell);

const StyledTableRow = withStyles((theme) => ({
  root: {
    "&:nth-of-type(odd)": {},
  },
}))(TableRow);

function createData(highlightID, date, time, thumbnail) {
  return { highlightID, time, thumbnail };
}

const useStyles = makeStyles({
  table: {
    minWidth: 700,
  },
});

const rows = [createData("1", "HH:MM:SS", "MM:SS", "thumbnail")];

function Highlights() {
  const [show] = useState(true);
  const classes = useStyles();

  return (
    <FadeInOut show={show} duration={600}>
      <div className="Highlights__container">
        <h1 className="Highlights__title">하이라이트 조회</h1>
        <div className="Highlights__item-container">
          <Calendar />
          <div className="Highlights__divider" />
          <TableContainer component={Paper}>
            <Table className={classes.table} aria-label="customized table">
              <TableHead>
                <TableRow>
                  <StyledTableCell width="100px" align="center">
                    영상번호
                  </StyledTableCell>
                  <StyledTableCell align="center">촬영시간</StyledTableCell>
                  <StyledTableCell marginRight="10px" align="right">
                    보기
                  </StyledTableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {rows.map((row) => (
                  <StyledTableRow key={row.highlightID}>
                    <StyledTableCell align="center">
                      {row.highlightID}
                    </StyledTableCell>
                    <StyledTableCell align="center">{row.time}</StyledTableCell>
                    <StyledTableCell align="right">
                      <ModalVideo />
                    </StyledTableCell>
                  </StyledTableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </div>
      </div>
    </FadeInOut>
  );
}

export default Highlights;
