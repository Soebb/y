from pyromod import listen
from pyrogram import Client, filters, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import os, glob, re, shutil
import pysubs2
from pyrogram.errors import FloodWait
import PTN
import uuid
import speech_recognition as sr
from tqdm import tqdm
from segmentAudio import silenceRemoval
from writeToFile import write_to_file
from hachoir import extractMetadata
from hachoir import createParser

Domain = 'https://mac-dl.tk'

Button_List = [

    'Ask Mantik Intikam',
    'Kaderimin Oyunu',
    'Kardeslerim',
    'Elkizi',
    'Destan',
    'Kalp Yarasi',
    'Yasak Elma',
    'Uc Kurus',
    'Bir Zamanlar Cukurova',
    'Camdaki Kiz',
    'Mahkum',
]


if 'BOT_TOKEN' in os.environ:
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    API_ID = os.environ.get('API_ID')
    API_HASH = os.environ.get('API_HASH')
else:
    BOT_TOKEN = " "
    API_ID = " "
    API_HASH = " "

Bot = Client(
    ":memory:",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

def onvan(title_splited):
    title = ''
    for i in range(0, len(title_splited)):
        s = title_splited[i]
        title += s[:1].upper() + s[1:len(s)].lower() + ' '
    return title

def get_cap(m):
    e = m.rsplit("E", 1)[1]
    E = "E"+e.split()[0]
    q = e.replace('.', ' ').split()[1]
    X, fa = serial_name(m)
    H = fa.replace("_", " ").replace("#", "")
    cap = f"🔺{H} قسمت {E} \n🔸 دوبله فارسی"
    cap = f"{cap}{q} \n🆔👉 @dlmacvin_new | {fa}"
    return cap

sended=[]
@Bot.on_message(filters.private & filters.text & filters.regex('/up'))
async def uptotg(bot, __):
    head = "@dlmacvin_new - "
    folder = "C:/example_folder"
    chat = -1001457054266
    total=[]
    titles = []
    dup_titles = []
    for f in glob.glob(folder+'/*'):
        m = f.rsplit('/', 1)[1] + '\\'
        f=f.replace(m, '')
        if ("dub" in f) and f.endswith((".mkv",".mp4",".ts")):
            ext=f.rsplit('.', 1)[1]
            t=f.split('-', 1)[1].split('-dub')[0].replace('-', ' ')
            t=onvan(t.split())
            e=f.replace('le','').replace('_',' ').replace('.',' ').split('dub')[1].split()[0]
            e="E"+e
            metadata = extractMetadata(createParser(folder+"/"+f))
            q=str(metadata.get('height'))
            q="240" if q[:1] in ['2','3'] else q
            q=f' {q}P.'
            new_name = t+e+q+ext
            if t in titles:
                dup_titles.append(t)
            os.rename(folder+"/"+f, folder+"/"+new_name)
            if not "1080" in q:
                titles.append(t)
                total.append(new_name)

    folder=folder+"/"
    tot=sort_alphanumeric(total)
    for f in tot:
        t = f.rsplit("E", 1)[0]
        if not f in sended:
            if not t in dup_titles:
                cap = get_cap(f)
                await bot.send_video(video=folder+f, file_name=head+f, chat_id=chat, caption=cap)
                await bot.send_document(document=folder+f, file_name=head+f, chat_id=chat, caption=cap)
                sended.append(f)
            else:
                for ff in tot:
                    if t in ff:
                        cap = get_cap(ff)
                        await bot.send_video(video=folder+ff, file_name=head+f, chat_id=chat, caption=cap)
                        sended.append(ff)
                for fff in tot:
                    if t in fff:
                        cap = get_cap(fff)
                        await bot.send_document(document=folder+fff, file_name=head+f, chat_id=chat, caption=cap)



previous_cut_time = '00:00:00 02:00:04'

dir = 'C:/dlmacvin/Pay-ss/'
msgid = 0
chatid = 0
@Bot.on_message(filters.private & filters.text & filters.regex('/list'))
async def startt(bot, m):
    keyboard = []
    #keyboard.append(refresh_button)
    try:
        for file in Button_List:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        text=file,
                        callback_data=file
                    )
                ]
            )
    except Exception as e:
        print(e)
        return
    # keyboard.append(refresh_button)
    #await bot.send_message(chat_id=id, text="Which one?", reply_markup=InlineKeyboardMarkup(keyboard))
    await m.reply_text(text="Which one?", reply_markup=InlineKeyboardMarkup(keyboard))


@Bot.on_callback_query()
async def callback(bot, update):
    #global chatid
    # global msgid
    #global previous_cut_time
    file = update.data
    if file in Button_List:
        ask = await update.message.reply_text('قسمت چندم')
        e: Message = await bot.listen(update.message.chat.id, filters=filters.text)
        fol = file+' E'+e.text+' - '+str(uuid.uuid4())[:6]+'/'
        folder = dir + fol
        if not os.path.isdir(folder):
            os.makedirs(folder)
        if not os.path.isfile('index.php'):
            open('index.php', 'w').close()
        if not os.path.isfile('index.html'):
            open('index.html', 'w').close()
        ff240 = '240-'+str(uuid.uuid4())[:6]+'/'
        ff480 = '480-'+str(uuid.uuid4())[:6]+'/'
        ff720 = '720-'+str(uuid.uuid4())[:6]+'/'
        ff1080 = '1080-'+str(uuid.uuid4())[:6]+'/'

        if not os.path.isdir(folder+ff240):
            os.makedirs(folder+ff240)
        if not os.path.isdir(folder+ff480):
            os.makedirs(folder+ff480)
        if not os.path.isdir(folder+ff720):
            os.makedirs(folder+ff720)
        if not os.path.isdir(folder+ff1080):
            os.makedirs(folder+ff1080)
        shutil.copyfile('index.html', folder+'index.html')
        shutil.copyfile('index.php', folder+ff240+'index.php')
        shutil.copyfile('index.html', folder+ff240+'index.html')
        shutil.copyfile('index.php', folder+ff480+'index.php')
        shutil.copyfile('index.html', folder+ff480+'index.html')
        shutil.copyfile('index.php', folder+ff720+'index.php')
        shutil.copyfile('index.html', folder+ff720+'index.html')
        shutil.copyfile('index.php', folder+ff1080+'index.php')
        shutil.copyfile('index.html', folder+ff1080+'index.html')
        head = Domain + '/pay-ss/' + fol
        l240 = head + ff240 + file + ' E' + e.text + ' Hard-Sub []240P[].mp4'
        l480 = head + ff480 + file + ' E' + e.text + ' Hard-Sub []480P[].mp4'
        l720 = head + ff720 + file + ' E' + e.text + ' Hard-Sub []720P[].mp4'
        l1080 = head + ff1080 + file + ' E' + e.text + ' Hard-Sub []1080P[].mp4'
        X, fa = serial_name(file)
        fa = fa.replace(" #", "").replace("# ", "").replace("_", " ")
        t1 = f'زیرنویس چسبیده قسمت {e.text} {fa} با کیفیت 240'
        t2 = f'زیرنویس چسبیده قسمت {e.text} {fa} با کیفیت 480'
        t3 = f'زیرنویس چسبیده قسمت {e.text} {fa} با کیفیت 720'
        t4 = f'زیرنویس چسبیده قسمت {e.text} {fa} با کیفیت 1080'
        links = f'`{l240.replace(" ", "%20")}`\n\n`{t1}`\n\n`{l480.replace(" ", "%20")}`\n\n`{t2}`\n\n`{l720.replace(" ", "%20")}`\n\n`{t3}`\n\n`{l1080.replace(" ", "%20")}`\n\n`{t4}`'
        await e.delete(True)
        await ask.delete()
        #process_msg = await update.message.reply_text('Processing..')
        #await process_msg.delete()
        #if chatid == 0:
        msg = await update.message.reply_text(links)
        fil = "#" + file.replace(' ', '_')
        Y = f'⬇️قسمت {e.text} سریال ( {fa} ) {fil} ، بازیرنویس چسبیده\n\n💾کیفیت 1080👈\n💾کیفیت 720👈\n💾کیفیت 480👈\n💾کیفیت 240👈\n\n\n✅ جهت تماشا از لینک بالا استفاده کنید'
        await update.message.reply_text(f'`{Y}`')
        #    msgid = msg.message_id
        #elif chatid != 0:
        #    await bot.edit_message_text(update.message.chat.id, msgid, links)
        #chatid = update.message.from_user.id


chnls = "-1001437294321 -1001437294321 -1001166919373 -1001437520825 -1658319171 -1001071120514 -1001546442991 -1001322014891 -1001409508844 -1001537554747 -1001462444753 -1001146657589 -1001592624165 -1001588137496"
CHANNELS = set(int(x) for x in chnls.split())

line_count = 0

def sort_alphanumeric(data):
    """Sort function to sort os.listdir() alphanumerically
    Helps to process audio files sequentially after splitting 
    Args:
        data : file name
    """
    
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)] 
    
    return sorted(data, key = alphanum_key)
def ds_process_audio(audio_file, file_handle):  
    # Perform inference on audio segment
    global line_count
    try:
        r=sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data=r.record(source)
            text=r.recognize_google(audio_data,language="tr-TR")
            print(text)
            infered_text = text
    except:
        infered_text=""
        pass
    
    # File name contains start and end times in seconds. Extract that
    limits = audio_file.split("/")[-1][:-4].split("_")[-1].split("-")
    print("time= ")
    print(limits)
    if len(infered_text) != 0:
        line_count += 1
        write_to_file(file_handle, infered_text, line_count, limits)

@Bot.on_message(filters.private & filters.text & filters.regex('/start'))
async def shoroo(bot, m):
    await m.reply("hi")

@Bot.on_message(filters.private & (filters.video | filters.document | filters.audio ) & ~filters.edited, group=-1)
async def speech2srt(bot, m):
    global line_count
    media = m.audio or m.video or m.document
    if m.document and (media.file_name.endswith(".srt") or media.file_name.endswith(".ass")):
        download_location = await bot.download_media(message = m, file_name = "temp/")
        filename = os.path.basename(download_location)
        ext = filename.split('.').pop()
        if ext in ['ass']:
            ex = ".ass"
        elif ext in ['srt']:
            ex = ".srt"
        os.rename("temp/"+filename,"temp/input"+ex)
        os.system(f"ffmpeg -i temp/input{ex} temp/out.ass")
        name = f"temp/{m.document.file_name.replace('.srt', '')}.ass"
        subs = pysubs2.load("temp/out.ass", encoding="utf-8")
        for line in subs:
            if (not line.text.__contains__("color")) and (not line.text.__contains__("macvin")):
                line.text = line.text + "\\N{\\b1\\c&H0080ff&}t.me/dlmacvin_new{\\c}{\\b0}"
            if "color" in line.text:
                line.text = line.text.split('color')[0] + "{\\b1\\c&H0080ff&}t.me/dlmacvin_new{\\c}{\\b0}"
        subs.save(name)
        return await m.reply_document(document=name)

    if m.document and (not media.file_name.endswith(".mkv")) and (not media.file_name.endswith(".mp4")):
        return
    if not os.path.isdir('temp/audio/'):
        os.makedirs('temp/audio/')
    ext = ".mp3" if m.audio else f".{media.file_name.rsplit('.', 1)[1]}"
    msg = await m.reply("`Processing...`", parse_mode='md')
    await m.download(f"temp/file{ext}")
    os.system(f"ffmpeg -i temp/file{ext} temp/audio/file.wav")
    base_directory = "temp/"
    audio_directory = os.path.join(base_directory, "audio")
    audio_file_name = os.path.join(audio_directory, "file.wav")
    srt_file_name = f'temp/{media.file_name.replace(".mp3", "").replace(".mp4", "").replace(".mkv", "")}.srt'
    
    print("Splitting on silent parts in audio file")
    silenceRemoval(audio_file_name)
    
    # Output SRT file
    file_handle = open(srt_file_name, "w")
    
    for file in tqdm(sort_alphanumeric(os.listdir(audio_directory))):
        audio_segment_path = os.path.join(audio_directory, file)
        if audio_segment_path.split("/")[-1] != audio_file_name.split("/")[-1]:
            ds_process_audio(audio_segment_path, file_handle)
            
    print("\nSRT file saved to", srt_file_name)
    file_handle.close()

    await m.reply_document(document=srt_file_name, caption=f'{media.file_name.replace(".mp3", "").replace(".mp4", "").replace(".mkv", "")}')
    await msg.delete()
    shutil.rmtree('temp/audio/')
    line_count = 0


def serial_name(m):
    fa = " "
    X = None
    if fa:
        if "Son Nefesime Kadar" in m:
            fa += "#تا_آخرین_نفسم"
        if "Maske Kimsin Sen" in m:
            fa += "#نقابدار_تو_کی_هستی؟"
        if "Etkileyici" in m:
            fa += "#تاثیرگذار"
        if "Emily in Paris" in m:
            fa += "#امیلی_در_پاریس"
        if "Gossip Girl" in m:
            fa += "#دختر_سخن_چین"
        if "The Great" in m:
            fa += "#کبیر"    
        if "The Witcher" in m:
            fa += "#ویچر"
        if "La Brea" in m:
            fa += "#لا_بریا"
        if "Annemizi Saklarken" in m:
            fa += "#وقتی_مادرمان_را_پنهان_میکردیم"
        if "Money Heist S05" in m:
            fa += "#خانه_کاغذی"
            X = "Money Heist S05" 
        if "Sakli" in m:
            fa += "#پنهان"
            X = "Sakli" 
        if "The Wheel of Time" in m:
            fa += "#چرخ_زمان"
            X = "The Wheel of Time"                      
        if "Foundation" in m:
            fa += "#بنیاد"
            X = "Foundation" 
        if "Hawkeye" in m:
            fa += "#هاکای"
            X = "Hawkeye" 
        if "The Lost Symbol" in m:
            fa += "#نماد_گمشده"
            X = "The Lost Symbol" 
        if "The Morning Show" in m:
            fa += "#نمایش_صبحگاهی"
            X = "The Morning Show" 
        if "The Umbrella Academy" in m:
            fa += "#آکادمی_آمبرلا"
            X = "The Umbrella Academy"
        if "Kulup" in m:
            fa += "#کلوپ"
            X = "Kulup"      
        if "Elbet Bir Gun" in m:
            fa += "#حتما_یه_روزی"
            X = "Elbet Bir Gun"
        if "Invasion" in m:
            fa += "#هجوم"
            X = "Invasion"
        if "Aziz" in m:
            fa += "#عزیز"
            X = "Aziz"
        if "Sana Soz" in m:
            fa += "#بهت_قول_میدم"
            X = "Sana Soz"
        if "Benim Hayatim" in m:
            fa += "#زندگی_من"
            X = "Benim Hayatim"
        if "Uc Kurus" in m:
            fa += "#سه_قرون"
            X = "Uc Kurus"
        if "Sen Cal Kapimi" in m:
            fa += "#تو_در_خانه_ام_را_بزن"
            X = "Sen Cal Kapimi"
        if "Dokhtarane Gol Foroosh" in m:
            fa += "#دختران_گل_فروش"
            X = "Dokhtarane Gol Foroosh"
        if "Marasli" in m:
            fa += "#اهل_ماراش"
            X = "Marasli"
        if "Kalp Yarasi" in m:
            fa += "#زخم_قلب"
            X = "Kalp Yarasi"
        if "Dunya Hali" in m:
            fa += "#احوال_دنیایی"
            X = "Dunya Hali"
        if "Ver Elini Ask" in m:
            fa += "#دستت_را_بده_عشق"
            X = "Ver Elini Ask"
        if "Ezel" in m:
            fa += "#ایزل"
            X = "Ezel"
        if "Ikimizin Sirri" in m:
            fa += "#راز_ما_دو_نفر"
            X = "Ikimizin Sirri"
        if "Dirilis Ertugrul" in m:
            fa += "#قیام_ارطغرل"
            X = "Dirilis Ertugrul"
        if "Yemin" in m:
            fa += "#قسم"
            X = "Yemin"
        if "Yargi" in m:
            fa += "#قضاوت"
            X = "Yargi"
        if "Ilk ve Son" in m:
            fa += "#اول_و_آخر"
            X = "Ilk ve Son"        
        if "See" in m:
            fa += "#دیدن"
            X = "See"        
        if "Ask i Memnu" in m:
            fa += "#عشق_ممنوع"
            X = "Ask i Memnu"
        if "Bozkir Arslani Celaleddin" in m:
            fa += "#جلال_الدین_خوارزمشاهی"
            X = "Bozkir Arslani Celaleddin"
        if "Kazara Ask" in m:
            fa += "#عشق_تصادفی"
            X = "Kazara Ask"
        if "Bas Belasi" in m:
            fa += "#بلای_جون"
            X = "Bas Belasi"
        if "Ask Mantik Intikam" in m:
            fa += "#عشق_منطق_انتقام"
            X = "Ask Mantik Intikam"
        if "Baht Oyunu" in m:
            fa += "#بازی_بخت"
            X = "Baht Oyunu"
        if "Ada Masali" in m:
            fa += "#قصه_جزیره"
            X = "Ada Masali"
        if "Askin Tarifi" in m:
            fa += "#طرز_تهیه_عشق"
            X = "Askin Tarifi"
        if "Yesilcam" in m:
            fa += "#سینمای_قدیم_ترکیه_فصل_دوم"
            X = "Yesilcam"
        if "Camdaki Kiz" in m:
            fa += "#دختر_پشت_پنجره"
            X = "Camdaki Kiz"
        if "Bir Zamanlar Kibris" in m:
            fa += "#روزی_روزگاری_در_قبرس"
            X = "Bir Zamanlar Kibris"
        if "Teskilat" in m:
            fa += "#تشکیلات"
            X = "Teskilat"
        if "Bizi Ayiran Oizgi" in m:
            fa += "#خط_فاصل_بین_ما"
            X = "Bizi Ayiran Oizgi"               
        if "Kardeslerim" in m:
            fa += "#خواهر_و_برادرانم"
            X = "Kardeslerim"
        if "Ogrenci Evi" in m:
            fa += "#خانه_دانشجویی"
            X = "Ogrenci Evi"
        if "Sihirli Annem" in m:
            fa += "#مادر_سحرآمیز_من"
            X = "Sihirli Annem"
        if "Yetis Zeynep" in m:
            fa += "#برس_زینب"
            X = "Yetis Zeynep"
        if "Hukumsuz" in m:
            fa += "#بی_قانون"
            X = "Hukumsuz"
        if "Saygi" in m:
            fa += "#احترام"
            X = "Saygi"
        if "Vahsi Seyler" in m:
            fa += "#چیز_های_وحشی"
            X = "Vahsi Seyler"
        if "Seref Bey" in m:
            fa += "#آقای_شرف"
            X = "Seref Bey"
        if "Gibi" in m:
            fa += "#مانند"
            X = "Gibi"
        if "Iste Bu Benim Masalim" in m:
            fa += "#این_داستان_من_است"
            X = "Iste Bu Benim Masalim"
        if "Akinci" in m:
            fa += "#مهاجم"
            X = "Akinci"
        if "Kirmizi Oda" in m:
            fa += "#اتاق_قرمز"
            X = "Kirmizi Oda"
        if "Emanet" in m:
            fa += "#امانت"
            X = "Emanet"
        if "Ibo Show" in m:
            fa += "#برنامه_ایبو_شو"
            X = "Ibo Show"
        if "EDHO" in m:
            fa += "#راهزنان"
            X = "EDHO"
        if "Uyanis Buyuk Selcuklu" in m:
            fa += "#بیداری_سلجوقیان_بزرگ"
            X = "Uyanis Buyuk Selcuklu"
        if "Yasak Elma" in m:
            fa += "#سیب_ممنوعه"
            X = "Yasak Elma"
        if "Sadakatsiz" in m:
            fa += "#بی_صداقت #بی_وفا"
            X = "Sadakatsiz"
        if "Bir Zamanlar Cukurova" in m:
            fa += "#روزی_روزگاری_چوکورا"
            X = "Bir Zamanlar Cukurova"
        if "Gonul Dagi" in m:
            fa += "#کوه_دل"
            X = "Gonul Dagi"
        if "Ufak Tefek Cinayetler" in m:
            fa += "#خرده_جنایت_ها"
            X = "Ufak Tefek Cinayetler"
        if "Sibe Mamnooe" in m:
            fa += "#سیب_ممنوعه"
            X = "Sibe Mamnooe"
        if "Setare Shomali" in m:
            fa += "#ستاره_شمالی"
            X = "Setare Shomali"
        if "Otaghe Ghermez" in m:
            fa += "#اتاق_قرمز"
            X = "Otaghe Ghermez"
        if "Mojeze Doctor" in m:
            fa += "#دکتر_معجزه_گر"
            X = "Mojeze Doctor"
        if "Mucize Doktor" in m:
            fa += "#دکتر_معجزه_گر"
            X = "Mucize Doktor"
        if "Be Eshghe To Sogand" in m:
            fa += "#به_عشق_تو_سوگند"
            X = "Be Eshghe To Sogand"
        if "Eshgh Az No" in m:
            fa += "#عشق_از_نو"
            X = "Eshgh Az No"
        if "Eshghe Mashroot" in m:
            fa += "#عشق_مشروط"
            X = "Eshghe Mashroot"
        if m.__contains__("Cukurova") and not m.__contains__("Bir"):
            fa += "#روزی_روزگاری_چکوروا"
            X = "Cukurova"
        if "Yek Jonun Yek Eshgh" in m:
            fa += "#یک_جنون_یک_عشق"
            X = "Yek Jonun Yek Eshgh"
        if "2020" in m:
            fa += "#2020"
            X = "2020"
        if "Hekim" in m:
            fa += "#حکیم_اوغلو"
            X = "Hekim"
        if "Godal" in m:
            fa += "#گودال"
            X = "Godal"
        if ("Cukur" in m) and not m.__contains__("Cukurova"):
            fa += "#گودال"
            X = "Cukur"
        if "Khaneh Man" in m:
            fa += "#سرنوشتت_خانه_توست"
            X = "Khaneh Man"
        if "Alireza" in m:
            fa += "#علیرضا"
            X = "Alireza"
        if "Dokhtare Safir" in m:
            fa += "#دختر_سفیر"
            X = "Dokhtare Safir"
        if "Marashli" in m:
            fa += "#ماراشلی - #اهل_ماراش"
            X = "Marashli"
        if "Zarabane Ghalb" in m:
            fa += "#ضربان_قلب"
            X = "Zarabane Ghalb"
        if "Aparteman Bigonahan" in m:
            fa += "#آپارتمان_بی_گناهان"
            X = "Aparteman Bigonahan" 
        if "Hayat Agaci" in m:
            fa += "#درخت_زندگی"
            X = "Hayat Agaci" 
        if "Ruya" in m:
            fa += "#رویا"
            X = "Ruya" 
        if "Uzak Sehrin Masali" in m:
            fa += "#داستان_شهری_دور"
            X = "Uzak Sehrin Masali"
        if "Icimizden Biri" in m:
            fa += "#یکی_از_میان_ما"
            X = "Icimizden Biri"
        if "Kocaman Ailem" in m:
            fa += "#خانواده_بزرگم"
            X = "Kocaman Ailem"
        if "Insanlik Sucu" in m:
            fa += "#جرم_انسانیت"
            X = "Insanlik Sucu"
        if "Tutsak" in m:
            fa += "#اسیر "
            X = "Tutsak"
        if "Fazilet Hanim ve Kızlari" in m:
            fa += "#فضیلت_خانم_و_دخترانش"
            X = "Fazilet Hanim ve Kızlari"
        if "Ferhat Ile Sirin" in m:
            fa += "#فرهاد_و_شیرین"
            X = "Ferhat Ile Sirin"
        if "Gel Dese Ask" in m:
            fa += "#عشق_صدا_میزند"
            X = "Gel Dese Ask"			
        if "Gibi" in m:
            fa += "#مانند"
            X = "Gibi"
        if "Halka" in m:
            fa += "#حلقه"
            X = "Halka"
        if "Hercai" in m:
            fa += "#هرجایی"
            X = "Hercai"
        if "Hizmetciler" in m:
            fa += "#خدمتکاران"
            X = "Hizmetciler"
        if "Istanbullu Gelin" in m:
            fa += "#عروس_استانبولی"
            X = "Istanbullu Gelin"
        if "Kalp Atisi" in m:
            fa += "#ضربان_قلب"
            X = "Kalp Atisi "
        if "Kara Sevda" in m:
            fa += "#کاراسودا #عشق_بی_پایان"
            X = "Kara Sevda"
        if "Kardes Cocuklari" in m:
            fa += "#خواهرزاده_ها"
            X = "Kardes Cocuklari"
        if "Kimse Bilmez" in m:
            fa += "#کسی_نمیداند"
            X = "Kimse Bilmez"
        if "Kursun" in m:
            fa += "#گلوله"
            X = "Kursun"
        if "Kuzey Yildizi Ilk Ask" in m:
            fa += "#ستاره_شمالی_عشق_اول"
            X = "Kuzey Yildizi Ilk Ask"
        if "Kuzgun" in m:
            fa += "#کلاغ #کوزگون"
            X = "Kuzgun"
        if "Meryem" in m:
            fa += "#مریم"
            X = "Meryem"
        if "Muhtesem Ikili" in m:
            fa += "#زوج_طلایی"
            X = "Muhtesem Ikili"
        if "Nefes Nefese" in m:
            fa += "#نفس_زنان"
            X = "Nefes Nefese"
        if "Ogretmen" in m:
            fa += "#معلم"
            X = "Ogretmen"
        if "Olene Kadar" in m:
            fa += "#تا_حد_مرگ"
            X = "Olene Kadar"
        if "Sahsiyet" in m:
            fa += "#شخصیت"
            X = "Sahsiyet"			
        if "Sahin Tepesi" in m:
            fa += "#تپه_شاهین"
            X = "Sahin Tepesi"
        if "Savasci" in m:
            fa += "#جنگجو"
            X = "Savasci"
        if "Sefirin Kizi" in m:
            fa += "#دختر_سفیر"
            X = "Sefirin Kizi"
        if "Sevgili Gecmis" in m:
            fa += "#گذشته_ی_عزیز"
            X = "Sevgili Gecmis"
        if "Sheref Bey" in m:
            fa += "#آقای_شرف"
            X = "Sheref Bey"
        if "Sihirlis Annem" in m:
            fa += "#مادر_جادویی_من"
            X = "Sihirlis Annem"
        if "The Protector" in m:
            fa += "#محافظ"
            X = "The Protector"
        if "Vahsi Seyler" in m:
            fa += "#چیزهای_وحشی"
            X = "Vahsi Seyler"
        if "Vurgun" in m:
            fa += "#زخمی"
            X = "Vurgun"
        if "Ya Istiklal Ya Olum" in m:
            fa += "#یا_استقلال_یا_مرگ"
            X = "Ya Istiklal Ya Olum"
        if ("Yalanci" in m) and not m.__contains__("Yalancilar ve Mumlari"):
            fa += "#دروغگو"
            X = "Yalanci"
        if "El Kizi" in m:
            fa += "#دختر_مردم"
            X = "El Kizi"
        if "Masumlar Apartmani" in m:
            fa += "#آپارتمان_بیگناهان"
            X = "Masumlar Apartmani"
        if "Yalancilar ve Mumlari" in m:
            fa += "#دروغگو_ها_و_شمع_هایشان"
            X = "Yalancilar ve Mumlari"
        if "Lise Devriyesi" in m:
            fa += "#گشت_مدرسه"
            X = "Lise Devriyesi"
        if "Evlilik Hakkinda Her Sey" in m:
            fa += "#همه_چیز_درباره_ازدواج"
            X = "Evlilik Hakkinda Her Sey"
        if "Son Yaz" in m:
            fa += "#آخرین_تابستان"
            X = "Son Yaz"
        if "Barbaroslar Akdenizin Kilici" in m:
            fa += "#بارباروس_ها_شمشیر_دریای_مدیترانه"
            X = "Barbaroslar Akdenizin Kilici"
        if "Bir Ask Hikayesi" in m:
            fa += "#حکایت_یک_عشق"
            X = "Bir Ask Hikayesi"
        if "Carpisma" in m:
            fa += "#تصادف"
            X = "Carpisma"
        if "Cocuk" in m:
            fa += "#بچه"
            X = "Cocuk"
        if "Lise Devriyesi" in m:
            fa += "#گشت_مدرسه"
            X = "Lise Devriyesi"
        if "Kurulus Osman" in m:
            fa += "#قیام_عثمان"
            X = "Kurulus Osman"
        if "Kanunsuz Topraklar" in m:
            fa += "#سرزمین_های_بی_قانون"
            X = "Kanunsuz Topraklar"
        if "Kibris Zafere Dogru" in m:
            fa += "#قبرس_پیش_به_سوی_پیروزی"
            X = "Kibris Zafere Dogru"
        if "Misafir" in m:
            fa += "#مهمان"
            X = "Misafir"
        if "Eskiya Dunyaya Hukumdar Olmaz" in m:
            fa += "#راهزنان "
            X = "EDHO"
        if "Kaderimin Oyunu" in m:
            fa += "#بازی_تقدیرم"
            X = "Kaderimin Oyunu"
        if "Squid Game" in m:
            fa += "#بازی_مرکب"
            X = "Squid Game"
        if "Alparslan Buyuk Selcuklu" in m:
            fa += "#آلپ_ارسلان_سلجوقیان_بزرگ"
            X = "Alparslan Buyuk Selcuklu"
        if "Elkizi" in m:
            fa += "#دختر_مردم"
            X = "Elkizi"
        if "Masumiat" in m:
            fa += "#معصومیت"
            X = "Masumiat"
        if "Destan" in m:
            fa += "#حماسه"
            X = "Destan"
        if "Hamlet" in m:
            fa += "#هملت"
            X = "Hamlet"
        if "Mahkum" in m:
            fa += "#محکوم"
        if "Chapelwaite" in m:
            fa += "#چپلویت"
        if "El Cid" in m:
            fa += "#ال _ید"
        if "Grimm" in m:
            fa += "#گریم"
        if "Heels" in m:
            fa += "#هیلز"
        if "Maid" in m:
            fa += "#خدمتکار "
        if "Mayor of Kingstown" in m:
            fa += "#شهردار_کینگزتاون"
        if "Only Murders in the Building" in m:
            fa += "#فقط_قتل_های_این_ساختمان"
        if "Scenes from a Marriage" in m:
            fa += "#صحنه_هایی_از_یک_ازدواج"            
        if "Skam" in m:
            fa += "#شرم"
        if "The Chestnut Man" in m:
            fa += "#مرد_بلوطی"
        if "Titans" in m:
            fa += "#تایتان ها"            
        if "War And Peace" in m:
            fa += "#جنگ_و_صلح"
        if "Yellowjackets" in m:
            fa += "#ژاک_ زرد"
        if "You" in m:
            fa += "#تو"
        if "Erkek Severse" in m:
            fa += "#اگر_مرد_دوست_داشته_باشد"
    return X, fa


@Bot.on_message((filters.video | filters.document) & filters.channel & ~filters.edited)
async def caption(bot, message):
    media = message.video or message.document
    
    if (message.chat.id == -1001516208383) and (media is not None) and (media.file_name is not None):
        await message.edit(f"{media.file_name.replace('.mp4', '').replace('.mkv', '').replace('.webm', '')}\n\n🆔👉 @dlmacvin_music")
        return
    if (media is not None) and (media.file_name is not None):
        m = media.file_name.replace("@turk7media - ", "").replace("-", " ").replace("HardSub", "Hard-Sub").replace("Hard Sub", "Hard-Sub").replace(".mkv", "").replace(".", " ").replace("_", " ").replace("Hardsub", "Hard-Sub").replace("0p", "0P").replace("Fragmanı", "").replace("mp4", "").replace("Fragmanlarım", "").replace("ı", "i").replace("İ", "I").replace("ö", "o").replace("Ö", "O").replace("Ü", "U").replace("ü", "u").replace("ë", "e").replace("@dlmacvin2 -", "").replace("@dlmacvin -", "").replace("Ë", "E").replace("Ä", "A").replace("ç", "c").replace("Ç", "C").replace("ş", "s").replace("Ş", "S").replace("ğ", "g").replace("Ğ", "G").replace("ä", "a")
        D = m.replace("720P", "").replace("E20", "").replace("E120", "").replace("E220", "").replace("E320", "").replace("E420", "")
        N = m
        Z = media.file_name
        fa = " "
        tz = " "
        Lo = " "
        Q = " "
        Fucc = " "
        E = None
        X, fa = serial_name(m)
        Ee = None
        if Z.__contains__("Fragman") or m.__contains__("Bolum") or m.__contains__("bolum") or Z.__contains__("fragman"):
            if " Bolum" in m:
                bul = " Bolum"
            elif " bolum" in m:
                bul = " bolum"
            elif not m.__contains__(" Bolum") and not m.__contains__(" bolum"):
                if "Bolum" in m:
                    bul = "Bolum"
                elif "bolum" in m:
                    bul = "bolum"
            Jn = m.split(f"{bul}")[1]
            if "2" in Jn:
                tz += "#دوم"
            elif "1" in Jn:
                tz += "#اول"
            elif "3" in Jn:
                tz += "#سوم"
            elif "4" in Jn:
                tz += "#چهارم"
            elif "5" in Jn:
                tz += "#پنجم"
            elif "6" in Jn:
                tz += "#ششم"
            Tzz = tz.replace("#", "")
            date = " "
            if "Alparslan Buyuk Selcuklu" in m:
                date += "سه شنبه ساعت 2:30 بامداد از رسانه اینترنتی دی ال مکوین"
            if "Ask Mantik Intikam" in m:
                date += "شنبه ساعت 2:30 بامداد از رسانه اینترنتی دی ال مکوین"
            if "Kaderimin Oyunu" in m:
                date += "شنبه ساعت 2:30 بامداد از رسانه اینترنتی دی ال مکوین"
            if "Kirmizi Oda" in m:
                date += "شنبه از رسانه اینترنتی دی ال مکوین"
            if "Aziz" in m:
                date += "شنبه از رسانه اینترنتی دی ال مکوین"
            if "Kardeslerim" in m:
                date += "یکشنبه ساعت 2:30 بامداد از رسانه اینترنتی دی ال مکوین"
            if "Yalancilar ve Mumlari" in m:
                date += "یکشنبه ساعت 2:30 از رسانه اینترنتی دی ال مکوین"
            if "Teskilat" in m:
                date += "دو شنبه از رسانه اینترنتی دی ال مکوین"
            if "Gonul Dagi" in m:
                date += "دو شنبه از رسانه اینترنتی دی ال مکوین"
            if "Ikimizin Sirri" in m:
                date += "دو شنبه از رسانه اینترنتی دی ال مکوین"
            if "Yargi" in m:
                date += "دو شنبه از رسانه اینترنتی دی ال مکوین"
            if ("Yalanci" in m) and not m.__contains__("Yalancilar ve Mumlari"):
                date += "شنبه از رسانه اینترنتی دی ال مکوین"
            if "Ada Masali" in m:
                date += "چهار شنبه ساعت 2:30 بامداد از رسانه اینترنتی دی ال مکوین"
            if "Baht Oyunu" in m:
                date += "چهار شنبه ساعت 2:30 بامداد از رسانه اینترنتی دی ال مکوین"
            if "Evlilik Hakkinda Her Sey" in m:
                date += "چهار شنبه از رسانه اینترنتی دی ال مکوین"
            if "Icimizden Biri" in m:
                date += "چهار شنبه از رسانه اینترنتی دی ال مکوین"
            if "Masumlar Apartmani" in m:
                date += "چهار شنبه از رسانه اینترنتی دی ال مکوین"
            if "Uc Kurus" in m:
                date += "سه شنبه از رسانه اینترنتی دی ال مکوین"
            if "Sadakatsiz" in m:
                date += "پنج شنبه از رسانه اینترنتی دی ال مکوین"
            if "Kurulus Osman" in m:
                date += "پنج شنبه ساعت 2:30 بامداد از رسانه اینترنتی دی ال مکوین"
            if "Kanunsuz Topraklar" in m:
                date += "پنج شنبه از رسانه اینترنتی دی ال مکوین"
            if "Destan" in m:
                date += "چهار شنبه از رسانه اینترنتی دی ال مکوین"
            if "Yasak Elma" in m:
                date += "سه شنبه ساعت 2:30 بامداد از رسانه اینترنتی دی ال مکوین"
            if "Sen Cal Kapimi" in m:
                date += "پنجشنبه ساعت 2:30 بامداد از رسانه اینترنتی دی ال مکوین"
            if "Kalp Yarasi" in m:
                date += "سه شنبه ساعت 2:30 بامداد از رسانه اینترنتی دی ال مکوین"
            if "Bir Zamanlar Cukurova" in m:
                date += "جمعه ساعت 2:30 بامداد از رسانه اینترنتی دی ال مکوین"
            if "Barbaroslar Akdeniz'in Kılıcı" in m:
                date += "جمعه از رسانه اینترنتی دی ال مکوین"
            if "Barbaroslar" in m:
                date += "جمعه از رسانه اینترنتی دی ال مکوین"
            if "Uzak Sehrin Masali" in m:
                date += "جمعه از رسانه اینترنتی دی ال مکوین"
            if "Elkizi" in m:
                date += "یکشنبه از رسانه اینترنتی دی ال مکوین"
            if "Camdaki Kiz" in m:
                date += "جمعه از رسانه اینترنتی دی ال مکوین"
            if "Misafir" in m:
                date += "جمعه از رسانه اینترنتی دی ال مکوین"
            if "Eskiya Dunyaya Hukumdar Olmaz" in m:
                date += "چهار شنبه از رسانه اینترنتی دی ال مکوین"
            if "Mahkum" in m:
                date += "جمعه از رسانه اینترنتی دی ال مکوین"
            if "Elbet Bir Gun" in m:
                date += "دو شنبه از رسانه اینترنتی دی ال مکوین"

            try:
                Uik = m.replace('-', ' ').replace("_", " ").replace('  ', ' ')
                Tyy = PTN.parse(m.replace('-', ' ').replace(".", " ").replace('  ', ' '))
                Rrt = Tyy['title']
                Lo, fa = serial_name(Rrt)
                Ee = Uik.split(Lo)[1]
                Ee = Ee.split(" ")[1] if Ee.split(" ")[1].isdigit() else ""
                Lo = "#"+Lo.replace(' ', '_')
                FA = fa.replace("#", "").replace("_", " ")
                MSG = f"⬇️ تیزر{Tzz} قسمت {Ee} ({FA} ) {Lo} ، بازیرنویس چسبیده"
                msg = await message.edit(f"{MSG.replace('  ', ' ').replace('720P', '').replace('1080P', '').replace('480P', '').replace('240P', '')}\n\n🔻پخش{date}\n\n🆔👉 @dlmacvin_new")
            except:
                Uik = m.replace('-', ' ').replace('.', ' ').replace("_", " ").replace('  ', ' ')
                Uikk = Uik.split()
                for iy in Uikk:
                    if iy.isdigit():
                        Ee = iy
                        namm = Uik.rsplit(" "+Ee, 1)[0]
                        #print(namm)
                        #Tyy = PTN.parse(namm)
                        #namm = Tyy['title']
                        #Lo, fa = serial_name(namm)
                        Lo = "#"+namm.replace(' ', '_')
                        FA = fa.replace("#", "").replace("_", " ")
                        MSG = f"⬇️ تیزر{Tzz} قسمت {Ee} ({FA} ) {Lo} ، بازیرنویس چسبیده"
                        msg = await message.edit(f"{MSG.replace('  ', ' ').replace('720P', '').replace('1080P', '').replace('480P', '').replace('240P', '')}\n\n🔻پخش{date}\n\n🆔👉 @dlmacvin_new")
                        return
        if (not m.__contains__("Bolum")) and (N.__contains__("E0") or N.__contains__("E1") or N.__contains__("E2") or N.__contains__("E3") or N.__contains__("E4") or N.__contains__("E5") or N.__contains__("E6") or N.__contains__("E7") or N.__contains__("E8") or N.__contains__("E9")):
            if '720P' in m:
                Q += '720'
            if '480P' in m:
                Q += '480'
            if '1080P' in m:
                Q += '1080'
            if '240P' in m:
                Q += '240'
            if m.__contains__("720P") or m.__contains__("1080P") or m.__contains__("240P") or m.__contains__("480P"):

                q = f"\n🔹کیفیت : {Q}"
            else:
                q = ""
            if 'E0' in N:
                O = N.split("E0")[1]
                T = O.split()[0]
                if T.startswith("0"):
                    E = f"{T.replace('0', '')}"
                else:
                    E = f"{T}"
                n = N.split("E0")[0]
            if 'E1' in N:
                O = N.split("E1")[1]
                T = O.split()[0]
                E = '1' + f"{T}"
                n = N.split("E1")[0]
            if 'E2' in N:
                O = N.split("E2")[1]
                T = O.split()[0]
                E = '2' + f"{T}"
                n = N.split("E2")[0]
            if 'E3' in N:
                O = N.split("E3")[1]
                T = O.split()[0]
                E = '3' + f"{T}"
                n = N.split("E3")[0]
            if 'E4' in N:
                O = N.split("E4")[1]
                T = O.split()[0]
                E = '4' + f"{T}"
                n = N.split("E4")[0]
            if 'E5' in N:
                O = N.split("E5")[1]
                T = O.split()[0]
                E = '5' + f"{T}"
                n = N.split("E5")[0]
            if 'E6' in N:
                O = N.split("E6")[1]
                T = O.split()[0]
                E = '6' + f"{T}"
                n = N.split("E6")[0]
            if 'E7' in N:
                O = N.split("E7")[1]
                T = O.split()[0]
                E = '7' + f"{T}"
                n = N.split("E7")[0]
            if 'E8' in N:
                O = N.split("E8")[1]
                T = O.split()[0]
                E = '8' + f"{T}"
                n = N.split("E8")[0]
            if 'E9' in N:
                O = N.split("E9")[1]
                T = O.split()[0]
                E = '9' + f"{T}"
                n = N.split("E9")[0]
            H = fa.replace("_", " ").replace("#", "")
            if not "Hard-Sub" in m:
                Fucc += f"🔺{H} قسمت {E} \n🔸 دوبله فارسی"
                Fuc = f"{Fucc}{q.replace('  ', ' ')} \n🆔👉 @dlmacvin_new | {fa}"
                msg = await message.edit(Fuc)
            else:
                if X == "O Ses Turkiye":
                    Fucc = f"♨️مسابقه{fa} ( {n}) بازیرنویس چسبیده\n👌قسمت : {E.replace('Hard-Sub', '')}"
                    Fuc = f"{Fucc}{q.replace('  ', ' ')} \n🔻تماشای آنلاین بدون فیلتر شکن: \n🆔👉 @dlmacvin_new"
                    msg = await message.edit(Fuc)
                if "Maske Kimsin Sen" in m:
                    X = "Maske Kimsin Sen"
                    Fucc = f"♨️برنامه{fa} ( {n}) بازیرنویس چسبیده\n👌قسمت : {E.replace('Hard-Sub', '')}"
                    Fuc = f"{Fucc}{q.replace('  ', ' ')} \n🔻تماشای آنلاین بدون فیلتر شکن: \n🆔👉 @dlmacvin_new"
                    msg = await message.edit(Fuc)
                if not X in ["Maske Kimsin Sen", "O Ses Turkiye"]:
                    try:
                        info = PTN.parse(m)
                        Fucc += f"♨️سریال{fa} ( {n}) فصل {info['season']} بازیرنویس چسبیده\n👌قسمت : {E.replace('Hard-Sub', '')}"
                        Fuc = f"{Fucc}{q.replace('  ', ' ')} \n🔻تماشای آنلاین بدون فیلتر شکن: \n🆔👉 @dlmacvin_new"
                        msg = await message.edit(Fuc)
                    except:
                        Fucc += f"♨️سریال{fa} ( {n}) بازیرنویس چسبیده\n👌قسمت : {E.replace('Hard-Sub', '')}"
                        Fuc = f"{Fucc}{q.replace('  ', ' ')} \n🔻تماشای آنلاین بدون فیلتر شکن: \n🆔👉 @dlmacvin_new"
                        msg = await message.edit(Fuc)
        elif (m.__contains__("0P")) and (not N.__contains__("E0") and not m.__contains__("bolum") and not m.__contains__("Fragman") and not m.__contains__("Bolum") and not N.__contains__("E1") and not N.__contains__("E2") and not N.__contains__("E3") and not N.__contains__("E4") and not N.__contains__("E5") and not N.__contains__("E6") and not N.__contains__("E7") and not N.__contains__("E8") and not N.__contains__("E9")):
            if " 20" in D:
                f = D.split("20", 1)[0]
                U = D.split("20", 1)[1]
                K = U.split()[0]
                Y = '20' + f"{K}"
                YR = f"\n👌سال : {Y}"
            if " 19" in D:
                f = D.split("19", 1)[0]
                U = D.split("19", 1)[1]
                K = U.split()[0]
                Y = '19' + f"{K}"
                YR = f"\n👌سال : {Y}"
            if (not D.__contains__("19")) and (not D.__contains__("20")):
                P = m.split("0P")[0]
                f = P.replace("72", "").replace("48", "").replace("108", "").replace("24", "")
                YR = f"\n👌سال :"
            if '720P' in m:
                Q += '720'
            if '480P' in m:
                Q += '480'
            if '1080P' in m:
                Q += '1080'
            if '240P' in m:
                Q += '240'
            if m.__contains__("720P") or m.__contains__("1080P") or m.__contains__("240P") or m.__contains__("480P"):
                G = f"\n🔹کیفیت : {Q}"
                q = G.replace(".1", " ").replace(".mkv", " ").replace("  ", " ")
            else:
                q = ""
            YrR = f"{YR.replace('720P', '').replace('480P', '').replace('1080P', '').replace('240P', '').replace('mkv', '').replace('mp4', '')}"
            msg = await message.edit(f"♨️ فیلم {f.replace('Hard-Sub', '').replace(' 20', '').replace('  ', ' ')} بازیرنویس چسبیده{YrR} {q} \n🔻تماشای آنلاین بدون فیلتر شکن: \n🆔👉 @dlmacvin_new")
            cpshn = f"⬇️فیلم () {f.replace('Hard-Sub', '').replace(' 20', '').replace('  ', ' ')} ، بازیرنویس چسبیده \n\n⬇️1080👉\n⬇️720👉\n⬇️480👉\n⬇️240👉\n\n🆔👉 @dlmacvin_new"
            await bot.send_message(chat_id=-1001457054266, text=cpshn, parse_mode='markdown')

        if message.chat.id in CHANNELS:
            return
             
        # Duble Haaye Tak File
        if (message.chat.id == -1001457054266):
            try:
                if "Ghermez" in media.file_name:
                    await msg.copy(chat_id=-1001166919373)
                    await bot.copy_message(chat_id=-1001457054266, from_chat_id=-1001441684079, message_id=msgid, caption=kap, parse_mode='markdown')
    
                elif media.file_name.__contains__("Cukurova") and media.file_name.__contains__("Duble"):
                    await msg.copy(chat_id=-1001437520825) 
                    await bot.copy_message(chat_id=-1001457054266, from_chat_id=-1001441684079, message_id=msgid, caption=kap, parse_mode='markdown')
    
                elif "Mojeze Doctor" in media.file_name:
                    await msg.copy(chat_id=-1001071120514)
                    await bot.copy_message(chat_id=-1001457054266, from_chat_id=-1001441684079, message_id=msgid, caption=kap, parse_mode='markdown')
    
                elif "Yek Jonun Yek Eshgh" in media.file_name:
                    await msg.copy(chat_id=-1001546442991)
                    await bot.copy_message(chat_id=-1001457054266, from_chat_id=-1001441684079, message_id=msgid, caption=kap, parse_mode='markdown')
    
                elif media.file_name.__contains__("2020") and media.file_name.__contains__("Duble"):
                    await msg.copy(chat_id=-1001322014891)
                    await bot.copy_message(chat_id=-1001457054266, from_chat_id=-1001441684079, message_id=msgid, caption=kap, parse_mode='markdown')
    
                elif "Eshghe Mashroot" in media.file_name:
                    await msg.copy(chat_id=-1001409508844)
                    await bot.copy_message(chat_id=-1001457054266, from_chat_id=-1001441684079, message_id=msgid, caption=kap, parse_mode='markdown')
    
                elif "Alireza" in media.file_name:
                    await msg.copy(chat_id=-1001537554747)
                    
                elif "Eshgh Az No" in media.file_name:
                    await msg.copy(chat_id=-1001462444753)
                    
                elif "Masumiat" in media.file_name:
                    await msg.copy(chat_id=-1001658319171)
                    
                elif "Sibe Mamnooe" in media.file_name:
                    await msg.copy(chat_id=-1001437294321)
                elif "Setare Shomali" in media.file_name:
                    await msg.copy(chat_id=-1001146657589)
                    
                elif "Be Eshghe To Sogand" in media.file_name:
                    await msg.copy(chat_id=-1001592624165)
                    await bot.copy_message(chat_id=-1001457054266, from_chat_id=-1001441684079, message_id=msgid, caption=kap, parse_mode='markdown')
    
                elif "Aparteman Bigonahan" in media.file_name:
                    await msg.copy(chat_id=-1001588137496)
                    await bot.copy_message(chat_id=-1001457054266, from_chat_id=-1001441684079, message_id=msgid, caption=kap, parse_mode='markdown')
    
            except Exception as error:
                print(error)
                   
    
Bot.run()
