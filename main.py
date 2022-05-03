from telegram.ext import Updater, MessageHandler, Filters  # итог: 708 строк
from telegram.ext import CommandHandler
import telegram
from flask import Flask
from flask_restful import Api
from data import db_session
from data.users import User
from telegram import ReplyKeyboardMarkup
from hab.type import *
from hab.make_pic import make_picture
import random
app = Flask(__name__)
app.config['SECRET_KEY'] = 'kkkk'
api = Api(app, catch_all_404s=True)
TOKEN = ''
bot = telegram.Bot(token=TOKEN)


def p_to_sth(update, context, chat_id, db_sess, f):
    user = is_it_new_user(chat_id, db_sess)
    user1 = db_sess.query(User).filter(User.room == user.room and User.telegram_id != user.telegram_id).first()
    for i in db_sess.query(User).all():
        if i.room == user.room and i.id != user.id:
            user1 = i
            break
    if is_pes_wanna_transform(user.moves, user.another):
        user.another = trans(user.moves, f, user.another)
        user1.another = trans(user1.moves, f, user1.another)
        db_sess.add(user)
        db_sess.add(user1)
        db_sess.commit()
        make_picture(user.moves, user.another)
        photo(update, context, int(user.telegram_id))
        photo(update, context, int(user1.telegram_id))


def p_to_lad(update, context):
    chat_id = update.message.chat_id
    db_sess = db_session.create_session()
    p_to_sth(update, context, chat_id, db_sess, 'l')


def p_to_hor(update, context):
    chat_id = update.message.chat_id
    db_sess = db_session.create_session()
    p_to_sth(update, context, chat_id, db_sess, 'h')


def p_to_ele(update, context):
    chat_id = update.message.chat_id
    db_sess = db_session.create_session()
    p_to_sth(update, context, chat_id, db_sess, 'e')


def p_to_fer(update, context):
    chat_id = update.message.chat_id
    db_sess = db_session.create_session()
    p_to_sth(update, context, chat_id, db_sess, 'f')


def new_user(telegram_id):
    user = User()
    user.telegram_id = telegram_id
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


def is_it_new_user(i, db_sess):
    if db_sess.query(User).filter(User.telegram_id == i).first() in db_sess.query(User).all():
        user = db_sess.query(User).filter(User.telegram_id == i).first()
    else:
        new_user(i)
        user = db_sess.query(User).filter(User.telegram_id == i).first()
        print('New user:', i)
    return user


def turn(update, context):
    db_sess = db_session.create_session()
    chat = update.effective_chat
    user = is_it_new_user(str(chat.id), db_sess)
    if user.color:
        user1 = db_sess.query(User).filter((User.room == user.room) and (User.id != user.id)).first()
        for i in db_sess.query(User).all():
            if i.room == user.room and i.id != user.id:
                user1 = i
                break
        flag = True
        if user.color == 'b':
            if (not user.moves) or (len(user.moves.split(';')) % 2 == 0):
                flag = False
                update.message.reply_text("Вы не можете ходить. Сейчас ход другого игрока.")

        else:
            if len(user.moves.split(';')) % 2 != 0 and user.moves:
                flag = False
                update.message.reply_text("Вы не можете ходить. Сейчас ход другого игрока.")
        if flag:
            a = update.message.text
            if is_it_correct(a):
                a = is_it_correct(a)
                if try_go(a, user.moves, user.color, user.another):
                    bot.send_message(chat_id=int(user1.telegram_id), text=f"Ваш оппонент сделал ход: {a}")
                    if user.moves:
                        if is_pes_wanna_transform(user.moves + ';' + a, user.another):

                            reply_keyboard = [['/promotion_to_bishop', '/promotion_to_queen'],
                                              ['/promotion_to_knight', '/promotion_to_rook']]
                            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
                            user.moves = user.moves + ';' + a
                            user1.moves = user1.moves + ';' + a
                            update.message.reply_text(
                                "Выбери в кого хочешь превратить пешку\n"
                                "(/promotion_to_bishop - слон, /promotion_to_queen - ферзь,\n"
                                " /promotion_to_knight - конь, /promotion_to_rook - ладья)", reply_markup=markup)
                        else:
                            user.moves = user.moves + ';' + a
                            user1.moves = user1.moves + ';' + a
                            make_picture(user.moves, user.another)
                            photo(update, context, int(user.telegram_id))
                            photo(update, context, int(user1.telegram_id))
                    else:
                        user.moves = a
                        user1.moves = a
                        make_picture(user.moves, user.another)
                        photo(update, context, int(user.telegram_id))
                        photo(update, context, int(user1.telegram_id))
                    end = is_shag(user.moves, user.another)
                    if end[user.color + 'k']:
                        update.message.reply_text("Вашему королю поставлен мат.")
                        bot.send_message(chat_id=int(user1.telegram_id), text=f"Вы выйграли!")
                        update.message.reply_text("Вы вышли из комнаты.")
                        bot.send_message(chat_id=int(user1.telegram_id), text=f"Вы вышли из комнаты.")
                        a = user.room
                        for i in db_sess.query(User).filter(User.room == a):
                            i.room = ''
                            i.moves = ''
                            i.color = ''
                            i.another = ''
                    elif end[user1.color + 'k']:
                        bot.send_message(chat_id=int(user1.telegram_id), text=f"Шах")
                else:
                    update.message.reply_text("Ход невозможен")
            else:
                update.message.reply_text("Ход введён не корректно.")

        db_sess.add(user)
        db_sess.add(user1)
        db_sess.commit()


def start(update, context):
    db_sess = db_session.create_session()
    chat = update.effective_chat
    is_it_new_user(str(chat.id), db_sess)
    reply_keyboard = [['/help', '/create_room']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Привет! Я Бот Крутых Шахмат, зови друзей и будем"
        " дуэлиться за звание главного шахматиста. Пропиши команду /help,"
        " чтобы узнать основны команды и правила пользования ботом.", reply_markup=markup)


def help(update, context):
    db_sess = db_session.create_session()
    chat = update.effective_chat
    is_it_new_user(str(chat.id), db_sess)
    update.message.reply_text(
        "Осовые команды Крутого Шахматного Бота:\n"
        "/create_room {ключ} - команда для создания комнаты,"
        " в которой и происходят поединки. Вы можете задать свой собственный"
        " ключ от комнаты просто написав его вместе с командой через пробел."
        " Если вы этого не сделаете Бот сам создаст ключ\n"
        "/join_room {ключ} - команда для присоединения к какой-либо комнате по ключу."
        " Ключ от комнаты вводится через пробел на строке вместе с командой."
        " Если не ввести ключ вы не можете ни к кому присоединиться. Максимальное число игроков в комнате - 2.\n"
        "/exit_room - команда для выхода из комнаты. Внимание при выходе из комнаты ход игры теряется."
        "Когда ваш оппонет выходит из комнаты, вы тоже автоматически из неё выходите.\n"
        "\n"
        "Как только вы вошли в комнату, вам случайным образом назначается цвет. (Первые ходят белые)\n"
        "Для того чтобы походить введите номер клетки фигуры,"
        " на которой стоит фигура, '-' клетка куда вы хотите её поставить.\nПример ввода: A2 - A3."
        " (Также возможно: a2 - a3/A2-A3/a2-a3)\n"
        "/roki {сторона} - команда для рокировки. После команды нужно написать "
        "в какую сторону делать рокировку l(лево)/r(право).\nПример ввода: /roki r. (или /roki l)\n\n"
        "Для игры с кем-то создайте в команту и передайте ключ от неё своему оппоненту,"
        " после чего наслаждайте любимыми шахматами.")


def photo(update, context, chat_id, n='1'):
    db_sess = db_session.create_session()
    is_it_new_user(str(chat_id), db_sess)
    bot.send_photo(chat_id=chat_id, photo=open(f'hab/pic/board{n}.png', 'rb'))


def room(update, context):
    db_sess = db_session.create_session()
    chat_id = update.message.chat_id
    user = is_it_new_user(str(chat_id), db_sess)
    if user.room:
        update.message.reply_text(
            "Вы уже находитесь в комнате")
    else:
        if not context.args:
            while True:
                a = str(random.randint(100000, 999999))
                if db_sess.query(User).filter(User.room == a).first() not in db_sess.query(User).all():
                    user.room = str(a)
                    db_sess.add(user)
                    db_sess.commit()
                    update.message.reply_text(
                        f"Вы создали комнату. Ключ для входа: {a}")
                    break
        else:
            a = context.args[0]
            if db_sess.query(User).filter(User.room == a).first() in db_sess.query(User).all():
                update.message.reply_text(
                    "Извините, такой ключ для комнаты уже имеется в базе, попробуйте другой")
            else:
                user.room = str(a)
                db_sess.add(user)
                db_sess.commit()
                update.message.reply_text(
                    f"Вы создали комнату. Ключ для входа: {a}")


def join_room(update, context):
    db_sess = db_session.create_session()
    chat_id = update.message.chat_id
    user = is_it_new_user(str(chat_id), db_sess)
    if user.room:
        update.message.reply_text(
            "Вы уже находитесь в комнате")
    else:
        if not context.args:
            update.message.reply_text(
                "Вы не ввели ключ от комнаты. Для понимания приципа работы команд, вызовите команду /help")
        else:
            a = context.args[0]
            if db_sess.query(User).filter(User.room == a).first() in db_sess.query(User).all():
                if len(db_sess.query(User).filter(User.room == a).all()) <= 2:
                    color = ['w', 'b']
                    c = {'w': 'белый', 'b': 'чёрный'}
                    random.shuffle(color)
                    user.room = str(a)
                    user.color = color[0]
                    print('room', user.room)

                    user1 = db_sess.query(User).filter((User.room == user.room) and (User.id != user.id)).first()
                    for i in db_sess.query(User).all():
                        if i.room == user.room and i.id != user.id:
                            user1 = i
                            break
                    user1.color = color[1]
                    print(user1.telegram_id, user1.color)
                    db_sess.add(user1)
                    db_sess.add(user)
                    db_sess.commit()
                    update.message.reply_text(
                        f"Вы успежно вошли в комнату. Ваш цвет - {c[color[0]]}")
                    bot.send_message(chat_id=int(user1.telegram_id), text=f"К вам присоединился оппонент. "
                                                                          f"Ваш цвет - {c[color[1]]}")
                    photo(update, context, int(user.telegram_id), '2')
                    photo(update, context, int(user1.telegram_id), '2')

                else:
                    update.message.reply_text(
                        f"Извините, комната переполнена (максимальное количество участников - 2)")
            else:
                update.message.reply_text(
                    "Извините, комнаты с таким ключом не существует.")


def exit_room(update, context):
    db_sess = db_session.create_session()
    chat_id = update.message.chat_id
    user = is_it_new_user(str(chat_id), db_sess)
    if user.room:
        a = user.room
        for i in db_sess.query(User).filter(User.room == a):
            i.room = ''
            i.moves = ''
            i.color = ''
            i.another = ''
            if i.telegram_id == user.telegram_id:
                update.message.reply_text("Вы успешно вышли из комнаты.")
            else:
                bot.send_message(chat_id=int(i.telegram_id), text="Ваш оппонент вышел из комнаты."
                                                                  " Вам тоже пришлось её покинуть.")

            db_sess.add(i)
        db_sess.commit()
    else:
        update.message.reply_text("Вы не находились в комнате.")


def roki(update, context):
    db_sess = db_session.create_session()
    chat = update.effective_chat
    user = is_it_new_user(str(chat.id), db_sess)
    user1 = db_sess.query(User).filter(User.room == user.room and User.telegram_id != user.telegram_id).first()
    for i in db_sess.query(User).all():
        if i.room == user.room and i.id != user.id:
            user1 = i
            break
    if user.moves:
        s = len(user.moves.split(';'))
    else:
        s = 0
    if s and ((user.color == 'w' and s % 2 == 0) or (user.color == 'b' and s % 2 != 0)):
        if (not context.args) or context.args[0] not in ['l', 'r']:
            update.message.reply_text("Не верно задана рокировка")
        else:
            a = rok(user.moves, user.color, context.args[0], user.another)
            if a:
                user.moves = user.moves + ';' + a
                user1.moves = user1.moves + ';' + a
                db_sess.add(user)
                db_sess.add(user1)
                db_sess.commit()
                make_picture(user.moves, user.another)
                photo(update, context, int(user.telegram_id))
                photo(update, context, int(user1.telegram_id))
            else:
                update.message.reply_text("Рокировка не возможна.")
    else:
        update.message.reply_text("Вы не можете сделать рокировку.")


def main():
    db_session.global_init("db/players.db")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("create_room", room))
    dp.add_handler(CommandHandler("join_room", join_room))
    dp.add_handler(CommandHandler("exit_room", exit_room))
    dp.add_handler(CommandHandler("promotion_to_bishop", p_to_ele))
    dp.add_handler(CommandHandler("promotion_to_queen", p_to_fer))
    dp.add_handler(CommandHandler("promotion_to_knight", p_to_hor))
    dp.add_handler(CommandHandler("promotion_to_rook", p_to_lad))
    dp.add_handler(CommandHandler("roki", roki))
    text_handler = MessageHandler(Filters.text, turn)
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
