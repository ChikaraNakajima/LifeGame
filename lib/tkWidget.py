# -*- coding: utf-8 -*-
import tkinter as tk


class FrameRGB(tk.Frame):
    def __init__(self, master=None, text="Color", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        frame = (tk.Frame(master=self), tk.Frame(master=self))
        self.label = {
            "text": tk.Label(master=frame[0], text=text),
            "color": tk.Label(master=frame[0]),
        }
        self.scale = {
            "red": tk.Scale(
                master=frame[1], from_=0, to=255, label="Red",
                orient=tk.HORIZONTAL, command=self.apply,
            ),
            "green": tk.Scale(
                master=frame[1], from_=0, to=255, label="Green",
                orient=tk.HORIZONTAL, command=self.apply,
            ),
            "blue": tk.Scale(
                master=frame[1], from_=0, to=255, label="Blue",
                orient=tk.HORIZONTAL, command=self.apply,
            ),
        }
        frame[0].pack(fill=tk.BOTH, side=tk.LEFT, expand=1)
        frame[1].pack(fill=tk.BOTH, side=tk.LEFT, expand=1)
        self.label["text"].pack(fill=tk.BOTH)
        self.label["color"].pack(fill=tk.BOTH, expand=1)
        self.scale["red"].pack(fill=tk.BOTH)
        self.scale["green"].pack(fill=tk.BOTH)
        self.scale["blue"].pack(fill=tk.BOTH)
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
        return (self.scale["red"].get(), self.scale["green"].get(), self.scale["blue"].get())


class FrameCheckbuttons(tk.Frame):
    def __init__(
        self, master=None, text="Checkbutton", labels=range(9),
        *args, **kwargs,
    ):
        super().__init__(master, *args, **kwargs)
        labels = tuple(str(i) for i in labels)
        self.value = tuple(tk.StringVar() for i in labels)
        self.checkbutton = {u: tk.Checkbutton(
            self, text=u, onvalue=u, offvalue="", variable=v,
        ) for u, v in zip(labels, self.value)}
        if text:
            tk.Label(self, text=text).pack(fill=tk.BOTH)
        for i in labels:
            self.checkbutton[i].pack(anchor=tk.W)
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


class FrameRadiobutton(tk.Frame):
    def __init__(
        self, master=None, text="Radiobutton", labels=range(9),
        *args, **kwargs,
    ):
        super().__init__(master, *args, **kwargs)
        labels = [str(i) for i in labels]
        self.value = tk.StringVar()
        self.radiobutton = {
            i: tk.Radiobutton(self, text=i, value=i, variable=self.value)
            for i in labels
        }
        if text:
            tk.Label(self, text=text).pack(fill=tk.BOTH)
        for i in labels:
            self.radiobutton[i].pack(anchor=tk.W)
        self.set(labels[0])
        return None

    def set(self, value):
        value = str(value)
        if value in self.radiobutton.keys():
            self.value.set(value)
        return None

    def get(self):
        return self.value.get()


class FrameScale(tk.Frame):
    def __init__(
        self, master=None,
        scale=(("Red", 0, 255), ("Green", 0, 255), ("Blue", 0, 255)),
        *args, **kwargs,
    ):
        super().__init__(master, *args, **kwargs)
        scale = [(str(p), int(q), int(r)) for p, q, r in scale]
        self.scale = {
            p: tk.Scale(master=self, label=p, from_=q, to=r, orient=tk.HORIZONTAL)
            for p, q, r in scale
        }
        for i in scale:
            self.scale[i[0]].pack(anchor=tk.W)
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
