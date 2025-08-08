Инструкция по развёртыванию на Render (24/7)

Файлы в архиве:
- bot.py         -- основной код бота (берёт TOKEN из переменных окружения или использует встроенный)
- requirements.txt -- зависимости (python-telegram-bot, flask)
- start.sh       -- команда запуска

Быстрая инструкция:
1) Создай репозиторий на GitHub и залей эти файлы в корень репозитория.
2) Зарегистрируйся/войди на https://render.com через GitHub.
3) На Render: New -> Web Service -> выбери репозиторий с ботом.
   - Branch: main
   - Build Command: pip install -r requirements.txt
   - Start Command: bash start.sh
   - Runtime: Python 3 (например 3.10 или 3.11)
4) В Settings сервиса добавь Environment Variable:
   - KEY: TOKEN
   - VALUE: (если хочешь, можешь заменить встроенный токен; значение можно оставить пустым, тогда будет использован токен из bot.py)
5) Deploy. В логах должно быть: "Бот работает... (Telegram polling started)"
6) Добавь бота в свою группу и сделай его админом. Проверь команды /start и приглашение новых участников.

Если хочешь, подключи UptimeRobot к URL, который Render выдаст (например https://your-service.onrender.com/),
чтобы периодически пинговать его и уменьшить задержки при "пробуждении".
