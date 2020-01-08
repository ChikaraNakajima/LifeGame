# -*- coding: utf-8 -*-
from tkinter import *


class FrameRGB(Frame):
    def __init__(self, master=None, text="Color", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        frame = (Frame(master=self), Frame(master=self))
        self.label = {
            "text": Label(master=frame[0], text=text),
            "color": Label(master=frame[0]),
        }
        self.scale = {
            "red": Scale(
                master=frame[1], label="Red", from_=0, to=255,
                orient=HORIZONTAL, command=self.apply,
            ),
            "green": Scale(
                master=frame[1], label="Green", from_=0, to=255,
                orient=HORIZONTAL, command=self.apply,
            ),
            "blue": Scale(
                master=frame[1], label="Blue", from_=0, to=255,
                orient=HORIZONTAL, command=self.apply,
            ),
        }
        frame[0].pack(fill=BOTH, side=LEFT, expand=1)
        frame[1].pack(fill=BOTH, side=LEFT, expand=1)
        self.label["text"].pack(fill=BOTH)
        self.label["color"].pack(fill=BOTH, expand=1)
        self.scale["red"].pack(fill=BOTH)
        self.scale["green"].pack(fill=BOTH)
        self.scale["blue"].pack(fill=BOTH)
        self.set()
        return None

    def apply(self, event=None):
        self.label["color"].configure(bg="#{0:02x}{1:02x}{2:02x}".format(
            self.scale["red"].get(),
            self.scale["green"].get(),
            self.scale["blue"].get(),
        ))
        return None

    def set(self, color=(0, 0, 0)):
        r, g, b = [int(i) for i in color[:3]]
        self.scale["red"].set(r)
        self.scale["green"].set(g)
        self.scale["blue"].set(b)
        self.apply()
        return None

    def get(self):
        return (
            self.scale["red"].get(),
            self.scale["green"].get(),
            self.scale["blue"].get(),
        )


class FrameCheckbuttons(Frame):
    def __init__(
        self, master=None, text="Checkbutton", labels=range(9),
        *args, **kwargs,
    ):
        super().__init__(master, *args, **kwargs)
        labels = tuple(str(i) for i in labels)
        self.value = tuple(StringVar() for i in labels)
        self.checkbutton = {u: Checkbutton(
            self, text=u, onvalue=u, offvalue="", variable=v,
        ) for u, v in zip(labels, self.value)}
        if text:
            Label(self, text=text).pack(fill=BOTH)
        for i in labels:
            self.checkbutton[i].pack(anchor=W)
        return None

    def set(self, config=None):
        if config:
            for i in self.checkbutton.values():
                i.deselect()
            for i in config:
                i = str(i)
                if i in self.checkbutton.keys():
                    self.checkbutton[i].select()
        return None

    def get(self):
        return tuple(i.get() for i in self.value if i.get())


class FrameRadiobutton(Frame):
    def __init__(
        self, master=None, text="Radiobutton", labels=range(9),
        *args, **kwargs,
    ):
        super().__init__(master, *args, **kwargs)
        labels = tuple(str(i) for i in labels)
        self.value = StringVar()
        self.radiobutton = {
            i: Radiobutton(self, text=i, value=i, variable=self.value)
            for i in labels
        }
        Label(self, text=text).pack(fill=BOTH)
        for i in labels:
            self.radiobutton[i].pack(anchor=W)
        self.set(labels[0])
        return None

    def set(self, value):
        value = str(value)
        if value in self.radiobutton.keys():
            self.value.set(value)
        return None

    def get(self):
        return self.value.get()


class FrameScale(Frame):
    def __init__(
        self, master=None,
        scale=(("Red", 0, 255), ("Green", 0, 255), ("Blue", 0, 255)),
        *args, **kwargs,
    ):
        super().__init__(master, *args, **kwargs)
        scale = tuple((str(p), int(q), int(r)) for p, q, r in scale)
        self.scale = {
            p: Scale(master=self, label=p, from_=q, to=r, orient=HORIZONTAL)
            for p, q, r in scale
        }
        for i in scale:
            self.scale[i[0]].pack(anchor=W)
        return None

    def set(self, scale):
        temp = set(self.scale.keys())
        for u, v in scale.items():
            u, v = str(u), int(v)
            if u in temp:
                self.scale[u].set(v)
        return None

    def get(self):
        return {u: v.get() for u, v in self.scale.items()}


if __name__ == "__main__":
    pass
