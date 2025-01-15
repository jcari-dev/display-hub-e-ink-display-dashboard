import { DndContext, rectIntersection } from "@dnd-kit/core";
import React, { useState } from "react";

import Draggable from "./components/Draggable/Draggable";
import DroppableCell from "./components/DroppableCell/DroppableCell";
import Grid from "./components/Grid/Grid";

import Settings from "./components/Settings/Settings";
import validatePosition from "./utils/validatePosition";

import "./App.css";

const GRID_ROWS = 2;
const GRID_COLS = 4;
const POSITION_MAP = {
  "0,0": 1,
  "0,1": 2,
  "0,2": 3,
  "0,3": 4,
  "1,0": 5,
  "1,1": 6,
  "1,2": 7,
  "1,3": 8,
};

const getPositionKey = (position) => POSITION_MAP[position.join(",")] || null;

const App = () => {
  const [components, setComponents] = useState([]);
  const [newModuleValue, setNewModuleValue] = useState("Weather::1x1");
  const [settingsData, setSettingsData] = useState("None");
  const [warning, setWarning] = useState("");
  const [modulesOnDisplay, setModulesOnDisplay] = useState([]);

  const refreshValues = [10, 15, 20, 30, 60, 90, 120];
  const defaultIndex = refreshValues.indexOf(15);
  const [refreshRate, setRefreshRate] = useState(refreshValues[defaultIndex]);

  const handleRefresh = (event) => {
    const value = refreshValues[event.target.value];
    setRefreshRate(value);
  };

  const handleDragEnd = (event) => {
    const { active, over } = event;
    if (!over) {
      setComponents((prev) => prev.filter((comp) => comp.id !== active.id));

      return;
    }

    const newPosition = over.id.split("-").map(Number);
    setComponents((prev) =>
      prev.map((comp) => {
        if (comp.id === active.id) {
          const [validRow, validCol] = validatePosition(
            comp.size,
            newPosition[0],
            newPosition[1],
            GRID_ROWS,
            GRID_COLS
          );
          const updatedComp = { ...comp, position: [validRow, validCol] };
          // Update Settings data here
          setSettingsData(updatedComp.label);
          return updatedComp;
        }
        return comp;
      })
    );
  };

  const addComponent = () => {
    const [label, sizeStr] = newModuleValue.split("::");
    // Check if a module with the same label already exists
    const alreadyExists = components.some((comp) => comp.label === label);
    if (alreadyExists) return;

    const [rows, cols] = sizeStr.split("x").map(Number);
    const id = `comp${components.length + 1}`;
    setComponents((prev) => [
      ...prev,
      { id, label, position: [0, 0], size: [rows, cols] },
    ]);
  };

  const handleSaveNew = (e) => {
    e.preventDefault();

    let moduleSettings = {};

    fetch("http://localhost:8001/save_settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        modules: modulesOnDisplay,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log("Response:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const handleSave = (e) => {
    e.preventDefault();
    console.log("Display State", components);
    let modulesOnDisplay = [];

    for (let i = 0; i < components.length; i++) {
      let moduleData = {
        type: components[i].label.toLowerCase(),
        start_position: getPositionKey(components[i].position),
      };
      modulesOnDisplay.push(moduleData);
    }

    fetch("http://localhost:8001/render", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        modules: modulesOnDisplay,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log("Response:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };
  const handleClearDisplay = () => {
    fetch("http://localhost:8001/render/clear")
      .then((response) => {
        if (response.status === 200) {
          return response.json().then((data) => {
            console.log(data.message);
            alert("Display cleared successfully");
          });
        } else {
          alert(`Failed to clear display: HTTP ${response.status}`);
        }
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  };

  return (
    <div style={{ textAlign: "center" }}>
      <label htmlFor="selectModule">Select a Module: </label>
      <select
        id="selectModule"
        value={newModuleValue}
        onChange={(e) => setNewModuleValue(e.target.value)}
      >
        <option value="Weather::1x1">Weather</option>
        <option value="News::1x3">News</option>
        <option value="Email::1x4">Email</option>
        <option value="Traffic::1x3">Traffic</option>
        <option value="Stocks::1x1">Stocks</option>
      </select>
      <button
        onClick={addComponent}
        style={{ height: "18.67px", lineHeight: "0px", marginLeft: "5px" }}
      >
        Add Module
      </button>
      <button
        onClick={handleClearDisplay}
        style={{ height: "18.67px", lineHeight: "0px", marginLeft: "5px" }}
      >
        Clear Display
      </button>

      <DndContext
        collisionDetection={rectIntersection}
        onDragEnd={handleDragEnd}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            marginTop: "15px",
          }}
        >
          <div
            style={{ position: "relative", width: "400px", height: "200px" }}
          >
            <Grid rows={GRID_ROWS} cols={GRID_COLS}>
              {Array.from({ length: GRID_ROWS }).map((_, row) =>
                Array.from({ length: GRID_COLS }).map((_, col) => {
                  const isOccupied = components.some(
                    (comp) =>
                      row >= comp.position[0] &&
                      row < comp.position[0] + comp.size[0] &&
                      col >= comp.position[1] &&
                      col < comp.position[1] + comp.size[1]
                  );
                  return (
                    <DroppableCell
                      key={`${row}-${col}`}
                      id={`${row}-${col}`}
                      isOccupied={isOccupied}
                    />
                  );
                })
              )}
            </Grid>
            {components.map((comp) => (
              <Draggable
                key={comp.id}
                id={comp.id}
                position={comp.position}
                size={comp.size}
                label={comp.label}
              />
            ))}
          </div>
        </div>
      </DndContext>
      <button
        onClick={handleSave}
        style={{
          height: "18.67px",
          lineHeight: "0px",
          marginTop: "15px",
          marginBottom: "15px",
        }}
      >
        Update Display
      </button>

      <div>
        <input
          id="input"
          type="range"
          min="0"
          max={refreshValues.length - 1}
          defaultValue={defaultIndex}
          step="1"
          onInput={handleRefresh}
        />
        <div id="output">Auto-Refresh Interval: {refreshRate} Minute(s)</div>
        <div style={{ marginTop: "10px" }}>
          Check your E-ink display manual for refresh limits.
        </div>
      </div>
      <Settings module={settingsData} />
    </div>
  );
};

export default App;
