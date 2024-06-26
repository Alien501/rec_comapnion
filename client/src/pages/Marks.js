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
  Button,
  // PaginationItem,
  // PaginationCursor,
  // Button,
  // Image,
} from "@nextui-org/react";
import { useNavigate } from "react-router-dom";
//debug
import { Audio } from "react-loader-spinner";
//

import './marks.css';
import Footer from "../components/Footer/Footer";
import Header from "../components/HeaderTop/Header";
import NavbarBottom from "../components/NavbarBottom/NavbarBottom";

function Marks() {
  // auth
  const navigate = useNavigate();
  const [token, setToken] = useState("");
  const [sempage, setSempage] = useState(1);
  const [catpage, setCatpage] = useState(0);
  const [data, setData] = useState({});

  useEffect(() => {

    if (localStorage.getItem("JWT_TOKEN") === null) {
      console.log("NOT LOGGED IN");
      navigate("/login");
    } else {
      setToken(localStorage.getItem("JWT_TOKEN"));
    }
  }, []);

  const getData = () => {
    if (token !== "") {
      if(localStorage.getItem('internal-marks') === null){
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}` 
        const url = `/api/internal-marks/`;
        axios
          .get(url, {})
          .then(function (response) {
            setData(response.data);
            localStorage.setItem('internal-marks', JSON.stringify(response.data));
          })
          .catch(function (error) {
            console.log(error);
            localStorage.clear();
            navigate("/login");
          })
          .finally(() => {
            // console.log(data[1][0]);
          });

      }
      else{
        setData(JSON.parse(localStorage.getItem('internal-marks')));
      }
    }

  }
  useEffect(getData, [token]);

  // debug
  // console.log(data);
  // voodoo magic to cache the data. Then use ?. operator to return only when the data is defined.
  // js sucks ass
  // don't ever use javascript.
  // waiting for wasm to take over tbh
  // if rust frontend was a bit more mature i would be using that instead of this react shit
  //
  // pagination just changes the `key` value
  // useing useState
  const rows = useMemo(() => {
    return data?.[sempage]?.[catpage];
  }, [data, catpage, sempage]);
  //debug

  //
  // auth ends

  //
  //
  // defines the columns in the table
  // the rows are supplied by the api backend
  const columns = [
    {
      key: "SubjName",
      label: "Subject Name",
    },
    {
      key: "Total",
      label: "Marks",
    },
  ];

  if (data[1] === undefined) {
    return <Audio className='center'/>;
  }
  const no_sems = Object.keys(data).length;
  if (rows === undefined) {
    return <h1>Loading</h1>;
  }

  function onHomeClick() {
    navigate('/home');
  }

  // console.log(data[1][0]);
  //
  return (
    <div className="bg-background text-foreground">
      <Header />
      <Table
        className="marks-table"
        radius="none"
        shadow="none"
        isStriped
        topContent={
          <div>
            <h1>Internals</h1>
            <Pagination
              showControls
              color="secondary"
              total={no_sems}
              initialPage={no_sems}
              page={sempage}
              onChange={(page) => setSempage(page)}
            />
            <h1>CAT</h1>
            <Pagination
              showControls
              color="secondary"
              total={3}
              initialPage={1}
              page={catpage + 1}
              onChange={(page) => setCatpage(page - 1)}
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
      <NavbarBottom />
    </div>
  );
}
export default Marks;
