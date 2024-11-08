from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from random import choice

class DraggableImage(Image):
    def __init__(self, source, **kwargs):
        super().__init__(source=source, **kwargs)
        self.size_hint = (0.2, 0.2)  # Ukuran gambar yang dapat digeser
        self.allow_stretch = True

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            self.center_x = touch.x
            self.center_y = touch.y
            return True
        return super().on_touch_move(touch)

class TargetImage(Image):
    def __init__(self, source, **kwargs):
        super().__init__(source=source, **kwargs)
        self.size_hint = (0.2, 0.2)  # Ukuran gambar target
        self.allow_stretch = True

class GameLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_images = ['images/image1.png', 'images/image2.png', 'images/image3.png', 'images/image4.png', 'images/image5.png', 'images/image6.png']
        self.setup_game()

    def setup_game(self):
        grid = GridLayout(cols=3, rows=3, size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Menambahkan gambar target ke dalam grid
        self.target_widgets = []  # Menyimpan referensi ke widget target
        for img in self.target_images:
            target_image = TargetImage(source=img)
            grid.add_widget(target_image)
            self.target_widgets.append(target_image)

        # Memilih gambar target secara acak untuk draggable
        self.target_image = choice(self.target_images)
        self.draggable_image = DraggableImage(source=self.target_image)
        self.add_widget(self.draggable_image)

        self.grid = grid
        self.add_widget(grid)

    def on_touch_up(self, touch):
        if self.draggable_image.collide_point(*touch.pos):
            matched = False
            # Mengecek apakah gambar draggable cocok dengan salah satu gambar target di drop area
            for target_widget in self.target_widgets:
                if target_widget.source == self.draggable_image.source:
                    matched = True
                    # Hapus gambar target dari drop area
                    target_widget.source = ''  # Menghapus gambar yang cocok
                    self.show_popup("You Win!", "Congratulations! You matched the image!")
                    break
            
            if not matched:
                # Jika tidak cocok, beri alert dan reset gambar draggable
                self.show_alert("Mismatch", "The images do not match. Try again!")
                self.reset_draggable_image()

    def reset_draggable_image(self):
        # Mengatur gambar draggable kembali ke gambar target yang benar
        self.draggable_image.source = self.target_image
        self.draggable_image.reload()  # Memuat ulang gambar untuk memperbarui tampilan
        self.draggable_image.center = self.center  # Mengembalikan posisi ke tengah

    def show_popup(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.6, 0.4))
        popup.open()

    def show_alert(self, title, message):
        alert = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.6, 0.4))
        alert.open()

class MyApp(App):
    def build(self):
        return GameLayout()

if __name__ == '__main__':
    MyApp().run()
