# ТГ-бот менеджер задач

### Установка

Сначала установите Postgres и запустите его.

Создайте телеграм бота.

Создайте базу данных для проекта.

Создайте файл ```.env``` и скопируйте туда содержимое из ```.env.example```. \
Измените переменную TOKEN на токен своего телеграм бота.\
Измените username, password и dbname для
DATABASE_URL на те, которые используются в вашем локальном Postgres.

```bash
TOKEN=YOUR_TOKEN
DATABASE_URL=postgres://username:password@localhost:5432/dbname
```

Установите зависимости проекта с помощью pip и активируйте виртуальную среду:

```bash
python -m venv .venv 
```
```bash
.venv\Scripts\Activate.ps1
```
```bash
pip install -r requirements.txt
```
