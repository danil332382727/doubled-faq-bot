import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# Вставьте сюда токен вашего FAQ-бота из BotFather
BOT_TOKEN = "8292169148:AAEJUrNRoJrSCzjWBjtNGKTByvD3MEBYni0"
# Юзернейм менеджера для прямой связи (без символа @)
MANAGER_USERNAME = "Double_DD_Manager" 

bot = Bot(
    token=BOT_TOKEN, 
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Кнопки главного меню
def main_menu_keyboard():
    kb = [
        [InlineKeyboardButton(text="📏 Как подобрать размер?", callback_data="faq_size")],
        [InlineKeyboardButton(text="🚚 Сроки и стоимость доставки", callback_data="faq_delivery")],
        [InlineKeyboardButton(text="🛒 Как оформить заказ?", callback_data="faq_order")],
        [InlineKeyboardButton(text="💳 Оплата", callback_data="faq_payment")],
        [InlineKeyboardButton(text="💬 Связаться с менеджером", url=f"https://t.me/{MANAGER_USERNAME}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

# Меню выбора страны в доставке
def delivery_keyboard():
    kb = [
        [InlineKeyboardButton(text="🇷🇺 Россия (СДЭК)", callback_data="del_ru")],
        [InlineKeyboardButton(text="🇰🇿 Казахстан (СДЭК)", callback_data="del_kz")],
        [InlineKeyboardButton(text="🇰🇬 Кыргызстан", callback_data="del_kg")],
        [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

# Кнопка возврата в меню
def back_keyboard():
    kb = [[InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back_to_main")]]
    return InlineKeyboardMarkup(inline_keyboard=kb)

@dp.message(CommandStart())
async def start_cmd(message: Message):
    text = (
        "<b>Привет! Это бот-помощник магазина Double_D Shop.</b>\n\n"
        "Здесь вы можете быстро узнать ответы на частые вопросы по доставке, подбору размеров и оформлению заказа.\n\n"
        "Выберите нужный раздел ниже:"
    )
    await message.answer(text, reply_markup=main_menu_keyboard())

@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    text = "<b>Главное меню FAQ:</b>\n\nВыберите интересующий вопрос:"
    await callback.message.edit_text(text, reply_markup=main_menu_keyboard())
    await callback.answer()

# --- 1. РАЗМЕРЫ ---
@dp.callback_query(F.data == "faq_size")
async def faq_size(callback: CallbackQuery):
    text = (
        "📏 <b>Как правильно подобрать размер:</b>\n\n"
        "<i>Если есть сантиметровая лента (замеряйте вещь в расправленном виде):</i>\n\n"
        "🧥 <b>Верхняя одежда / Худи / Футболки / Бомберы:</b>\n"
        "• <b>Ширина плеч:</b> от плечевого шва до плечевого шва.\n"
        "• <b>Ширина груди:</b> от подмышки до подмышки.\n"
        "• <b>Длина рукава:</b> от плечевого шва до края манжета.\n"
        "• <b>Общая длина:</b> по спине от воротника до низа.\n\n"
        "👖 <b>Штаны / Джинсы:</b>\n"
        "• <b>Полупояс:</b> ширина пояса в расправленном виде.\n"
        "• <b>Обхват бёдер:</b> по наиболее выступающим точкам.\n"
        "• <b>Длина:</b> внешняя (от пояса до низа) и внутренняя (шаговый шов).\n\n"
        "👟 <b>Обувь:</b>\n"
        "• Достаньте стельку из вашей удобной пары и измерьте её длину в сантиметрах (см) от пятки до носка.\n\n"
        "💡 <b>Нет ленты под рукой?</b>\n"
        "Напишите менеджеру ваш <b>рост и вес</b>, а также уточните посадку (в обтяжку, по размеру или оверсайз) — мы подберем размер индивидуально!"
    )
    await callback.message.edit_text(text, reply_markup=back_keyboard())
    await callback.answer()

# --- 2. ДОСТАВКА ---
@dp.callback_query(F.data == "faq_delivery")
async def faq_delivery(callback: CallbackQuery):
    text = (
        "🚚 <b>Сроки и стоимость доставки:</b>\n\n"
        "<i>(Важно: если вещь идёт по предзаказу, сначала 10–12 дней занимает доставка до нашего склада, и только потом отправляется к вам).</i>\n\n"
        "Выберите ваше направление:"
    )
    await callback.message.edit_text(text, reply_markup=delivery_keyboard())
    await callback.answer()

@dp.callback_query(F.data == "del_ru")
async def del_ru(callback: CallbackQuery):
    text = (
        "🇷🇺 <b>Доставка в Россию (СДЭК):</b>\n\n"
        "• <b>Сроки:</b> 10–14 дней после отправки.\n"
        "• <b>Стоимость:</b> в среднем от 1 000 до 1 200 ₽ (итоговая цена зависит от веса и объёма коробки).\n"
        "• Все посылки идут с индивидуальным трек-номером СДЭК."
    )
    await callback.message.edit_text(text, reply_markup=delivery_keyboard())
    await callback.answer()

@dp.callback_query(F.data == "del_kz")
async def del_kz(callback: CallbackQuery):
    text = (
        "🇰🇿 <b>Доставка в Казахстан (СДЭК):</b>\n\n"
        "• <b>Сроки:</b> от 8 до 12 дней (зависит от города).\n"
        "• <b>Стоимость:</b> от 3 500 до 4 500 ₸ (зависит от города и габаритов посылки).\n"
        "• Посылка отслеживается по трек-номеру СДЭК."
    )
    await callback.message.edit_text(text, reply_markup=delivery_keyboard())
    await callback.answer()

@dp.callback_query(F.data == "del_kg")
async def del_kg(callback: CallbackQuery):
    text = (
        "🇰🇬 <b>Доставка по Кыргызстану:</b>\n\n"
        "• <b>Сроки:</b> 1–2 дня после отправки.\n"
        "• <b>Стоимость:</b> 300 сом (Бишкек и все регионы).\n"
        "• Отправка курьером / региональными службами."
    )
    await callback.message.edit_text(text, reply_markup=delivery_keyboard())
    await callback.answer()

# --- 3. ЗАКАЗ ---
@dp.callback_query(F.data == "faq_order")
async def faq_order(callback: CallbackQuery):
    text = (
        "🛒 <b>Как оформить заказ:</b>\n\n"
        "1. Выберите вещь в канале или отправьте фото/запрос в нашего бота по поиску @Double_D_Searchbot, чтобы мы нашли нужный вариант.\n"
        "2. Определитесь с размером (по нашей инструкции с замерами или назвав рост/вес).\n"
        "3. Напишите менеджеру в личные сообщения.\n"
        "4. Уточняем наличие или оформляем предзаказ, согласуем данные доставки и оплачиваем."
    )
    await callback.message.edit_text(text, reply_markup=back_keyboard())
    await callback.answer()

# --- 4. ОПЛАТА ---
@dp.callback_query(F.data == "faq_payment")
async def faq_payment(callback: CallbackQuery):
    text = (
        "💳 <b>Оплата:</b>\n\n"
        "• Оплата принимается на удобные реквизиты (карты / электронные кошельки).\n"
        "• Сразу после оплаты ваш заказ фиксируется.\n"
        "• После отправки товара менеджер передаёт вам индивидуальный трек-номер для отслеживания в СДЭКе."
    )
    await callback.message.edit_text(text, reply_markup=back_keyboard())
    await callback.answer()

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
