# -*- coding: utf-8 -*-
from LifeGame import LifeGame
from tkWidget import *


class FrameRule(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.frame = (
            FrameCheckbuttons(self, text="Survive", labels=range(9)),
            FrameCheckbuttons(self, text="Birth", labels=range(9)),
        )
        self.frame[0].pack(fill=tk.BOTH, side=tk.LEFT)
        self.frame[1].pack(fill=tk.BOTH, side=tk.LEFT)
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


class FrameLifeGame(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        frame = [tk.Frame(self), tk.Frame(self), tk.Frame(self)]
        self.color_1 = FrameRGB(master=frame[0], text="Living Cell".center(12))
        self.color_0 = FrameRGB(master=frame[0], text="Dead Cell".center(12))
        self.rule = FrameRule(frame[1])
        self.checkbutton = FrameCheckbuttons(frame[2],text="others", labels=["top bottom", "left right", "generation"])
        self.scale = FrameScale(master=frame[2], scale=(("width", 120, 360), ("height", 120, 360), ("pixel", 1, 6), ("probability", 1, 100)))
        for i in frame:
            i.pack(fill=tk.BOTH, side=tk.LEFT)
        self.color_1.pack(fill=tk.BOTH)
        self.color_0.pack(fill=tk.BOTH)
        self.rule.pack(fill=tk.BOTH)
        self.scale.pack(fill=tk.BOTH)
        self.checkbutton.pack(fill=tk.BOTH)
        self.set()
        return None

    def set(self, config=None, *args, **kwargs):
        if not isinstance(config, dict):
            config = {}
        self.color_0.set(config.get("color_0", [72, 72, 96]))
        self.color_1.set(config.get("color_1", [255, 195, 191]))
        self.rule.set(config.get("rule", "23/3"))
        self.checkbutton.set(config.get("checkbutton", ["top bottom", "left right", "generation"]))
        self.scale.set(config.get("scale", {"width": 300, "height": 240, "pixel": 2, "probability": 15}))
        return None

    def get(self, *args, **kwargs):
        temp_scale = self.scale.get()
        temp_checkbutton = self.checkbutton.get()
        temp_checkbutton = {i: i in temp_checkbutton for i in ["top bottom", "left right", "generation"]}
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


if __name__ == "__main__":
    temp = FrameLifeGame()
    temp.pack()
    temp.mainloop()
