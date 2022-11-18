from global_variables import bot  # , dp
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from magic_with_database.work_with_DB import DataBaseInterface
from global_variables import BotSet
from keyboard.admins_kb import admin_main_kb as main_kb, admin_reactions_kb as reaction_kb, admin_seen_reaktion_kb, \
    ReplyKeyboardRemove
from keyboard.users_kb import blocked_user_kb
import random

db = DataBaseInterface()


class FSMAdmin(StatesGroup):
    check = State()
    reaction = State()


class CleanDB(StatesGroup):
    confirming = State()


class GetSeenOfferFSM(StatesGroup):
    get_seen = State()


# @dp.message_handler(user_id=BotSet.ADMIN, commands=["start", "help"])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, "Hello admin", reply_markup=main_kb)


# @dp.message_handler(user_id=BotSet.ADMIN, commands=["clean_DB"])
async def clean_db(message: types.Message):
    await CleanDB.confirming.set()
    await bot.send_message(message.chat.id, "Are you sure ?\n Write 'yes' or 'no'.", reply_markup=ReplyKeyboardRemove())


# @dp.message_handler(user_id=BotSet.ADMIN, state=CleanDB.confirming)
async def confirming(message: types.Message, state: FSMContext):
    if message.text.lower() == "yes":
        async with state.proxy() as data:
            data["key"] = random.randint(1000, 9999)
            await bot.send_message(message.chat.id, f"Please write a pin:\n{data['key']}")
    elif message.text.lower() == "no":
        message.text = "quit"
        await quit_state(message, state)
    else:
        async with state.proxy() as data:
            if message.text == str(data["key"]):
                db.clean_db()
                await state.finish()
                await bot.send_message(message.chat.id, "--successfully", reply_markup=main_kb)
            else:
                message.text = "quit"
                await quit_state(message, state)


# @dp.message_handler(commands=["get_offers"])
async def get_offers(message: types.Message, state: FSMContext):
    await FSMAdmin.check.set()
    await FSMAdmin.next()
    offer: list = db.get_one_no_seen_offers()
    if offer is not None:
        async with state.proxy() as data:
            data["message"] = offer[0]
            data["user_id"] = offer[1]
            data["message_id"] = offer[2]
            await bot.send_message(message.chat.id, data["message"], reply_markup=reaction_kb)
    else:
        await state.finish()
        await bot.send_message(message.chat.id, "offers are over", reply_markup=main_kb)


# @dp.message_handler(user_id=BotSet.ADMIN, commands=["get_seen_offers"])
async def get_seen_offer_command(message: types.Message, state: FSMContext):
    await GetSeenOfferFSM.get_seen.set()
    async with state.proxy() as data:
        if "offerList" not in data.keys():
            data["offerList"] = db.get_seen_offer()
        if len(data["offerList"]) == 0:
            await bot.send_message(message.chat.id, "Seen offers are over.", reply_markup=main_kb)
            await state.finish()
            return
    await get_seen_command(message, state)
    # await bot.send_message(message.chat.id, "Start successfully", reply_markup=admin_seen_reaktion_kb)


# @dp.message_handler(user_id=BotSet.ADMIN, commands=["skip_seen"], state=GetSeenOfferFSM.get_seen)
async def get_seen_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if len(data["offerList"]) == 0:
            await bot.send_message(message.chat.id, "Seen offers are over.", reply_markup=main_kb)
            await state.finish()
            return
        temp_data = data["offerList"].pop(0)
        data["message"] = temp_data[0]
        data["user_id"] = temp_data[1]
        data["message_id"] = temp_data[2]
        await bot.send_message(message.chat.id, str(data["message"]), reply_markup=admin_seen_reaktion_kb)


# @dp.message_handler(user_id=BotSet.ADMIN, commands=["contact"], state=[FSMAdmin.reaction, GetSeenOfferFSM.get_seen])
async def skip_person(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot.send_message(message.chat.id, f"tg://openmessage?user_id={data['user_id']}")


# @dp.message_handler(user_id=BotSet.ADMIN, commands=["block"], state=[FSMAdmin.reaction, GetSeenOfferFSM.get_seen])
async def block_person(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        temp = db.plus_chance(data["user_id"])
        if temp == 3:
            await bot.send_message(message.chat.id, "Person is blocked")
            await bot.send_message(data["user_id"], "Admin blocked you.", reply_markup=blocked_user_kb)
        elif temp is False:
            await bot.send_message(message.chat.id, "Person is blocked")
        else:
            await bot.send_message(message.chat.id, f"""Person have {temp}/{BotSet.USER_CHANCES}""")
            await bot.send_message(data["user_id"],
                                   f"""Admin gave you a warning. 
                                   \nIf you have {BotSet.USER_CHANCES} warnings you will be block
                                   """)
            await bot.send_message(data["user_id"], f"Now you have {temp}/{BotSet.USER_CHANCES} chances")


# @dp.message_handler(user_id=BotSet.ADMIN, commands=["unblock"], state=[FSMAdmin.reaction, GetSeenOfferFSM.get_seen])
async def unblock_person(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        db.user_del_one_chance(data["user_id"])
        temp = db.get_user_chance(data["user_id"])
        await bot.send_message(message.chat.id,
                               f"""Person have {temp}/{BotSet.USER_CHANCES}""")
        await bot.send_message(data["user_id"], f"Admin give you one chance {temp}/{BotSet.USER_CHANCES}")


async def quit_state(message: types.Message, state: FSMContext):
    if message.text == "quit":
        await state.finish()
        await bot.send_message(message.chat.id, "ok+", reply_markup=main_kb)


def register_message_for_admins(dp: Dispatcher):
    dp.register_message_handler(start, user_id=BotSet.ADMIN, commands=["start", "help"])
    dp.register_message_handler(clean_db, user_id=BotSet.ADMIN, commands=["clean_DB"])
    dp.register_message_handler(confirming, user_id=BotSet.ADMIN, state=CleanDB.confirming)
    dp.register_message_handler(get_offers, user_id=BotSet.ADMIN, commands=["get_offers", "next"], state="*")
    dp.register_message_handler(get_seen_offer_command, user_id=BotSet.ADMIN, commands=["get_seen_offers"])
    dp.register_message_handler(get_seen_command, user_id=BotSet.ADMIN, commands=["skip_seen"],
                                state=GetSeenOfferFSM.get_seen)
    dp.register_message_handler(skip_person, user_id=BotSet.ADMIN, commands=["contact"],
                                state=[FSMAdmin.reaction, GetSeenOfferFSM.get_seen])
    dp.register_message_handler(block_person, user_id=BotSet.ADMIN, commands=["block"],
                                state=[FSMAdmin.reaction, GetSeenOfferFSM.get_seen])
    dp.register_message_handler(unblock_person, user_id=BotSet.ADMIN, commands=["unblock"],
                                state=[FSMAdmin.reaction, GetSeenOfferFSM.get_seen])
    dp.register_message_handler(quit_state, user_id=BotSet.ADMIN, state='*')
