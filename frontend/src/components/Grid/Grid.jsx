import React from "react";
import "./Grid.css";

const Grid = ({ rows, cols, children }) => {
	return (
		<div
			className="grid-container"
			style={{
				display: "grid",
				gridTemplateRows: `repeat(${rows}, 100px)`,
				gridTemplateColumns: `repeat(${cols}, 100px)`,
			}}
		>
			{children}
		</div>
	);
};

export default Grid;
