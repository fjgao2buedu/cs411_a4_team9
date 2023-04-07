import { Input } from "@mui/material";
import React, { useEffect, useState } from "react";
import { GET_DEFAULT_HEADERS, GET_URL } from "../globals";

const SearchBar = ({ parentCallback }) => {
  const [query, setQuery] = useState<string>("");
  useEffect(() => {
    const timeout = setTimeout(() => {
      fetchQuery(query);
    }, 1000);
    return () => clearTimeout(timeout);
  }, [query]);

  const fetchQuery = async (query: string) => {
    var url = GET_URL("");
    const queryResult = await fetch(url, {
      method: "GET",
      headers: GET_DEFAULT_HEADERS(),
    })
      .then((res) => res.json())
      .then((json) => parentCallback(json));
    return queryResult;
  };

  return (
    <Input
      value={query}
      placeholder={"Search"}
      onChange={(e) => setQuery(e.target.value)}
    />
  );
};

export default SearchBar;
