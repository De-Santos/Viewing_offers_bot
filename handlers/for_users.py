from global_variables import bot, dp
from global_variables import BotSet
from aiogram import types, Dispatcher
from keyboard.users_kb import user_kb, inline_yes_no_button, in_state_kb, del_all_offers_kb
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from magic_with_database.work_with_DB import DataBaseInterface

db = DataBaseInterface()


# @dp.message_handler(commands=["start", "help"])
async def start_command(message: types.Message):
    if db.user_in_table(user_id=message.chat.id) is True:
        await bot.send_message(message.chat.id, text=BotSet.HELP_AND_START_TEXT, reply_markup=user_kb)
    else:
        db.add_user(message.chat.id, message.chat.first_name)
        await bot.send_message(message.chat.id, "welcome to our bot")


# IN OLD VERSION
# @dp.message_handler(content_types=["contact"], state=FSMRegistrationUser.contact)
# async def create_offer_command(message: types.Message, state: FSMContext):
#     if db.user_have_three_chance(message.chat.id) is False:
#         if db.user_in_table(user_id=message.chat.id) is False:
#             current_state = await state.get_state()
#             if current_state is None:
#                 return
#
#             db.add_user(message.chat.id, message.contact.first_name, message.contact.phone_number)
#             await bot.send_message(message.chat.id, "Your contact save successfully", reply_markup=user_kb)
#             await state.finish()
#         else:
#             await bot.send_message(message.chat.id, "Hello", reply_markup=user_kb)
#     else:
#         await bot.send_message(message.chat.id, "You can't create offer since you are blocked")

class OfferMessageState(StatesGroup):
    offer_message = State()


# @dp.message_handler(commands=["my_offers"])
async def my_offers_message(message: types.Message):
    offers = db.get_user_offers(message.chat.id)
    await OfferMessageState.offer_message.set()
    if len(offers) == 0:
        await bot.send_message(message.chat.id, "You haven't got any offer", reply_markup=user_kb)
    else:
        await bot.send_message(message.chat.id, "Your offers is:", reply_markup=user_kb)
        for obj in offers:
            await bot.send_message(message.chat.id, f"{obj[0]} \n seen -- {db.get_message_info(int(obj[1]))}")
        await bot.send_message(message.chat.id,
                               "If you want del seen offers you can use \n/del_offers command",
                               reply_markup=del_all_offers_kb)
        await bot.send_message(message.chat.id, f"You have {len(offers)} offers")


@dp.message_handler(commands=["del_offers"], state=OfferMessageState.offer_message)
async def del_seen_message(message: types.Message, state: FSMContext):
    db.del_all_seen_messages(message.chat.id)
    await bot.send_message(message.chat.id, "All seen message was deleted \n--successfully", reply_markup=user_kb)
    await state.finish()


class FSMCreateOffer(StatesGroup):
    take_message = State()
    confirm_message = State()


# @dp.message_handler(commands=["create_offer"])
async def new_offer_message(message: types.Message):
    if db.user_have_three_chance(message.chat.id) is False:
        await FSMCreateOffer.take_message.set()
        await bot.send_message(message.chat.id, "Write offer message", reply_markup=in_state_kb)
    else:
        await bot.send_message(message.chat.id, "You can't create offer since you are blocked")


# @dp.message_handler(state=FSMCreateOffer.take_message)
async def catch_offer_message(message: types.Message, state: FSMContext):
    if message.text == "quit":
        await quit_state(message, state)
    else:
        async with state.proxy() as data:
            data['take_message'] = message.text
        message = await bot.send_message(message.chat.id, f"{message.text}")
        await message.reply("It is right ?", reply_markup=inline_yes_no_button)
        await FSMCreateOffer.next()


# @dp.callback_query_handler(state=FSMCreateOffer.confirm_message, text="yes")
async def callback_offer_message_yes(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        db.add_message_row(callback.message.chat.id, data["take_message"])
        await callback.message.answer(f"message: {data['take_message']} \n-- append successfully", reply_markup=user_kb)
    await callback.answer()
    await state.finish()


# @dp.callback_query_handler(state=FSMCreateOffer.confirm_message, text="no")
async def callback_offer_message_no(callback: types.CallbackQuery):
    await FSMCreateOffer.take_message.set()
    await callback.message.answer("Write offer message")


async def quit_state(message: types.Message, state: FSMContext):
    if message.text == "quit":
        await state.finish()
        await bot.send_message(message.chat.id, "ok", reply_markup=user_kb)


def register_message_for_users(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start", "help"])
    dp.register_message_handler(my_offers_message, commands=["my_offers"])
    dp.register_message_handler(new_offer_message, commands=["create_offer"])
    dp.register_message_handler(catch_offer_message, state=FSMCreateOffer.take_message)
    dp.register_callback_query_handler(callback_offer_message_yes, state=FSMCreateOffer.confirm_message, text="yes")
    dp.register_callback_query_handler(callback_offer_message_no, state=FSMCreateOffer.confirm_message, text="no")
    dp.register_message_handler(quit_state, state='*')
