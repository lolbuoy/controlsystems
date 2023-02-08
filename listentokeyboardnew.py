from sshkeyboard import listen_keyboard


def press(key):
 print(f"'{key}' is pressed")

def main():
 listen_keyboard(on_press=press)

if __name__ == "__main__":
 main()

