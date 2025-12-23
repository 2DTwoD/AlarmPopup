from pynput.keyboard import Key, Listener


def on_press(key):
    key_press = key
    print("PRESSED", key_press)
    if key_press == "'a'":
        print("A HEARD!")


with Listener(on_press=on_press) as listener:
    listener.join()