from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove  # ReplyKeyboardRemove need for other import

get_offers_button = KeyboardButton(text="/get_offers")
get_seen_offers_button = KeyboardButton(text="/get_seen_offers")
clean_DB_button = KeyboardButton(text="/clean_DB")
admin_main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(get_offers_button).add(get_seen_offers_button)
admin_main_kb.add(clean_DB_button)

skip_offer_button = KeyboardButton(text="/next")
take_contact_button = KeyboardButton(text="/contact")
block_person_button = KeyboardButton(text="/block")
unblock_person_button = KeyboardButton(text="/unblock")
quit_button = KeyboardButton(text="quit")
admin_reactions_kb = ReplyKeyboardMarkup(resize_keyboard=True)
admin_reactions_kb.add(skip_offer_button).add(take_contact_button).add(block_person_button).add(unblock_person_button)
admin_reactions_kb.add(quit_button)

skip_seen_offer_button = KeyboardButton(text="/skip_seen")
admin_seen_reaktion_kb = ReplyKeyboardMarkup(resize_keyboard=True)
admin_seen_reaktion_kb.add(skip_seen_offer_button).add(take_contact_button).add(block_person_button)
admin_seen_reaktion_kb.add(unblock_person_button).add(quit_button)
