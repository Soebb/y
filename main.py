import os, time, glob, datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import PTN
import shutil
from pyromod import listen


BOT_TOKEN=" "
API_ID=" "
API_HASH=" "

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

main = folder.rsplit('/', 1)[1] + '\\'

refresh_button = [
    InlineKeyboardButton(
        text='Refresh List',
        callback_data='refresh'
    )
]
def gettime(t2):
    t3 = sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(t2[:8].split(":"))))
    if "." in t2:
        t = t3
    else:
        t = int(t3) + int(t2[9:][:3])
    return str(t)

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
        try:
            await update.message.edit(text=f"Which one of these {len(keyboard)} videos?", reply_markup=InlineKeyboardMarkup(keyboard))
        except:
            await update.message.reply_text("error!! Send /start")
        return
    tmp = 'khorooji/'
    if not os.path.isdir(tmp):
        os.makedirs(tmp)
    input = folder + "/" + update.data
    try:
        vname = update.data.replace('.ts', '.mp4')
        aac = vname.rsplit(".", 1)[0]+'.aac'
        n = PTN.parse(vname.rsplit(".", 1)[0])
        title = n['title'].replace("-", " ")
        au2_1 = f'C:/All Projact Primer Pro/Audio Sound Serial Primer Pro Tag/{title}/2.1.mp3'

        t2t = await update.message.reply_text('همه‌ی تایم‌هارو بکجا بفرست')
        t22: Message = await bot.listen(update.message.chat.id, filters=filters.text)        
        t2, t3_1, t3_2, t3_3, t3_4, t3_5, t6 = get_time(t22.text)
        prccs = await update.message.reply_text("processing..")
        os.system(f'ffmpeg -i "{au2_1}" -i 2.2.mp3 -y 2.mp3')
        os.system(f'ffmpeg -i "{input}" -vn -i {a1} -vn -i {a2} -vn -i {a3} -vn -i {a6} -vn -filter_complex "[1]adelay=00000|00000[b]; [2]adelay={t2}|{t2}[c]; [3]adelay={t3_1}|{t3_1}[d]; [3]adelay={t3_2}|{t3_2}[e]; [3]adelay={t3_3}|{t3_3}[f]; [3]adelay={t3_4}|{t3_4}[g]; [3]adelay={t3_5}|{t3_5}[h]; [4]adelay={t6}|{t6}[i]; [0][b][c][d][e][f][g][h][i]amix=9" -c:a aac -b:a 125k -y "{tmp}{aac}"')   
        time.sleep(10)
        os.system(f'ffmpeg -i "{input}" -i "{tmp}{aac}" -c copy -map 0:0 -map 1:0 -y "{tmp}{vname}"')
        time.sleep(10)
        #await update.message.reply_text(f"Done. Check {tmp}{vname}")
        await bot.send_audio(chat_id=update.message.chat.id, audio=tmp+aac, caption=f"also saved in {tmp}{aac}")
        os.remove(tmp+aac)
        await bot.send_video(chat_id=update.message.chat.id, video=tmp+vname, caption=f"also saved in {tmp}{vname}")
        ask = await update.message.reply_text('remove merged video in system?\n /yes or /no')
        ans: Message = await bot.listen(update.message.chat.id, filters=filters.text)
        if "yes" in ans.text:
            os.remove(tmp+vname)
        await ans.delete(True)
        await ask.delete()
        await prccs.delete()
        await t22.delete(True)
        await t2t.delete()
    except Exception as e:
        print(e)

Bot.run()
