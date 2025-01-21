# Barbaric Web Server with Cross-Platform Build

This project demonstrates a standalone dynamic web server capable of serving HTML templates with JSON-configured dynamic content. The server can be built and executed on **Linux**, **Windows**, and **macOS** using GitHub Actions pipelines. The final product is a **standalone binary** that does not require Python to run.

### Who is this for?

This project is designed to help beginners or those unfamiliar with programming set up a dynamic web server with minimal effort. By following the simple steps outlined here, you can:

- Serve dynamic HTML content without needing extensive technical knowledge.
- Easily configure server settings using a `config.json` file.
- Quickly get started with pre-built binaries or Python scripts.

If you’re new to web servers, this guide provides a straightforward way to learn and experiment without requiring advanced skills.



---

## Features

- **Dynamic HTML Rendering**: Uses `data.json` for variable substitution in templates.
- **Route Management**: Define routes and corresponding HTML templates in `routes.json`.
- **Cross-Platform Builds**: Automated pipeline builds for Linux, Windows, and macOS.
- **You can use it with python 3.8 too**, starting the server with "python3 server.py"
- **Standalone Execution**: Creates self-contained binaries using `PyInstaller` or download the binary from here.

---

## Project Structure

```
project/
├── server.py            # Python server script
├── data.json            # Dynamic content configuration
├── routes.json          # Route-to-template mapping
├── public/              # Directory for static files
│   ├── base.css
│   ├── base.js
│   └── cica.jpeg
├── templates/           # Directory for HTML templates
│   ├── index.html
│   ├── about.html
│   └── contact.html
├── config.json          # Server configuration file
```

---

## Usage

### Running Standalone Binary

1. Build or download from right hand side the standalone binary for your platform (see the **Building Standalone Binaries** section).

2. Execute the binary (default is the config.json so you only have to use "--config" switch if the file name differs):

   - **Linux**:
     ```bash
     ./server --config config.json
     ```
   - **Windows**:
     ```bash
     server.exe --config config.json
     ```
   - **macOS**:
     ```bash
     ./server --config config.json
     ```

3. Access the server in your browser:

   - [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Building Standalone Binaries

### Prerequisite

Install **PyInstaller**:

```bash
pip install pyinstaller
```

### Build Commands

- **Linux**:
  ```bash
  pyinstaller --onefile server.py
  ```
- **Windows**:
  ```bash
  pyinstaller --onefile server.py
  ```
- **macOS**:
  ```bash
  pyinstaller --onefile server.py
  ```

The binary will be available in the `dist/` folder.

---

## Configuration Files

### `config.json`

This file defines the server's runtime settings. Example:

```json
{
    "port": 8000,
    "host": "127.0.0.1",
    "directory": ".",
    "debug": false
}
```

#### Fields:

- **`port`**: The port on which the server will run.
- **`host`**: The IP address to bind the server to (e.g., `127.0.0.1` for localhost).
- **`directory`**: The root directory containing the server's files.
- **`debug`**: Enables or disables debug mode (set to `true` for more verbose logging).

### `data.json`

This file contains key-value pairs for dynamic content.

```json
{
    "title": "Barbaric Web Server",
    "description": "A dynamic server rendering templates based on JSON content.",
    "show_list": true,
    "items": ["Item 1", "Item 2", "Item 3"]
}
```

### `routes.json`

Defines routes and their corresponding HTML templates.

```json
{
    "/": "index.html",
    "/about": "about.html",
    "/contact": "contact.html"
}
```

---

## Templates

Templates are standard HTML files with placeholders for dynamic content:

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}</h1>
    <p>{{ description }}</p>

    {% if show_list %}
    <ul>
        {% for item in items %}
        <li>{{ item }}</li>
        {% endfor %}
    </ul>
    {% endif %}
</body>
</html>
```

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contribution

Contributions are welcome! Feel free to open issues or submit pull requests.

