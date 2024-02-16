import { React, useEffect, useState, useMemo } from "react";
import axios from "axios";
import {
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
  getKeyValue,
  Pagination,
  SortDescriptor,
  PaginationItem,
  PaginationCursor,
  Button,
  Image,
} from "@nextui-org/react";
import { useNavigate } from "react-router-dom";
//debug
import { Audio } from "react-loader-spinner";
//

function Grade() {
  // auth
  const [token, setToken] = useState("");
  const [sempage, setSempage] = useState(1);
  const navigate = useNavigate();
  const [data, setData] = useState({});
  useEffect(() => {
    if (localStorage.getItem("JWT_TOKEN") === null) {
      console.log("NOT LOGGED IN");
      navigate("/login");
    } else {
      setToken(localStorage.getItem("JWT_TOKEN"));
      console.log("token set", token)
    }
  }, []);

  const getData = () => {
    if (token !== '') {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}` 
      const url = `/api/sem-marks/`;
      axios
        .get(url, {})
        .then(function(response) {
          setData(response.data);
          console.log("grade:", data);
        })
        .catch(function(error) {
          console.log(error);
        });
    }

  };
  useEffect(getData, [token]);

  // debug
  // console.log(data);
  const rows = useMemo(() => {
    return data?.[sempage];
  }, [data, sempage]);
  //debug

  //
  // auth ends

  //
  //
  //
  //
  //
  //
  //
  //
  //
  //
  //

  const columns = [
    {
      key: "AcademicYear",
      label: "Academic Year",
    },
    {
      key: "Subject",
      label: "Subject Name",
    },
    {
      key: "SubjCode",
      label: "Subject Code",
    },
    {
      key: "Exam_Type",
      label: "Exam/Supplementary/Arrear",
    },
    {
      key: "Grade",
      label: "Grade",
    },
  ];

  if (data[1] === undefined) {
    return <Audio />;
  }
  const no_sems = Object.keys(data).length;
  if (rows === undefined) {
    return <h1>Loading</h1>;
  }

  // console.log(data[1][0]);
  //
  return (
    <div>
      <Table
        radius="none"
        shadow="none"
        isStriped
        topContent={
          <div>
            <h1>Semester</h1>
            <Pagination
              showControls
              total={no_sems}
              initialPage={no_sems}
              page={sempage}
              onChange={(page) => setSempage(page)}
            />
          </div>
        }
      >
        <TableHeader columns={columns}>
          {(column) => (
            <TableColumn key={column.key}>{column.label}</TableColumn>
          )}
        </TableHeader>
        <TableBody items={rows}>
          {(item) => (
            <TableRow key={1}>
              {(columnKey) => (
                <TableCell>{getKeyValue(item, columnKey)}</TableCell>
              )}
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  );
}
export default Grade;
