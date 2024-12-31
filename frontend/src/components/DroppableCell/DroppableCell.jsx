import React from "react";
import { useDroppable } from "@dnd-kit/core";
import "./DroppableCell.css";

const DroppableCell = ({ id, isOccupied }) => {
	const { setNodeRef } = useDroppable({ id });

	return (
		<div
			ref={setNodeRef}
			className="droppable-cell"
			style={{
				backgroundColor: isOccupied ? "lightgray" : "white",
			}}
		></div>
	);
};

export default DroppableCell;
