# -*- coding: utf-8 -*-
from pathlib import Path
from LifeGame import LifeGame
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2


def main():
    width = 240
    height = 240
    rule = "23/3"
    pixel = 3
    home = Path(__file__).resolve().parent
    result = home.joinpath(datetime.now().strftime("%Y%m%d-%H%M%S"))
    result.mkdir(exist_ok=True)
    lg = LifeGame(
        width=width,
        height=height,
        generation=True,
        probability=15,
        rule=rule,
        pixel=pixel,
        color_0=(64, 64, 64, ),
        color_1=(192, 192, 255, ),
    )
    text = "\n".join([
        "Generation : {0:>5}",
        "Population : {1:>5}",
        "Rule       : {0:>5}".format(rule),
        "Width      : {0:>5}".format(width),
        "Height     : {0:>5}".format(height),
    ])
    background = Image.new("RGB", (1280, 720), (209, 240, 251, ))
    font = ImageFont.truetype(font="courbd.ttf", size=36)
    output = cv2.VideoWriter(
        str(result.joinpath("output.mp4")),
        cv2.VideoWriter_fourcc(*"avc1"),
        30.0,
        (1280, 720),
    )
    for i in range(180):
        temp = background.copy()
        temp.paste(lg.imagepil, (0, 0))
        draw = ImageDraw.Draw(temp)
        draw.text(
            xy=(756, 36),
            fill="black",
            font=font,
            text=text.format(lg.generation, lg.population),
        )
        output.write(np.uint8(temp))
        lg.next()
    output.release()
    return None


if __name__ == "__main__":
    main()
