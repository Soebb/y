import os, time, glob, datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import PTN
import shutil
from pyromod import listen

BOT_TOKEN = " "
API_ID = " "
API_HASH = " "


Bot = Client(
    ":memory:",
    bot_token = BOT_TOKEN,
    api_id = API_ID,
    api_hash = API_HASH
)


folder = 'C:/Users/Administrator/Downloads/Telegram Desktop'
msgid = 0
chatid = 0
vdir = folder + '/*'
a1 = '1.mp3'
a2 = '2.mp3'
a3 = '3.mp3'
a6 = '6.mp3'
aac = 'a2.aac'
main = folder.rsplit('/', 1)[1] + '\\'

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

@Bot.on_message(filters.text)
async def stt(bot, m):
    keyboard = []
    keyboard.append(refresh_button)
    try:
        for file in glob.glob(vdir):
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
    await m.reply_text(text="Which one?", reply_markup=InlineKeyboardMarkup(keyboard))


@Bot.on_callback_query()
async def callback(bot, update):
    #global chatid
    #global msgid
    #global previous_cut_time
    if update.data == "refresh":
        keyboard = []
        keyboard.append(refresh_button)
        try:
            for file in glob.glob(vdir):
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
        await update.message.edit(text="Which one?", reply_markup=InlineKeyboardMarkup(keyboard))
        return
    tmp = 'khorooji/'
    if not os.path.isdir(tmp):
        os.makedirs(tmp)
    input = folder + "/" + update.data
    try:
        vname = update.data.replace('.ts', '.mp4')
        n = PTN.parse(vname)
        title = n['title'].replace("-", " ")
        au2_1 = f'C:/All Projact Primer Pro/Audio Sound Serial Primer Pro Tag/{title}/2.1.mp3'
        
        t2t = await update.message.reply_text('تایم واسه تگ صوت 2 (2.2 + 2.1) رو بفرست')
        t22: Message = await bot.listen(update.message.chat.id, filters=filters.text)
        t3t = await update.message.reply_text('پنج تا تایم واسه تگ صوت سوم رو بفرست\n3.mp3')
        t33: Message = await bot.listen(update.message.chat.id, filters=filters.text)
        t6t = await update.message.reply_text('تایم واسه تگ صوت 6 رو بفرست\n6.mp3')
        t66: Message = await bot.listen(update.message.chat.id, filters=filters.text)
        t2 = int(gettime(t22.text))
        t3_1, t3_2, t3_3, t3_4, t3_5 = t33.text.split()
        t3_1 = int(gettime(t3_1))
        t3_2 = int(gettime(t3_2))
        t3_3 = int(gettime(t3_3))
        t3_4 = int(gettime(t3_4))
        t3_5 = int(gettime(t3_5))
        t6 = int(gettime(t66.text))
        prccs = await update.message.reply_text("processing..")
        os.system(f'ffmpeg -i "{au2_1}" -i 2.2.mp3 -y 2.mp3')
        os.system(f'ffmpeg -i "{input}" -vn -i {a1} -vn -i {a2} -vn -i {a3} -vn -i {a6} -vn -filter_complex "[1]adelay=00000|00000[b]; [2]adelay={t2}|{t2}[c]; [3]adelay={t3_1}|{t3_1}[d]; [3]adelay={t3_2}|{t3_2}[e]; [3]adelay={t3_3}|{t3_3}[f]; [3]adelay={t3_4}|{t3_4}[g]; [3]adelay={t3_5}|{t3_5}[h]; [4]adelay={t6}|{t6}[i]; [0][b][c][d][e][f][g][h][i]amix=9" -c:a aac -b:a 125k -y {aac}')   
        time.sleep(10)
        os.system(f'ffmpeg -i "{input}" -i {aac} -c copy -map 0:0 -map 1:0 -y "{tmp}{vname}"')
        #await update.message.reply_text(f"Done. Check {tmp}{vname}")
        await bot.send_video(chat_id=update.message.chat.id, video=tmp+vname, caption=f"also saved in {tmp}{vname}")
        ask = await update.message.reply_text('remove output in system?\n /yes or /no')
        ans: Message = await bot.listen(update.message.chat.id, filters=filters.text)
        if "yes" in ans.text:
            os.remove(tmp+vname)
        await ans.delete(True)
        await ask.delete()
        await prccs.delete()
        await t66.delete(True)
        await t22.delete(True)
        await t33.delete(True)
        await t2t.delete()
        await t6t.delete()
        await t3t.delete()
    except Exception as e:
        print(e)

Bot.run()
