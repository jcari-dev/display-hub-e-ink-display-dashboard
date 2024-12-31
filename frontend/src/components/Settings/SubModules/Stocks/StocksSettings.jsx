
import { useState } from "react";
import "./StocksSettings.css"

const StocksSettings = () =>{
    const handleSaveStocksSettings = () => {
        console.log("Yup Saved the weather settings.");
    };

    const [ticker, setTicker] = useState("");

    return (
        <div>
            <button
                onClick={handleSaveStocksSettings}
                style={{ height: "18.67px", lineHeight: "0px" }}
            >
                Test Stocks API
            </button>
            <br />
            Current Ticker: {ticker}
            <br />
            <label htmlFor="ticker-input">Enter a Ticker Symbol: </label>
            <input
                type="text"
                id="ticker-input"
            />
            <br />
            <button
                onClick={handleSaveStocksSettings}
                style={{ height: "18.67px", lineHeight: "0px", marginTop: "15px" }}
            >
                Save Stocks Settings
            </button>
        </div>
    );
}   

export default StocksSettings;