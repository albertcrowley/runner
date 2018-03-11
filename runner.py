import kivy
kivy.require('1.1.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

from flappy import Sprite
from kivy_fix import SpriteAtlas
from flappy import params
from flappy import Background
from kivy.uix.label import Label
from flappy import Blank
from kivy.core.window import Window

import math

class Terrain(Widget):

    def __init__(self, screen_dim, floor):
        super(Terrain, self).__init__(pos=(0,0))
        self.tiles = SpriteAtlas("jungle_tileset.atlas")


        self.filled_to = 0
        self.screen_dim = screen_dim
        self.elements = []
        self.velocity = -4 * params.scale

        while not self.fill():
            pass


    def fill(self):
        if self.filled_to < self.screen_dim[0]:
            floor = Sprite(texture=self.tiles['floor'], pos=(self.filled_to, -7 * params.scale))
            self.elements.append(floor)
            self.add_widget(floor)

            self.filled_to = self.filled_to + floor.width
        else:
            return True

    def update(self):
        for e in self.elements:
            e.pos.x = e.pos.x - self.velocity


class Player(Sprite):

    def __init__(self, pos, floor):
        self.images = SpriteAtlas('RUN.atlas')
        super(Player, self).__init__(texture=self.images['1'], pos=pos)
        self.velocity_y = 0
        self.gravity = -.3 * params.scale
        self.ticks = 0;
        self.floor = floor

    def update(self):
        self.ticks += 1
        if self.y < self.floor:
            self.velocity_y = 0;
        else:
            self.velocity_y += self.gravity
            self.velocity_y = max(self.velocity_y, -10 * params.scale)
            self.y += self.velocity_y
        frame = int(math.floor( self.ticks / 10)) % 8
        self.texture = self.images[str(frame)]

    def jump(self):
        if self.y < self.floor:
            self.velocity_y = 10;
            self.y = self.floor+1

        print "jump"

    # def on_touch_down(self, *ignore):
    #     self.velocity_y = 5.5 * params.scale
    #     self.texture = self.images['wing-down']

#
# class PongPaddle(Widget):
#     score = NumericProperty(0)
#
#     def bounce_ball(self, ball):
#         if self.collide_widget(ball):
#             vx, vy = ball.velocity
#             offset = (ball.center_y - self.center_y) / (self.height / 2)
#             bounced = Vector(-1 * vx, vy)
#             vel = bounced * 1.1
#             ball.velocity = vel.x, vel.y + offset


class PongGame(Widget):
    def __init__(self):
        super(PongGame, self).__init__()
        Clock.schedule_interval(self.update, 1.0 / 60.0)

        self.background = Background(source='background.png')
        self.size = self.background.size
        Window.size = (self.size[0], self.size[1])
        params.init()
        self.floor = 35 * params.scale

        self.add_widget(self.background)
        self.score_label = Label(center_x=self.center_x,
            top=self.top - 30 * params.scale, text="0")
        self.add_widget(self.score_label)
        self.over_label = Label(center=self.center, opacity=0,
            text="Game Over")
        self.add_widget(self.over_label)
        # self.add_widget(Blank(*params.blank_rect))
        self.game_over = False
        self.score = 0
        self.player= Player(pos=(20 * params.scale, self.height / 2), floor = self.floor);
        self.add_widget(self.player)
        self.add_widget(Blank(*params.blank_rect))

        self.terrain = Terrain(screen_dim=(self.size[0], self.size[1]), floor=self.floor)
        self.add_widget(self.terrain)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)


    def update(self, dt):
        self.background.update()
        self.player.update()

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'spacebar':
            self.jump()
        return True

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def on_touch_down(self, touch):
        self.jump()

    def jump(self):
        print("touch")
        self.player.jump()
        self.score += 5
        self.score_label.text = str(self.score)


class Runner(App):
    def build(self):
        params.init()
        game = Widget()
        pg = PongGame()
        game.add_widget(pg)
        return game


if __name__ == '__main__':
    Runner().run()
