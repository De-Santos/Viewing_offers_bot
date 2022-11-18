from aiogram import executor
from global_variables import dp
from handlers import for_users, for_admins, other


async def on_startup(_):
    print("bot is working...")

for_admins.register_message_for_admins(dp)
for_users.register_message_for_users(dp)
other.register_message_other(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
