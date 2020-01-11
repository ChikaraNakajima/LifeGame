# -*- coding: utf-8 -*-
import numpy as np
from PIL.Image import fromarray
from PIL.ImageTk import PhotoImage


class LifeGame:
    def __init__(
        self,
        color_0=(29, 29, 29),
        color_1=(26, 195, 191),
        rule="23/3",
        width=120,
        height=120,
        pixel=6,
        probability=20,
        tb=True,
        lr=True,
        generation=False,
        *args, **kwargs
    ):
        width = int(width)
        height = int(height)
        self.lattice = np.zeros([height, width], dtype=int)
        self.lattice[np.random.randint(1, 100, [height, width]) <= probability] = 1
        temp = [-1, 0, 1]
        self.ij = [(u, v) for u in temp for v in temp if u or v]
        self.rule = {
            u: sorted({int(i) for i in v if i in "012345678"})
            for u, v in enumerate(rule.split("/")[::-1])
        }
        self.imarray = np.zeros([height, width, len(color_0)], dtype=np.uint8)
        self.color_0 = np.uint8(color_0)
        self.color_1 = np.uint8(color_1)
        pixel = int(pixel)
        self.imsize = (pixel*width, pixel*height)
        if not tb:
            def deco(func):
                temp = np.zeros(width, dtype=int)
                self.lattice[0] = temp
                self.lattice[-1] = temp
                def wrap():
                    func()
                    self.lattice[0] = temp
                    self.lattice[-1] = temp
                    return None
                return wrap
            self.next = deco(self.next)
        if not lr:
            def deco(func):
                temp = np.zeros(height, dtype=int)
                self.lattice[:, 0] = temp
                self.lattice[:, -1] = temp
                def wrap():
                    func()
                    self.lattice[:, 0] = temp
                    self.lattice[:, -1] = temp
                    return None
                return wrap
            self.next = deco(self.next)
        if generation:
            def deco(func):
                self.generation = 0
                def wrap():
                    func()
                    self.generation += 1
                    return None
                return wrap
            self.next = deco(self.next)
        return None

    def next(self):
        temp = sum([
            np.roll(self.lattice, shift=i, axis=(0, 1))
            for i in self.ij
        ])
        self.lattice = sum([
            (self.lattice == u) * sum([temp == i for i in v])
            for u, v in self.rule.items()
        ])
        return None

    @property
    def imagearray(self):
        self.imarray[self.lattice == 0] = self.color_0
        self.imarray[self.lattice == 1] = self.color_1
        return self.imarray

    @property
    def imagepil(self):
        return fromarray(self.imagearray).resize(self.imsize)

    @property
    def imagetk(self):
        return PhotoImage(self.imagepil)

    @property
    def population(self):
        return np.count_nonzero(self.lattice)


if __name__ == "__main__":
    pass
