import { useEffect, useState } from "react";
import { backendUrl } from "../../../../utils/backendUrl";
import "./StocksSettings.css";

const StocksSettings = () => {
    const [stocksSettings, setStocksSettings] = useState({
        ticker: "NFLX",
    });


    const [formValues, setFormValues] = useState({
        ticker: "NFLX",
    });

    const [notification, setNotification] = useState({ message: "", type: "" });


    useEffect(() => {
        const loadStocksSettings = async () => {
            try {
                const response = await fetch(`${backendUrl}/settings/get?module=stocks`, {
                    method: "GET",
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                if (data) {
                    setStocksSettings(data);
                    setFormValues(data);
                }
            } catch (error) {
                console.error("Error loading stocks settings:", error);
            }
        };

        loadStocksSettings();
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormValues((prevValues) => ({
            ...prevValues,
            [name]: value,
        }));
    };

    const handleSaveStocksSettings = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`${backendUrl}/settings/save`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    module: "stocks",
                    settings: formValues,
                }),
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            setStocksSettings(formValues);
            setNotification({ message: "Settings successfully saved!", type: "success" });
        } catch (error) {
            console.error("Error saving stocks settings:", error);
            setNotification({ message: "Unable to save settings!", type: "error" });
        } finally {
            setTimeout(() => setNotification({ message: "", type: "" }), 3000);
        }
    };

    const testStockAPI = async () => {
        try {
            const response = await fetch(`${backendUrl}/stocks/test`, {
                method: "GET",
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
        } catch (error) {
            console.error("Error testing Stock API:", error);
        }
    };


    return (
        <div>

            <button
                onClick={testStockAPI}
                style={{ height: "18.67px", lineHeight: "0px" }}
            >
                Test Stocks API
            </button>
            <br />
            <div style={{ marginTop: "15px" }}>
                Current Stocks code: {stocksSettings?.ticker || "Loading..."}
            </div>

            <div style={{ marginTop: "15px" }}>
                <label htmlFor="ticker-input">Enter a Ticker: </label>
                <input
                    type="text"
                    id="ticker-input"
                    name="ticker"
                    value={formValues?.ticker}
                    onChange={handleInputChange}
                    style={{ width: "70px" }}
                />
            </div>

            {notification.message && (
                <div
                    style={{
                        color: notification.type === "success" ? "green" : "red",
                        marginBottom: "15px",
                    }}
                >
                    {notification.message}
                </div>
            )}
            <br />
            <button
                onClick={handleSaveStocksSettings}
                style={{ height: "18.67px", lineHeight: "0px", marginTop: "15px" }}
            >
                Save Stock Settings
            </button>

        </div>
    );
};

export default StocksSettings;
