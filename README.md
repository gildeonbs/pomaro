# Pomaro

An elegant, efficient Pomodoro timer fully integrated into the Linux desktop ecosystem (focused on KDE Plasma/Wayland). Built with **Python 3.10+** and **PyQt6**, Pomaro respects your system's native theme, manages your time asynchronously, and consumes very few resources.


<img width="280" height="322" alt="Pomaro_Screenshot" src="https://github.com/user-attachments/assets/db6f52b7-3773-401c-904f-c7f84ac1023a" />


## Features

* **Automatic Cycles:** Automatically manages Focus, Short Break, and Long Break (after 4 cycles) periods.
* **Native Integration:** DBus notifications, System Tray icon, and seamless Wayland support.
* **Mini To-Do List:** Add and cross off ongoing tasks directly from the main interface.
* **Lightweight & Asynchronous:** Uses `QTimer` to ensure the interface never freezes while keeping CPU usage close to zero.
* **Fully Customizable:** Change cycle durations through a simple settings interface (saved locally in JSON format).

## Technologies Used

* [Python 3.10+](https://www.python.org/)
* [PyQt6](https://pypi.org/project/PyQt6/) (Python bindings for the Qt framework)
* [PyInstaller](https://pyinstaller.org/) (For packaging)

## How to Run in a Development Environment

1. **Clone the repository:**
```bash
   git clone https://github.com/gildeonbs/pomaro.git
   cd pomaro
```

2. **Create and activate a virtual environment (Recommended):**
```bash
python -m venv venv
source venv/bin/activate
```


3. **Install the dependencies:**
```bash
pip install PyQt6
```


4. **Run the application:**
```bash
python main.py
```



## 📦 How to Package and Install on Your System (KDE Plasma / Linux)

If you want to turn Pomaro into a native application on your system, complete with a launcher menu entry and a vector icon, follow these steps:

### 1. Build the Binary

With your virtual environment activated, install PyInstaller and build the executable, making sure to bundle the SVG icon:

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --name="Pomaro" --add-data="icon.svg:." main.py
```

### 2. Install the Binary and the Icon

Move the generated executable to your user's binary folder and copy the icon to the system's icon directory:

```bash
mkdir -p ~/.local/bin/
mkdir -p ~/.local/share/icons/

mv dist/Pomaro ~/.local/bin/
cp icon.svg ~/.local/share/icons/pomaro.svg
```

Ensure `~/.local/bin` is included in your PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

For Zsh users:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 3. Create the Launcher (Desktop Entry)

Create a `.desktop` file so your desktop environment can recognize the application:

```bash
nano ~/.local/share/applications/pomaro.desktop
```

Paste the following configuration:

```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=Pomaro
Comment=Native Pomodoro timer integrated with KDE
Exec=Pomaro
Icon=pomaro
Terminal=false
StartupNotify=true
Categories=Utility;Clock;Office;
StartupWMClass=Pomaro
```

Grant execution permissions to the launcher:

```bash
chmod +x ~/.local/share/applications/pomaro.desktop
```

Done! Now you can simply open your system's application launcher and search for **Pomaro**.

## Project Structure

```text
pomaro/
├── core.py              # Business logic (Timer, State Machine)
├── ui.py                # Graphical Interface, System Tray, Notifications
├── main.py              # Entry Point, Wayland setup, and app_id
├── config.py            # Preferences persistence (JSON)
├── icon.svg             # Application vector icon
└── README.md            # Documentation
```

## Contributing

Contributions are always welcome! If you have any ideas to improve Pomaro, feel free to open an *Issue* or submit a *Pull Request*.

1. Fork the project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

