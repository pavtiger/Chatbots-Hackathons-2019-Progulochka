import datetime
import time
from random import randint

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from bs4 import BeautifulSoup
import requests
import vk_api

from my_token import my_token


CITIES = ['москва', 'санкт-петербург', 'казань', 'новосибирск', 'екатеринбург', 'нижний новгород', 'самара', 'красноярск', 'краснодар', 'сочи']
GREETINGS = ['привет', 'ку', 'здорово', 'здравствуй', 'спасибо', 'пока']
CMD = ['start', 'начать', 'начало', 'ну привет', 'hello there']
FREE = {}

vk_session = vk_api.VkApi(token=my_token)
longpoll = VkLongPoll(vk_session)

Exit = False
City = ''
user_old = dict()

# Dictionary to convert Russian city names to english format for web parsing
translation_dictionary = {'москва': 'msk', 'санкт-петербург': 'spb', 'казань': 'kzn',
 'новосибирск': 'nsk', 'екатеринбург': 'ekb', 'нижний новгород': 'nnb', 'самара': 'smr', 'уфа': 'ufa', 'красноярск': 'krasnoyarsk',
 'краснодар': 'krd', 'сочи': 'sochi'}

def send(message):
    vk.messages.send(
        user_id=event.user_id,
        keyboard=StartKeyboard.get_keyboard(),
        message=message, random_id=randint(0, 2147483647))


def get_names(town, used):
    town = translation_dictionary[town]

    if FREE[event.user_id] == False:
        links = []
        from random import randint
        page = requests.get('https://kudago.com/' +  town + '/events/')
        soup = BeautifulSoup(page.text, 'html.parser')
        all_list = soup.find_all(class_ = 'post-title' )
        mas = []
        for a in all_list:
            links.append('https://kudago.com' + a.find('a').get('href'))
            a =  a.find('span').text.replace(u'\xa0', u' ')
            a = a.replace(u'\u200b\u200b', u' ')
            mas.append(a)
        ans_name = []
        ans_link = []

        for i in range(3):
            try:
                for j in range(len(mas)):
                    if mas == ans_name:
                        break
                    elif mas == used:
                        break
                    elif mas[j] in ans_name:
                        continue
                    elif mas[j] in used:
                        continue
                    else:
                        break
                if mas[j] in ans_name or mas[j] in used:
                    ans_name.append('Я не нашёл мероприятие')
                    ans_link.append('прости :(')
                else:
                    used.append(mas[j])
                    ans_name.append(mas[j])
                    ans_link.append(links[j])
            except:
                ans_name.append('Я не нашёл мероприятие')
                ans_link.append('прости :(')

        return [ans_name, ans_link]
    else:
        links = []
        from random import randint
        page = requests.get('https://kudago.com/' + town + '/events/')
        soup = BeautifulSoup(page.text, 'html.parser')
        free_list = soup.find_all(class_ = 'post-title-free' )
        mas = []
        for free in free_list:
            links.append('https://kudago.com' + free.find('a').get('href'))
            free =  free.find('span').text.replace(u'\xa0', u' ')
            free = free.replace(u'\u200b\u200b', u' ')
            mas.append(free)
        ans_name = []
        ans_link = []
        for i in range(3):
            try:
                for j in range(len(mas)):
                    if mas == ans_name:
                        break
                    elif mas == used:
                        break
                    elif mas[j] in ans_name:
                        continue
                    elif mas[j] in used:
                        continue
                    else:
                        break
                if mas[j] in ans_name or mas[j] in used:
                    ans_name.append('Я не нашёл мероприятие')
                    ans_link.append('прости :(')
                else:
                    used.append(mas[j])
                    ans_name.append(mas[j])
                    ans_link.append(links[j])
            except:
                ans_name.append('Я не нашёл мероприятие')
                ans_link.append('прости :(')

        return [ans_name, ans_link]


def geo(array):
    links = array[1]
    do = array[0]
    ans = []
    for i in range(3):
        try:
            page = requests.get(links[i])
            soup = BeautifulSoup(page.text, 'html.parser')
            text = str(soup.find(class_ = 'addressItem addressItem--single').contents[0])
            text = text.replace('\n','')
            text = text[24:]
            ans.append([do[i], links[i], text])
        except:
            ans.append([do[i], links[i]])
    return ans


def create_keyboard_for_CITIES():
    StartKeyboard = VkKeyboard(one_time=True)
    StartKeyboard.add_button('Москва', color=VkKeyboardColor.PRIMARY)
    StartKeyboard.add_button('Санкт-Петербург', color=VkKeyboardColor.SECONDARY)
    StartKeyboard.add_line()
    StartKeyboard.add_button('Казань', color=VkKeyboardColor.SECONDARY)
    StartKeyboard.add_button('Новосибирск', color=VkKeyboardColor.SECONDARY)
    StartKeyboard.add_line()
    StartKeyboard.add_button('Екатеринбург', color=VkKeyboardColor.SECONDARY)
    StartKeyboard.add_button('Нижний Новгород', color=VkKeyboardColor.SECONDARY)
    StartKeyboard.add_line()
    StartKeyboard.add_button('Самара', color=VkKeyboardColor.SECONDARY)
    StartKeyboard.add_button('Красноярск', color=VkKeyboardColor.SECONDARY)
    StartKeyboard.add_line()
    StartKeyboard.add_button('Краснодар', color=VkKeyboardColor.SECONDARY)
    StartKeyboard.add_button('Сочи', color=VkKeyboardColor.SECONDARY)
    return StartKeyboard



try:
    for event in longpoll.listen():
        vk = vk_session.get_api()
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            event.text = event.text.lower()
            for a in CITIES:
                if a == event.text:
                    Exit = True

            event.text = event.text.lower()

            if event.text in GREETINGS:
                StartKeyboard = VkKeyboard(one_time=True)
                StartKeyboard.add_button('Поменять Настройки', color=VkKeyboardColor.NEGATIVE)
                StartKeyboard.add_button('Хочу погулять', color=VkKeyboardColor.POSITIVE)
                send('Привет''&#128075;')

            elif event.text == 'пока':
                send('Пока''&#128533;')

            elif event.text == 'спасибо':
                send('Обращайся''&#128519;')

            elif event.text in CMD:
                if event.text != 'поменять настройки':
                    user_old[event.user_id] = []

                vk = vk_session.get_api()
                StartKeyboard = create_keyboard_for_CITIES()
                send('Здравствуйте, если вы хотите погулять где-то в Москве, но не знаете где, то можете обратиться ко мне. Для начала выберете город, а потом нажав на кнопку "хочу погулять" вам выдастся 3 случайных мероприятия в ваше городе. если хотите узнать подробнее про одно из них, просто нажмите на кнпку с числом.\nВыберете город:')

            elif Exit == True:
                Exit = False
                City = event.text
                vk = vk_session.get_api()
                StartKeyboard = VkKeyboard(one_time=True)
                StartKeyboard.add_button('Все мероприятия', color=VkKeyboardColor.SECONDARY)
                StartKeyboard.add_button('Бесплатное мероприятие', color=VkKeyboardColor.PRIMARY)
                send('Выберите формат:')

            elif event.text == 'все мероприятия':
                vk = vk_session.get_api()
                StartKeyboard = VkKeyboard(one_time=True)
                StartKeyboard.add_button('Хочу погулять', color=VkKeyboardColor.POSITIVE)
                FREE[event.user_id] = False
                send('Хорошо')

            elif event.text == 'бесплатное мероприятие':
                FREE[event.user_id] = True
                vk = vk_session.get_api()
                StartKeyboard = VkKeyboard(one_time=True)
                StartKeyboard.add_button('Хочу погулять', color=VkKeyboardColor.POSITIVE)
                send('Хорошо')


            elif event.text == 'хочу погулять':
                    send('Минутку...')
                    StartKeyboard = VkKeyboard(one_time=True)
                    StartKeyboard.add_button('1', color=VkKeyboardColor.SECONDARY)
                    StartKeyboard.add_button('2', color=VkKeyboardColor.SECONDARY)
                    StartKeyboard.add_button('3', color=VkKeyboardColor.SECONDARY)
                    StartKeyboard.add_line()
                    StartKeyboard.add_button('Поменять Настройки', color=VkKeyboardColor.PRIMARY)
                    StartKeyboard.add_button('Хочу погулять', color=VkKeyboardColor.POSITIVE)
                    Name = geo(get_names(City, user_old[event.user_id]))
                    user_old[event.user_id].append(Name[0][0])
                    user_old[event.user_id].append(Name[1][0])
                    user_old[event.user_id].append(Name[2][0])
                    send('1 - ' + str(Name[0][0]))
                    send('2 - ' + str(Name[1][0]))
                    send('3 - ' + str(Name[2][0]))

            else:
                if event.text == '1':
                    if len(Name[0]) == 3:
                        send(Name[0][0] + ': ' + '\n' + Name[0][2] + '\n' + Name[0][1])
                    else:
                        send(Name[0][0] + ': ' + '\n' + Name[0][1])

                elif event.text == '2':
                    if len(Name[1]) == 3:
                        send(Name[1][0] + ': ' + '\n' + Name[1][2] + '\n' + Name[1][1])
                    else:
                        send(Name[1][0] + ': ' + '\n' + Name[1][1])

                elif event.text == '3':
                    if len(Name[2]) == 3:
                        send(Name[2][0] + ': ' + '\n' + Name[2][2] + '\n' + Name[2][1])
                    else:
                        send(Name[2][0] + ': ' + '\n' + Name[2][1])

                else:
                    StartKeyboard = VkKeyboard(one_time=True)
                    StartKeyboard.add_button('Начать', color=VkKeyboardColor.SECONDARY)
                    send('Извини, не понял тебя. Напиши "начать" чтобы если хочешь сбросить диалог')

except requests.exceptions.ReadTimeout:
        print("VK services read timeout")
        time.sleep(3)
