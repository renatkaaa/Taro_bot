from urllib.request import urlopen
from bs4 import BeautifulSoup
import logging
from random import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.ext import CommandHandler


senior_arcana = {'Шут': 'shut', 'Маг': 'mag', 'Жрица': 'zhrica', 'Императрица': 'imperatrica', 'Император': 'imperator',
                 'Иерофант': 'ierofant', 'Влюблённые': 'vlyublennye',
                 'Колесница': 'kolesnica', 'Справедливость': 'spravedlivost', 'Отшельник': 'otshelnik',
                 'Колесо Фортуны': 'koleso-fortuny', 'Сила': 'sila', 'Повешенный': 'poveshennyi',
                 'Смерть': 'smert', 'Умеренность': 'umerennost', 'Дьявол': 'diavol', 'Башня': 'bashnya',
                 'Звезда': 'zvezda', 'Луна': 'luna', 'Солнце': 'solnce',
                 'Страшный Суд': 'sud', 'Мир': 'mir'}
minor_arcana = {'Туз жезлов': 'tuz-zhezlov', 'Двойка жезлов': '2-zhezlov', 'Тройка жезлов': '3-zhezlov',
                'Четвёрка жезлов': '4-zhezlov', 'Пятёрка жезлов': '5-zhezlov', 'Шестёрка жезлов': '6-zhezlov',
                'Семёрка жезлов': '7-zhezlov',
                'Восьмёрка жезлов': '8-zhezlov', 'Девятка жезлов': '9-zhezlov', 'Десятка жезлов': '10-zhezlov',
                'Паж жезлов': 'pazh-zhezlov', 'Рыцарь жезлов': 'rytsar-zhezlov', 'Королева жезлов':
                    'koroleva-zhezlov', 'Король жезлов': 'korol-zhezlov', 'Туз кубков': 'tuz-kubkov',
                'Двойка кубков': '2-kubkov', 'Тройка кубков': '3-kubkov', 'Четвёрка кубков': '4-kubkov',
                'Пятёрка кубков': '5-kubkov', 'Шестёрка кубков': '6-kubkov', 'Семёрка кубков': '7-kubkov',
                'Восьмёрка кубков': '8-kubkov', 'Девятка кубков': '9-kubkov', 'Десятка кубков': '10-kubkov',
                'Паж кубков': 'pazh-kubkov', 'Рыцарь кубков': 'rytsar-kubkov', 'Королева кубков': 'koroleva-kubkov',
                'Король кубков': 'korol-kubkov', 'Туз мечей': 'tuz-metchey', 'Двойка мечей': '2-metchey',
                'Тройка мечей': '3-metchey', 'Четвёрка мечей': '4-metchey', 'Пятёрка мечей': '5-metchey',
                'Шестёрка мечей': '6-metchey', 'Семёрка мечей': '7-metchey', 'Восьмёрка мечей': '8-metchey',
                'Девятка мечей': '9-metchey', 'Десятка мечей': '10-metchey', 'Паж мечей': 'pazh-metchey',
                'Рыцарь мечей': 'rytsar-metchey', 'Королева мечей': 'koroleva-metchey', 'Король мечей':
                    'korol-metchey', 'Туз монет': 'tuz-monet', 'Двойка монет': '2-monet', 'Тройка монет': '3-monet',
                'Четвёрка монет': '4-monet', 'Пятёрка монет': '5-monet', 'Шестёрка монет': '6-monet',
                'Семёрка монет': '7-monet', 'Восьмёрка монет': '8-monet', 'Девятка монет': '9-monet',
                'Десятка монет': '10-monet', 'Паж монет': 'pazh-monet', 'Рыцарь монет': 'rytsar-monet',
                'Королева монет': 'koroleva-monet', 'Король монет': 'korol-monet'}
kolode = ['Шут', 'Маг', 'Жрица', 'Императрица', 'Император', 'Иерофант', 'Влюблённые', 'Колесница', 'Справедливость',
          'Отшельник', 'Колесо Фортуны', 'Сила', 'Повешенный', 'Смерть', 'Умеренность', 'Дьявол', 'Башня', 'Звезда',
          'Луна', 'Солнце', 'Страшный Суд', 'Мир', 'Туз жезлов', 'Двойка жезлов', 'Тройка жезлов', 'Четвёрка жезлов',
          'Пятёрка жезлов', 'Шестёрка жезлов', 'Семёрка жезлов', 'Восьмёрка жезлов', 'Девятка жезлов', 'Десятка жезлов',
          'Паж жезлов', 'Рыцарь жезлов', 'Королева жезлов', 'Король жезлов', 'Туз кубков', 'Двойка кубков',
          'Тройка кубков', 'Четвёрка кубков', 'Пятёрка кубков', 'Шестёрка кубков', 'Семёрка кубков',
          'Восьмёрка кубков', 'Девятка кубков', 'Десятка кубков', 'Паж кубков', 'Рыцарь кубков',
          'Королева кубков', 'Король кубков', 'Туз мечей', 'Двойка мечей', 'Тройка мечей', 'Четвёрка мечей',
          'Пятёрка мечей', 'Шестёрка мечей', 'Семёрка мечей', 'Восьмёрка мечей', 'Девятка мечей', 'Десятка мечей',
          'Паж мечей', 'Рыцарь мечей', 'Королева мечей', 'Король мечей', 'Туз монет', 'Двойка монет',
          'Тройка монет', 'Четвёрка монет', 'Пятёрка монет', 'Шестёрка монет', 'Семёрка монет', 'Восьмёрка монет',
          'Девятка монет', 'Десятка монет', 'Паж монет', 'Рыцарь монет', 'Королева монет', 'Король монет']
avatars = ['https://klike.net/uploads/posts/2022-09/1663161864_j-31.jpg',
          'https://avatars.dzeninfra.ru/get-zen_doc/5130440/pub_635f88cfea780a09c3d67172_635f8d644fec5a635dcdaadb'
          '/scale_1200', 'https://sotni.ru/wp-content/uploads/2023/08/taro-nuit-1.webp']
phrases = ['Я всё вижу...', 'Твоя судьба на ладони', 'Не делай этого...', 'Смотри глубже...', 'Да', 'Нет']


def mean_of_card(card):
    url = f"https://www.predskazanie.ru/znacheniya-kart-taro/{card}.php"
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = [chunk.encode('utf-8', 'ignore').decode('utf-8', 'ignore') for chunk in chunks if chunk]
    text = text[2:text.index('Смотрите все толкования карт: Значения карт Таро.')]
    massive_text = ['Основное значение карты', 'Любовь и отношения', 'Карьера', 'Совет карты Таро']
    cursive_text = ['Прямое положение', 'Перевернутое положение']
    messages = []
    message = []
    for i in range(len(text)):
        if text[i] in massive_text:
            if message:
                messages.append('\n'.join(message))
                message = []
            text[i] = '*' + text[i] + '*'
        if text[i] in cursive_text:
            text[i] = '_' + text[i] + '_'
        message.append(text[i])
    messages.append('\n'.join(message))
    return messages


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


async def echo(update, context):
    await update.message.reply_text(choice(phrases + [f'Я видел будущее уже {open("count.txt").readline()} раз...']))


async def start(update, context):
    await context.bot.sendPhoto(chat_id=update.message.chat.id, photo=choice(avatars),
                                caption='Я - *Таро Бот*\n *Узнать судьбу* - /fortune\n *Значение карт* - '
                                        '/cards', parse_mode='Markdown')


async def cards(update, context):
    keyboard = [[InlineKeyboardButton(i, callback_data=i)] for i in senior_arcana
                ]
    reply_markup_senior = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('*Старшие арканы*', parse_mode='Markdown', reply_markup=reply_markup_senior)
    keyboard = [[InlineKeyboardButton(i, callback_data=i)] for i in minor_arcana
    ]
    reply_markup_minor = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('*Младшие арканы*', parse_mode='Markdown', reply_markup=reply_markup_minor)


async def fortune(update, context):
    k = int(open('count.txt').readline())
    f = open('count.txt', 'w')
    f.write(str(k + 1))
    f.close()
    fortune_cards = set()
    while len(fortune_cards) < 3:
        fortune_cards.add(choice(kolode))
    keyboard = [
        [InlineKeyboardButton(i, callback_data=i) for i in fortune_cards]
    ]
    reply_markup_card = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f'Вам выпали: {", ".join([choice(["*обычная*", "*перевернутая*"]) + " карта " + f"*{i}*" for i in fortune_cards])}',
                                    reply_markup=reply_markup_card, parse_mode='Markdown')


async def card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data in senior_arcana:
        for i in mean_of_card(senior_arcana[query.data]):
            await query.message.reply_text(i, parse_mode='Markdown')
    if query.data in minor_arcana:
        for i in mean_of_card(minor_arcana[query.data]):
            await query.message.reply_text(i, parse_mode='Markdown')


def main():
    application = Application.builder().token('6948142504:AAHq2w4gByVXH8ONK1Go36UMMYuaz0aF6YQ').build()
    text_handler = MessageHandler(filters.TEXT, echo)
    application.add_handler(CallbackQueryHandler(card))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("cards", cards))
    application.add_handler(CommandHandler("fortune", fortune))
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
