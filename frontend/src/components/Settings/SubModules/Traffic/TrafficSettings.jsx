import { useState } from "react";
import "./TrafficSettings.css";

const TrafficSettings = () => {
	const handleSaveTrafficSettings = () => {
		console.log("Yup Saved the weather settings.");
	};

	const [zipcode, setZipcode] = useState("00000");

	return (
		<div>
			DO NOT FORGET TO ADD WHICH ALERTS DO YOU ACTUALLY WANT, LIKE HEAVY TRAFFIC, ETC.
			<br />
			Current Zip code: {zipcode}
			<br />
			<label htmlFor="zipcode-input">Enter a Zip code: </label>
			<input
				type="text"
				id="zipcode-input"
                style={{marginBottom: "15px"}}
			/>
			<br />
            <button
				onClick={handleSaveTrafficSettings}
				style={{ height: "18.67px", lineHeight: "0px" }}
			>
				Generate API File
			</button>
            <button
				onClick={handleSaveTrafficSettings}
				style={{ height: "18.67px", lineHeight: "0px", marginLeft: "5px" }}
			>
				Consume API File
			</button>
            <br />
            <button
				onClick={handleSaveTrafficSettings}
				style={{ height: "18.67px", lineHeight: "0px", marginBottom: "25px", marginTop: "25px" }}
			>
				Test Traffic API
			</button>
            <br />
			<button
				onClick={handleSaveTrafficSettings}
				style={{ height: "18.67px", lineHeight: "0px" }}
			>
				Save Traffic Settings
			</button>
		</div>
	);
};

export default TrafficSettings;
