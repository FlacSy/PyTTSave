import os
import requests
from typing import Dict, Any, List
from enum import Enum
from ttsave_api.exceptions import ServerError, ParserError


class ContentType(Enum):
    """
    Перечисление типов контента, которые могут быть загружены.

    - Original: Оригинальный контент (Колаж из фото будет ввиде отдельных фото-файлов и аудио файла).
    - VideoOnly: Фото будут преобразованы в видео колаж из них.
    """
    Original = "ORIGINAL"
    VideoOnly = "VIDEO_ONLY"


class TTSave:
    """
    Класс для взаимодействия с API сервиса TTSave.
    """
    
    def __init__(self, api_url: str = "http://45.13.225.104:4347/api/v3/"):
        """
        Инициализация объекта TTSave.

        :param api_url: URL API сервера, по умолчанию "http://45.13.225.104:4347/api/v3/".
        """
        self.api_url = api_url

    def _parse_multipart_stream(self, response, boundary: str, downloads_dir: str) -> List[str]:
        """
        Обрабатывает multipart stream от сервера и сохраняет полученные файлы.

        :param response: Ответ от сервера, содержащий multipart данные.
        :param boundary: Разделитель для multipart данных.
        :return: Список имен сохраненных файлов.
        :raises ParserError: Если возникает ошибка при парсинге заголовков или содержимого.
        """
        boundary = f"--{boundary}".encode("utf-8")
        buffer = b""
        
        files: List[str] = []

        for chunk in response.iter_content(chunk_size=1024):
            buffer += chunk
            while boundary in buffer:
                part, buffer = buffer.split(boundary, 1)
                if b"\r\n\r\n" in part:
                    headers, content = part.split(b"\r\n\r\n", 1)

                    headers = headers.decode("utf-8").split("\r\n")
                    content_type = next((h.split(": ")[1] for h in headers if h.startswith("Content-Type")), None)
                    filename = next((h.split("filename=")[1].strip() for h in headers if "filename=" in h), None)
                    
                    if not os.path.exists(downloads_dir):
                        os.makedirs(downloads_dir, exist_ok=True)

                    if content_type and filename:
                        filepath = os.path.join(downloads_dir, filename.strip('"'))
                        with open(filepath, "wb") as f:
                            f.write(content)
                        files.append(filepath)
                    else:
                        raise ParserError("Ошибка при парсинге заголовков или содержимого файла.")
        else:
            return files

    def _send_request(self, data: Dict[str, Any], endpoint: str) -> requests.Response | None:
        """
        Отправляет POST запрос на сервер.

        :param data: Данные, которые отправляются в запросе.
        :param endpoint: Путь к ресурсу на сервере (например, 'download').
        :return: Ответ от сервера, если запрос успешен, или None, если произошла ошибка.
        :raises requests.exceptions.RequestException: В случае ошибки при отправке запроса.
        """
        try:
            response = requests.post(f"{self.api_url}{endpoint}", json=data)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None

    def ping(self) -> bool:
        """
        Проверяет доступность сервера, отправляя запрос на эндпоинт 'ping'.

        :return: True, если сервер доступен, иначе False.
        :raises requests.exceptions.RequestException: В случае ошибки при отправке запроса.
        """
        try:
            response = self._send_request({}, 'ping')
            if response is None or response.status_code != 200:
                return False
            else:
                return True
        except requests.exceptions.RequestException:
            return False

    def download(self, url: str, content_type: ContentType, downloads_dir: str = './') -> List[str] | None:
        """
        Отправляет запрос на сервер для скачивания контента с TikTok.

        :param url: URL TikTok, с которого нужно скачать контент.
        :param content_type: Тип контента для скачивания.
        :raises ServerError: Если произошла ошибка при скачивании контента или сервер недоступен.
        :raises ParserError: Если возникла ошибка при разборе ответа от сервера.
        """
        data = {
            "url": url,
            "content_type": content_type.value
        }

        try:
            response = self._send_request(data, 'download')
            if response is None or response.status_code != 200:
                if self.ping():
                    raise ServerError('Произошла ошибка при попытке скачивания')
                else:
                    raise ServerError('Сервер недоступен')
            
            boundary = response.headers["Content-Type"].split("boundary=")[-1]
            return self._parse_multipart_stream(response, boundary, downloads_dir)
        except KeyError:
            print("Ошибка: Не удалось найти boundary в заголовках ответа.")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
