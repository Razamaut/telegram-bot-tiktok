import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from TikTokApi import TikTokApi

# ================================
# Встав сюди свій токен від BotFather
BOT_TOKEN = "8395251030:AAFsZE4faqCygYGgOt6W2be4NCfhtCITr90'"
# ================================

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# --- Меню ---
def main_menu():
    kb = ReplyKeyboardBuilder()
    kb.button(text="📥 Завантажити відео")
    kb.button(text="ℹ️ Допомога")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

# --- Команда /start ---
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        "👋 Привіт! Я бот для завантаження відео з TikTok без водяного знаку.\n\n"
        "Надішли мені посилання або скористайся кнопкою нижче 👇",
        reply_markup=main_menu()
    )

# --- Команда /help ---
@dp.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer(
        "📖 <b>Як користуватись ботом:</b>\n"
        "1️⃣ Скопіюй посилання на відео з TikTok.\n"
        "2️⃣ Надішли його мені у чат.\n"
        "3️⃣ Отримай відео без водяного знаку 🎥\n\n"
        "⚙️ Бот використовує TikTokApi для завантаження."
    )

# --- Команда /about ---
@dp.message(Command("about"))
async def about_cmd(message: types.Message):
    await message.answer(
        "🤖 <b>Про бота:</b>\n"
        "Цей бот створено для навчального проєкту.\n"
        "Розробник: Влад Бачинський\n"
        "Мова: Python + aiogram"
    )

# --- Обробка тексту ---
@dp.message(F.text)
async def handle_text(message: types.Message):
    text = message.text.strip()

    if "tiktok.com" in text:
        await download_tiktok_video(message, text)
    elif "завантажити" in text.lower():
        await message.answer("📎 Надішли мені посилання на відео TikTok.")
    elif "допомога" in text.lower():
        await help_cmd(message)
    else:
        await message.answer("⚠️ Надішли мені посилання на відео TikTok.")

# --- Завантаження відео через TikTokApi 7.x ---
async def download_tiktok_video(message: types.Message, url: str):
    await message.reply("⏳ Завантажую відео...")
    try:
        # Використовуємо контекстний менеджер, як в TikTokApi 7.x
        with TikTokApi() as api:
            video = api.video(url=url)
            data = video.bytes()

        tmp_file = "video.mp4"
        with open(tmp_file, "wb") as f:
            f.write(data)

        await bot.send_video(chat_id=message.chat.id, video=open(tmp_file, "rb"),
                             caption="✅ Ось твоє відео без водяного знаку!")

    except Exception as e:
        await message.reply("❌ Не вдалося завантажити відео. Перевір посилання.")
        print("Помилка:", e)

# --- Запуск бота ---
async def main():
    print("🚀 Бот запущений і працює!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
