import { useEffect, useState } from "react";
import { backendUrl } from "../../../../utils/backendUrl";

import "./TrafficSettings.css";

const TrafficSettings = () => {
	const [trafficSettings, setTrafficSettings] = useState({
		zipcode: "00000",
	});
	const [formValues, setFormValues] = useState({
		zipcode: "00000",
	});
	const [notification, setNotification] = useState({ message: "", type: "" });
	const [notificationFileCreated, setNotificationFileCreated] = useState(false);

	useEffect(() => {
		const loadTrafficSettings = async () => {
			try {
				const response = await fetch(
					`${backendUrl}/settings/get?module=traffic`,
					{
						method: "GET",
					},
				);
				if (!response.ok) {
					throw new Error(`HTTP error! status: ${response.status}`);
				}
				const data = await response.json();
				if (data) {
					setTrafficSettings(data);
					setFormValues(data);
				}
			} catch (error) {
				console.error("Error loading traffic settings:", error);
			}
		};

		loadTrafficSettings();
	}, []);

	const handleInputChange = (e) => {
		const { name, value } = e.target;
		setFormValues((prevValues) => ({
			...prevValues,
			[name]: value,
		}));
	};

	const handleSaveTrafficSettings = async () => {
		try {
			const response = await fetch(`${backendUrl}/settings/save`, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					module: "traffic",
					settings: formValues,
				}),
			});
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}
			setTrafficSettings(formValues);
			setNotification({
				message: "Settings successfully saved!",
				type: "success",
			});
		} catch (error) {
			console.error("Error saving traffic settings:", error);
			setNotification({ message: "Unable to save settings!", type: "error" });
		} finally {
			setTimeout(() => setNotification({ message: "", type: "" }), 3000);
		}
	};

	const handleGenerateFile = async () => {
		try {
			const response = await fetch(`${backendUrl}/traffic/generate`, {
				method: "GET",
			});
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}
			// Show the static notification when the file is generated
			setNotificationFileCreated(true);
			setNotification({
				message: "File generated successfully!",
				type: "success",
			});
		} catch (error) {
			console.error("Error generating file:", error);
			setNotification({ message: "Unable to generate file!", type: "error" });
		} finally {
			setTimeout(() => setNotification({ message: "", type: "" }), 3000);
		}
	};

	const handleConsumeFile = async () => {
		try {
			const response = await fetch(`${backendUrl}/traffic/consume`, {
				method: "GET",
			});
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}
			// Hide the notification when the file is consumed successfully
			setNotificationFileCreated(false);
			setNotification({
				message: "File consumed successfully!",
				type: "success",
			});
		} catch (error) {
			console.error("Error consuming file:", error);
			setNotification({ message: "Unable to consume file!", type: "error" });
		} finally {
			setTimeout(() => setNotification({ message: "", type: "" }), 3000);
		}
	};

	const testTrafficAPI = async () => {
		try {
			const response = await fetch(`${backendUrl}/traffic/test`, {
				method: "GET",
			});
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}
			setNotification({
				message: "Traffic API test successful!",
				type: "success",
			});
		} catch (error) {
			console.error("Error testing Traffic API:", error);
			setNotification({ message: "Traffic API test failed!", type: "error" });
		} finally {
			setTimeout(() => setNotification({ message: "", type: "" }), 3000);
		}
	};

	return (
		<div>
			{/* <div style={{ marginBottom: "15px" }}>
				DO NOT FORGET TO ADD WHICH ALERTS DO YOU ACTUALLY WANT, LIKE HEAVY
				TRAFFIC, ETC.
			</div> */}
			<div style={{ marginBottom: "15px" }}>
				Current Zip code: {trafficSettings?.zipcode || "Loading..."}
			</div>
			<label htmlFor="zipcode-input">Enter a Zip code: </label>
			<input
				type="text"
				id="zipcode-input"
				name="zipcode"
				value={formValues.zipcode}
				onChange={handleInputChange}
				style={{ marginBottom: "15px" }}
			/>
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



			<div>
				<button
					onClick={testTrafficAPI}
					style={{ height: "18.67px", lineHeight: "0px", marginRight: "5px" }}
				>
					Test Traffic API
				</button>
				<br />
				<br />
				<button
					onClick={handleGenerateFile}
					style={{ height: "18.67px", lineHeight: "0px", marginRight: "5px" }}
				>
					Generate API File
				</button>
				<button
					onClick={handleConsumeFile}
					style={{ height: "18.67px", lineHeight: "0px", marginRight: "5px", marginBottom: "15px" }}
				>
					Consume API File
				</button>
				{notificationFileCreated && (
					<div
						style={{
							color: "white",
							backgroundColor: "#2c3e50",
							padding: "15px",

							borderRadius: "8px",
							maxWidth: "600px",
							lineHeight: "1.6",
							fontSize: "14px",
							textAlign: "left",
							boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
							margin: "0 auto"
						}}
					>
						<strong>API file generated successfully!</strong>
						<ul style={{ marginTop: "10px", paddingLeft: "20px" }}>
							<li>Open your Pi terminal.</li>
							<li>Enter the following command to edit the file:&nbsp; &nbsp;                <code
								style={{
									backgroundColor: "#1a1a1a",
									color: "#f8f8f2",
									padding: "2px 5px",
									borderRadius: "4px",

								}}
							>
								nano /tmp/e-ink.txt
							</code></li>
							<li>Paste your TOMTOM API key on the first line of the file.</li>
							<li>Press <strong>Ctrl+X</strong> to exit the editor.</li>
							<li>Press <strong>Y</strong> to confirm saving the changes.</li>
						</ul>
						<p style={{ marginTop: "10px" }}>
							Note: Once completed, your API key will be encrypted, consumed, and the file will be deleted.
							You will need to repeat this process each time the component starts if you wish to enable traffic alerts.
						</p>
					</div>
				)}
				<br />
				<button
					onClick={handleSaveTrafficSettings}
					style={{ height: "18.67px", lineHeight: "0px", marginBottom: "50px" }}
				>
					Save Traffic Settings
				</button>
			</div>
		</div>
	);
};

export default TrafficSettings;
