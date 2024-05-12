from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

from random import randint

class Player(Image):
    def move_to(self, pos):
        self.center_x = pos[0]
        self.center_y = pos[1]

class Asteroid(Image):
    velocity_y = -3

    def move(self):
        if self.parent:
            self.y += self.velocity_y

class Star(Image):
    velocity_y = -2

    def move(self):
        if self.parent:
            self.y += self.velocity_y

class GameWidget(Widget):
    player = ObjectProperty(None)
    game_over = False
    background = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_game()

    def start_game(self):
        self.clear_widgets()
        self.background = Image(source='background2.jpg', allow_stretch=True, keep_ratio=False, size=Window.size)
        self.add_widget(self.background)
        self.player = Player(source='spaceship.png', size=(100, 100), x=Window.width / 2, y=Window.height / 2)
        self.add_widget(self.player)
        Clock.schedule_interval(self.spawn_asteroid, 1.5)
        Clock.schedule_interval(self.spawn_star, 3)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.game_over = False

    def spawn_asteroid(self, dt):
        if not self.game_over:
            asteroid = Asteroid(source='asteroid.png', size=(80, 80), x=randint(0, self.width), y=self.height)
            self.add_widget(asteroid)

    def spawn_star(self, dt):
        if not self.game_over:
            star = Star(source='star.png', size=(50, 50), x=randint(0, self.width), y=self.height)
            self.add_widget(star)

    def on_touch_move(self, touch):
        if not self.game_over:
            self.player.move_to(touch.pos)

    def update(self, dt):
        if not self.game_over:
            for child in list(self.children):
                if isinstance(child, Asteroid):
                    child.move()
                    if child.y < 0 or self.player.collide_widget(child):
                        if self.player.collide_widget(child):
                            self.end_game()
                        self.remove_widget(child)
                elif isinstance(child, Star):
                    child.move()
                    if child.y < 0 or self.player.collide_widget(child):
                        self.remove_widget(child)

    def end_game(self):
        self.game_over = True
        self.player.source = 'explosion.png'
        Clock.unschedule(self.update)
        info_layout = BoxLayout(orientation='vertical', size_hint=(None, None), size=(300, 200), pos=(Window.width / 2 - 150, Window.height / 2 - 100))
        stars_label = Label(text='Stars collected: ', size_hint=(1, None), height=50)
        score_label = Label(text='Score: ', size_hint=(1, None), height=50)
        distance_label = Label(text='You traveled ', size_hint=(1, None), height=50)
        btn = Button(text='Play Again', background_color=(0.1, 0.5, 0.8, 1), size_hint=(1, None), height=50)
        btn.bind(on_release=self.restart_game)
        info_layout.add_widget(stars_label)
        info_layout.add_widget(score_label)
        info_layout.add_widget(distance_label)
        info_layout.add_widget(btn)
        self.add_widget(info_layout)

    def restart_game(self, instance):
        Clock.unschedule(self.spawn_asteroid)
        Clock.unschedule(self.spawn_star)
        self.start_game()

class HomeScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.bg = Image(source='spaceship.png')
        title = Label(text="Welcome to Space Adventure!", font_size=40, color=(1, 1, 1, 1))
        start_button = Button(text="Start", background_color=(0.1, 0.5, 0.8, 1), size_hint=(None, None), size=(200, 50), font_size=20, pos_hint={'center_x': 0.5})
        start_button.bind(on_release=self.start_game)
        self.add_widget(self.bg)
        self.add_widget(title)
        self.add_widget(start_button)

    def start_game(self, instance):
        self.clear_widgets()
        game_widget = GameWidget()
        self.add_widget(game_widget)

class SpaceGameApp(App):
    def build(self):
        return HomeScreen()

if __name__ == '__main__':
    SpaceGameApp().run()
