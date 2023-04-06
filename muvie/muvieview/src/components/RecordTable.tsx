import React from "react";
import { DataGrid } from "@mui/x-data-grid";

export const RecordTable = (props: { data: any[] }) => {
  const tableColumn = [
    {
      headerName: "more columns",
      field: "not yet",
      flex: 1.5,
    }
  ];

  return <DataGrid
    aria-label="Results"
    getRowId={row => row.id}
    rows={props.data}
    columns={tableColumn}
    pagination />
};

export default RecordTable;
