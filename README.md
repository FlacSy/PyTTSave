Документация PyTTSave  
=========================  

Эта документация описывает библиотеку PyTTSave, которая предоставляет интерфейс для загрузки контента из TikTok с использованием API.  

---  

Установка:

```bash
pip3 install PyTTSave==1.0.0
```

---  

### Пример использования  

```python
from ttsave_api import TTSave, ContentType

# Инициализация клиента TTSave
client = TTSave()

# Проверка доступности сервера
if client.ping():
    print("Сервер доступен.")

# Загрузка контента
try:
    client.download("https://www.tiktok.com/@example/video/123456789", ContentType.Original)
    print("Загрузка успешно завершена.")
except Exception as e:
    print(f"Ошибка при загрузке: {e}")
```  

Классы  
-------  

1. `ContentType`  
   - Перечисление, представляющее типы контента, которые можно загрузить.  

2. `TTSave`  
   - Основной класс для взаимодействия с API TTSave.  

---  

### ContentType  

Перечисление, представляющее типы контента, которые можно загрузить.  

- **Атрибуты:**  
  - `Original`: Оригинальный контент. Для фото-коллажей возвращает отдельные фотофайлы и аудиофайл.  
  - `VideoOnly`: Преобразует фотографии в видеоколлаж.  

```python
class ContentType(Enum):
    Original = "ORIGINAL"
    VideoOnly = "VIDEO_ONLY"
```  

---  

### TTSave  

Основной класс для взаимодействия с API TTSave.  

#### Конструктор  

```python
TTSave(api_url: str = "http://45.13.225.104:4347/api/v3/")
```  

- **Параметры:**  
  - `api_url` *(str)*: URL API сервера.  

#### Методы  

##### `_parse_multipart_stream`  

```python
_parse_multipart_stream(response, boundary: str) -> List[str]
```  

- **Описание:**  
  Обрабатывает multipart-стрим от сервера и сохраняет полученные файлы.  

- **Параметры:**  
  - `response`: Ответ от сервера, содержащий multipart-данные.  
  - `boundary` *(str)*: Разделитель для multipart-данных.  

- **Возвращает:**  
  - *(List[str])*: Список сохранённых имён файлов.  

- **Исключения:**  
  - `ParserError`: Если возникает ошибка при разборе заголовков или содержимого.  

##### `_send_request`  

```python
_send_request(data: Dict[str, Any], endpoint: str) -> requests.Response | None
```  

- **Описание:**  
  Отправляет POST-запрос на сервер.  

- **Параметры:**  
  - `data` *(Dict[str, Any)*: Данные для отправки в запросе.  
  - `endpoint` *(str)*: Конечная точка сервера (например, `download`).  

- **Возвращает:**  
  - *(requests.Response | None)*: Ответ сервера при успешном запросе или `None`, если произошла ошибка.  

- **Исключения:**  
  - `requests.exceptions.RequestException`: Если возникает ошибка запроса.  

##### `ping`  

```python
ping() -> bool
```  

- **Описание:**  
  Проверяет доступность сервера, отправляя запрос на конечную точку `ping`.  

- **Возвращает:**  
  - *(bool)*: `True`, если сервер доступен, иначе `False`.  

- **Исключения:**  
  - `requests.exceptions.RequestException`: Если возникает ошибка запроса.  

##### `download`  

```python
download(url: str, content_type: ContentType) -> None
```  

- **Описание:**  
  Отправляет запрос на сервер для загрузки контента из TikTok.  

- **Параметры:**  
  - `url` *(str)*: URL TikTok для загрузки контента.  
  - `content_type` *(ContentType)*: Тип загружаемого контента.  
  - `downloads_path` *(str)*: Путь для сохранения файлов.
- **Исключения:**  
  - `ServerError`: Если происходит ошибка при загрузке контента или сервер недоступен.  
  - `ParserError`: Если возникает ошибка при разборе ответа сервера.  

