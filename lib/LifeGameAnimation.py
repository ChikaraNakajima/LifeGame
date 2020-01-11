# -*- coding: utf-8 -*-
import json
from pathlib import Path
import tkinter as tk
import tkinter.font as Font
from LifeGameConfigure import FrameLifeGame


class FrameLifeGameAnimationConfigure(tk.Frame):
    def __init__(self, master=None, flg=FrameLifeGame(), *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.flg = flg
        self.home = Path(__file__).resolve().parent
        self.json = self.home.joinpath("config_animation.json")
        self.interval = tk.Scale(master=self, label="interval", from_=10, to=100, orient=tk.HORIZONTAL)
        self.button = {
            "start": tk.Button(master=self, text="Start", command=self.start),
            "stop" : tk.Button(master=self, text="Stop",  command=self.stop, state=tk.DISABLED),
            "reset": tk.Button(master=self, text="Reset", command=self.reset),
            "save" : tk.Button(master=self, text="Save",  command=self.save),
        }
        self.interval.pack(fill=tk.BOTH)
        self.button["start"].pack(fill=tk.BOTH, expand=1)
        self.button["stop"].pack(fill=tk.BOTH, expand=1)
        self.button["reset"].pack(fill=tk.BOTH)
        self.button["save"].pack(fill=tk.BOTH)
        self.reset()
        return None

    def start(self):
        self.button["start"].configure(state=tk.DISABLED)
        self.button["stop"].configure(state=tk.NORMAL)
        self.button["reset"].configure(state=tk.DISABLED)
        self.button["save"].configure(state=tk.DISABLED)
        self.lga = tk.Toplevel(self)
        temp = FrameLifeGameAnimation(master=self.lga, interval=self.interval.get(), lifegame=self.flg.get())
        temp.pack()
        return None

    def stop(self):
        self.button["start"].configure(state=tk.NORMAL)
        self.button["stop"].configure(state=tk.DISABLED)
        self.button["reset"].configure(state=tk.NORMAL)
        self.button["save"].configure(state=tk.NORMAL)
        if self.lga.winfo_exists():
            self.lga.destroy()
        return None

    def reset(self):
        if self.json.is_file():
            config = json.loads(self.json.read_text())
        else:
            config = {}
        self.interval.set(config.get("interval", 10))
        self.flg.set(config.get("lifegame", None))
        return None

    def save(self):
        config = {
            "interval": self.interval.get(),
            "lifegame": self.flg.config(),
        }
        self.json.write_text(json.dumps(config))
        return None


class FrameLifeGameAnimation(tk.Frame):
    def __init__(self, master=None, interval=10, lifegame=FrameLifeGame().get(), *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master.title("LifeGame")
        self.interval = interval
        self.lifegame = lifegame
        if "generation" in dir(self.lifegame):
            self.text = "  Generation : {0:>5}\n  Population : {1:>5}"
            self.label_info = tk.Label(self, anchor="w", font=Font.Font(self, family="Courier New", size=24, weight="bold"))
            self.label_info.pack(fill=tk.BOTH, expand=1)
            def deco(func):
                def wrap():
                    self.label_info.configure(text=self.text.format(self.lifegame.generation, self.lifegame.population))
                    func()
                return wrap
            self.next = deco(self.next)
        self.image = lifegame.imagetk
        self.label = tk.Label(self, image=self.image)
        self.label.pack()
        self.after(self.interval, self.next)
        return None

    def next(self):
        self.image = self.lifegame.imagetk
        self.label.configure(image=self.image)
        self.lifegame.next()
        self.after(self.interval, self.next)
        return None


if __name__ == "__main__":
    pass
