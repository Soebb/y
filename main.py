import os, time, glob, datetime
import PTN
import shutil
from telethon import TelegramClient, events, Button


BOT_TOKEN = " "
API_ID = " "
API_HASH = " "

BOT_NAME = "cuttttter"


Bot = TelegramClient(BOT_NAME, API_ID, API_HASH).start(bot_token=BOT_TOKEN)

refresh_button = [
    Button.inline(
        "Refresh List",
        data="refresh"
    )
]

folder = 'C:/Users/Administrator/Downloads/Telegram Desktop'
msgid = 0
chatid = 0
vdir = folder + '/*'
a1 = '1.mp3'
a2 = '2.mp3'
a3 = '3.mp3'
a6 = '6.mp3'

main = folder.rsplit('/', 1)[1] + '\\'


def get_time(t2):
    t3 = sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(t2[:8].split(":"))))
    if not "." in t2:
        t = int(t3)*1000
    else:
        t = int(t3)*1000 + int(t2[9:][:3])
    return str(t)

@Bot.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def stt(event):
    keyboard = []
    keyboard.append(refresh_button)
    try:
        for file in glob.glob(vdir):
            keyboard.append(
                [
                    Button.inline(
                        file.rsplit('/', 1)[1].replace(main, ''),
                        data=file.rsplit('/', 1)[1].replace(main, '')
                    )
                ]
            )
    except Exception as e:
        print(e)
        return
    keyboard.append(refresh_button)
    #await bot.send_message(chat_id=id, text="Which one?", reply_markup=InlineKeyboardMarkup(keyboard))
    await event.reply("Which one?", buttons=keyboard)


@Bot.on(events.CallbackQuery)
async def callback(event):
    #global chatid
    #global msgid
    #global previous_cut_time
    if update.data == b"refresh":
        keyboard = []
        keyboard.append(refresh_button)
        try:
            for file in glob.glob(vdir):
                keyboard.append(
                    [
                        Button.inline(
                            file.rsplit('/', 1)[1].replace(main, ''),
                            data=file.rsplit('/', 1)[1].replace(main, '')
                        )
                    ]
                )
        except Exception as e:
            print(e)
            return
        keyboard.append(refresh_button)
        try:
            await event.edit(f"Which one of these {len(keyboard)} videos?", buttons=keyboard)
        except:
            await Bot.send_message("error!! Send /start")
        return
    tmp = 'khorooji/'
    if not os.path.isdir(tmp):
        os.makedirs(tmp)
    input = folder + "/" + update.data.decode('utf-8')
    try:
        vname = update.data.decode('utf-8').replace('.ts', '.mp4')
        aac = vname.rsplit(".", 1)[0]+'.aac'
        n = PTN.parse(vname.rsplit(".", 1)[0])
        title = n['title'].replace("-", " ")
        au2_1 = f'C:/All Projact Primer Pro/Audio Sound Serial Primer Pro Tag/{title}/2.1.mp3'
        async with Bot.conversation(event.chat_id) as conv:
            t2t = await conv.send_message('همه‌ی تایم‌هارو بکجا بفرست')
            t22 = await conv.get_response()
            t223 = t22.text
        t2, t3_1, t3_2, t3_3, t3_4, t3_5, t6 = get_time(t223.split())
        prccs = await Bot.send_message("processing..")
        os.system(f'ffmpeg -i "{au2_1}" -i 2.2.mp3 -y 2.mp3')
        os.system(f'ffmpeg -i "{input}" -vn -i {a1} -vn -i {a2} -vn -i {a3} -vn -i {a6} -vn -filter_complex "[1]adelay=00000|00000[b]; [2]adelay={t2}|{t2}[c]; [3]adelay={t3_1}|{t3_1}[d]; [3]adelay={t3_2}|{t3_2}[e]; [3]adelay={t3_3}|{t3_3}[f]; [3]adelay={t3_4}|{t3_4}[g]; [3]adelay={t3_5}|{t3_5}[h]; [4]adelay={t6}|{t6}[i]; [0][b][c][d][e][f][g][h][i]amix=9" -c:a aac -b:a 125k -y "{tmp}{aac}"')   
        time.sleep(10)
        os.system(f'ffmpeg -i "{input}" -i "{tmp}{aac}" -c copy -map 0:0 -map 1:0 -y "{tmp}{vname}"')
        time.sleep(10)
        #await update.message.reply_text(f"Done. Check {tmp}{vname}")
        await bot.send_audio(chat_id=update.message.chat.id, audio=tmp+aac, caption=f"also saved in {tmp}{aac}")
        os.remove(tmp+aac)
        await bot.send_video(chat_id=update.message.chat.id, video=tmp+vname, caption=f"also saved in {tmp}{vname}")
        async with Bot.conversation(event.chat_id) as conv:
            ask = await conv.send_message('remove merged video in system?\n /yes or /no')
            ans = await conv.get_response()
        if "yes" in ans.text:
            os.remove(tmp+vname)
        await ans.delete()
        await ask.delete()
        await prccs.delete()
        await t22.delete()
        await t2t.delete()
    except Exception as e:
        print(e)

Bot.run_until_disconnected()
