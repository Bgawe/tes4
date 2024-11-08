from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Rectangle, RoundedRectangle, Color
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.metrics import dp



class RoundedButton(Button):
    def __init__(self, image_source='', **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (1, 1, 1, 0)

        # Draw rounded rectangle
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rounded_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])

        # Draw image
        with self.canvas:
            self.rect = Rectangle(source=image_source, size=self.size, pos=self.pos)

        # Bind for updates
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rounded_rect.pos = self.pos
        self.rounded_rect.size = self.size
        self.rect.pos = self.pos
        self.rect.size = self.size


class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)


class LowercaseLetterScreen(Screen):
    def __init__(self, **kwargs):
        super(LowercaseLetterScreen, self).__init__(**kwargs)

        layout = FloatLayout()
        background = Image(source='backgroundLowercase.png', allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)

        # Back button
        back_button = ImageButton(source='images/back.png', size_hint=(None, None), size=(dp(150), dp(70)), pos_hint={'x': 0.05, 'top': 0.95})
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        # Central Image
        center_image = Image(source='images/ABCALPHA.png', size_hint=(None, None), size=(550, 350), pos_hint={'center_x': 0.15, 'center_y': 0.6})
        layout.add_widget(center_image)

        description_label = Label(
            text="ABC Alphabet",
            size_hint=(None, None),
            size=(700, 200),
            pos_hint={'center_x': 0.35, 'center_y': 0.70},
            font_name='ProtestStrike-Regular.ttf', 
            font_size='28sp' ,
            color=(1,1,1, 1)
        )
        layout.add_widget(description_label)

        button_layout = FloatLayout(size_hint=(1, 0.2), pos_hint={'center_x': 0.5, 'y': 0.55})
        
        button_images = ['images/test.png', 'images/result.png', 'images/reports.png']
        button_positions = [(0.65, 0.5), (0.75, 0.5), (0.85, 0.5)]  

        for img_source, pos in zip(button_images, button_positions):
            img_button = ImageButton(source=img_source, size_hint=(None, None), size=(1500, 1000), pos_hint={'center_x': pos[0], 'center_y': pos[1]})
            img_button.bind(on_press=self.on_button_press) 
            button_layout.add_widget(img_button)

        layout.add_widget(button_layout)

        # Scroll view for other 
        scroll_view = ScrollView(size_hint=(1, 0.4), do_scroll_x=True, do_scroll_y=False)
        scroll_view.pos_hint = {'center_x': 0.5, 'y': 0.0}

        menu_grid = GridLayout(cols=20, padding=20, spacing=20, size_hint_x=None, height='100dp')
        menu_grid.bind(minimum_width=menu_grid.setter('width'))

        buttons = [
            ('Lowercase Letter', self.go_to_FlashCard, 'images/AbcAlphabet/image1.png'),
            ('Instructions', self.show_instructions, 'images/AbcAlphabet/image2.png'),
            ('Settings', self.show_settings, 'images/AbcAlphabet/image3.png'),
            ('Exit', self.exit_game, 'images/AbcAlphabet/image4.png'),
            ('High Scores', self.show_high_scores, 'images/AbcAlphabet/image5.png'),
            ('Help', self.show_help, 'images/AbcAlphabet/image6.png'),
        ]

        for text, action, image_source in buttons:
            button = RoundedButton(image_source=image_source, size_hint=(None, 1), width=450)
            button.bind(on_press=action)
            menu_grid.add_widget(button)

        scroll_view.add_widget(menu_grid)
        layout.add_widget(scroll_view)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'menu'

    def on_button_press(self, instance):
        print(f"Button pressed: {instance.source}")

    def go_to_FlashCard(self, instance):
        self.manager.current = 'Flashcard'

    def start_game(self, instance):
        print("Game Started!")

    def show_instructions(self, instance):
        print("Show instructions here")

    def show_settings(self, instance):
        print("Open settings here")

    def exit_game(self, instance):
        print("Exiting game...")

    def show_high_scores(self, instance):
        print("Show high scores")

    def show_help(self, instance):
        print("Show help")

