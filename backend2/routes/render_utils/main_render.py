import xml.etree.ElementTree as ET
from datetime import datetime

from db import get_db
from db.models import WeatherSettings
from module_data_gen.thirdparty_apis.weather import gather_weather_data
from PIL import Image, ImageDraw, ImageFont
from waveshare.epd2in13_V4 import EPD

MODULE_SIZES = {
    "traffic": 3,
    "weather": 1,
    "email": 4,
    "news": 3,
    "stocks": 1,
    "fill": 2,
}

MODULE_FONT_SIZES = {
    "traffic": 15,
    "weather": 15,
    "email": 15,
    "fill": 15,
    "news": 15,
    "stocks": 15,
}

WEATHER_CODES_MAP = {
    0: "\nClear",
    1: "\nMostly\nClear",
    2: "\nPartly\nCloudy",
    3: "\nOvercast",
    45: "\nFog",
    48: "\nIcy\nFog",
    51: "\nLight\nDrizzle",
    53: "\nDrizzle",
    55: "\nHeavy\nDrizzle",
    56: "\nLight Icy\nDrizzle",
    57: "\nIcy\nDrizzle",
    61: "\nLight\nRain",
    63: "\nRain",
    65: "\nHeavy\nRain",
    66: "\nLight Icy\nRain",
    67: "\nIcy\nRain",
    80: "\nLight\nShowers",
    81: "\nShowers",
    82: "\nHeavy\nShowers",
}

SQUARE_W = 62.5
SQUARE_H = 61

DISPLAY_LOCATIONS = {
    1: {"x": 0, "y": 0},
    2: {"x": 62.5, "y": 0},
    3: {"x": 125, "y": 0},
    4: {"x": 187.5, "y": 0},
    5: {"x": 0, "y": 61},
    6: {"x": 62.5, "y": 61},
    7: {"x": 125, "y": 61},
    8: {"x": 187, "y": 61},
}


def format_time(pub_date):
    """Convert pubDate to local time and format it for display."""
    utc_time = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")
    local_time = utc_time.astimezone()
    return local_time.strftime("|%I:%M %p").lstrip("0")


def process_news_for_display(file_path, item_index=0):
    # Parse the XML file
    # TODO YOU HAVE TO REMOVE THE LAST WORD IF THE LENGTH EXCEEDS
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract all <item> elements
    items = root.findall("channel/item")
    if len(items) <= item_index:
        return f'text="""No news available at index {item_index}.\n\n"""'

    # Get the specified <item>
    item = items[item_index]

    # Get title, description, and pubDate
    title = item.findtext("title", "").strip()

    pub_date = item.findtext("pubDate", "").strip()

    # Format time
    formatted_time = format_time(pub_date)

    content = title

    # Truncate content to fit lines
    top_line = content[:20].strip()
    middle_line = content[20:40].strip()
    bottom_text = content[40:50].strip()
    bottom_line = f"{bottom_text} {formatted_time}"

    # Format final text
    return f"{top_line}\n{middle_line}\n{bottom_line}"


def allocate_module(module):
    location_x_y = DISPLAY_LOCATIONS[module["start_position"]]
    return location_x_y


def generate_traffic_data(zipcode):
    return [
        ("366 Revere Beach Blvd,\nRevere, MA 02151", "Heavy Traffic"),
        ("90 North Shore Rd,\nRevere, MA 02151", "Lane Closed"),
        (
            "1234 Jean Baptiste Point du Sable Lake Shore Drive,\nChicago, IL 60601",
            "Lane Closed",
        ),
        ("44 Raymond Ave,\nSalem, MA 01970", "Heavy Traffic"),
    ][:1]


def get_email_data():
    # unread_emails = 625
    # subject_most_recent = "Security alert"
    # most_recent_sender = "Google <no-reply@accounts.google.com>"
    # unread_emails = 0
    # subject_most_recent = ""
    # most_recent_sender = ""
    unread_emails = 1
    subject_most_recent = "Follow up from IBM"
    most_recent_sender = "IBMRecruitment_noreply <Enterprise@trm.brassring.com>"

    if unread_emails > 0 and subject_most_recent and most_recent_sender:
        email_data = (
            f"{unread_emails} Unread Email{'s' if unread_emails != 1 else ''}\n"
            f"Title: {subject_most_recent}\n"
            f"From: {most_recent_sender}"
        )
    else:
        email_data = "No Unread Emails\nYou’re all caught up!\n(~^_^)~ ~~~ (~^_^)~"

    return email_data


def get_weather_data():

    db = next(get_db())

    weather_settings = db.get(WeatherSettings, 1)

    db.close()
    print("we got here?")
    timezone = weather_settings.timezone
    scale = weather_settings.scale
    zipcode = weather_settings.zipcode

    weather_data = gather_weather_data(scale, timezone, zipcode)

    current = weather_data['data']['current_weather']

    current_temperature = current['temperature']

    current_weather_code = current['weathercode']

    current_scale = scale[0].upper()
    print("pass it?")
    return f"{current_temperature}°{current_scale}{WEATHER_CODES_MAP[current_weather_code]}"


def generate_drawings(modules):
    drawings = []

    for module in modules:
        module_type = module["type"]

        if module_type == "traffic":

            incidents = generate_traffic_data("01902")

            for street_name, event in incidents:
                traffic_event = f"{event} Near\n{street_name}"
            text = traffic_event
            xy = allocate_module(module)

            x = xy["x"]
            y = xy["y"]

        elif module_type == "weather":

            weather_data = get_weather_data()
            xy = allocate_module(module)

            x = xy["x"]
            y = xy["y"]
            text = weather_data

        elif module_type == "email":
            email_data = get_email_data()

            xy = allocate_module(module)

            x = xy["x"]
            y = xy["y"]
            text = email_data

        elif module_type == "fill":
            fill = "This Should\nFill\nAbout 2 Squares"

            xy = allocate_module(module)

            x = xy["x"]
            y = xy["y"]
            text = fill

        elif module_type == "news":

            news = process_news_for_display("./sample_data/World.xml", 12)

            xy = allocate_module(module)

            x = xy["x"]
            y = xy["y"]
            text = news

        elif module_type == "stocks":
            stock_data = "NFLX\n904.77\n-1.72%"

            xy = allocate_module(module)

            x = xy["x"]
            y = xy["y"]
            text = stock_data

        # Update with the correct path to your font
        font_path = "./display_fonts/RobotoMono-SemiBold.ttf"
        font_size = MODULE_FONT_SIZES[module_type]

        if module_type == "weather" or module_type == "stocks":
            font_path = "./display_fonts/Roboto-Medium.ttf"
            font_size = MODULE_FONT_SIZES[module_type]

        font = ImageFont.truetype(font_path, font_size)
        drawings.append(
            {
                "x": x,
                "y": y,
                "text": text,
                "font": font,
                "fill": 0,
                "max_width": MODULE_SIZES[module_type] * SQUARE_W,
                "type": module_type,
            }
        )

    return drawings


def inner_boundaries_map_line(line_drawing):

    line_a = {"x1": 0, "y1": 61, "x2": 187.5, "y2": 61}  # "___ "

    line_b = {"x1": 187.5, "y1": 61, "x2": 187.5,
              "y2": 0}  # "   | " upper half

    line_c = {"x1": 62.5, "y1": 61, "x2": 62.5, "y2": 0}  # " |  " upper half

    line_d = {"x1": 62.5, "y1": 61, "x2": 250,
              "y2": 61}  # " ___" # middle line

    line_e = {"x1": 187.5, "y1": 61, "x2": 187.5,
              "y2": 122}  # "   | " # lower half

    line_f = {"x1": 0, "y1": 61, "x2": 250, "y2": 61}  # "____" middle_ilne

    line_g = {"x1": 62.5, "y1": 61, "x2": 62.5,
              "y2": 250}  # " |   "  lower half

    line_h = {"x1": 0, "y1": 61, "x2": 62.5, "y2": 61}  # "_   " middle line

    line_i = {"x1": 62.5, "y1": 61, "x2": 125, "y2": 61}  # " _  " middle line

    line_j = {"x1": 125, "y1": 61, "x2": 125, "y2": 0}  # "  |  " upper half

    line_k = {"x1": 125, "y1": 61, "x2": 187.5, "y2": 61}  # "  _ " middle line

    line_l = {"x1": 187.5, "y1": 61, "x2": 250, "y2": 61}  # "   _" middle line

    line_m = {"x1": 125, "y1": 61, "x2": 125, "y2": 250}  # "  |  " lower half

    line_n = {"x1": 187.5, "y1": 61, "x2": 187.5,
              "y2": 250}  # "   | " lower half

    if line_drawing == "____":
        return [line_f]

    elif line_drawing == "___| ":
        return [line_a, line_b]

    elif line_drawing == " |___":
        return [line_c, line_d]

    elif line_drawing == "‾‾‾| ":
        return [line_a, line_e]

    elif line_drawing == " |‾‾‾":
        return [line_g, line_d]

    elif line_drawing == "_|   ":
        return [line_h, line_c]

    elif line_drawing == " |_|  ":
        return [line_c, line_i, line_j]

    elif line_drawing == "  |_| ":
        return [line_j, line_k, line_b]

    elif line_drawing == "   |_":
        return [line_b, line_l]

    elif line_drawing == "‾|   ":
        return [line_h, line_g]

    elif line_drawing == " |‾|  ":
        return [line_g, line_i, line_m]

    elif line_drawing == "  |‾| ":
        return [line_m, line_k, line_n]

    elif line_drawing == "   |‾":
        return [line_n, line_l]

    # Type 2 boundaries
    elif line_drawing == "__|  ":
        return [line_h, line_i, line_j]

    elif line_drawing == " |__| ":
        return [line_c, line_i, line_k, line_b]

    elif line_drawing == "  |__":
        return [line_j, line_k, line_l]

    elif line_drawing == "‾‾|  ":
        return [line_h, line_i, line_m]

    elif line_drawing == " |‾‾| ":
        return [line_g, line_i, line_k, line_e]

    elif line_drawing == "  |‾‾":
        return [line_m, line_k, line_l]


def draw_module_inner_boundaries(module):

    if MODULE_SIZES[module["type"]] == 4:
        return inner_boundaries_map_line("____")
    elif MODULE_SIZES[module["type"]] == 3:
        if module["start_position"] == 1:
            return inner_boundaries_map_line("___| ")
        elif module["start_position"] == 2:
            return inner_boundaries_map_line(" |___")
        elif module["start_position"] == 5:
            return inner_boundaries_map_line("‾‾‾| ")
        elif module["start_position"] == 6:
            return inner_boundaries_map_line(" |‾‾‾")
    elif MODULE_SIZES[module["type"]] == 2:
        if module["start_position"] == 1:
            return inner_boundaries_map_line("__|  ")
        elif module["start_position"] == 2:
            return inner_boundaries_map_line(" |__| ")
        elif module["start_position"] == 3:
            return inner_boundaries_map_line("  |__")
        elif module["start_position"] == 5:
            return inner_boundaries_map_line("‾‾|  ")
        elif module["start_position"] == 6:
            return inner_boundaries_map_line(" |‾‾| ")
        elif module["start_position"] == 7:
            return inner_boundaries_map_line("  |‾‾")
    elif MODULE_SIZES[module["type"]] == 1:
        if module["start_position"] == 1:
            return inner_boundaries_map_line("_|   ")
        elif module["start_position"] == 2:
            return inner_boundaries_map_line(" |_|  ")
        elif module["start_position"] == 3:
            return inner_boundaries_map_line("  |_| ")
        elif module["start_position"] == 4:
            return inner_boundaries_map_line("   |_")
        elif module["start_position"] == 5:
            return inner_boundaries_map_line("‾|   ")
        elif module["start_position"] == 6:
            return inner_boundaries_map_line(" |‾|  ")
        elif module["start_position"] == 7:
            return inner_boundaries_map_line("  |‾| ")
        elif module["start_position"] == 8:
            return inner_boundaries_map_line("   |‾")


def truncate_text_line_by_line(text, font, max_width):
    lines = text.split("\n")
    truncated_lines = []

    for line in lines:
        # Truncate each line to fit within max_width
        truncated_line = line
        while font.getbbox(truncated_line)[2] > max_width:
            truncated_line = truncated_line[:-1]  # Remove last character
        truncated_lines.append(truncated_line)

    return truncated_lines


def display_text_at_position(modules):
    """
    Display text centered horizontally, truncated as needed, and left-aligned on the e-paper screen.
    """
    # Initialize the e-paper display
    epd = EPD()
    epd.init()  # Start the display

    # Create a blank image (255 = white background)
    image = Image.new("1", (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)
    # ------------------------------------------------------------

    drawings = generate_drawings(modules)

    for drawing in drawings:
        x = drawing["x"]
        y = drawing["y"]
        text = drawing["text"]
        max_width = drawing["max_width"]
        font = drawing["font"]

        truncated_lines = truncate_text_line_by_line(text, font, max_width)

        # Calculate total height of the text block to center it vertically
        line_height = font.getbbox("A")[3]
        total_text_height = len(truncated_lines) * line_height
        vertical_offset = (SQUARE_H - total_text_height) / 2

        # Draw each truncated line
        for index, line in enumerate(truncated_lines):
            # Measure the truncated line width
            text_width = font.getbbox(line)[2]

            # Calculate the x-coordinate to center the line
            centered_x = x + (max_width - text_width) / 2

            # Calculate the y-coordinate for the current line
            line_y = y + vertical_offset + index * line_height

            # Draw the text
            draw.text((centered_x, line_y), line,
                      font=font, fill=0)  # 0 = black text

    for module in modules:
        line_coordinates = draw_module_inner_boundaries(module)
        if line_coordinates:
            for line in line_coordinates:
                x1 = line["x1"]
                x2 = line["x2"]
                y1 = line["y1"]
                y2 = line["y2"]

                draw.line([(x1, y1), (x2, y2)], fill=0)

    # Rotate the image for the correct display orientation
    rotated_image = image.rotate(180, expand=True)

    # Send the image to the e-paper display
    epd.display(epd.getbuffer(rotated_image))
    epd.sleep()  # Put the display into sleep mode to save power


def display_clear():
    epd = EPD()
    epd.init()
    epd.Clear()
