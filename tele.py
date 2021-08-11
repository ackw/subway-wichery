import os, random, sys, asyncio, telepot
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from pyswip import Prolog
from convert import SubwayProlog

# @wicherybot on telegram (https://t.me/wicherybot)

class WicheryBot(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(WicheryBot, self).__init__(*args, **kwargs)
        self.counter = 0
        self.prolog = SubwayProlog()
        self.questions = ['meals', 'breads', 'mains', 'veggies', 'sauces', 'topups', 'sides', 'drinks']

    # resets counter when user enters /start for new order
    def newOrder(self):
        self.counter = 0
        self.prolog = SubwayProlog()
    
    # update counter
    async def updateCounter(self):
        nextqn = self.questions[self.counter + 1]
        if self.prolog.availableOptions(nextqn):
            self.counter += 1
        else:
            self.counter += 2

    # send telegram messages
    async def sendMsg(self, id, bot, question):
        if question == 'meals':
            menu = 'meal'
            meals = self.prolog.userOptions(question)
            await bot.sendMessage(id, displayStart(meal_options=meals, restart=False),
            reply_markup=optKeys(meals, passable=False))

        elif question == 'breads':
            menu = 'bread'
            breads = self.prolog.userOptions(question)
            await bot.sendMessage(id, displayMenu(menu, opt=breads),
            reply_markup=optKeys(breads, passable=False))

        elif question == 'mains':
            menu = 'main'
            mains = self.prolog.userOptions(question)
            await bot.sendMessage(id, displayMenu(menu, opt=mains),
            reply_markup=optKeys(mains, passable=False))

        elif question == 'veggies':
            menu = 'veg'
            veggies = self.prolog.userOptions(question)
            await bot.sendMessage(id, displayMenu(menu, opt=veggies),
            reply_markup=optKeys(veggies, passable=True))

        elif question == 'sauces':
            menu = 'sauce'
            sauces = self.prolog.userOptions(question)
            await bot.sendMessage(id, displayMenu(menu, opt=sauces),
            reply_markup=optKeys(sauces, passable=True))

        elif question == 'topups':
            menu = 'topup'
            topups = self.prolog.userOptions(question)
            await bot.sendMessage(id, displayMenu(menu, opt=topups),
            reply_markup=optKeys(topups, passable=True))

        elif question == 'sides':
            menu = 'side'
            sides = self.prolog.userOptions(question)
            await bot.sendMessage(id, displayMenu(menu, opt=sides),
            reply_markup=optKeys(sides, passable=True))

        elif question == 'drinks':
            menu = 'drink'
            drinks = self.prolog.userOptions(question)
            await bot.sendMessage(id, displayMenu(menu, opt=drinks),
            reply_markup=optKeys(drinks, passable=False))

        else:
            await bot.sendMessage(
              id, displayReceipt(
                meals=self.prolog.chosenOptions("meals"),
                breads=self.prolog.chosenOptions("breads"),
                mains=self.prolog.chosenOptions("mains"),
                veggies=self.prolog.chosenOptions("veggies"),
                sauces=self.prolog.chosenOptions("sauces"),
                topups=self.prolog.chosenOptions("topups"),
                sides=self.prolog.chosenOptions("sides"),
                drinks=self.prolog.chosenOptions("drinks")
              ),
              reply_markup=ReplyKeyboardRemove(),
              parse_mode='HTML'
            )
            await bot.sendDocument(id, document=open('img/sub.gif', 'rb'))
            await bot.sendMessage(id, "Here ya go, enjoy your sub! 🥰")
            await bot.sendMessage(id, "/start for another order 🥳")

    # converting prolog for text message
    async def on_chat_message(self, msg):
        _, _, id = telepot.glance(msg)

        if msg['text'] == '/start':
            self.newOrder()
            await self.sendMsg(id, bot, self.questions[self.counter])
        else:
            user_input = msg['text'].lower().replace(" ", "_")
            if user_input not in self.prolog.defaultOptions("drinks"):
                if "⛔️" in user_input:
                    await self.updateCounter()
                elif user_input in self.prolog.defaultOptions("meals"):
                    op = "meal"
                    self.prolog.addChoice(user_input, op)
                    await self.updateCounter()
                elif user_input in self.prolog.defaultOptions("breads"):
                    op = "bread"
                    self.prolog.addChoice(user_input, op)
                    await self.updateCounter()
                elif user_input in self.prolog.defaultOptions("mains"):
                    op = "main"
                    self.prolog.addChoice(user_input, op)
                    await self.updateCounter()
                elif user_input in self.prolog.defaultOptions("veggies"):
                    op = "veg"
                    self.prolog.addChoice(user_input, op)
                    if not self.prolog.userOptions("veggies"):
                        await self.updateCounter()
                elif user_input in self.prolog.defaultOptions("sauces"):
                    op = "sauce"
                    self.prolog.addChoice(user_input, op)
                    if not self.prolog.userOptions("sauces"):
                        await self.updateCounter()
                elif user_input in self.prolog.defaultOptions("topups"):
                    op = "topup"
                    self.prolog.addChoice(user_input, op)
                    if not self.prolog.userOptions("topups"):
                        await self.updateCounter()
                elif user_input in self.prolog.defaultOptions("sides"):
                    op = "side"
                    self.prolog.addChoice(user_input, op)
                    await self.updateCounter()

                await self.sendMsg(id, bot, self.questions[self.counter])
            else:
                op = "drink"
                self.prolog.addChoice(user_input, op)
                await self.sendMsg(id, bot, None)

# replace normal keyboard with huge keys
def optKeys(options, passable=False):
    j = 2
    new_list = []
    keyboard = []

    for item in options:
        new_list.append(item.capitalize().replace("_", " "))

    if passable: new_list += ["⛔️ Next item!"]
    new_list = [new_list[i * j:(i + 1) * j] for i in range((len(new_list) + j - 1)// j)]

    for temp in new_list:
        temp2 = []
        for item in temp:
            temp2.append(KeyboardButton(text=item))
        keyboard.append(temp2)

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)

# formatting of first text message
def displayStart(meal_options, restart=False):
    meal_opt = convertList(meal_options)
    return ("Welcome to Subway! \nWhat meal are you having today?\n\n{}".format(meal_opt).replace('👉🏼', '👩‍🍳'))

# formatting of question and options based on category
def displayMenu(menu, opt):
    if menu == 'bread':
        return ("Type of bread?\n\n{}".format(convertList(opt).replace('👉🏼', '🥖')))
    elif menu == 'main':
        return ("Filling?\n\n{}".format(convertList(opt).replace('👉🏼', '🥘')))
    elif menu == 'veg':
        return ("Greens?\n\n{}".format(convertList(opt).replace('👉🏼', '🫒')))
    elif menu == 'sauce':
        return ("Sauce?\n\n{}".format(convertList(opt).replace('👉🏼', '🥫')))
    elif menu == 'topup':
        return ("Additionals?\n\n{}".format(convertList(opt).replace('👉🏼', '🥑'))) 
    elif menu == 'side':
        return ("Side?\n\n{}".format(convertList(opt).replace('👉🏼', '🍪')))
    else:
        return ("Drink?\n\n{}".format(convertList(opt).replace('👉🏼', '🥤')))

# formatting of order summary
def displayReceipt(meals, breads, mains, veggies, sauces, topups, sides, drinks):
    return (
        "Here's your receipt!\n\n"
        "👩‍🍳{meals} Meal\n{breads}{mains}{veggies}{sauces}{topups}{sides}{drinks}\n"
        "Preparing order now...\n"
    ).format(
        meals=notSelected(convertList(meals)).replace('👉🏼', '').strip('\n'),
        breads=notSelected(convertList(breads)).replace('👉🏼', '🥖'),
        mains=notSelected(convertList(mains)).replace('👉🏼', '🥘'),
        veggies=notSelected(convertList(veggies)).replace('👉🏼', '🫒'),
        sauces=notSelected(convertList(sauces)).replace('👉🏼', '🥫'),
        topups=notSelected(convertList(topups)).replace('👉🏼', '🥑'),
        sides=notSelected(convertList(sides)).replace('👉🏼', '🍪'),
        drinks=notSelected(convertList(drinks)).replace('👉🏼', '🥤')
    )

# convert the list into strings 
def convertList(list_input):
    string = ""
    for item in list_input:
        string += "👉🏼 {item}\n".format(item=item.capitalize().replace("_", " "))
    return string

# return null if the list is empty
def notSelected(string_input):
    return "" if not string_input else string_input

# generated telegram api token
bot = telepot.aio.DelegatorBot("1717502198:AAGd54Ew0dDuqeMDkQQW_jGchoJaLDOClTg", 
[pave_event_space()(per_chat_id(), create_open, WicheryBot, timeout=(60*20)),])

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
print('WicheryBot is online now! Enter /start in bot to start ordering!')
loop.run_forever()