import React, { useState } from "react";
import {
  Typography,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  SelectChangeEvent,
  FormHelperText,
} from "@mui/material";
import "./Module.css";

const Module: React.FC = () => {
  const [selectedModule, setSelectedModule] = useState<string>("");

  const handleChange = (event: SelectChangeEvent) => {
    setSelectedModule(event.target.value);
  };

  const modules = [
    { value: "", label: "None", italic: true },
    { value: "1", label: "News" },
    { value: "2", label: "Email" },
    { value: "3", label: "Weather" },
    { value: "4", label: "Traffic" },
    { value: "5", label: "Datetime" },
    { value: "6", label: "URL Monitor" },
  ];

  const moduleSettings: Record<string, string> = {
    "1": "Settings for News Module",
    "2": "Settings for Email Module",
    "3": "Settings for Weather Module",
    "4": "Settings for Traffic Module",
    "5": "Settings for Datetime Module",
    "6": "Settings for URL Monitor Module",
  };

  const renderSettings = () => {
    return (
      <Typography>
        {moduleSettings[selectedModule] ||
          "Select a module to configure settings"}
      </Typography>
    );
  };

  return (
    <div className="module-container">
      <div className="module-selector">
        <Typography>Select a module:</Typography>
        <FormControl sx={{ minWidth: 120 }}>
          <InputLabel id="module-select-label">Modules</InputLabel>
          <Select
            labelId="module-select-label"
            id="module-select"
            value={selectedModule}
            label="Modules"
            onChange={handleChange}
          >
            {modules.map(({ value, label, italic }) => (
              <MenuItem key={value} value={value}>
                {italic ? <em>{label}</em> : label}
              </MenuItem>
            ))}
          </Select>
          <FormHelperText>Select a module from the list above</FormHelperText>
        </FormControl>
      </div>
      <div className="module-settings">
        <Typography variant="h6">Module Settings</Typography>
        {renderSettings()}
      </div>
      <div className="module-draggable-placeholder">
        <Typography>Draggable Component Placeholder</Typography>
      </div>
    </div>
  );
};

export default Module;
