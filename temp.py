# -*- coding: utf-8 -*-
from datetime import datetime
import json
from pathlib import Path
import tkinter.font as font

import cv2
import PIL
from PIL import ImageDraw, ImageFont
import numpy as np

from lib.LifeGame import LifeGame
from lib.tkWidget import *

home = Path(__file__).resolve().with_name("lib")

class FrameRule(Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.frame = (
            FrameCheckbuttons(self, text="Survive", labels=range(9)),
            FrameCheckbuttons(self, text="Birth", labels=range(9)),
        )
        self.frame[0].pack(fill=BOTH, side=LEFT)
        self.frame[1].pack(fill=BOTH, side=LEFT)
        self.set()
        return None

    def set(self, rule="23/3"):
        temp = rule.split("/")
        self.frame[0].set(temp[0])
        self.frame[1].set(temp[1])
        return None

    def get(self):
        rule = "/".join([
            "".join([str(i) for i in self.frame[0].get()]),
            "".join([str(i) for i in self.frame[1].get()]),
        ])
        return rule


class FrameLifeGame(Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        frame = [Frame(self), Frame(self), Frame(self)]
        self.color_1 = FrameRGB(master=frame[0], text="Living Cell".center(12))
        self.color_0 = FrameRGB(master=frame[0], text="Dead Cell".center(12))
        self.rule = FrameRule(frame[1])
        self.checkbutton = FrameCheckbuttons(
            frame[2],
            text="others",
            labels=["top bottom", "left right", "generation"]
        )
        self.scale = FrameScale(
            master=frame[2],
            scale=(("width", 120, 360), ("height", 120, 360), ("pixel", 1, 6), ("probability", 1, 100)),
        )
        for i in frame:
            i.pack(fill=BOTH, side=LEFT)
        self.color_1.pack(fill=BOTH)
        self.color_0.pack(fill=BOTH)
        self.rule.pack(fill=BOTH)
        self.scale.pack(fill=BOTH)
        self.checkbutton.pack(fill=BOTH)
        self.set()
        return None

    def set(self, config=None, *args, **kwargs):
        if not isinstance(config, dict):
            config = {}
        self.color_0.set(config.get("color_0", [72, 72, 96]))
        self.color_1.set(config.get("color_1", [255, 195, 191]))
        self.rule.set(config.get("rule", "23/3"))
        self.checkbutton.set(config.get("checkbutton", ["top bottom", "left right"]))
        self.scale.set(config.get("scale", {
            "width": 300,
            "height": 240,
            "pixel": 2,
            "probability": 15,
        }))
        return None

    def get(self, *args, **kwargs):
        temp_scale = self.scale.get()
        temp_checkbutton = self.checkbutton.get()
        temp_checkbutton = {
            i: i in temp_checkbutton
            for i in ["top bottom", "left right", "generation"]
        }
        lg = LifeGame(
            color_0=self.color_0.get(),
            color_1=self.color_1.get(),
            rule=self.rule.get(),
            width=temp_scale["width"],
            height=temp_scale["height"],
            pixel=temp_scale["pixel"],
            probability=temp_scale["probability"],
            tb=temp_checkbutton["top bottom"],
            lr=temp_checkbutton["left right"],
            generation=temp_checkbutton["generation"],
        )
        return lg

    def config(self, *args, **kwargs):
        config = {
            "color_0": self.color_0.get(),
            "color_1": self.color_1.get(),
            "rule": self.rule.get(),
            "scale": self.scale.get(),
            "checkbutton": self.checkbutton.get(),
        }
        return config


class FrameLifeGameAnimationConfigure(Frame):
    def __init__(self, master=None, flg=FrameLifeGame(), *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.flg = flg
        self.json = home.joinpath("config_animation.json")
        self.interval = Scale(master=self, label="interval", from_=10, to=100, orient=HORIZONTAL)
        self.button = {
            "start": Button(master=self, text="Start", command=self.start),
            "stop": Button(master=self, text="Stop", command=self.stop, state=DISABLED),
            "reset": Button(master=self, text="Reset", command=self.reset),
            "save": Button(master=self, text="Save", command=self.save),
        }
        self.interval.pack(fill=BOTH)
        self.button["start"].pack(fill=BOTH, expand=1)
        self.button["stop"].pack(fill=BOTH, expand=1)
        self.button["reset"].pack(fill=BOTH)
        self.button["save"].pack(fill=BOTH)
        self.reset()
        return None

    def start(self):
        self.button["start"].configure(state=DISABLED)
        self.button["stop"].configure(state=NORMAL)
        self.button["reset"].configure(state=DISABLED)
        self.button["save"].configure(state=DISABLED)
        self.LGI = Toplevel(self)
        temp = FrameLifeGameAnimation(master=self.LGI, interval=self.interval.get(), lifegame=self.flg.get())
        temp.pack()
        return None

    def stop(self):
        self.button["start"].configure(state=NORMAL)
        self.button["stop"].configure(state=DISABLED)
        self.button["reset"].configure(state=NORMAL)
        self.button["save"].configure(state=NORMAL)
        if self.LGI.winfo_exists():
            self.LGI.destroy()
        del self.LGI
        return None

    def reset(self):
        if self.json.is_file():
            config = json.loads(self.json.read_text())
            self.interval.set(config["interval"])
            self.flg.set(config["lifegame"])
        return None

    def save(self):
        config = {
            "interval": self.interval.get(),
            "lifegame": self.flg.config(),
        }
        self.json.write_text(json.dumps(config))
        return None


class FrameLifeGameAnimation(Frame):
    def __init__(self, master=None, interval=10, lifegame=LifeGame(), *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.interval = interval
        self.lifegame = lifegame
        self.image = lifegame.imagetk
        self.label = Label(self, image=self.image)
        if "generation" in dir(self.lifegame):
            self.text = "\n".join(["  Generation : {0:>5}", "  Population : {1:>5}"])
            font_info = font.Font(self, family="Courier New", size=20, weight="bold")
            self.label_info = Label(
                self,
                anchor="w",
                font=font_info,
            )
            self.label_info.pack(fill=BOTH, expand=1)
            def deco(func):
                def wrap():
                    self.label_info.configure(text=self.text.format(self.lifegame.generation, self.lifegame.population))
                    func()
                return wrap
            self.next = deco(self.next)
        self.label.pack()
        self.after(self.interval, self.next)
        return None

    def next(self):
        self.image = self.lifegame.imagetk
        self.label.configure(image=self.image)
        self.lifegame.next()
        self.after(self.interval, self.next)
        return None


class FrameLifeGameMovieConfigure(Frame):
    def __init__(self, master=None, flg=FrameLifeGame(), *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.flg = flg
        self.json = home.joinpath("config_movie.json")
        frame = [Frame(self), Frame(self)]
        self.color_background = FrameRGB(master=frame[0], text="Background".center(16))
        self.color_font = FrameRGB(master=frame[0], text="Font".center(16))
        self.radiobutton = {
            "resolution": FrameRadiobutton(master=frame[1], text="resolution", labels=["1920 1080", "1280  720"]),
            "fps": FrameRadiobutton(master=frame[1], text="fps", labels=["30", "24"])
        }
        self.scale = Scale(
            master=frame[1], label="second", from_=10, to=60,
            orient=HORIZONTAL
        )
        self.button = {
            "start": Button(master=frame[1], text="Start", command=self.start),
            "reset": Button(master=frame[1], text="Reset", command=self.reset),
            "save": Button(master=frame[1], text="Save", command=self.save),
        }
        for i in frame:
            i.pack(fill=BOTH, side=LEFT)
        self.color_background.pack(fill=BOTH)
        self.color_font.pack(fill=BOTH)
        self.radiobutton["resolution"].pack(fill=BOTH)
        self.radiobutton["fps"].pack(fill=BOTH)
        self.scale.pack(fill=BOTH)
        self.button["start"].pack(fill=BOTH, expand=1)
        self.button["reset"].pack(fill=BOTH)
        self.button["save"].pack(fill=BOTH)
        self.reset()
        return None

    def start(self):
        self.button["start"].configure(state=DISABLED)
        config = self.flg.config()
        if "generation" in config["checkbutton"]:
            lifegame = self.flg.get()
        else:
            config["checkbutton"] = ["generation"] + list(config["checkbutton"])
            self.flg.set(config)
            lifegame = self.flg.get()
            config["checkbutton"].remove("generation")
            self.flg.set(config)
        self.button["start"].configure(state=NORMAL)
        return None

    def reset(self):
        if self.json.is_file():
            config = json.loads(self.json.read_text())
        else:
            config = {}
        self.color_background.set(config.get("color_background", [209, 240, 251]))
        self.color_font.set(config.get("color_font", [0, 0, 0]))
        self.radiobutton["resolution"].set(config.get("resolution", "1920 1080"))
        self.radiobutton["fps"].set(config.get("fps", 30))
        self.scale.set(config.get("second", 60))
        self.flg.set(config.get("lifegame", {}))
        return None

    def save(self):
        config = {
            "color_background": self.color_background.get(),
            "color_font": self.color_font.get(),
            "resolution": self.radiobutton["resolution"].get(),
            "fps": self.radiobutton["fps"].get(),
            "second": self.scale.get(),
            "lifegame": self.flg.config(),
        }
        self.json.write_text(json.dumps(config))
        return None


class FrameIntegration(Frame):
    def __init__(self, master=None, lifegame=LifeGame(), *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master.title("LifeGame")
        self.lifegame = FrameLifeGame(self, bd=2, relief="ridge")
        self.animation = FrameLifeGameAnimationConfigure(self, flg=self.lifegame, bd=2, relief="ridge")
        self.movie = FrameLifeGameMovieConfigure(self, flg=self.lifegame, bd=2, relief="ridge")
        self.lifegame.pack(fill=BOTH, side=LEFT)
        self.animation.pack(fill=BOTH, side=LEFT)
        self.movie.pack(fill=BOTH, side=LEFT)
        return None


if __name__ == "__main__":
    temp = FrameIntegration()
    temp.pack(fill=BOTH)
    temp.mainloop()
