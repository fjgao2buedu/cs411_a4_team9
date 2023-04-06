import { useState } from "react";
import "./App.css";
import { Grid, Typography } from "@mui/material";
import SearchBar from "./components/SearchBar";
import RecordTable from "./components/RecordTable";

function App() {
  const [content, setContent] = useState([]);
  const callback = (content) => {
    setContent(content);
  };
  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      <Grid container spacing={2} style={{ padding: "1rem" }}>
        <Grid xs={12} container alignItems="center" justifyContent="center">
          <Typography variant="h2" gutterBottom>
            Muvie Prototype
          </Typography>
        </Grid>
        <Grid xs={12} md={4}>
          <Typography variant="h4" gutterBottom>
            Search
          </Typography>
          <div style={{ width: "100%" }}>
            <SearchBar parentCallback={callback}></SearchBar>
          </div>
        </Grid>
        <Grid xs={12} md={8}>
          <Typography variant="h4" gutterBottom>
            Results
          </Typography>
          <div style={{ height: 600, width: "100%" }}>
            <RecordTable data={content} />
          </div>
        </Grid>
      </Grid>
    </div>
  );
}

export default App;
