#!/usr/bin/env python3
"""show_toll.py - visualize specific 405 toll rates on a Unicorn HAT"""
import os
from datetime import datetime
import colorsys
import requests

try:
    import unicornhathd
except ImportError:
    try:
        from unicorn_hat_sim import unicornhathd
    except ImportError as exc:
        raise ImportError(
            "error! couldn't import either unicornhathd or unicorn_hat_sim"
        ) from exc

MAX_TOLL = 1500  # $15.00 ... for now :|
PIXELS = unicornhathd.WIDTH


# LED gamma correction table -
# https://learn.adafruit.com/led-tricks-gamma-correction/the-quick-fix
# fmt: off
gamma = [
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
   10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
   17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
   25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
   37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
   51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
   69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
   90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
  115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
  144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
  177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
  215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255
]
# fmt: on

PURPLE = (gamma[255], gamma[0], gamma[255])
BLUE = (gamma[0], gamma[0], gamma[255])
GREEN = (gamma[0], gamma[255], gamma[0])
YELLOW = (gamma[255], gamma[255], gamma[0])
ORANGE = (gamma[255], gamma[165], gamma[0])
RED = (gamma[255], gamma[0], gamma[0])

WSDOT_TOLL_URL = "https://wsdot.wa.gov/Traffic/api/TollRates/TollRatesREST.svc/GetTollRatesAsJson?AccessCode="  # pylint: disable=line-too-long

LONG_TRIP_SOUTH = "405tp02898"  # "SR 524" -> "NE 6th"
SHORT_TRIP_SOUTH = "405tp02162"  # "NE 145th" -> "NE 6th"
LONG_TRIP_NORTH = "405tp01353"  # "NE 4th" -> "I-5"
SHORT_TRIP_NORTH = "405tp01352"  # "NE 4th" -> "SR 522"


def get_rate() -> dict:
    """
    get the current toll rates from WSDOT
    """

    wsdot_token = os.environ.get("WSDOT_API_TOKEN")
    if not wsdot_token:
        raise ValueError("error! could not find token environment variable")
    lookup_url = WSDOT_TOLL_URL + wsdot_token
    header = {"Accept": "application/json"}
    rate = requests.get(url=lookup_url, headers=header, timeout=10)
    rate.raise_for_status()
    return rate.json()


def main():
    """
    ...main.
    """
    unicornhathd.setup()
    unicornhathd.brightness(0.8)
    unicornhathd.rotation(0)

    # south in the morning, north in the afternoon
    if datetime.now().hour < 12:
        long_trip = LONG_TRIP_SOUTH
        short_trip = SHORT_TRIP_SOUTH
    else:
        long_trip = LONG_TRIP_NORTH
        short_trip = SHORT_TRIP_NORTH

    long_rate = short_rate = 0

    # grab the specific rates from the big response from the API
    # (probably a better way to do this)
    toll_rates = get_rate()
    for entry in toll_rates:
        if entry["TripName"] == long_trip:
            long_rate = entry["CurrentToll"]
        elif entry["TripName"] == short_trip:
            short_rate = entry["CurrentToll"]

    # print(f"long rate = {long_rate}, short rate = {short_rate}")

    # divide up the rate
    long_dots = min(round(long_rate / (MAX_TOLL / PIXELS)), PIXELS)
    short_dots = min(round(short_rate / (MAX_TOLL / PIXELS)), PIXELS)

    # print(f"long dots = {long_dots}, short dots = {short_dots}")

    # rainbow!
    palette = (
        [PURPLE] * 2
        + [BLUE] * 2
        + [GREEN] * 3
        + [YELLOW] * 3
        + [ORANGE] * 3
        + [RED] * 3
    )

    # convert to HSV to make it easier to set brightness
    hsv_palette = [
        colorsys.rgb_to_hsv(r / 255, g / 255, b / 255) for r, g, b in palette
    ]

    # bright dots indicate the cost for the short trip,
    # dim dots indicate the cost for the long trip
    bright_palette = [(h, s, 1.0) for h, s, v in hsv_palette]
    dim_palette = [(h, s, 0.5) for h, s, v in hsv_palette]

    # long trip is always greater than or equal to short trip,
    # so draw long trip first, from left to right
    for i in range(long_dots):
        for x in range(unicornhathd.HEIGHT):
            unicornhathd.set_pixel_hsv(
                x, i, dim_palette[i][0], dim_palette[i][1], dim_palette[i][2]
            )

    for i in range(short_dots):
        for x in range(unicornhathd.HEIGHT):
            unicornhathd.set_pixel_hsv(
                x, i, bright_palette[i][0], bright_palette[i][1], bright_palette[i][2]
            )

    unicornhathd.show()
    # leave the display on, will be refreshed on next run
    # (or run something else to clear it)


if __name__ == "__main__":
    main()
