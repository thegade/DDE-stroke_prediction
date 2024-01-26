import re

import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Bot
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, filters, Filters
from telegram.ext import CallbackContext, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.main import prediction_from_model
from src.models import session, User, GenderEnum, get_worktypeenum_mapping, create_enum_mapping, gender_mapping, \
    work_type_mapping, residence_type_mapping, smoking_status_mapping

GENDER, AGE, HYPERTENSION, HEART_DISEASE, EVER_MARRIED, WORK_TYPE, RESIDENCE_TYPE, AVG_GLUCOSE_LEVEL, WEIGHT, HEIGHT, SMOKING_STATUS = range(
    11)


def start(update, context):
    user = update.message.from_user
    update.message.reply_text(
        'Привет! Я помогу вам создать анкету. Давай начнем с вашего пола.',
        reply_markup=ReplyKeyboardMarkup([['Мужской', 'Женский']], resize_keyboard=True, row_width=1, one_time_keyboard=True))

    return GENDER


def gender(update, context):
    user_id = update.message.from_user.id
    user = update.message.from_user
    context.user_data['gender'] = update.message.text
    update.message.reply_text('Сколько вам лет?')

    save_data(user_id, 'gender', update.message.text)
    return AGE


def age(update, context):
    user = update.message.from_user
    input_text = update.message.text

    pattern = re.compile("^[-+]?[0-9]+$")

    pattern.match(input_text)
    if pattern.match(input_text):
        context.user_data['age'] = update.message.text
    else:
        update.message.reply_text('Вы ввели число в неверном формате. Введите заново')
        return AGE
    update.message.reply_text('Есть ли у вас гипертония?',
                              reply_markup=
                              ReplyKeyboardMarkup([['Да', 'Нет'], ],
                                                  resize_keyboard=True, row_width=1,
                                                  one_time_keyboard=True))
    user_id = update.message.from_user.id
    save_data(user_id, 'age', update.message.text)
    return HYPERTENSION


def hypertension(update, context):
    user = update.message.from_user
    context.user_data['hypertension'] = update.message.text
    update.message.reply_text('Есть ли у вас сердечные заболевания? (Да/Нет)',
                              reply_markup=ReplyKeyboardMarkup([['Да', 'Нет']], resize_keyboard=True, row_width=1, one_time_keyboard=True)
                              )
    user_id = update.message.from_user.id
    value = False
    if update.message.text == 'Да':
        value = True
    save_data(user_id, 'hypertension', value)
    return HEART_DISEASE


def heart_disease(update, context):
    user = update.message.from_user
    context.user_data['heart_disease'] = update.message.text
    update.message.reply_text('Вы когда-либо были в браке? (Да/Нет)',
                              reply_markup=ReplyKeyboardMarkup([['Да', 'Нет']], resize_keyboard=True, row_width=1, one_time_keyboard=True)
                              )
    user_id = update.message.from_user.id
    value = False
    if update.message.text == 'Да':
        value = True
    save_data(user_id, 'heart_disease', value)
    return EVER_MARRIED


def ever_married(update, context):
    user = update.message.from_user
    context.user_data['ever_married'] = update.message.text

    but1 = telegram.KeyboardButton(text='Ребенок')
    but2 = telegram.KeyboardButton(text='Государственная работа')
    but3 = telegram.KeyboardButton(text='Не работал')
    but4 = telegram.KeyboardButton(text='Конфиденциально')
    but5 = telegram.KeyboardButton(text='Самозанятый')
    row1 = [but1, but2, but3]
    row2 = [but4, but5]
    # ['Ребенок', 'Государственная работа',
    #  'Не работал', 'Конфиденциально', 'Самозанятый']
    update.message.reply_text('Какой у вас тип работы?', reply_markup=ReplyKeyboardMarkup(
        [row1, row2], row_width=1,  one_time_keyboard=True))
    user_id = update.message.from_user.id
    value = False
    if update.message.text == 'Да':
        value = True
    save_data(user_id, 'ever_married', value)

    return WORK_TYPE


def work_type(update, context):
    user = update.message.from_user
    context.user_data['work_type'] = update.message.text
    update.message.reply_text('Какой ваш тип места жительства?',
                              reply_markup=ReplyKeyboardMarkup([['Сельский',
                                                                 'Городской']], resize_keyboard=True, row_width=1, one_time_keyboard=True))
    user_id = update.message.from_user.id
    save_data(user_id, 'work_type', update.message.text)

    return RESIDENCE_TYPE


def residence_type(update, context):
    user = update.message.from_user
    context.user_data['residence_type'] = update.message.text
    update.message.reply_text('Какой у вас средний уровень глюкозы в крови(мг/100мл)?')

    user_id = update.message.from_user.id
    save_data(user_id, 'residence_type', update.message.text)

    return AVG_GLUCOSE_LEVEL


def avg_glucose_level(update, context):
    user = update.message.from_user

    input_text = update.message.text

    pattern = re.compile(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?')

    input_text = input_text.replace(',', '.')
    if pattern.match(input_text):
        context.user_data['avg_glucose_level'] = float(input_text)
    else:
        update.message.reply_text('Вы ввели число в неверном формате. Введите заново')
        return AVG_GLUCOSE_LEVEL
    context.user_data['avg_glucose_level'] = update.message.text
    update.message.reply_text('Введите ваш вес(кг)')
    user_id = update.message.from_user.id
    save_data(user_id, 'avg_glucose_level', float(input_text))

    return WEIGHT


def weight(update, context):
    user = update.message.from_user
    input_text = update.message.text

    pattern = re.compile("^[-+]?[0-9]+$")

    pattern.match(input_text)
    if pattern.match(input_text):
        context.user_data['weight'] = update.message.text
    else:
        update.message.reply_text('Вы ввели число в неверном формате. Введите заново')
        return WEIGHT
    update.message.reply_text('Введите ваш рост(см)')
    user_id = update.message.from_user.id

    return HEIGHT


def height(update, context):
    user = update.message.from_user
    input_text = update.message.text

    pattern = re.compile("^[-+]?[0-9]+$")

    pattern.match(input_text)
    if pattern.match(input_text):
        context.user_data['height'] = update.message.text
    else:
        update.message.reply_text('Вы ввели число в неверном формате. Введите заново')
        return WEIGHT
    update.message.reply_text('Как вы оцениваете свой статус курения?',
                              reply_markup=ReplyKeyboardMarkup(
                                  [['Раньше курил', 'Никогда не курил',
                                    'Курю', 'Не скажу']], resize_keyboard=True,one_time_keyboard=True))
    user_id = update.message.from_user.id
    bmi = (int(context.user_data['weight']) / ((int(context.user_data['height']) / 100)
                                               * (int(context.user_data['height']) / 100)))
    save_data(user_id, 'bmi', bmi)
    return SMOKING_STATUS


# def bmi(update, context):
#     user = update.message.from_user
#     input_text = update.message.text
#
#     pattern = re.compile(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?')
#
#     input_text = input_text.replace(',', '.')
#     if pattern.match(input_text):
#         context.user_data['bmi'] = float(input_text)
#     else:
#         update.message.reply_text('Вы ввели число в неверном формате. Введите заново')
#         return SMOKING_STATUS
#     context.user_data['bmi'] = update.message.text
#     update.message.reply_text('Как вы оцениваете свой статус курения?',
#                               reply_markup=ReplyKeyboardMarkup(
#                                   [['Раньше курил', 'Никогда не курил',
#                                     'Курю', 'Не скажу']], one_time_keyboard=True))
#
#     user_id = update.message.from_user.id
#     save_data(user_id, 'bmi', float(input_text))
#
#     return SMOKING_STATUS


def smoking_status(update, context):
    user = update.message.from_user
    context.user_data['smoking_status'] = update.message.text
    user_id = update.message.from_user.id
    save_data(user_id, 'smoking_status', update.message.text)

    user_data = session.query(User).filter_by(tg_id=user_id).first()

    if user_data.hypertension:
        hypertension = 'Да'
    else:
        hypertension = 'Нет'

    if user_data.heart_disease:
        heartdisease = 'Да'
    else:
        heartdisease = 'Нет'

    if user_data.ever_married:
        ever_married = 'Да'
    else:
        ever_married = 'Нет'

    update.message.reply_text(
        f"Спасибо за заполнение анкеты!\n\n"
        f"Пол: {user_data.gender.value}\n"
        f"Возраст: {user_data.age}\n"
        f"Гипертония: {hypertension}\n"
        f"Сердечные заболевания: {heartdisease}\n"
        f"Состоите ли в браке: {ever_married}\n"
        f"Тип работы: {user_data.work_type.value}\n"
        f"Тип места жительства: {user_data.residence_type.value}\n"
        f"Средний уровень глюкозы: {user_data.avg_glucose_level}\n"
        f"Индекс массы тела (BMI): {user_data.bmi}\n"
        f"Статус курения: {user_data.smoking_status.value}\n"
        f"Чтобы посмотреть риск инсульта команда /prediction"
    )

    return ConversationHandler.END


def main():
    updater = Updater("6853612786:AAGC5TDG5_CcAfMLjvDKHVN_ARSN51rrykU")

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            GENDER: [MessageHandler(Filters.text & ~Filters.command, gender)],
            AGE: [MessageHandler(Filters.text & ~Filters.command, age)],
            HYPERTENSION: [MessageHandler(Filters.text & ~Filters.command, hypertension)],
            HEART_DISEASE: [MessageHandler(Filters.text & ~Filters.command, heart_disease)],
            EVER_MARRIED: [MessageHandler(Filters.text & ~Filters.command, ever_married)],
            WORK_TYPE: [MessageHandler(Filters.text & ~Filters.command, work_type)],
            RESIDENCE_TYPE: [MessageHandler(Filters.text & ~Filters.command, residence_type)],
            AVG_GLUCOSE_LEVEL: [MessageHandler(Filters.text & ~Filters.command, avg_glucose_level)],
            WEIGHT: [MessageHandler(Filters.text & ~Filters.command, weight)],
            HEIGHT: [MessageHandler(Filters.text & ~Filters.command, height)],
            SMOKING_STATUS: [MessageHandler(Filters.text & ~Filters.command, smoking_status)],
        },

        fallbacks=[CommandHandler('start', start)]
    )

    dp.add_handler(conv_handler)

    dp.add_handler(CommandHandler("prediction", prediction))

    updater.start_polling()
    updater.idle()


def prediction(update, context):
    user_id = update.message.from_user.id
    user = session.query(User).filter_by(tg_id=user_id).first()
    prediction_text = prediction_from_model(user)
    print(prediction_text)
    if prediction_text == 0:
        prediction_text = "В данный момент вы не подвержены риску инсульта"
    else:
        prediction_text = "В данный момент вы подвержены риску инсульта. Обратитесь к врачу"
    update.message.reply_text(prediction_text)


def save_data(user_id, attribute, value):
    user = session.query(User).filter_by(tg_id=user_id).first()

    if not user:
        user = User(tg_id=user_id)

    if attribute == 'gender':
        value = gender_mapping.get(value)
    if attribute == 'work_type':
        value = work_type_mapping.get(value)
    if attribute == 'residence_type':
        value = residence_type_mapping.get(value)
    if attribute == 'smoking_status':
        value = smoking_status_mapping.get(value)

    setattr(user, attribute, value)

    session.add(user)
    session.commit()


def replace_substring(test_str, s1, s2):
    test_str = re.sub(s1, s2, test_str)
    return test_str


if __name__ == '__main__':
    main()
