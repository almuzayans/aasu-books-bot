import os
import logging
from typing import Dict, Any

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================
# Logging
# =========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# =========================
# Bot Token (Environment Variable)
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable not set")

# =========================
# Books Data
# =========================

BOOKS: Dict[str, Dict[str, Any]] = {
    "ENGLISH": {
        "emoji": "📘",
        "items": {
            "IEP098": [
                "BQACAgQAAxkBAAIL3Gl-EzrZzs2g07czYxViZnFQUmuMAAIdGwAC8nHxUxzXjXFnArCtOAQ",
                "BQACAgQAAxkBAAIL3Wl-EzoDyNzQ5XjTE_FRGbrVuotoAAIeGwAC8nHxU3nuGyUha9KHOAQ",
            ],
            "IEP099": [
                "BQACAgQAAxkBAANiaX5DlJuH3ba_Ayl9T2Tf3gOfqdMAAiEbAALycfFTpy3dulVQaRw4BA",
                "BQACAgQAAxkBAANkaX5DnKijQjw-ZL2xUrQEgwV6kCAAAiIbAALycfFTg7sY1hTGlJ44BA",
            ],
            "ENL101": [
                "BQACAgQAAxkBAAIMGWl-FOUnbh4wOGsNbtLngKoYyPtuAAIjGwAC8nHxU0Y7oQvq1Z2NOAQ",
            ],
            "ENL102": [
                "BQACAgQAAxkBAAIMHWl-FQXlddgKlr3P5iYirVVA9rNrAAIkGwAC8nHxU2BsDB5e1iDjOAQ",
            ],
            "ENL201": [
                "BQACAgQAAxkBAAIMIWl-FQ_weESJKCt12xhL4jhS_qGWAAIlGwAC8nHxU1b2DjPqD5tVOAQ",
            ],
        },
    },

    "MATHEMATICS": {
        "emoji": "📕",
        "items": {
            "IMP098": [
                "BQACAgQAAxkBAAILz2l-ECGbiXh0jlcNWQAB4rH6wVDivgACERsAAvJx8VOGbCjs9abLrjgE",
            ],
            "IMP099": [
                "BQACAgQAAxkBAAIL0Gl-ECHaJnh4p1bVl_2xEYmrvF5zAAITGwAC8nHxUws9ZXV3xq5fOAQ",
            ],
            "MAT120": [
                "BQACAgQAAxkBAAIL0Wl-ECGAbAkm5fcbYxKLUQWTmAABBwACFBsAAvJx8VO5FMY6jCWnFzgE",
            ],
            "MAT202": [
                "BQACAgQAAxkBAAIL0ml-ECF-irXDHPkbWBXHC8KIb-WnAAIWGwAC8nHxU58M0c9N4NY1OAQ",
                "BQACAgQAAxkBAAIL02l-ECEG1xtclFYQE9nfddmOy-iTAAIXGwAC8nHxU5KDFOw2KgrAOAQ",
            ],
            "MAT240": [
                "BQACAgQAAxkBAAIL1Gl-ECGkSQWzVoimStRO2izZYIsaAAIYGwAC8nHxU1w3q6vTihc5OAQ",
            ],
        },
    },
}

# =========================
# UI Buttons
# =========================

BACK_BTN = "⬅️ القائمة الرئيسية"
REQUEST_BTN = "📩 طلب كتاب غير موجود"

def main_menu():
    return ReplyKeyboardMarkup(
        [[KeyboardButton(f"{k} {v['emoji']}")] for k, v in BOOKS.items()]
        + [[KeyboardButton(REQUEST_BTN)]],
        resize_keyboard=True,
    )

def books_menu(section):
    return ReplyKeyboardMarkup(
        [[KeyboardButton(book)] for book in BOOKS[section]["items"].keys()]
        + [[KeyboardButton(BACK_BTN)], [KeyboardButton(REQUEST_BTN)]],
        resize_keyboard=True,
    )

# =========================
# Handlers
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحبًا بك في بوت الكتب غير الرسمي لجامعة عبدالله السالم 📚\n\n"
        "اختر القسم ثم الكتاب، وسيصلك PDF مباشرة.\n"
        "في حال عدم وجود كتاب، استخدم زر الطلب.",
        reply_markup=main_menu(),
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # رجوع
    if text == BACK_BTN:
        await update.message.reply_text("اختر القسم:", reply_markup=main_menu())
        return

    # طلب كتاب
    if text == REQUEST_BTN:
        await update.message.reply_text(
            "📩 لطلب كتاب غير موجود:\n"
            "أرسل اسم المقرر + اسم الكتاب + الإصدار.\n"
            "أو راسلنا على تليقرام:\n@BOOKADVISORS",
            reply_markup=main_menu(),
        )
        return

    # اختيار قسم
    for section in BOOKS:
        if text.startswith(section):
            context.user_data["section"] = section
            await update.message.reply_text(
                f"اختر كتاب من {section}:",
                reply_markup=books_menu(section),
            )
            return

    # اختيار كتاب
    section = context.user_data.get("section")
    if section and text in BOOKS[section]["items"]:
        await update.message.reply_text(f"📚 جاري إرسال: {text}")
        for file_id in BOOKS[section]["items"][text]:
            try:
                await context.bot.send_document(
                    chat_id=update.effective_chat.id,
                    document=file_id,
                )
            except Exception as e:
                logger.error(e)
                await update.message.reply_text(
                    "❌ حدث خطأ أثناء إرسال الملف.\n"
                    "راسلنا على إنستغرام:\n@BOOKADVISORS"
                )
        return

    await update.message.reply_text(
        "استخدم الأزرار بالأسفل للتنقل.",
        reply_markup=main_menu(),
    )

# =========================
# Main
# =========================

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    logger.info("Bot started")
    app.run_polling()

if __name__ == "__main__":
    main()
