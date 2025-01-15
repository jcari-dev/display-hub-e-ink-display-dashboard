import { useEffect, useState } from "react";
import "./WeatherSettings.css";

const WeatherSettings = () => {
  const [weatherSettings, setWeatherSettings] = useState({
    zipcode: "00000",
    scale: "fahrenheit",
    timezone: "Not set (GMT+0)",
  });


  const [formValues, setFormValues] = useState({
    zipcode: "00000",
    scale: "fahrenheit",
    timezone: "Not set (GMT+0)",
  });

  const [notification, setNotification] = useState({ message: "", type: "" });


  useEffect(() => {
    const loadWeatherSettings = async () => {
      try {
        const response = await fetch("http://0.0.0.0:8001/settings/get?module=weather", {
          method: "GET",
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (data) {
          setWeatherSettings(data);
          setFormValues(data);
        }
      } catch (error) {
        console.error("Error loading weather settings:", error);
      }
    };

    loadWeatherSettings();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormValues((prevValues) => ({
      ...prevValues,
      [name]: value,
    }));
  };

  const handleSaveWeatherSettings = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://0.0.0.0:8001/settings/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          module: "weather",
          settings: formValues,
        }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setWeatherSettings(formValues);
      setNotification({ message: "Settings successfully saved!", type: "success" });
    } catch (error) {
      console.error("Error saving weather settings:", error);
      setNotification({ message: "Unable to save settings!", type: "error" });
    } finally {
      setTimeout(() => setNotification({ message: "", type: "" }), 3000);
    }
  };

  const testWeatherAPI = async () => {
    try {
      const response = await fetch("http://0.0.0.0:8001/weather/test", {
        method: "GET",
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
    } catch (error) {
      console.error("Error testing Weather API:", error);
    }
  };

  const scaleOptions = [
    { value: "fahrenheit", label: "Fahrenheit" },
    { value: "celsius", label: "Celsius" },
    { value: "kelvin", label: "Kelvin 😂" },
  ];

  const timezones = [
    "America/Anchorage",
    "America/Los_Angeles",
    "America/Denver",
    "America/Chicago",
    "America/New_York",
    "America/Sao_Paulo",
    "Not set (GMT+0)",
    "GMT+0",
    "Automatically detect time zone",
    "Europe/London",
    "Europe/Berlin",
    "Europe/Moscow",
    "Africa/Cairo",
    "Asia/Bangkok",
    "Asia/Singapore",
    "Asia/Tokyo",
    "Australia/Sydney",
    "Pacific/Auckland",
  ];

  return (
    <div>

      <button
        onClick={testWeatherAPI}
        style={{ height: "18.67px", lineHeight: "0px" }}
      >
        Test Weather API
      </button>
      <br />
      <div style={{ marginTop: "15px" }}>
        Current Zip code: {weatherSettings?.zipcode || "Loading..."}
      </div>

      <div style={{ marginTop: "15px" }}>
        <label htmlFor="zipcode-input">Enter a Zip code: </label>
        <input
          type="text"
          id="zipcode-input"
          name="zipcode"
          value={formValues?.zipcode}
          onChange={handleInputChange}
          style={{ width: "70px" }}
        />
      </div>

      <div style={{ marginTop: "15px" }}>
        <label htmlFor="scale-select">Select Scale: </label>
        <select
          id="scale-select"
          name="scale"
          value={formValues?.scale}
          onChange={handleInputChange}
        >
          {scaleOptions.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>

      <div style={{ marginTop: "15px" }}>
        <label htmlFor="timezone-select">Select Timezone: </label>
        <select
          id="timezone-select"
          name="timezone"
          value={formValues?.timezone}
          onChange={handleInputChange}
        >
          {timezones.map((zone) => (
            <option key={zone} value={zone}>
              {zone}
            </option>
          ))}
        </select>
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
        onClick={handleSaveWeatherSettings}
        style={{ height: "18.67px", lineHeight: "0px", marginTop: "15px" }}
      >
        Save Weather Settings
      </button>

    </div>
  );
};

export default WeatherSettings;
