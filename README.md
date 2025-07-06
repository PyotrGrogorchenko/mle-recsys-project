Здесь укажите имя вашего бакета: **s3-student-mle-20241221-2d3d22a101**

# Подготовка виртуальной машины

## Склонируйте репозиторий

Склонируйте репозиторий проекта:

```
git clone https://github.com/yandex-praktikum/mle-project-sprint-4-v001.git
```

## Активируйте виртуальное окружение

Используйте то же самое виртуальное окружение, что и созданное для работы с уроками. Если его не существует, то его следует создать.

Создать новое виртуальное окружение можно командой:

```
python3 -m venv .env_recsys_start
```

После его инициализации следующей командой

```
. .env_recsys_start/bin/activate
```

установите в него необходимые Python-пакеты следующей командой

```
pip install -r requirements.txt
```

```
python3 -m ipykernel install --user --name='.env_recsys_start'
```

### Скачайте файлы с данными

Для начала работы понадобится три файла с данными:
- [tracks.parquet](https://storage.yandexcloud.net/mle-data/ym/tracks.parquet)
- [catalog_names.parquet](https://storage.yandexcloud.net/mle-data/ym/catalog_names.parquet)
- [interactions.parquet](https://storage.yandexcloud.net/mle-data/ym/interactions.parquet)
 
Скачайте их в директорию локального репозитория. Для удобства вы можете воспользоваться командой wget:

```
cd data

wget https://storage.yandexcloud.net/mle-data/ym/tracks.parquet

wget https://storage.yandexcloud.net/mle-data/ym/catalog_names.parquet

wget https://storage.yandexcloud.net/mle-data/ym/interactions.parquet
```

## Запустите Jupyter Lab

Запустите Jupyter Lab в командной строке

```
jupyter lab --ip=0.0.0.0 --no-browser
```

# Расчёт рекомендаций

Код для выполнения первой части проекта находится в файле `recommendations.ipynb`. Изначально, это шаблон. Используйте его для выполнения первой части проекта.

# Сервис рекомендаций

Шаги для запуска сервиса рекомендаций:

```
docker compose up --build
```

Адреса сервисов:
- recs_service: http://localhost:8000
- features_service: http://localhost:8010
- events_service: http://localhost:8020

Cтратегия смешивания онлайн- и офлайн-рекомендаций:
- получаем онлайн- и офлайн-рекомендации
- чередуем элементы из списков, пока позволяет минимальная длина
- добавляем оставшиеся элементы в конец
- удаляем дубликаты
- оставляем только первые k рекомендаций

# Инструкции для тестирования сервиса

Код для тестирования сервиса находится в файле `test_service.py`.

```
python3 -m venv .env_recsys_start
. .env_recsys_start/bin/activate
pip install -r requirements.txt
python test_service.py
```
Логи тестирования сервиса находится в файле `test_service.log`.

