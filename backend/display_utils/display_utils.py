from waveshare.epd2in13_V4 import EPD


def clear_display():
    print("clear_display() was called")  # Debug log
    epd = EPD()
    epd.init()
    epd.Clear()
