import React, { useState } from "react";
import "./NewsSettings.css";

const NewsSettings = () => {

	const handleSaveNewsSettings = () =>{

	}
	const providers = {
		English: {
			"The New York Times": [
				"World",
				"Africa",
				"Americas",
				"Asia Pacific",
				"Europe",
				"Middle East",
				"U.S.",
				"Education",
				"Politics",
				"N.Y. / Region",
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
				"España",
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

	const [selectedLanguage, setSelectedLanguage] = useState("");
	const [selectedProvider, setSelectedProvider] = useState("");
	const [currentNewsSettings, setCurrentNewsSettings] = useState({
		Language: "English",
		Outlet: "The New York Times",
		RSS: "Business",
	});

	const handleLanguageChange = (e) => {
		setSelectedLanguage(e.target.value);
		setSelectedProvider(""); // Reset provider when language changes
	};

	const handleProviderChange = (e) => {
		setSelectedProvider(e.target.value);
	};

	return (
		<div>
			Current Settings: {currentNewsSettings.Language},{" "}
			{currentNewsSettings.Outlet}, {currentNewsSettings.RSS}
			{/* Language Selector */}
			<br />
			---
			<br />
			<label>
				Select a Language: &nbsp;
				<select
					value={selectedLanguage}
					onChange={handleLanguageChange}
				>
					<option value="">---Select---</option>
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
			<br />
			{/* News Provider Selector */}
			{selectedLanguage && (
				<label>
					Select News Outlet: &nbsp;
					<select
						value={selectedProvider}
						onChange={handleProviderChange}
					>
						<option value="">----------Select---------</option>
						{Object.keys(providers[selectedLanguage]).map((provider) => (
							<option
								key={provider}
								value={provider}
							>
								{provider}
							</option>
						))}
					</select>
				</label>
			)}
			<br />
			{/* RSS Feed Selector */}
			{selectedProvider && (
				<label>
					Pick an RSS Feed: &nbsp;
					<select>
						<option value="">-----------Select-----------</option>

						{providers[selectedLanguage][selectedProvider].map((feed) => (
							<option
								key={feed}
								value={feed}
							>
								{feed}
							</option>
						))}
					</select>
				</label>
			)}
			<br />
			<button
				onClick={handleSaveNewsSettings}
				style={{ height: "18.67px", lineHeight: "0px", marginTop: "15px" }}
			>
				Save News Settings
			</button>
		</div>
	);
};

export default NewsSettings;
