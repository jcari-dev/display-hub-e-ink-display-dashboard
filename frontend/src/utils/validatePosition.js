export default function validatePosition(size, row, col, gridRows, gridCols) {
	const [rowsNeeded, colsNeeded] = size;

	if (row + rowsNeeded > gridRows) {
		row = Math.max(0, gridRows - rowsNeeded);
	}

	if (col + colsNeeded > gridCols) {
		col = Math.max(0, gridCols - colsNeeded);
	}

	return [row, col];
}
