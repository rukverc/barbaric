import os
import json
import re
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler

class DynamicHTMLHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Ellenőrizni, hogy a kérés statikus fájlra vonatkozik-e
        static_path = os.path.join(self.server.config["directory"], "public")
        requested_path = os.path.join(static_path, self.path.lstrip("/"))

        if os.path.isfile(requested_path):
            self.serve_static_file(requested_path)
        else:
            # Inicializáljuk a session adatokat
            if not hasattr(self.server, "session"):
                self.server.session = {}

            # Útvonalak betöltése
            with open(os.path.join(self.server.config["directory"], "routes.json"), "r", encoding="utf-8") as routes_file:
                routes = json.load(routes_file)

            # Útvonal ellenőrzése
            if self.path in routes:
                self.serve_dynamic_html(routes[self.path])
            else:
                self.send_error(404, "Page not found")

    def serve_static_file(self, file_path):
        try:
            self.send_response(200)
            if file_path.endswith(".css"):
                self.send_header("Content-type", "text/css")
            elif file_path.endswith(".js"):
                self.send_header("Content-type", "application/javascript")
            elif file_path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')):
                self.send_header("Content-type", "image/*")
            else:
                self.send_header("Content-type", "application/octet-stream")
            self.end_headers()

            with open(file_path, "rb") as file:
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404, "File not found")

    def serve_dynamic_html(self, template_name):
        try:
            # Template betöltése
            template_path = os.path.join(self.server.config["directory"], "templates", template_name)
            with open(template_path, "r", encoding="utf-8") as file:
                template_content = file.read()

            # Dinamikus adatok betöltése
            with open(os.path.join(self.server.config["directory"], "data.json"), "r", encoding="utf-8") as json_file:
                data = json.load(json_file)

            # Egyesítjük a session-t az adatokkal
            full_context = {**data, **self.server.session}

            # Feldolgozás: for ciklusok
            template_content = self.process_loops(template_content, full_context)

            # Feldolgozás: if feltételek
            template_content = self.process_conditionals(template_content, full_context)

            # Feldolgozás: változók behelyettesítése
            for key, value in full_context.items():
                template_content = template_content.replace(f"{{{{ {key} }}}}", str(value))
            
            # HTML válasz küldése
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(template_content.encode("utf-8"))
        except FileNotFoundError:
            self.send_error(404, "Template not found")

    def process_conditionals(self, template_content, data):
        # If feltételek feldolgozása
        conditional_pattern = r"{% if (\w+) %}(.*?){% endif %}"
        
        def evaluate_condition(match):
            variable, content = match.groups()
            if data.get(variable):
                return content
            return ""
        
        return re.sub(conditional_pattern, evaluate_condition, template_content, flags=re.S)

    def process_loops(self, template_content, data):
        # For ciklusok feldolgozása
        loop_pattern = r"{% for (\w+) in (\w+) %}(.*?){% endfor %}"
        
        def evaluate_loop(match):
            item_name, list_name, content = match.groups()
            items = data.get(list_name, [])
            if not isinstance(items, list):
                return ""

            rendered_content = ""
            for item in items:
                local_content = content
                local_content = local_content.replace(f"{{{{ {item_name} }}}}", str(item))
                rendered_content += local_content
            return rendered_content

        return re.sub(loop_pattern, evaluate_loop, template_content, flags=re.S)

def main():
    # Argumentumok feldolgozása
    parser = argparse.ArgumentParser(description="Egyszerű dinamikus webszerver")
    parser.add_argument("--port", type=int, default=8000, help="A szerver portja (alapértelmezett: 8000)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="A szerver IP címe (alapértelmezett: 127.0.0.1)")
    parser.add_argument("--directory", type=str, default=".", help="A gyökérmappa, ahonnan a fájlokat szolgáltatjuk (alapértelmezett: aktuális mappa)")
    parser.add_argument("--debug", action="store_true", help="Debug mód bekapcsolása")
    args = parser.parse_args()

    # Konfiguráció beállítása
    server_config = {
        "port": args.port,
        "host": args.host,
        "directory": os.path.abspath(args.directory),
        "debug": args.debug,
    }

    # Debug logolás
    if server_config["debug"]:
        print(f"Konfiguráció: {server_config}")

    # Szerver indítása
    server_address = (server_config["host"], server_config["port"])
    httpd = HTTPServer(server_address, DynamicHTMLHandler)
    httpd.config = server_config  # Konfiguráció elérhető a handlerben
    print(f"Szerver fut a http://{server_config['host']}:{server_config['port']} címen")
    httpd.serve_forever()

if __name__ == "__main__":
    main()
