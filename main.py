import threading
import keyboard
from pynput import mouse
import pystray
from PIL import Image, ImageDraw


left_pressed = False


def switch_desktop(direction: str):
    """
    direction:
        left  -> предыдущий стол
        right -> следующий стол
    """

    if direction == "left":
        keyboard.press("ctrl+windows+left")
        keyboard.release("ctrl+windows+left")

    elif direction == "right":
        keyboard.press("ctrl+windows+right")
        keyboard.release("ctrl+windows+right")


def on_click(x, y, button, pressed):
    global left_pressed

    if button == mouse.Button.left:
        left_pressed = pressed


def on_scroll(x, y, dx, dy):
    global left_pressed

    if not left_pressed:
        return

    # mouse wheel up
    if dy > 0:
        switch_desktop("left")

    # mouse wheel down
    elif dy < 0:
        switch_desktop("right")


def create_image():
    image = Image.new("RGB", (64, 64), color=(30, 30, 30))
    draw = ImageDraw.Draw(image)

    draw.rectangle((16, 16, 48, 48), outline="white", width=3)

    return image


def quit_app(icon, item):
    icon.stop()


def start_mouse_listener():
    listener = mouse.Listener(
        on_click=on_click,
        on_scroll=on_scroll
    )

    listener.start()
    listener.join()


def main():
    mouse_thread = threading.Thread(
        target=start_mouse_listener,
        daemon=True
    )
    mouse_thread.start()

    icon = pystray.Icon(
        "DesktopSwitcher",
        create_image(),
        "Desktop Switcher",
        menu=pystray.Menu(
            pystray.MenuItem("Exit", quit_app)
        )
    )

    icon.run()


if __name__ == "__main__":
    main()