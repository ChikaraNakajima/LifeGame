# -*- coding: utf-8 -*-
import json
from pathlib import Path
from LifeGame import LifeGame
from tkWidget import *


class FrameLifeGame(Frame):
    def __init__(self, master=None, interval=10, lifegame=LifeGame(), *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master.title("Life Game")
        self.interval = interval
        self.lifegame = lifegame
        self.image = lifegame.imagetk
        self.label = Label(self, image=self.image)
        self.label.pack()
        self.after(self.interval, self.next)
        return None

    def next(self):
        self.lifegame.next()
        self.image = self.lifegame.imagetk
        self.label.configure(image=self.image)
        self.after(self.interval, self.next)
        return None


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
        return "/".join([
            "".join([str(i) for i in self.frame[0].get()]),
            "".join([str(i) for i in self.frame[1].get()]),
        ])


class FrameConfigure(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("Life Game")
        self.json = Path(__file__).resolve().with_suffix(".json")
        frame = (Frame(self), Frame(self), Frame(self), Frame(self))
        self.color = (
            FrameRGB(master=frame[0], text="Living Cell"),
            FrameRGB(master=frame[0], text="Dead Cell"),
        )
        self.loop = (
            FrameRadiobutton(master=frame[1], text="Top Bottom", labels=("True", "False")),
            FrameRadiobutton(master=frame[2], text="Left Right", labels=("True", "False")),
        )
        self.rule = FrameRule(frame[1])
        self.scale = FrameScale(
            master=frame[2],
            scale=(
                ("width", 12, 300),
                ("height", 12, 300),
                ("probability", 1, 99),
                ("pixel", 1, 12),
                ("interval", 10, 1000),
            ),
        )
        self.button = {
            "start": Button(master=frame[3], text="Start", command=self.start),
            "stop": Button(master=frame[3], text="Stop", command=self.stop, state=DISABLED),
            "reset": Button(master=frame[3], text="Reset", command=self.reset),
            "save": Button(master=frame[3], text="Save", command=self.save),
        }
        self.reset()
        for i in frame:
            i.pack(fill=BOTH, side=LEFT)
        self.color[0].pack(fill=BOTH)
        self.color[1].pack(fill=BOTH)
        self.loop[0].pack(fill=BOTH)
        self.loop[1].pack(fill=BOTH)
        self.rule.pack(fill=BOTH)
        self.scale.pack(fill=BOTH)
        self.button["start"].pack(fill=BOTH, expand=1)
        self.button["stop"].pack(fill=BOTH, expand=1)
        self.button["reset"].pack(fill=BOTH)
        self.button["save"].pack(fill=BOTH)
        return None

    def start(self):
        self.button["start"].configure(state=DISABLED)
        self.button["stop"].configure(state=NORMAL)
        self.button["reset"].configure(state=DISABLED)
        self.button["save"].configure(state=DISABLED)
        config = self.config()
        self.LGI = Toplevel(self)
        FrameLifeGame(
            master=self.LGI,
            interval=config["interval"],
            lifegame=LifeGame(**config["lifegame"])
        ).pack()
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
            with self.json.open(mode="r", encoding="utf-8") as fo:
                config = json.load(fo)
        else:
            config = {
                "interval": 20,
                "lifegame": {
                    "tb": True,
                    "lr": True,
                    "rule": "23/3",
                    "width": 120,
                    "height": 120,
                    "probability": 20,
                    "pixel": 3,
                    "color_0":(29, 29, 29),
                    "color_1": (26, 195, 191),
                },
            }
        self.color[0].set(config["lifegame"]["color_1"])
        self.color[1].set(config["lifegame"]["color_0"])
        self.loop[0].set(config["lifegame"]["tb"])
        self.loop[1].set(config["lifegame"]["lr"])
        self.rule.set(config["lifegame"]["rule"])
        self.scale.set({
            "width": config["lifegame"]["width"],
            "height": config["lifegame"]["height"],
            "probability": config["lifegame"]["probability"],
            "pixel": config["lifegame"]["pixel"],
            "interval": config["interval"],
        })
        return None

    def save(self):
        with self.json.open(mode="w", encoding="utf-8") as fo:
            json.dump(self.config(), fo, ensure_ascii=False, indent=4, sort_keys=True)
        return None

    def config(self):
        temp = self.scale.get()
        return {
            "interval": temp["interval"],
            "lifegame": {
                "tb": self.loop[0].get() == "True",
                "lr": self.loop[1].get() == "True",
                "rule": self.rule.get(),
                "width": temp["width"],
                "height": temp["height"],
                "probability": temp["probability"],
                "pixel": temp["pixel"],
                "color_0": self.color[1].get(),
                "color_1": self.color[0].get(),
            },
        }


if __name__ == "__main__":
    root = Tk()
    FrameConfigure(master=root).pack(fill=BOTH)
    root.mainloop()
