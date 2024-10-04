#!/usr/bin/env python3
"""
display multi-color "rounded" rectangles
on a unicorn hat hd
press ctrl-c to quit
"""

import time
import numpy as np

try:
    import unicornhathd
except ImportError:
    try:
        from unicorn_hat_sim import unicornhathd
    except ImportError as exc:
        raise ImportError(
            "Neither unicornhathd nor unicorn_hat_sim could be imported."
        ) from exc


def fade_in():
    """
    fade in brightness
    """
    unicornhathd.brightness(0)
    unicornhathd.show()
    for i in range(1, 10):
        unicornhathd.brightness(i / 10)
        unicornhathd.show()
        time.sleep(0.025)


def fade_out():
    """
    fade out brightness
    """
    unicornhathd.brightness(1)
    unicornhathd.show()
    for i in range(10, 1, -1):
        unicornhathd.brightness(i / 10)
        unicornhathd.show()
        time.sleep(0.025)


def getcolor():
    """
    choose a color at random
    taken from https://pynative.com/python-random-choice/#h-a-random-choice-from-a-2d-array

    """
    colors = np.array(
        [
            [255, 165, 0],  # orange
            [173, 216, 230],  # light blue
            [0, 255, 0],  # green
            [255, 0, 0],  # red
            [255, 192, 203],  # pink
            [32, 32, 32],  # dark gray
            [255, 255, 0],  # yellow
            [255, 0, 255],  # purple
        ]
    )
    color_choice = np.random.randint(len(colors), size=1)
    return colors[color_choice[0], :]


def main():
    """
    they call it main.
    """
    # random.seed()
    unicornhathd.rotation(0)
    unicornhathd.brightness(0)
    uhat = np.array(
        [
            [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0],
        ]
    )
    width, height = unicornhathd.get_shape()
    black = [0, 0, 0]
    try:
        while True:
            color = getcolor()
            for point_x in range(width):
                for point_y in range(height):
                    if uhat[point_x, point_y] == 0:
                        point_r, point_g, point_b = black
                    elif uhat[point_x, point_y] == 1:
                        point_r, point_g, point_b = (
                            (color[0] * 0.5),
                            (color[1] * 0.5),
                            (color[2] * 0.5),
                        )
                    elif uhat[point_x, point_y] == 2:
                        point_r, point_g, point_b = color
                    unicornhathd.set_pixel(point_x, point_y, point_r, point_g, point_b)
            unicornhathd.set_pixel(
                0, 0, 255, 255, 255
            )  # testing orientation with unicorn_hat_sim
            fade_in()
            unicornhathd.set_pixel(
                0, 0, 0, 0, 0
            )  # testing orientation with unicorn_hat_sim
            fade_out()
    except KeyboardInterrupt:
        unicornhathd.off()


if __name__ == "__main__":
    main()
