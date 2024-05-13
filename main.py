import os
import telebot
import psycopg2
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)

DATABASE_URL = os.getenv('DATABASE_URL')

try:
    # Подключение к базе данных
    conn = psycopg2.connect(DATABASE_URL)
    print('Connection to PostgreSQL DB successful')

    # Создание таблицы, если не создана
    with conn.cursor() as cursor:

        cursor.execute('''
             CREATE TABLE IF NOT EXISTS public.tasks
            (
                id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
                user_id integer NOT NULL,
                task text COLLATE pg_catalog."default" NOT NULL,
                CONSTRAINT tasks_pkey PRIMARY KEY (id)
            )
        ''')
        conn.commit()

        print('Table created successfully')

except:
    print('Can`t establish connection to database')


# Старт бота
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(
        message.chat.id,
        '''
        /add - добавить задачу
        /list - список задач
        ''',
    )


# Добавление задачи
@bot.message_handler(commands=['add'])
def handle_add(message):
    with conn.cursor() as cursor:
        user_id = message.from_user.id
        task = message.text.replace('/add ', '')
        cursor.execute('INSERT INTO tasks (user_id, task) VALUES (%s, %s)', (user_id, task,))
        conn.commit()

        bot.send_message(
            message.chat.id,
            f'Задача "{task}" добавлена',
        )


# Список задач пользователя
@bot.message_handler(commands=['list'])
def handle_add(message):
    with conn.cursor() as cursor:
        user_id = message.from_user.id
        cursor.execute('SELECT task FROM tasks WHERE user_id = %s', (user_id,))
        tasks = cursor.fetchall()
        tasks_list = 'Список задач:\n\n' + '\n'.join(map(lambda x: x[0], tasks))

        bot.send_message(
            message.chat.id,
            tasks_list,
        )


bot.polling(none_stop=True)
