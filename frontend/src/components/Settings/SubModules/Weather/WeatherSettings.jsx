import { useState } from "react";
import "./WeatherSettings.css";

const WeatherSettings = () => {
  const handleSaveWeatherSettings = () => {
    console.log("Yup Saved the weather settings.");
  };

  const [zipcode, setZipcode] = useState("00000");
  const [scaleTemp, setScaleTemp] = useState("F");
  const [timezone, setTimezone] = useState("America/New_York");

  // Dynamic scale options
  const scaleOptions = [
    { value: "fahrenheit", label: "Fahrenheit" },
    { value: "celsius", label: "Celsius" },
    { value: "kelvin", label: "Kelvin 😂" },
  ];

  // Timezone options
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
        onClick={handleSaveWeatherSettings}
        style={{ height: "18.67px", lineHeight: "0px" }}
      >
        Test Weather API
      </button>
      <br />
      <div style={{ marginTop: "15px" }}>Current Zip code: {zipcode}</div>

      <div style={{ marginTop: "15px" }}>
        <label htmlFor="zipcode-input">Enter a Zip code: </label>
        <input
          type="text"
          id="zipcode-input"
          value={zipcode}
          onChange={(e) => setZipcode(e.target.value)}
          style={{ width: "70px" }}
        />
      </div>

      <div style={{ marginTop: "15px" }}>
        <label htmlFor="scale-select">Select Scale: </label>
        <select
          name="scale-select"
          id="scale-select"
          value={scaleTemp}
          onChange={(e) => setScaleTemp(e.target.value)}
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
          name="timezone-select"
          id="timezone-select"
          value={timezone}
          onChange={(e) => setTimezone(e.target.value)}
        >
          {timezones.map((zone) => (
            <option key={zone} value={zone}>
              {zone}
            </option>
          ))}
        </select>
      </div>

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
