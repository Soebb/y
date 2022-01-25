import os, datetime, glob, subprocess, json
from telethon import TelegramClient, events, Button
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser


folder = "C:/temp"
BOT_TOKEN = " "
API_ID = " "
API_HASH = " "

BOT_NAME = "cuut"


Bot = TelegramClient(BOT_NAME, API_ID, API_HASH).start(bot_token=BOT_TOKEN)

refresh_button = [
    Button.inline(
        "Refresh List",
        data="refresh"
    )
]
msgid = 0
chatid = 0
v=folder+'*/'
main = folder.rsplit('/', 1)[1] + '\\'
@Bot.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def start(event):
    keyboard = []
    keyboard.append(refresh_button)
    try:
        for file in glob.glob(v):
            try:
                keyboard.append(
                    [
                        Button.inline(
                            file.rsplit('/', 1)[1].replace(main, ''),
                            data=file.rsplit('/', 1)[1].replace(main, '')
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
            for file in glob.glob(v):
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
    try:
        name = event.data.decode('utf-8')
        input = folder + "/" + name
        metadata = extractMetadata(createParser(input))
        duration = int(metadata.get('duration').seconds)
        process_msg = await Bot.send_message(event.chat_id, "processing..")
        ext = '.' + name.rsplit('.', 1)[1]
        x = duration // 3
        os.system(f'''ffmpeg -ss 0 -i "{input}" -to {x} -c copy "C:/dlmacvin/1aa/videos/{name.replace(ext, '-0'+ext)}"''')

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
