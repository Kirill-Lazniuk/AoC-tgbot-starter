import subprocess
import time
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# Настройки
TOKEN = '8651697968:AAGliiWha3A52MOAVglzyN2drF5tQprOBd8'  # Вставь новый токен, старый лучше сбросить!
ALLOWED_IDS = [1520423269, 7744567156]

bot = Bot(token=TOKEN)
dp = Dispatcher()

def snap_ngrok_now():
    """Not supported in server environment (requires desktop/GUI)."""
    return None

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🚀 Запустить сеть", callback_data="run_bat")],
        [types.InlineKeyboardButton(text="📸 Скриншот Ngrok", callback_data="snap_only")],
        [types.InlineKeyboardButton(text="🛑 Выключить всё", callback_data="stop_all")]
    ])
    await message.answer("🎮 Панель управления:", reply_markup=kb)

@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    if callback.from_user.id not in ALLOWED_IDS:
        return

    if callback.data == "run_bat":
        try:
            subprocess.Popen(['/bin/sh', '-c', 'echo "Run command not configured"'], shell=False)
            await callback.answer("✅ Команда запуска не настроена для этой среды")
        except Exception as e:
            await callback.answer(f"Ошибка запуска: {e}")

    elif callback.data == "snap_only":
        await callback.message.answer("📸 Навожу порядок на столе...")
        path = snap_ngrok_now()
        if path:
            await callback.message.answer_photo(types.FSInputFile(path), caption="📸 Текущий статус Ngrok")
        else:
            await callback.message.answer("⚠️ Окно ngrok не найдено. Убедись, что оно открыто и содержит слово 'ngrok' в заголовке.")

    elif callback.data == "stop_all":
        os.system("pkill -f java || true")
        os.system("pkill -f ngrok || true")
        await callback.answer("🛑 Всё остановлено")

if __name__ == '__main__':
    print("Бот запущен. Ожидаю команд...")
    dp.run_polling(bot)
