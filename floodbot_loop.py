import requests, random, time, json, wget, os
from audioplayer import AudioPlayer
from colorama import init, Fore
init(autoreset=True)
c1 = 0
anow = ''

def login():
    global c1, acs_tkn, rfr_tkn, uid
    acs_tkn = Fore.LIGHTYELLOW_EX + 'Здесь должен быть ваш токен'
    while c1 == 0:
        mail = input(Fore.MAGENTA + "Введите почту(F - если из файла) или токен:")
        if len(mail) == 32:
            acs_tkn = mail
            c1 = 2
        elif mail.count('@') == 1:
            pw = input(Fore.MAGENTA + "Введите пароль:")
            if len(pw) < 8:
                print(Fore.RED + 'Неверный формат пароля')
            else:
                lrqst = requests.get(f"https://monopoly-one.com/api/auth.signin?email={mail}&password={replaces(pw)}").json()
                if 'data' in lrqst:
                    if lrqst['code'] == 0:
                        if 'totp_session_token' in lrqst['data']:
                            tfa = ''
                            while True:
                                while tfa == "":
                                    tfa = input('Введите код 2FA:')
                                else:
                                    auth2 = requests.get(f'https://monopoly-one.com/api/auth.totpVerify?totp_session_token={lrqst["data"]["totp_session_token"]}&code={tfa}').json()
                                    if auth2['code'] == 0:
                                        c1 = 1
                                        acs_tkn = auth2['data']['access_token']
                                        rfr_tkn = auth2['data']['refresh_token']
                                        uid = auth2['data']['user_id']
                                        return acs_tkn, rfr_tkn, uid
                                    else:
                                        print(Fore.RED + 'Ошибка')
                                        tfa = ''
                        else:
                            c1 = 1
                            acs_tkn = lrqst['data']['access_token']
                            rfr_tkn = lrqst['data']['refresh_token']
                            uid = lrqst['data']['user_id']
                            return acs_tkn, rfr_tkn, uid

                else:
                    err = lrqst['code']
                    print(Fore.RED + f'Код ошибки: {err}')
        elif mail == 'F':
            read()
            lrqst = requests.get(f"https://monopoly-one.com/api/auth.signin?email={maild}&password={replaces(pwd)}").json()
            #print(lrqst)
            if 'data' in lrqst:
                if lrqst['code'] == 0:
                    if 'totp_session_token' in lrqst['data']:
                        tfa = ''
                        while True:
                            while tfa == "":
                                tfa = input('Введите код 2FA:')
                            else:
                                auth2 = requests.get(
                                    f'https://monopoly-one.com/api/auth.totpVerify?totp_session_token={lrqst["data"]["totp_session_token"]}&code={tfa}').json()
                                if auth2['code'] == 0:
                                    c1 = 1
                                    acs_tkn = auth2['data']['access_token']
                                    rfr_tkn = auth2['data']['refresh_token']
                                    uid = auth2['data']['user_id']
                                    return acs_tkn, rfr_tkn, uid
                                else:
                                    print(Fore.RED + 'Ошибка')
                                    tfa = ''
                    else:
                        c1 = 1
                        acs_tkn = lrqst['data']['access_token']
                        rfr_tkn = lrqst['data']['refresh_token']
                        uid = lrqst['data']['user_id']
                        return acs_tkn, rfr_tkn, uid
            else:
                err = lrqst['code']
                print(Fore.RED + f'Код ошибки: {err}')
        else:
            print(Fore.RED + 'Неверный формат данных')

def params():
    global messages,tm, tm1
    messages = (input(Fore.MAGENTA + 'Введите сообщение для флуда(F - если в файле):').strip().split('~'))
    if "F" in messages:
        read()
        messages.remove('F')
        messages += spammsgd.split('~')
    print(messages)
    tm = int(input(Fore.MAGENTA + 'Введите время ожидания (в секундах):'))*100
    tm1 = int(tm * 1.2)

def spam():
    global anow
    while True:
        #print('start sending')
        now = messages[random.randint(0,len(messages)-1)]
        #print(now)
        if (now != anow) | (len(messages) == 1):
            send = requests.get(f'https://monopoly-one.com/api/gchat.send?access_token={acs_tkn}&message={replaces(now)}').json()
            #print(send)
            #print(send['code'])
            if send['code'] != 0:
                if send['code'] == 8:
                    print(Fore.YELLOW + 'Введите капчу')
                    time.sleep(150)
                elif send['code'] == 104:
                    muted = send['data']['mute_ts_end']
                    print(f'Вас замутили до {time.strftime("%a, %d %b %Y %H:%M:%S",time.localime(muted))}')
                elif send['code'] == 1:
                    refresh()
                print(Fore.RED + 'Неудача')
            else:
                print(Fore.GREEN + 'Успех')
                time.sleep(random.randint(tm,tm1)/100)
                anow = now

def read():
    global maild, pwd, idd, spammsgd
    with open("config.txt",'r',-1,'utf-8') as file:
        str = file.read()
        dicti = json.loads(str)
    if bool(dicti['email']) == 1 & bool(dicti['password']) == 1:
        maild = dicti['email']
        pwd = dicti['password']
    if bool(dicti['spammsg']) == 1:
        spammsgd = dicti['spammsg']
        #print(spammsgd)

def config():
    if not os.path.exists('config.txt'):
        wget.download('https://raw.githubusercontent.com/AssKissStudio/M1Config/main/config.txt')
        print('==> Загружен файл параметров. Вы можете изменить его в любом текстовом редакторе')

def error():
    print('Токен недействителен, либо лимиты')
    if not os.path.exists('error.mp3'):
        wget.download('https://raw.githubusercontent.com/AssKissStudio/M1Config/main/error.mp3')
    AudioPlayer('error.mp3').play(block=True)
    os.remove('error.mp3')
    exit()

def refresh():
    global acs_tkn,rfr_tkn
    if c1 == 1:
        refreshh = requests.get(f'https://monopoly-one.com/api/auth.refresh?refresh_token={rfr_tkn}').json()
        if refreshh['code'] == 0:
            print('Обновил токены')
            acs_tkn = refreshh['data']['access_token']
            rfr_tkn = refreshh['data']['refresh_token']
            time.sleep(random.randint(400,800)/100)
            return acs_tkn,rfr_tkn
    else:
        error()

def replaces(var):
    var = var.replace('!','%21')
    var = var.replace('\"', '%22')
    var = var.replace('#', '%23')
    var = var.replace('$', '%24')
    var = var.replace('&', '%26')
    var = var.replace('\'', '%27')
    var = var.replace('(', '%28')
    var = var.replace(')', '%29')
    var = var.replace('!', '%21')
    var = var.replace('*', '%2A')
    var = var.replace('+', '%2B')
    var = var.replace('/', '%2F')
    return var

print(Fore.LIGHTWHITE_EX + 'EZ Floodbot. Made by AssKiss Studio https://github.com/AssKissStudio/M1FloodBot')
config()
login()
params()
while True:
    try:
        spam()
    except:
        if c1 == 1:
            refresh()
        else:
            error()