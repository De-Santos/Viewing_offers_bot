from global_variables import bot  # , dp
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


# @dp.message_handler(lambda message: message == 'quit', state='*')
async def quit_state(message: types.Message, state: FSMContext):
    if message.text == "quit":
        await state.finish()
        await bot.send_message(message.chat.id, "ok+")


def register_message_other(dp: Dispatcher):
    dp.register_message_handler(quit_state, state='*')
