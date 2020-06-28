import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TablePagination from "@material-ui/core/TablePagination";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";
import SimpleTableToolbar from "./components/simpleToolbar";
import PropTypes from "prop-types";

import {
  useTable,
  // useGroupBy,
  // useFilters,
  // useSortBy,
  // useExpanded,
  usePagination,
} from "react-table";

const useStyles = makeStyles({
  root: {
    width: "100%",
  },
  container: {
    maxHeight: 400,
  },
});

export interface Props {
  title: string;
  onClick: any;
  actionIcon: any;
  content: object[];
}

const SimpleTable = ({ title, onClick, actionIcon, content }: Props) => {
  const classes = useStyles();

  const handleChangePage = (event: any, newPage: any) => {
    gotoPage(newPage);
  };

  const handleChangeRowsPerPage = (event: any) => {
    setPageSize(Number(event.target.value));
  };

  const getKeys = (data: any) => {
    return Object.keys(data[0]);
  };

  const getHeader = (data: any) => {
    var keys = getKeys(data);
    var header = [];
    for (const name of keys) {
      header.push({ Header: name, accessor: name });
    }

    return header;
  };

  const columns = React.useMemo(() => getHeader(content), [content]);
  const data = React.useMemo(() => {
    return content;
  }, [content]);

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
    gotoPage,
    setPageSize,
    state: { pageIndex, pageSize },
  } = useTable({ columns, data }, usePagination);

  return (
    <Paper className={classes.root}>
      <SimpleTableToolbar
        actionIcon={actionIcon}
        onClick={onClick}
        title={title}
      />
      <TableContainer className={classes.container}>
        <Table aria-label="sticky table" stickyHeader {...getTableProps()}>
          <TableHead>
            {headerGroups.map((headerGroup) => (
              <TableRow {...headerGroup.getHeaderGroupProps()}>
                {headerGroup.headers.map((column) => (
                  <TableCell {...column.getHeaderProps()}>
                    {column.render("Header")}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableHead>
          <TableBody {...getTableBodyProps()}>
            {rows.map((row) => {
              prepareRow(row);
              return (
                <TableRow {...row.getRowProps()}>
                  {row.cells.map((cell) => {
                    return (
                      <TableCell {...cell.getCellProps()}>
                        {cell.render("Cell")}
                      </TableCell>
                    );
                  })}
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        component="div"
        count={rows.length}
        onChangePage={handleChangePage}
        onChangeRowsPerPage={handleChangeRowsPerPage}
        page={pageIndex}
        rowsPerPage={pageSize}
        rowsPerPageOptions={[25, 100]}
      />
    </Paper>
  );
};

SimpleTable.propTypes = {
  data: PropTypes.array.isRequired,
  onClick: PropTypes.func,
  title: PropTypes.string,
};

export default SimpleTable;
