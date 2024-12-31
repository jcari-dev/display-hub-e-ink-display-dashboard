import { useState } from "react";

const EmailSettings = () => {
	const [status, setStatus] = useState("Inactive");
    const [message, setMessage] = useState("")

	const handleSaveEmailSettings = () => {
		console.log("Ayep.");
        settingsMessage("Email Files Generated")
	};

    const settingsMessage = (message) => {
        setMessage(message)
    }

 	return (
		<div>
			<div>Status:</div>
			<div id="email-settings-status">{status}</div>

			<br />
			<button
				onClick={handleSaveEmailSettings}
				style={{ height: "18.67px", lineHeight: "0px", marginTop: "15px" }}
			>
				Generate Email Files
			</button>
			<button
				onClick={handleSaveEmailSettings}
				style={{
					height: "18.67px",
					lineHeight: "0px",
					marginTop: "15px",
					marginLeft: "15px",
					marginBottom: "15px",
				}}
			>
				Consume Email Files
			</button>
            <div id="email-settings-message">
                {message}
            </div>
		</div>
	);
};

export default EmailSettings;
