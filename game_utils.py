import random
import kivy
import platform

kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.logger import Logger
from kivy.metrics import Metrics
from kivy.graphics import Color, Rectangle
from kivy_fix import SpriteAtlas


class MultiSound(object):
    def __init__(self, file, num):
        self.num = num
        self.sounds = [SoundLoader.load(file) for n in range(num)]
        self.index = 0

    def play(self):
        self.sounds[self.index].play()
        self.index += 1
        if self.index == self.num:
            self.index = 0



class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(allow_stretch=True, **kwargs)
        self.texture.mag_filter = 'nearest'
        w, h = self.texture_size
        self.size = (params.scale * w, params.scale * h)



class Background(Widget):
    def __init__(self, source):
        super(Background, self).__init__()
        self.image = Sprite(source=source)
        self.add_widget(self.image)
        self.size = self.image.size
        self.image_dupe = Sprite(source=source, x=self.width)
        self.add_widget(self.image_dupe)

    def update(self, dt):
        self.image.x -= 60 * params.scale * dt
        self.image_dupe.x -= 60 * params.scale * dt
        if self.image.right <= 0:
            self.image.x = 0
            self.image_dupe.x = self.width


class Ground(Sprite):
    def update(self):
        self.x -= 2 * params.scale
        if self.x < -24 * params.scale:
            self.x += 24 * params.scale

class Blank(Widget):
    def __init__(self, pos, size):
        super(Blank, self).__init__()
        with self.canvas:
            Color(0, 0, 0)
            Rectangle(pos=pos, size=size)
            Color(1, 1, 1)


class params(object):
    def init(self):
        self.bg_width, self.bg_height = 288, 384

        # if platform.system() == "Windows":

        if Window != None:
            self.width, self.height = Window.size
        else:
            self.width, self.height = (288, 384)
            self.scale = 1
            ws = 1
            hs = 1
            self.scale = min(ws,hs)
            return
        self.center = Window.center
        ws = float(self.width) / self.bg_width
        hs = float(self.height) / self.bg_height
        self.scale = min(ws, hs)
        print "set scale"
        Logger.info('size=%r; dpi=%r; density=%r; SCALE=%r',
            Window.size, Metrics.dpi, Metrics.density, self.scale)
        if ws > hs:
            gap = self.width - (self.bg_width * hs)
            self.blank_rect = ((self.width - gap, 0), (gap, self.height))
        else:
            gap = self.height - (self.bg_height * ws)
            self.blank_rect = ((0, self.height - gap), (self.width, gap))
params = params()



