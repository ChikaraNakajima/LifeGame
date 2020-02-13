# -*- coding: utf-8 -*-
import tkinter as tk
from lib.LifeGameConfigure import FrameLifeGame
from lib.LifeGameAnimation import FrameLifeGameAnimationConfigure
from lib.LifeGameMovie import FrameLifeGameMovieConfigure


class FrameIntegration(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master.title("LifeGame")
        edge = {"bd": 2, "relief": "ridge"}
        self.lifegame = FrameLifeGame(self, **edge)
        self.movie = FrameLifeGameMovieConfigure(self, flg=self.lifegame, **edge)
        self.animation = FrameLifeGameAnimationConfigure(self, flg=self.lifegame, **edge)
        self.lifegame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.animation.pack(fill=tk.BOTH, side=tk.LEFT)
        self.movie.pack(fill=tk.BOTH, side=tk.LEFT)
        return None


if __name__ == "__main__":
    temp = FrameIntegration()
    temp.pack()
    temp.mainloop()
