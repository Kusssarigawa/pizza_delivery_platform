# Базовый образ
FROM python:3.11.5

# Создание пользователя с правами
RUN useradd -m -s /bin/bash yt

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl && \
    apt-get clean

# Установка Node.js для работы с npm и Bootstrap
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Создание рабочего каталога
WORKDIR /pizza_delivery_platform

# Копирование файлов проекта
COPY . /pizza_delivery_platform

# Изменение владельца и прав для каталогов
RUN mkdir /pizza_delivery_platform/static && mkdir /pizza_delivery_platform/media && \
    chown -R yt:yt /pizza_delivery_platform && \
    chmod 755 /pizza_delivery_platform

# Установка зависимостей Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Установка зависимостей Node.js
RUN npm install

# Переключение на созданного пользователя
USER yt

# Экспонирование порта приложения
EXPOSE 8000

# Команда запуска сервера разработки (можно заменить на gunicorn для продакшена)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
