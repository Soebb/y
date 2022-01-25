import os, datetime, glob, subprocess, json
from telethon import TelegramClient, events, Button
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

previous_cut_time = '02:00:04'


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
msgid = 0
chatid = 0
@Bot.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def start(event):
    keyboard = []
    keyboard.append(refresh_button)
    try:
        for file in glob.glob('C:/dlmacvin/1aa/*'):
            try:
                keyboard.append(
                    [
                        Button.inline(
                            file.rsplit('/', 1)[1].replace('1aa\\', ''),
                            data=file.rsplit('/', 1)[1].replace('1aa\\', '')
                        )
                    ]
                )
            except Exception as e:
                print("problem with "+file)
                pass
    except Exception as e:
        print(e)
        pass
    keyboard.append(refresh_button)
    await event.reply("Which one?", buttons=keyboard)


@Bot.on(events.CallbackQuery)
async def callback(event):
    global msgid, previous_cut_time, chatid
    if event.data == b"refresh":
        keyboard = []
        keyboard.append(refresh_button)
        try:
            for file in glob.glob('C:/dlmacvin/1aa/*'):
                keyboard.append(
                    [
                        Button.inline(
                            file.rsplit('/', 1)[1].replace('1aa\\', ''),
                            data=file.rsplit('/', 1)[1].replace('1aa\\', '')
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
    try:
        name = event.data.decode('utf-8')
        input = 'C:/dlmacvin/1aa/' + name
        metadata = extractMetadata(createParser(input))
        duration = int(metadata.get('duration').seconds)
        dtime = str(datetime.timedelta(seconds=duration))[:11]
        async with Bot.conversation(event.chat_id) as conv:
            ask = await conv.send_message(f'تایم کل ویدیو : {dtime} \n\nجهت کات ویدیو تایم را به این صورت ارسال کنید \n 00:00:00 02:10:00 \n\nOr send /previous to keep the previous cut time.')
            time = await conv.get_response()
            time2 = time.text

        if time2 == "/previous":
            end = previous_cut_time
        else:
            end = f'0{time2[:1]}:{time2[:3][1:]}:{time2[3:]}'
            previous_cut_time = end
        start = "00:00:00"
        await time.delete()
        await ask.delete()
        process_msg = await Bot.send_message(event.chat_id, "processing..")

        ext = '.' + name.rsplit('.', 1)[1]
        end_sec = sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(end.split(":"))))
        os.system(f'''ffmpeg -ss {start} -i "{input}" -to {end} -c copy "C:/dlmacvin/1aa/videos/{name.replace(ext, '-0'+ext)}"''')
        cut_steps = []
        dif = duration - int(end_sec)
        for i in range(dif // 10):
            cut_steps.append(i * 10)
        for step in cut_steps:
            stp = str(end_sec + step)
            os.system(f'''ffmpeg -ss {start} -i "{input}" -to {stp} -c copy "C:/dlmacvin/1aa/videos/{name.replace(ext, '-'+str(step/10)+ext)}"''')
        await process_msg.delete()
        if chatid == 0:
            msg = await Bot.send_message(event.chat_id, 'Done! ' + name)
            msgid = msg.id
        elif chatid != 0:
            try:
                await Bot.edit_message(event.chat_id, msgid, 'Done! ' + name)
            except:
                await Bot.edit_message(event.chat_id, msgid, 'تمام')
        chatid = event.chat_id
    except Exception as e:
        print(e)


Bot.run_until_disconnected()
