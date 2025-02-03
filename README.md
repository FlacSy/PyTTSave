Документация PyTTSave
=========================

Эта документация описывает библиотеку PyTTSave, которая предоставляет интерфейс для загрузки контента из TikTok с использованием API.

---

## Установка

Установить PyTTSave можно с помощью pip:

```bash
pip3 install PyTTSave==1.1.0
```

Последнюю версию всегда можно скачать с GitHub, с помощью команды:
```bash
pip3 install git+https://github.com/FlacSy/PyTTSave
```

---

## Быстрый старт

Пример использования библиотеки:

```python
from ttsave_api import TTSave, ContentType

# Инициализация клиента TTSave
client = TTSave()

# Проверка доступности сервера
if client.ping():
    print("Сервер доступен.")

# Загрузка контента
try:
    files = client.download("https://www.tiktok.com/@example/video/123456789", ContentType.Original)
    print("Загрузка успешно завершена. Сохраненные файлы:", files)
except Exception as e:
    print(f"Ошибка при загрузке: {e}")
```

---

## Классы

### ContentType

Перечисление типов контента, доступных для загрузки:

- `Original`: Оригинальный контент (фото-коллажи загружаются в виде отдельных изображений и аудиофайла).
- `VideoOnly`: Фото преобразуются в видеоколлаж.

Пример объявления:

```python
class ContentType(Enum):
    Original = "ORIGINAL"
    VideoOnly = "VIDEO_ONLY"
```

### TTSave

Основной класс для взаимодействия с API TTSave.

#### Конструктор

```python
TTSave(api_url: str = "http://45.13.225.104:4347/api/v3/")
```

**Параметры:**
- `api_url` *(str)* — URL API сервера (по умолчанию задано стандартное значение).

---

## Методы

### `ping()`

```python
ping() -> bool
```

**Описание:** Проверяет доступность сервера API.

**Возвращает:**
- `True`, если сервер доступен.
- `False`, если сервер недоступен.

**Исключения:**
- `requests.exceptions.RequestException` — Ошибка запроса.

---

### `download()`

```python
download(url: str, content_type: ContentType, downloads_dir: str = './') -> dict[str, dict | str | List[str]] | None
```

**Описание:** Загружает контент с TikTok, используя API TTSave.

**Параметры:**
- `url` *(str)* — Ссылка на видео в TikTok.
- `content_type` *(ContentType)* — Тип загружаемого контента.
- `downloads_dir` *(str, optional)* — Папка для сохранения загруженных файлов (по умолчанию текущая директория).

**Возвращает:**
- `dict[str, dict | str | List[str]]` — Словарь, состоящий из списка **files** и словаря **meta**.
- `None` — При неудачной загрузке.

**Исключения:**
- `ServerError` — Ошибка при загрузке контента или недоступность сервера.
- `ParserError` — Ошибка при обработке ответа сервера.

---

### `_send_request()`

```python
_send_request(data: Dict[str, Any], endpoint: str) -> requests.Response | None
```

**Описание:** Вспомогательный метод для отправки POST-запросов к API.

**Параметры:**
- `data` *(Dict[str, Any])* — Данные запроса.
- `endpoint` *(str)* — Путь API (например, `download`).

**Возвращает:**
- `requests.Response` —  При успешном запросе.
- `None` —  При ошибке возвращается None.

**Исключения:**
- `requests.exceptions.RequestException` — Ошибка при отправке запроса.

---

### `_parse_multipart_stream()`

```python
_parse_multipart_stream(response, boundary: str, downloads_dir: str) -> List[str]
```

**Описание:** Обрабатывает multipart-ответ от сервера и сохраняет файлы.

**Параметры:**
- `response` — Ответ сервера с multipart-данными.
- `boundary` *(str)* — Разделитель multipart-данных.
- `downloads_dir` *(str)* — Директория для сохранения файлов.

**Возвращает:**
- `List[str]` — Список имен сохраненных файлов.

**Исключения:**
- `ParserError` — Ошибка при разборе заголовков или содержимого.

---

## Ошибки и Исключения

Библиотека использует два пользовательских исключения:

- `ServerError` — Вызывается при ошибках загрузки или недоступности сервера.
- `ParserError` — Вызывается при проблемах обработки ответа API.

Пример обработки исключений:

```python
try:
    files = client.download("https://www.tiktok.com/@example/video/123456789", ContentType.Original)
    print("Файлы загружены:", files)
except ServerError:
    print("Ошибка сервера!")
except ParserError:
    print("Ошибка обработки данных!")
except Exception as e:
    print(f"Неизвестная ошибка: {e}")
```

---

## Заключение

PyTTSave предоставляет удобный интерфейс для скачивания контента из TikTok. Он автоматически обрабатывает запросы и сохраняет файлы, упрощая интеграцию с различными проектами.

Если у вас возникли вопросы или предложения по улучшению библиотеки, пожалуйста, создавайте issues или pull requests в репозитории проекта.
