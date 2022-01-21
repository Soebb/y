from pydub import AudioSegment
import os, time, glob, datetime
import PTN
import shutil
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, MessageHandler, CallbackQueryHandler, CallbackContext, Filters

BOT_TOKEN = " "


folder = 'C:/Users/Administrator/Downloads/Telegram Desktop'
msgid1 = msgid2 = 0
vdir = folder + '/*'
dir = 'C:/voicetag/'
a1 = dir + '1.mp3'
a2 = dir + '2.mp3'
a3 = dir + '3.mp3'
a6 = dir + '6.mp3'
aac = dir + 'a.aac'
org = dir + 'org.mp3'
main = folder.rsplit('/', 1)[1] + '\\'
texxt = None

refresh_button = [
    InlineKeyboardButton(
        text='Refresh List',
        callback_data='refresh'
    )
]

def gettime(t2):
    try:
        tt2 = t2.split('.')[1]
        t2 = t2.split('.')[0]
        t2 = f'0{t2[:1]}:{t2[:3][1:]}:{t2[3:]}'
    except:
        tt2 = None
        t2 = f'0{t2[:1]}:{t2[:3][1:]}:{t2[3:]}'
    t2 = sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(t2.split(":"))))
    if tt2 != None:
        t2 = f'{t2}{tt2[:1]}00'
    else:
        t2 = f'{t2}000'
    return t2

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    global msgid1, texxt
    if not "/" in update.message.text:
        msg = update.effective_message.reply_text("ذخیره شد")
        texxt = update.message.text
        #msgid1 = msg.message_id
        update.message.delete()
        msg.delete()
        return
    keyboard = []
    keyboard.append(refresh_button)
    try:
        for file in glob.glob(vdir):
            if file.endswith(('.ts', '.mp4', '.mkv')):
                keyboard.append(
                    [
                        InlineKeyboardButton(
                            text=file.rsplit('/', 1)[1].replace(main, ''),
                            callback_data=file.rsplit('/', 1)[1].replace(main, '')
                        )
                    ]
                )
    except Exception as e:
        print(e)
        return
    keyboard.append(refresh_button)
    #await bot.send_message(chat_id=id, text="Which one?", reply_markup=InlineKeyboardMarkup(keyboard))
    update.effective_message.reply_text(text="Which one?", reply_markup=InlineKeyboardMarkup(keyboard))
    if texxt == None:
        msg = update.effective_message.reply_text(" تایم‌هارو نفرستادی، اول همه‌ی تایم‌هارو یکجا باهم بفرست ")
        msgid1 = msg.message_id
    update.message.delete()


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    global msgid1, texxt, msgid2
    query = update.callback_query
    try:
        context.bot.delete_message(chat_id=query.effective_message.chat_id, message_id=msgid1)
    except:
        pass
    if query.data == "refresh":
        keyboard = []
        keyboard.append(refresh_button)
        try:
            for file in glob.glob(vdir):
                if file.endswith(('.ts', '.mp4', '.mkv')):
                    keyboard.append(
                        [
                            InlineKeyboardButton(
                                text=file.rsplit('/', 1)[1].replace(main, ''),
                                callback_data=file.rsplit('/', 1)[1].replace(main, '')
                            )
                        ]
                    )
        except Exception as e:
            print(e)
            return
        keyboard.append(refresh_button)
        query.edit_message_text(text="Which one?", reply_markup=InlineKeyboardMarkup(keyboard))
        return
    vname = query.data
    try:
        if vname:
            if vname != "refresh":
                #ext = '.' + file.rsplit('.', 1)[1]
                v = folder + '/' + vname
                vname = vname.replace('.ts', '.mp4')
                try:
                    os.remove(a2)
                except:
                    pass
                try:
                    os.remove(dir + '2.1.mp3')
                except:
                    pass
                try:
                    os.remove(dir + 'mix.mp3')
                except:
                    pass
                n = PTN.parse(vname)
                title = n['title'].replace("-", " ")
                au2_1 = f'C:/All Projact Primer Pro/Audio Sound Serial Primer Pro Tag/{title}/2.1.mp3'
                shutil.copyfile(au2_1, dir + '2.1.mp3')
                t2, t3_1, t3_2, t3_3, t3_4, t3_5, t6 = texxt.split()
                t3_1 = gettime(t3_1)
                t3_2 = gettime(t3_2)
                t3_3 = gettime(t3_3)
                t3_4 = gettime(t3_4)
                t3_5 = gettime(t3_5)
                t6 = gettime(t6)
                t2 = gettime(t2)
                processmsg = update.effective_message.reply_text('processing..')
                a2_1 = AudioSegment.from_mp3(dir + '2.1.mp3')
                a2_2 = AudioSegment.from_mp3(dir + '2.2.mp3')
                aa2 = a2_1.append(a2_2)
                aa2.export(dir+"2.mp3", format="mp3")
                os.system(f'ffmpeg -i "{v}" -vn -y org.mp3')
                aud2 = AudioSegment.from_mp3(a2)
                aud3 = AudioSegment.from_mp3(a3)
                audorg = AudioSegment.from_mp3(org)
                aud1 = AudioSegment.from_mp3(a1)
                aud6 = AudioSegment.from_mp3(a6)
                out = audorg.overlay(aud1, gain_during_overlay=-2)
                out = out.overlay(aud2, position=t2, gain_during_overlay=-2)
                out = out.overlay(aud3, position=t3_1, gain_during_overlay=-2)
                out = out.overlay(aud3, position=t3_2, gain_during_overlay=-2)
                out = out.overlay(aud3, position=t3_3, gain_during_overlay=-2)
                out = out.overlay(aud3, position=t3_4, gain_during_overlay=-2)
                out = out.overlay(aud3, position=t3_5, gain_during_overlay=-2)
                out = out.overlay(aud6, position=t6, gain_during_overlay=-2)
                out.export(dir+"mix.mp3", format="mp3")
                os.system(f'ffmpeg -i mix.mp3 a.aac')
                time.sleep(10)
                os.system(f'ffmpeg -i "{v}" -i a.aac -c copy -map 0:0 -map 1:0 -y "{vname}"')
                processmsg.delete()
                if msgid2 == 0:
                    msg = update.effective_message.reply_text('Done! ' + vname)
                    msgid2 = msg.message_id
                elif msgid2 != 0:
                    try:
                        context.bot.edit_message_text(text='Done! ' + vname, chat_id=update.effective_message.chat.id, message_id=msgid2)
                    except:
                        try:
                            context.bot.edit_message_text(text='تمام', chat_id=update.effective_message.chat.id, message_id=msgid2)
                        except:
                            pass
    except Exception as e:
        print(e)
        pass
    texxt = None

updater = Updater(BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_handler(MessageHandler(Filters.text, start))
updater.start_polling()
updater.idle()
