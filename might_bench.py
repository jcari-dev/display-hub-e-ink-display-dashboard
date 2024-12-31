def truncate_text_line_by_line_old(text, font, max_width):
    """
    Truncate each line of text to ensure no line exceeds the max_width.

    Parameters:
    - text (str): The original text, potentially with line breaks.
    - font (ImageFont): The font used to measure the text.
    - max_width (float): The maximum allowed width in pixels.

    Returns:
    - str: Text where each line is truncated to fit within max_width.
    """
    lines = text.split('\n')  # Split the text into lines
    truncated_lines = []

    for line in lines:
        truncated_line = line
        # Use getbbox to calculate text width
        # getbbox returns (x0, y0, x1, y1)
        while font.getbbox(truncated_line)[2] > max_width:
            truncated_line = truncated_line[:-1]  # Remove the last character
        truncated_lines.append(truncated_line)

    return '\n'.join(truncated_lines)  # Rejoin the lines


def display_text_at_position_old(modules):
    """
    Display text at a specified position on the e-paper screen,
    truncating lines that exceed max_width.

    Parameters:
    - text (str): The text to display on the screen.
    - x (int): The x-coordinate (horizontal) position to start the text.
    - y (int): The y-coordinate (vertical) position to start the text.
    - max_width (float): Maximum width in pixels for each line of text.
    """
    # Initialize the e-paper display
    epd = EPD()
    epd.init()  # Start the display

    # Create a blank image (255 = white background)
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)
    # ------------------------------------------------------------

    drawings = generate_drawings(modules)

    for drawing in drawings:
        x = drawing["x"]
        y = drawing["y"]
        text = drawing["text"]
        max_width = drawing["max_width"]
        font = drawing["font"]


        truncated_text = truncate_text_line_by_line(text, font, max_width)

        # Draw the truncated text at the specified position
        draw.text((x, y), truncated_text, font=font, fill=0)  # 0 = black text

    for module in modules:
        line_coordinates = draw_module_inner_boundaries(module)
        if line_coordinates:
            for line in line_coordinates:
                x1 = line["x1"]
                x2 = line["x2"]
                y1 = line["y1"]
                y2 = line["y2"]

                draw.line([(x1, y1), (x2, y2)], fill=0)

    # # Draw boundary lines (top, bottom, left, and right)
    # draw.line([(0, 61), (250, 61)], fill=0)  # Top boundary
    # draw.line([(62.5*3, 61), (62.5*3, 0)], fill=0)  # Top boundary


    # ------------------------------------------------------------


    # Rotate the image for the correct display orientation
    rotated_image = image.rotate(180, expand=True)

    # Send the image to the e-paper display
    epd.display(epd.getbuffer(rotated_image))
    epd.sleep()  # Put the display into sleep mode to save power
