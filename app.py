from http.server import BaseHTTPRequestHandler, HTTPServer
import os

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split('?')[0]

        # Главная страница
        if path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("index.html", "r", encoding="utf-8") as file:
                self.wfile.write(bytes(file.read(), "utf-8"))

        # Обработка всех HTML файлов
        elif path.endswith(".html"):
            try:
                with open(path[1:], "r", encoding="utf-8") as file:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(bytes(file.read(), "utf-8"))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")

        # Статика (CSS, JS)
        elif path.endswith((".css", ".js")):
            try:
                with open(path[1:], "rb") as file:
                    self.send_response(200)
                    self.send_header("Content-type",
                                     "text/css" if path.endswith(".css") else
                                     "text/javascript")
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_error(404, "File Not Found")

        else:
            # Для SPA - всегда возвращаем index.html
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("index.html", "r", encoding="utf-8") as file:
                self.wfile.write(bytes(file.read(), "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started at http://{hostName}:{serverPort}")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")