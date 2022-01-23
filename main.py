import os, time, glob, datetime
import PTN
import shutil
from telethon import TelegramClient, events, Button


BOT_TOKEN = " "
API_ID = " "
API_HASH = " "

BOT_NAME = "tagsot"


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
org = 'org.mp3'
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
            if file.endswith(('.ts', '.mp4', '.mkv')):
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
    if event.data == b"refresh":
        keyboard = []
        keyboard.append(refresh_button)
        try:
            for file in glob.glob(vdir):
                if file.endswith(('.ts', '.mp4', '.mkv')):
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
            await Bot.send_message(event.chat_id, "error!! Send /start")
        return
    tmp = "C:/Users/Administrator/Downloads/Telegram Desktop/tage soti zade shode/"

    if not os.path.isdir(tmp):
        os.makedirs(tmp)
    input = folder + "/" + event.data.decode('utf-8')
    try:
        vname = event.data.decode('utf-8').replace('.ts', '.mp4')
        aac = vname.rsplit(".", 1)[0]+'.aac'
        n = PTN.parse(vname.rsplit(".", 1)[0])
        title = n['title'].replace("-", " ")
        au2_1 = f'C:/All Projact Primer Pro/Audio Sound Serial Primer Pro Tag/{title}/2.1.mp3'
        async with Bot.conversation(event.chat_id) as conv:
            t2t = await conv.send_message('همه‌ی تایم‌هارو بکجا بفرست')
            t22 = await conv.get_response()
            o = t22.text.split()
        t2 = int(get_time(o[0]))
        t3_1=int(get_time(o[1]))
        t3_2=int(get_time(o[2]))
        t3_3=int(get_time(o[3]))
        t3_4=int(get_time(o[4]))
        t3_5=int(get_time(o[5]))
        t6=int(get_time(o[-1]))
        prccs = await Bot.send_message(event.chat_id, f"🔹Name : {title}\n\n🟠status : working")

        os.system(f'ffmpeg -i "{au2_1}" -i 2.2.mp3 -y 2.mp3')
        os.system(f'ffmpeg -i "{input}" -vn -y org.mp3')
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
        out.export("mix.mp3", format="mp3")
        os.system(f'ffmpeg -i mix.mp3 -y "{tmp}{aac}"')
        os.system(f'ffmpeg -i "{input}" -i "{tmp}{aac}" -c copy -map 0:0 -map 1:0 -y "{tmp}{vname}"')
        done = await Bot.send_message(event.chat_id, f"🔹Name : {title}\n\n🟢status : done")
        time.sleep(5)
        #await update.message.reply_text(f"Done. Check {tmp}{vname}")
        await Bot.send_file(event.chat_id, file=tmp+aac)
        #os.remove(tmp+aac)
        os.remove("mix.mp3")
        await Bot.send_file(event.chat_id, file=tmp+vname)
        await prccs.delete()
        await t22.delete()
        await t2t.delete()
        async with Bot.conversation(event.chat_id) as conv:
            ask = await conv.send_message('send /video , /audio to remove them in system.\nOr send /both to remove /both ,\nOr send /skip to skip and delete this msg')
            ans = await conv.get_response()
        if "video" in ans.text:
            os.remove(tmp+vname)
        elif "audio" in ans.text:
            os.remove(tmp+aac)
        elif "both" in ans.text:
            os.remove(tmp+vname)
            os.remove(tmp+aac)
        await ans.delete()
        await ask.delete()
    except Exception as e:
        print(e)

Bot.run_until_disconnected()
