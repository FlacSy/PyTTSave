from ttsave_api import TTSave, ContentType

client = TTSave(api_url='http://0.0.0.0:4347/api/v3/')

if client.ping():
    print("Сервер доступен.")

try:
    response = client.download(input("Ссылка на TikTok: "), ContentType.Original)
    print(f"Загрузка {response['meta']['title']} ({response['meta']['desc']}) завершена.\nСохраненные файлы: {response['files']}")
except Exception as e:
    print(f"Ошибка при загрузке: {e}")