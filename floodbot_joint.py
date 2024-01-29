import requests, random, time, json, wget, os
from colorama import init, Fore
init(autoreset=True)
c1 = 0

def login():
    global c1, acs_tkn
    acs_tkn = Fore.LIGHTYELLOW_EX + 'Здесь должен быть ваш токен'
    while c1 == 0:
        mail = input(Fore.BLUE + "Введите почту(F - если из файла) или токен:")
        if len(mail) == 32:
            acs_tkn = mail
            c1 = 1
        elif mail.count('@') == 1:
            pw = input(Fore.BLUE + "Введите пароль:")
            if len(pw) < 8:
                print(Fore.RED + 'Неверный формат пароля')
            else:
                lrqst = requests.get(f"https://monopoly-one.com/api/auth.signin?email={mail}&password={pw}").json()
                if lrqst['code'] == 0:
                    c1 = 1
                    acs_tkn = lrqst['data']['access_token']
                    return acs_tkn

                else:
                    err = lrqst['code']
                    print(Fore.RED + f'Код ошибки: {err}')
        elif mail == 'F':
            read()
            mail = maild
            pw = pwd
            lrqst = requests.get(f"https://monopoly-one.com/api/auth.signin?email={mail}&password={pw}").json()
            if lrqst['code'] == 0:
                c1 = 1
                acs_tkn = lrqst['data']['access_token']
            else:
                err = lrqst['code']
                print(Fore.RED + f'Код ошибки: {err}')
        else:
            print(Fore.RED + 'Неверный формат данных')
        print(Fore.LIGHTYELLOW_EX + acs_tkn)


def spam():
    spammsg = ''
    while len(spammsg) <= 1:
        spammsg = input(Fore.BLUE + 'Введите сообщение для флуда(F - если в файле):')
        if spammsg == "F":
            read()
            spammsg = spammsgd
        print(spammsg)
        tm = int(input(Fore.BLUE + 'Введите время ожидания (в секундах):'))
        tm1 = tm * 1.2
        while True:
            send = requests.get(f'https://monopoly-one.com/api/gchat.send?access_token={acs_tkn}&message={spammsg}').json()['code']
            #print(send)
            if send != 0:
                if send == 8:
                    print(Fore.YELLOW + 'Введите капчу')
                print(Fore.RED + 'Неудача')
                time.sleep(150)
            else:
                print(Fore.GREEN + 'Успех')
                time.sleep(random.randint(tm,tm1))

def read():
    global maild, pwd, idd, spammsgd
    with open("config.txt") as file:
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

print(Fore.LIGHTWHITE_EX + 'EZ Floodbot. Made by AssKiss Studio https://github.com/AssKissStudio/M1FloodBot')
config()
login()
spam()