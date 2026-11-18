from http.server import BaseHTTPRequestHandler, HTTPServer


class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        # Определяем, какой файл отдавать. По умолчанию - contacts.html
        file_path = 'contacts.html'

        # Если запросили главную страницу, отдаем index.html
        if self.path == '/' or self.path == '/index.html':
            file_path = 'index.html'

        try:
            # Чтение файла через контекстный менеджер
            with open(file_path, 'r', encoding='utf-8') as file:
                page_content = file.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(page_content.encode('utf-8'))

        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                "<html><head><meta charset='utf-8'></head>"
                "<body><h1>404 - Страница не найдена</h1></body></html>"
                .encode('utf-8')
            )

    def do_POST(self):
        # 1. Получаем длину данных из заголовков
        content_length = int(self.headers['Content-Length'])

        # 2. Читаем данные из тела запроса
        post_data = self.rfile.read(content_length).decode('utf-8')

        # 3. Выводим данные в консоль (как требует задание)
        print("=========================================")
        print("ПОЛУЧЕНЫ ДАННЫЕ ОТ ПОЛЬЗОВАТЕЛЯ (POST):")
        print(post_data)
        print("=========================================")

        # 4. Отправляем ответ в браузер (чтобы страница не зависла)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            "<html><head><meta charset='utf-8'></head><body>"
            "<h1>Данные успешно отправлены!</h1>"
            "<a href='/'>Вернуться назад</a></body></html>"
            .encode('utf-8')
        )


if __name__ == "__main__":
    webServer = HTTPServer(('localhost', 8080), MyServer)
    print("Server started http://localhost:8080")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")
