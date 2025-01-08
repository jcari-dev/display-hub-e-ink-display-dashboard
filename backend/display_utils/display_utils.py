from waveshare.epd2in13_V4 import EPD


def clear_display():
    epd = EPD()
    epd.init()
    epd.Clear()
