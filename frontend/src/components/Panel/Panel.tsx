import React, { useEffect, useState } from "react";
import "./Panel.css";
import { fetchPing, PingResponse } from "../../services/api";
import { Typography } from "@mui/material";
import Module from "../Module/Module";

const Panel: React.FC = () => {
  const [data, setData] = useState<PingResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [render, setRender] = useState<boolean>(false);

  useEffect(() => {
    const pingAttempt = async () => {
      try {
        const response = await fetchPing();
        setData(response);
        if (response.vitals.connected && response.vitals.ready) {
          setRender(true);
        }
      } catch (err) {
        setError("Failed to fetch data.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    pingAttempt();
  }, []);

  if (loading || error) {
    return (
      <div className="panel centered">
        <Typography variant="h1">
          {loading
            ? "Panel loading..."
            : `Panel Failed to Load - Error: ${error}`}
        </Typography>
      </div>
    );
  }
  if (render) {
    return (
      <div className="panel">
        <Module />
      </div>
    );
  }
};

export default Panel;
