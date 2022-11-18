from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


offer_button = KeyboardButton(text="/create_offer")
my_offers = KeyboardButton(text="/my_offers")
help_button = KeyboardButton(text="/help")
user_kb = ReplyKeyboardMarkup(resize_keyboard=True)
user_kb.add(offer_button).add(my_offers).add(help_button)

in_state_quit_button = KeyboardButton(text="quit")
in_state_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(in_state_quit_button)

del_all_offers = KeyboardButton(text="/del_offers")
del_all_offers_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
del_all_offers_kb.add(del_all_offers).add(in_state_quit_button)

# start_button = KeyboardButton(text="give contact", request_contact=True)
# user_kb_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(start_button)

blocked_help_button = KeyboardButton(text="/help")
blocked_my_offers_button = KeyboardButton(text="/my_offers")
blocked_user_kb = ReplyKeyboardMarkup(resize_keyboard=True)
blocked_user_kb.add(blocked_help_button).add(blocked_help_button)

yes_inline_button = InlineKeyboardButton(text="confirm", callback_data="yes")
no_inline_button = InlineKeyboardButton(text="rewrite", callback_data="no")
inline_yes_no_button = InlineKeyboardMarkup().add(yes_inline_button).add(no_inline_button)
