import React, { useEffect, useState } from "react";
import { fetchPing, PingResponse } from "./services/api";

const App: React.FC = () =>{
  const [data, setData] = useState<PingResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

    useEffect(() =>{
      const loadPing = async() =>{
        try{
          const response = await fetchPing();
          setData(response);
        } catch (err){
          setError("Failed to fetch data.");
          console.error(err)
        } finally {
          setLoading(false)
        }
      }
      loadPing();
    }, [])

    if (loading) return <h1>Loading...</h1>
    if (error) return <h1>Error: {error}</h1>

    return (
      <div>
        <h1>{data?.message || "No message available"}</h1>
        <p>Timestamp: {data?.timestamp}</p>
      </div>
    )
}

export default App;