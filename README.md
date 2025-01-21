# Dynamic Web Server with Cross-Platform Build

This project demonstrates a standalone dynamic web server capable of serving HTML templates with JSON-configured dynamic content. The server can be built and executed on **Linux**, **Windows**, and **macOS** using GitLab CI/CD pipelines. The final product is a **standalone binary** that does not require Python to run.

---

## Features

- **Dynamic HTML Rendering**: Uses `data.json` for variable substitution in templates.
- **Route Management**: Define routes and corresponding HTML templates in `routes.json`.
- **Cross-Platform Builds**: Automated pipeline builds for Linux, Windows, and macOS.
- **Standalone Execution**: Creates self-contained binaries using `PyInstaller`.

---

## Project Structure

```
project/
├── server.py            # Python server script
├── data.json            # Dynamic content configuration
├── routes.json          # Route-to-template mapping
├── public/           # Directory for HTML templates
│   ├── base.css
│   ├── base.js
│   └── cica.jpeg
├── templates/           # Directory for HTML templates
│   ├── index.html
│   ├── about.html
│   └── contact.html

```

---

## Usage

### Running Standalone Binary

1. Build the standalone binary for your platform (see the **Building Standalone Binaries** section).

2. Execute the binary:
   - **Linux**:
     ```bash
     ./server --port 8000 --host 127.0.0.1 --directory . --debug
     ```
   - **Windows**:
     ```bash
     server.exe --port 8000 --host 127.0.0.1 --directory . --debug
     ```
   - **macOS**:
     ```bash
     ./server --port 8000 --host 127.0.0.1 --directory . --debug
     ```

3. Access the server in your browser:
   - [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

### Building Standalone Binaries

#### Prerequisite

Install **PyInstaller**:
```bash
pip install pyinstaller
```

#### Build Commands

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

### CI/CD Pipeline with GitLab

#### Setup Steps

1. Register runners for Linux, Windows, and macOS:
   ```bash
   gitlab-runner register
   ```

2. Define the runners in `.gitlab-ci.yml`.

#### GitLab CI/CD Configuration

A sample `.gitlab-ci.yml` is provided with this project. Upon pushing to the repository, the pipeline will:

1. Build the binary for each platform.
2. Save the results as artifacts, downloadable from the GitLab UI.

---

## Configuration Files

### `data.json`

This file contains key-value pairs for dynamic content.

```json
{
    "title": "Dynamic Web Server",
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

