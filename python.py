"""Не забудьте указать токин для вашего бота в поле "Токен вашего бота"
Для установки библиотек используйте команду pip install python-telegram-bot"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext, \
    ApplicationBuilder, ContextTypes
import random

# Токен вашего бота, который вы получили от BotFather
TOKEN = 'Укажите ваш токин для бота'

# Банк заданий
tasks_bank = [
    "Участвуешь в фестивале? Расскажи, а лучше покажи как ты проводишь время на мероприятии. Выложи фотографию с фестиваля к себе на страницу ВКонтакте с хештегом #CareerSchoolFest и получай свой приз!",
    "Сегодня важный день - профориентация вместе с granate.space, которая поможет тебе в выборе будущей профессии. Запиши в телеграм-канале фестиваля кружочек под постом “Профориентация сейчас” и расскажи, какое мероприятие тебе понравилось больше всего? Как профориентация помогла тебе в выборе профессии?",
    "В течение всего фестиваля будут проходить лекции по твоему карьерному продвижению. Посети не менее 3 лекций, запиши на каждый историю в ВК, отметь сообщество granate.space и Career School Fest ссылкой и проходи ступеньку!",
    "Погрузись в день медицины. Посети мастер-класс или лекции от партнеров в этой сфере, пройди тест (организатор покажет QR-код с ссылкой на тест во время занятия) и переходи на следующий этап!",
    "Время АйТи. Все мы знаем, что сейчас это одна из самых перспективных сфер в нашем мире. Попробуй себя в этой сфере на интерактивных выставках, скажи организаторам кодовое слово ЭТАП и забирай приз!",
    "Менеджмент везде, как и маркетинг. Напиши в комментариях под постом “Управление” в телеграм-канале фестиваля свое мнение по поводу этой сферы, что тебя привлекает и нет, хотел(а) бы ты работать в ней?",
    "Строительство — это не только про строителя. Посети одну из лекций/мастер-класс от партнеров, узнай, какие профессии есть в этой сфере и запиши кружок в телеграм-канал фестиваля под постом “Строительство”.",
    "Покреативим? В честь этот день посети интерактивную выставку из этой сферы и создай свое уникальное творение, выложи в ВК пост о своем искусстве, как ты его создавал(а) и забирай последний приз! Не забудь добавить хештег #CareerSchoolFest :)"
]


# Функция для команды /start
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [KeyboardButton("Партнеры"), KeyboardButton("Получить задание")],
        [KeyboardButton("Наши соц. сети")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Привет! Я бот фестиваля Career School Fest. Буду выдавать тебе задания и информировать о наших партнерах. Кстати, подпишись на наши соц. сети, туда нужно будет отправлять решения к заданиям.\n"
        "\nСейчас бот находится в тестовом режиме, поэтому выдает задания рандомно. На фестивале задания будут выдаваться каждый день.",
        reply_markup=reply_markup
    )


partners_links = {
    "Медицина": [
        ("ООО «СЛ МЕДИКАЛГРУП»", "https://cl-lab.info/"),
        ("Кубанский государственный медицинский университет", "https://www.ksma.ru/"),
        ("Краснодарский краевой базовый медицинский колледж", "https://kkbmk.ru/")],
    "Строительство": [
        ("ООО ГК ТОЧНО", "https://tochno.life/"),
        ("Краснодарский архитектурно-строительный техникум", "https://spokast.ru/"),
        ("Кубанский государственный университет", "https://kubsu.ru")],
    "IT": [
        ("ОАО «СБЕР»", "https://sbertech.ru/"),
        ("Колледж «Сириус»", "https://siriuscollege.ru"),
        ("Краснодарский колледж электронного приборостроения", "https://kkep.ru")],
    "Управление и маркетинг": [
        ("НАО «Красная Поляна»", "https://krasnayapolyana.com"),
        ("Академический колледж Академии маркетинга и социально-информационных технологий", "https://imsit.ru/abitur/"),
        ("Сочинский государственный университет", "https://sutr.ru")],
    "Дизайн": [
        ("ООО «Концепт Дизайнерс»", "https://concept2all.ru/"),
        ("Краснодарское художественное училище", "https://kxudu.krd.muzkult.ru/"),
        ("Отделение СПО Краснодарского государственного института культуры",
         "https://kgik1966.ru/institut/otdelenie-srednego-professionaljnogo-obrazovaniya-kolledzh")]
}


# Функция для команды /partners
async def partners(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton(category, callback_data=f'category_{category}')] for category in partners_links.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text('Выберите категорию партнеров:', reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text('Выберите категорию партнеров:', reply_markup=reply_markup)


async def button_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    category = query.data.split('_')[1]
    keyboard = [
        [InlineKeyboardButton(f"{i + 1}. {name}", url=url)] for i, (name, url) in enumerate(partners_links[category])
    ]
    keyboard.append([InlineKeyboardButton("Назад", callback_data='back_to_categories')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=f'Партнеры по категории "{category}":', reply_markup=reply_markup)


# Функция для обработки нажатия кнопки "Назад"
async def button_back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    await partners(update, context)


# Функция для команды /tasks
async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    task = random.choice(tasks_bank)
    await update.message.reply_text(task)


# Функция для команды /socials
async def socials(update: Update, context: CallbackContext) -> None:
    socials_info = "Соц. сети фестиваля:\nTelegram: https://t.me/careerschoolfest, ВКонтакте: https://vk.com/careerschoolfest\n\nСоц. сети granate.space:\nTelegram: https://t.me/granateyoung, ВКонтакте: https://vk.com/granateyoung"
    await update.message.reply_text(socials_info)


# Функция для обработки нажатия кнопки
async def handle_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data.startswith('category_'):
        await button_category(update, context)
    elif query.data == 'back_to_categories':
        await button_back(update, context)

async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if text == "Партнеры":
        await partners(update, context)
    elif text == "Получить задание":
        await tasks(update, context)
    elif text == "Наши соц. сети":
        await socials(update, context)
    else:
        await update.message.reply_text("Пожалуйста, выберите одну из предложенных опций.")


def main() -> None:
    # Создаем Application и передаем ему токен бота
    application = ApplicationBuilder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("tasks", tasks))
    application.add_handler(CommandHandler("partners", partners))
    application.add_handler(CommandHandler("socials", socials))
    application.add_handler(CallbackQueryHandler(handle_button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    application.run_polling()


if __name__ == '__main__':
    main()
