from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
import random

class DraggableImage(Widget):
    def __init__(self, source, app_instance, **kwargs):
        super(DraggableImage, self).__init__(**kwargs)
        self.image = Image(source=source, size_hint=(None, None), size=(100, 100))
        self.add_widget(self.image)

        # Synchronize position and size with DraggableImage
        self.bind(pos=self.update_image_pos, size=self.update_image_pos)
        self.update_image_pos()

        # Additional attributes for control
        self.app_instance = app_instance
        self.source = source
        self.original_pos = (300, 50)  # Set initial position for draggable image

    def update_image_pos(self, *args):
        # Ensure the image is centered in DraggableImage
        self.image.pos = self.pos
        self.image.size = self.size

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self._touch_offset_x = touch.x - self.x
            self._touch_offset_y = touch.y - self.y
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if hasattr(self, '_touch_offset_x') and hasattr(self, '_touch_offset_y'):
            self.x = touch.x - self._touch_offset_x
            self.y = touch.y - self._touch_offset_y
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if hasattr(self, '_touch_offset_x'):
            drop_area = self.app_instance.check_drop(self)
            if drop_area and drop_area.source == self.source:
                print(f"Gambar '{self.source}' ditempatkan di area yang benar.")
                drop_area.add_image(self.image.source)
                self.disable()
                self.app_instance.update_game_state()
            else:
                print(f"Gambar '{self.source}' kembali ke posisi awal.")
                self.pos = self.original_pos
            del self._touch_offset_x
            del self._touch_offset_y
            return True
        return super().on_touch_up(touch)

    def disable(self):
        self.unbind(on_touch_down=self.on_touch_down)
        self.unbind(on_touch_move=self.on_touch_move)
        self.unbind(on_touch_up=self.on_touch_up)

class DropArea(Widget):
    def __init__(self, source=None, **kwargs):
        super(DropArea, self).__init__(**kwargs)
        self.is_filled = False
        self.source = source
        self.add_image(source)

    def add_image(self, source):
        for child in self.children:
            if isinstance(child, Image) and child.source == source:
                return

        img = Image(source=source, size_hint=(None, None), size=(100, 100))
        img.pos = (self.x + (self.width - img.width) / 2, self.y + (self.height - img.height) / 2)
        self.add_widget(img)
        self.is_filled = True

class MyGameApp(App):
    def build(self):
        self.layout = FloatLayout(size=(800, 600))
        with self.layout.canvas:
            Color(0.8, 0.8, 1, 1)
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self._update_rect, pos=self._update_rect)

        # List of images used in the game
        self.labels = [
            'images/image1.png',
            'images/image2.png',
            'images/image3.png',
            'images/image4.png',
            'images/image5.png',
            'images/image6.png'
        ]
        
        self.drop_areas = []
        for i in range(6):
            x_pos = 50 + (i % 3) * 140
            y_pos = 300 - (i // 3) * 120
            drop_area = DropArea(source=self.labels[i], size_hint=(None, None), size=(100, 100), pos=(x_pos, y_pos))
            self.layout.add_widget(drop_area)
            self.drop_areas.append(drop_area)

        # Status for the number of correctly placed images
        self.correctly_placed = 0
        self.remaining_images = self.labels[:]  # Keep track of images yet to be used

        # Show the first image
        self.show_next_image()
        return self.layout

    def _update_rect(self, *args):
        self.rect.pos = self.layout.pos
        self.rect.size = self.layout.size

    def check_drop(self, draggable_image):
        for drop_area in self.drop_areas:
            if drop_area.collide_widget(draggable_image) and not drop_area.is_filled:
                return drop_area
        return None

    def update_game_state(self):
        self.correctly_placed += 1
        print(f"Gambar yang berhasil ditempatkan: {self.correctly_placed}")

        if self.correctly_placed < len(self.labels):
            self.show_next_image()
        else:
            print("Selamat, Anda telah menyelesaikan permainan!")

    def show_next_image(self):
        if self.correctly_placed < len(self.labels):
            # Check if there are any remaining images
            if self.remaining_images:
                # Randomly select an image from the remaining images
                next_image_source = random.choice(self.remaining_images)
                self.remaining_images.remove(next_image_source)  # Remove selected image from the list
                self.current_draggable = DraggableImage(source=next_image_source, app_instance=self, size_hint=(None, None), size=(100, 100))
                self.current_draggable.pos = (300, 50)
                self.layout.add_widget(self.current_draggable)
                print(f"Menampilkan gambar {self.current_draggable.source} di posisi {self.current_draggable.pos}")
            else:
                print("Semua gambar telah ditampilkan.")

if __name__ == '__main__':
    MyGameApp().run()
