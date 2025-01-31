import React, { useEffect, useState } from "react";
import { backendUrl } from "../../../../utils/backendUrl";

import "./NewsSettings.css";

const NewsSettings = () => {
	const [newsSettings, setNewsSettings] = useState({
		language: "",
		outlet: "",
		rss_feed: "",
	});

	const [formValues, setFormValues] = useState({
		language: "",
		outlet: "",
		rss_feed: "",
	});

	const [notification, setNotification] = useState({ message: "", type: "" });

	const providers = {
		English: {
			"The New York Times": [
				"NYT Home Page",
				"World",
				"Africa",
				"Americas",
				"Asia Pacific",
				"Europe",
				"Middle East",
				"U.S.",
				"Education",
				"Politics",
				"The Upshot",
				"N.Y./Region",
				"Business",
				"Energy & Environment",
				"Small Business",
				"Economy",
				"DealBook",
				"Media & Advertising",
				"Your Money",
				"Technology",
				"Personal Tech",
				"Sports",
				"Baseball",
				"College Basketball",
				"College Football",
				"Golf",
				"Hockey",
				"Pro-Basketball",
				"Pro-Football",
				"Soccer",
				"Tennis",
				"Science",
				"Environment",
				"Space & Cosmos",
				"Health",
				"Well Blog",
				"Arts",
				"Art & Design",
				"Book Review",
				"Dance",
				"Movies",
				"Music",
				"Television",
				"Theater",
				"Fashion & Style",
				"Dining & Wine",
				"Love",
				"T Magazine",
				"Travel",
				"Jobs",
				"Real Estate",
				"Autos",
				"Lens Blog",
				"Obituaries",
				"Times Wire",
				"Most E-Mailed",
				"Most Shared",
				"Most Viewed",
				"Charles M. Blow",
				"Jamelle Bouie",
				"David Brooks",
				"Frank Bruni",
				"Gail Collins",
				"Ross Douthat",
				"Maureen Dowd",
				"Thomas L. Friedman",
				"Michelle Goldberg",
				"Ezra Klein",
				"Nicholas D. Kristof",
				"Paul Krugman",
				"Farhad Manjoo",
				"Bret Stephens",
				"Sunday Opinion",
			],
			"Reuters": [
				"All Sectors",
				"Equities",
				"Foreign Exchange & Fixed Income",
				"Economy",
				"Commodities & Energy",
				"All Topics",
				"Business & Finance",
				"Deals",
				"Politics",
				"Environment",
				"Tech",
				"Health",
				"Sports",
				"Entertainment & Lifestyle",
				"Human Interest",
				"Journalist Spotlight",
				"All Regions",
				"Middle East",
				"Africa",
				"Europe",
				"North America",
				"South America",
				"Asia",
				"All Impacts",
				"Market Impact",
				"Media Customer Impact",
				"All Updates",
				"The Big Picture",
				"Reuters News First",
			],
		},
		Spanish: {
			"El País": [
				"España",
				"América",
				"In English",
				"México",
				"Colombia",
				"Chile",
				"Argentina",
				"Últimas Noticias",
				"Lo Más Visto",
				"Fotografías",
				"Vídeos",
				"Podcasts",
				"Sociedad",
				"Internacional",
				"Opinión",
				"España", // Dupe?
				"Economía",
				"Ciencia",
				"Tecnología",
				"Cultura",
				"Estilos",
				"Deportes",
				"Televisión",
				"Gente",
				"Clima y Medio Ambiente",
				"Educación",
				"Gastronomía",
				"El Comidista",
				"S Moda",
				"EPS",
				"Babelia",
				"El Viajero",
				"Icon",
				"Planeta Futuro",
				"Mamás y Papas",
				"Escaparate",
				"Ideas",
				"Quadern",
				"Cinco Días",
				"Motor",
				"Negocios",
			],
		},
	};

	useEffect(() => {
		const loadNewsSettings = async () => {
			try {
				const response = await fetch(
					`${backendUrl}/settings/get?module=news`,
				);
				if (!response.ok)
					throw new Error(`HTTP error! status: ${response.status}`);
				const data = await response.json();
				if (data) {
					setNewsSettings(data);
					setFormValues(data);
				}
			} catch (error) {
				console.error("Error loading news settings:", error);
			}
		};

		loadNewsSettings();
	}, []);

	const handleInputChange = (e) => {
		const { name, value } = e.target;
		setFormValues((prevValues) => {
			const updatedValues = { ...prevValues, [name]: value };

			if (name === "language") {
				updatedValues.outlet = "";
				updatedValues.rss_feed = "";
			}

			if (name === "outlet") {
				updatedValues.rss_feed = "";
			}

			return updatedValues;
		});
	};

	const handleSaveNewsSettings = async (e) => {
		e.preventDefault();
		try {
			const response = await fetch(`${backendUrl}/settings/save`, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					module: "news",
					settings: formValues,
				}),
			});
			if (!response.ok)
				throw new Error(`HTTP error! status: ${response.status}`);
			const data = await response.json();
			setNewsSettings(formValues);
			setNotification({
				message: "Settings successfully saved!",
				type: "success",
			});
		} catch (error) {
			console.error("Error saving news settings:", error);
			setNotification({ message: "Unable to save settings!", type: "error" });
		} finally {
			setTimeout(() => setNotification({ message: "", type: "" }), 3000);
		}
	};

	return (
		<div>
			<div>
				Current Settings: {newsSettings.language || "None"},{" "}
				{newsSettings.outlet || "None"}, {newsSettings.rss_feed || "None"}
			</div>

			{/* Language Selector */}
			<div style={{ marginTop: "15px" }}>
				<label>
					Select a Language: &nbsp;
					<select
						name="language"
						value={formValues.language}
						onChange={handleInputChange}
					>
						<option value="">--- Select ---</option>
						{Object.keys(providers).map((language) => (
							<option
								key={language}
								value={language}
							>
								{language}
							</option>
						))}
					</select>
				</label>
			</div>

			{/* Outlet Selector */}
			<div style={{ marginTop: "15px" }}>
				<label>
					Select News Outlet: &nbsp;
					<select
						name="outlet"
						value={formValues.outlet}
						onChange={handleInputChange}
						disabled={!formValues.language}
					>
						<option value="">--- Select ---</option>
						{formValues.language &&
							Object.keys(providers[formValues.language]).map((outlet) => (
								<option
									key={outlet}
									value={outlet}
								>
									{outlet}
								</option>
							))}
					</select>
				</label>
			</div>

			{/* RSS Feed Selector */}
			<div style={{ marginTop: "15px" }}>
				<label>
					Pick an RSS Feed: &nbsp;
					<select
						name="rss_feed"
						value={formValues.rss_feed}
						onChange={handleInputChange}
						disabled={!formValues.outlet}
					>
						<option value="">--- Select ---</option>
						{formValues.outlet &&
							providers[formValues.language][formValues.outlet].map((feed) => (
								<option
									key={feed}
									value={feed}
								>
									{feed}
								</option>
							))}
					</select>
				</label>
			</div>

			{/* Notification */}
			{notification.message && (
				<div
					style={{
						color: notification.type === "success" ? "green" : "red",
						marginTop: "15px",
					}}
				>
					{notification.message}
				</div>
			)}

			{/* Save Button */}
			<button
				onClick={handleSaveNewsSettings}
				style={{ marginTop: "15px" }}
			>
				Save News Settings
			</button>
		</div>
	);
};

export default NewsSettings;
