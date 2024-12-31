import React from "react";
import { useDraggable } from "@dnd-kit/core";
import "./Draggable.css";

const Draggable = ({ id, position, size, label, onClickModule }) => {
	const { attributes, listeners, setNodeRef, transform } = useDraggable({ id });
	const style = {
		transform: transform
			? `translate(${transform.x}px, ${transform.y}px)`
			: undefined,
		width: `${size[1] * 100}px`,
		height: `${size[0] * 100}px`,
		left: position[1] * 100,
		top: position[0] * 100,
	};

	return (
		<div
			ref={setNodeRef}
			className="draggable-item"
			style={style}
			{...listeners}
			{...attributes}
		>
			{label}
		</div>
	);
};

export default Draggable;
