import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from lib.LifeGameConfigure import FrameLifeGame
from lib.tkWidget import *


class FrameProgressBar(tk.Frame):
    def __init__(
        self, master=None,
        lifegame=FrameLifeGame().get(),
        color_background=(255, 255, 255), color_font=(0, 0, 0),
        resolution=(1920, 1080), fps=30, second=60,
        *args, **kwargs
    ):
        super().__init__(master, *args, **kwargs)
        self.lifegame = lifegame
        self.color_font = color_font
        self.resolution = resolution
        self.fps = fps
        self.frame_number = fps * second
        self.background = Image.new("RGB", resolution, color_background)
        height, width = self.lifegame.lattice.shape
        rule = "/".join(["".join([str(j) for j in self.lifegame.rule[i]]) for i in [1, 0]])
        self.text = "\n".join([
            "Generation : {0:>5}",
            "Population : {1:>5}",
            "Rule       : {0:>5}".format(rule),
            "Width      : {0:>5}".format(width),
            "Height     : {0:>5}".format(height),
        ])
        size = self.lifegame.imsize[1]//20
        self.font = ImageFont.truetype(font="courbd.ttf", size=size)
        self.text_xy = (size + self.lifegame.imsize[1] , size)
        self.output = cv2.VideoWriter("./output.mp4", cv2.VideoWriter_fourcc(*"avc1"), self.fps, tuple(self.resolution))
        self.text_label = "{0:>" + str(len(str(self.frame_number))) + "}" + "/{0}".format(self.frame_number)
        self.label = tk.Label(self, text=self.text_label.format(self.lifegame.generation))
        self.label.pack()
        self.after(1, self.makemovie)
        return None

    def makemovie(self, *args, **kwargs):
        temp = self.background.copy()
        temp.paste(self.lifegame.imagepil, (0, 0))
        draw = ImageDraw.Draw(temp)
        draw.text(
            xy=self.text_xy,
            fill=self.color_font,
            font=self.font,
            text=self.text.format(self.lifegame.generation, self.lifegame.population),
        )
        self.output.write(np.uint8(temp))
        self.label.configure(text=self.text_label.format(self.lifegame.generation))
        self.lifegame.next()
        if self.frame_number == self.lifegame.generation:
            self.output.release()
            self.master.destroy()
        else:
            self.after(1, self.makemovie)
        return None


class FrameLifeGameMovieConfigure(tk.Frame):
    def __init__(self, master=None, flg=FrameLifeGame(), *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.flg = flg
        self.home = Path(__file__).resolve().parent
        self.json = self.home.joinpath("config_movie.json")
        frame = [tk.Frame(self), tk.Frame(self)]
        self.color_background = FrameRGB(master=frame[0], text="Background".center(16))
        self.color_font = FrameRGB(master=frame[0], text="Font".center(16))
        self.radiobutton = {
            "resolution": FrameRadiobutton(master=frame[1], text="resolution", labels=["1920 1080", "1280  720"]),
            "fps": FrameRadiobutton(master=frame[1], text="fps", labels=["30", "24"])
        }
        self.scale = tk.Scale(master=frame[1], label="second", from_=10, to=60, orient=tk.HORIZONTAL)
        self.button = {
            "start": tk.Button(master=frame[1], text="Start", command=self.start),
            "reset": tk.Button(master=frame[1], text="Reset", command=self.reset),
            "save": tk.Button(master=frame[1], text="Save", command=self.save),
        }
        for i in frame:
            i.pack(fill=tk.BOTH, side=tk.LEFT)
        self.color_background.pack(fill=tk.BOTH)
        self.color_font.pack(fill=tk.BOTH)
        self.radiobutton["resolution"].pack(fill=tk.BOTH)
        self.radiobutton["fps"].pack(fill=tk.BOTH)
        self.scale.pack(fill=tk.BOTH)
        self.button["start"].pack(fill=tk.BOTH, expand=1)
        self.button["reset"].pack(fill=tk.BOTH)
        self.button["save"].pack(fill=tk.BOTH)
        self.progress = None
        self.reset()
        return None

    def start(self):
        if isinstance(self.progress, tk.Toplevel) and self.progress.winfo_exists():
            return None
        kwargs = {
            "color_background": self.color_background.get(),
            "color_font": self.color_font.get(),
            "resolution": [int(i) for i in self.radiobutton["resolution"].get().split()],
            "fps": int(self.radiobutton["fps"].get()),
            "second": int(self.scale.get()),
        }
        config = self.flg.config()
        if "generation" in config["checkbutton"]:
            kwargs["lifegame"] = self.flg.get()
        else:
            config["checkbutton"].append("generation")
            self.flg.set(config)
            kwargs["lifegame"] = self.flg.get()
            config["checkbutton"].remove("generation")
            self.flg.set(config)
        self.progress = tk.Toplevel(self)
        temp = FrameProgressBar(master=self.progress, **kwargs)
        temp.pack()
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
        self.flg.set(config.get("lifegame", None))
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
