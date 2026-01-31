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
# إعداد اللوج
# =========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# =========================
# BOT TOKEN من متغير البيئة
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Environment variable BOT_TOKEN is not set")

# =========================
# ADMIN USER ID
# =========================
ADMIN_ID = 946972632  # اليوزر آي دي الخاص بك


# =========================
# بيانات الكتب (كل الأقسام) بالـ file_id الجديدة
# =========================

BOOKS: Dict[str, Dict[str, Any]] = {
    "ENGLISH": {
        "title": "ENGLISH",
        "emoji": "📘",
        "items": {
            "IEP098": {
                "files": [
                    "BQACAgQAAxkBAAMtaX5vLh2iuAElC-X22jGB98M4jZ8AAh0bAALycfFT5P2OaRVqwU84BA",
                    "BQACAgQAAxkBAAMvaX5vM_EQ6RxDldR1UepLJJ4ThlcAAh4bAALycfFTYVhoJo16sB44BA",
                ]
            },
            "IEP099": {
                "files": [
                    "BQACAgQAAxkBAAMxaX5vOj988pEn5TzlDgzvrJDia1QAAiEbAALycfFT2W31fcmOoow4BA",
                    "BQACAgQAAxkBAAMzaX5vP7hvzNPZl_xdB2XVjWsuyO0AAiIbAALycfFTQXNw8qVhWCI4BA",
                ]
            },
            "ENL101": {
                "files": [
                    "BQACAgQAAxkBAAM1aX5vRkeJ41v7AAEWIuToJThE9IrFAAIjGwAC8nHxU2bQqlVZtJfvOAQ"
                ]
            },
            "ENL102": {
                "files": [
                    "BQACAgQAAxkBAAM3aX5vUK4JTepwI09EGtcE292tb9wAAiQbAALycfFTECxkQ79jFU04BA"
                ]
            },
            "ENL201": {
                "files": [
                    "BQACAgQAAxkBAAM5aX5vUx92hdn6zXjhkqAZFbChK9oAAiUbAALycfFTGuJAaEpW-M04BA"
                ]
            },
        },
    },

    "MATHEMATICS": {
        "title": "MATHEMATICS",
        "emoji": "📕",
        "items": {
            "IMP098": {
                "files": [
                    "BQACAgQAAxkBAAMbaX5u6LHTcAsUMAIXVkRLUBLqYq8AAhEbAALycfFT4uWe0Pm7Wu04BA"
                ]
            },
            "IMP099": {
                "files": [
                    "BQACAgQAAxkBAAMdaX5u-lkVZz9-1TieLF7huHmeAAGjAAITGwAC8nHxU7NFF816Q8QsOAQ"
                ]
            },
            "MAT120": {
                "files": [
                    "BQACAgQAAxkBAAMfaX5u_iBEJk23DIk0EEzI6YlzYy4AAhQbAALycfFTZLidRhDFcNs4BA"
                ]
            },
            "MAT202": {
                "files": [
                    "BQACAgQAAxkBAAMhaX5vBZ-ET_Q7o9nd9-faLRNPBEUAAhYbAALycfFTuI5CJPA_jEw4BA",
                    "BQACAgQAAxkBAAMjaX5vDWbzyzJcC5xYv8FXiL2vhywAAhcbAALycfFTFHbX1IBzlMI4BA",
                ]
            },
            "MAT240": {
                "files": [
                    "BQACAgQAAxkBAAMlaX5vFBFA0ake--vnTaVzJnp9VuYAAhgbAALycfFToTmwpGqKj5k4BA"
                ]
            },
            "CALCULUS 1+2+3, 14th edition": {
                "files": [
                    "BQACAgQAAxkBAAMnaX5vHECBsVrJ-uHHVyzMc-yrWiEAAhkbAALycfFT7UITGbt4LLQ4BA",
                    "BQACAgQAAxkBAAMpaX5vIoy91eRXWDC8bYvGSNMdAzwAAhsbAALycfFTxc1zW-wDk5I4BA",
                ]
            },
            "CALCULUS 1+2+3, 15th edition": {
                "files": [
                    "BQACAgQAAxkBAAMraX5vKDQd7n7l20KsKnHf3IcMuUwAAhwbAALycfFTFMxbX1rb5v44BA"
                ]
            },
        },
    },

    "SCIENCE": {
        "title": "SCIENCE",
        "emoji": "📙",
        "items": {
            "CHEMISTRY": {
                "files": [
                    "BQACAgQAAxkBAAM9aX5vXw6jqLT2_27mI2g8uVX83mEAAicbAALycfFTdeszOqRQtRc4BA"
                ]
            },
            "BIOLOGY": {
                "files": [
                    "BQACAgQAAxkBAAM7aX5vV1Uo8AXYlmY8Y1MGFVZl4s8AAiYbAALycfFTLQ1hBZ3XuD04BA"
                ]
            },
            "PHYSICS 1+2": {
                "files": [
                    "BQACAgQAAxkBAAM_aX5vZ5ACLX5TvMb6p2KvoJm-Mf8AAigbAALycfFTolMDH2dhD_84BA",
                    "BQACAgQAAxkBAANBaX5vbuKlAk8l3njOGB9pfB99SZoAAikbAALycfFT8Q_neukjlvc4BA",
                ]
            },
        },
    },

    "ENGINEERING": {
        "title": "ENGINEERING",
        "emoji": "📗",
        "items": {
            "Sustainable Energy": {
                "files": [
                    "BQACAgQAAxkBAANDaX5vdKZMmaYPuhltN_TIe_xco8kAAiobAALycfFTAx7sWTv9SO44BA"
                ]
            },
            "Numerical Methods": {
                "files": [
                    "BQACAgQAAxkBAANFaX5vdwY8DCgmhLoWoPZd25L1HUAAAisbAALycfFT-UITF_higVQ4BA"
                ]
            },
            "Statistics and Probability": {
                "files": [
                    "BQACAgQAAxkBAANHaX5vfZHA-5BlwaYzhlbC8Unx43MAAiwbAALycfFTxRbbjbUx65E4BA"
                ]
            },
            "STATICS AND ENGINEERING": {
                "files": [
                    "BQACAgQAAxkBAANJaX5vgsXRFe6lGkmx-u65xH-ytLEAAi0bAALycfFTVwMCgJk9umo4BA"
                ]
            },
            "Power Electronics": {
                "files": [
                    "BQACAgQAAxkBAANLaX5vhwmamnjb3KYBKhEBtPfWzpwAAi4bAALycfFTXMmRtuDK_XM4BA"
                ]
            },
            "Thermodynamics": {
                "files": [
                    "BQACAgQAAxkBAANNaX5vjp4lfg3vBTz5lqgOHrXiE3EAAi8bAALycfFTJidjTWKvx8U4BA",
                    "BQACAgQAAxkBAANPaX5vlnBfqLT1-21sEuBwZ6kqfoYAAjAbAALycfFT2jd3xW8rRh44BA",
                ]
            },
        },
    },

    "COMPUTING": {
        "title": "COMPUTING",
        "emoji": "💻",
        "items": {
            "Digital Logic": {
                "files": [
                    "BQACAgQAAxkBAANRaX5vmhUAAek-JvkWDQTimHLRvfM8AAIxGwAC8nHxU-ZSNlrZ2HqrOAQ"
                ]
            },
            "JAVA": {
                "files": [
                    "BQACAgQAAxkBAANVaX5voNXM9mpJO1kZBAjEPIxnRQEAAjMbAALycfFT9wG2BLTjPBw4BA"
                ]
            },
            "C++": {
                "files": [
                    "BQACAgQAAxkBAANTaX5vnQiqvofg5LuQIAaiOtUPZ_UAAjIbAALycfFT-lhCayDIsTw4BA"
                ]
            },
        },
    },

    "BUSINESS": {
        "title": "BUSINESS",
        "emoji": "💼",
        "items": {
            "International Economics": {
                "files": [
                    "BQACAgQAAxkBAANXaX5vo19zY_BJSxWz33f6Ay5DuXEAAjQbAALycfFTzBSWuQOD7o44BA"
                ]
            },
        },
    },

    "GENERAL": {
        "title": "GENERAL",
        "emoji": "📚",
        "items": {
            "INF": {
                "files": [
                    "BQACAgQAAxkBAANZaX5vpXYQcowX2CjATbgexP7N7dAAAjUbAALycfFT7CkQzdYYr8E4BA"
                ]
            },
            "ETHICS": {
                "files": [
                    "BQACAgQAAxkBAANbaX5vqoHIY6TFG5_xxVxbRWtlpogAAjYbAALycfFT02sE7fCCZTM4BA"
                ]
            },
        },
    },
}

# سيتم تعبئتهما من BOOKS
SECTION_BUTTONS: Dict[str, str] = {}
BOOK_BUTTONS: Dict[str, tuple] = {}

def build_button_maps() -> None:
    SECTION_BUTTONS.clear()
    BOOK_BUTTONS.clear()
    for sec_key, sec_data in BOOKS.items():
        sec_button = f"{sec_data['title']} {sec_data['emoji']}"
        SECTION_BUTTONS[sec_button] = sec_key
        for book_title in sec_data["items"].keys():
            BOOK_BUTTONS[book_title] = (sec_key, book_title)

build_button_maps()

BACK_BUTTON = "⬅️ القائمة الرئيسية"
REQUEST_BUTTON = "📩 طلب كتاب غير موجود"


def main_menu() -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text)] for text in SECTION_BUTTONS.keys()]
    rows.append([KeyboardButton(REQUEST_BUTTON)])
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)


def section_menu(section_key: str) -> ReplyKeyboardMarkup:
    sec = BOOKS[section_key]
    rows = [[KeyboardButton(book_title)] for book_title in sec["items"].keys()]
    rows.append([KeyboardButton(BACK_BUTTON)])
    rows.append([KeyboardButton(REQUEST_BUTTON)])
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)


# =========================
# Handlers
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "مرحبًا بك في UNIVERSITIES BOOKS BOT 📚\n\n"
        "بوت غير رسمي لمساعدة طلاب الجامعات في الكويت على الوصول للكتب الانجليزية.\n\n"
        "اختر القسم من الأزرار بالأسفل، ثم اختر الكتاب.\n"
        f"إذا لم تجد كتابك اضغط «{REQUEST_BUTTON}».",
        reply_markup=main_menu(),
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (update.message.text or "").strip()

    # رجوع للقائمة الرئيسية
    if text == BACK_BUTTON:
        context.user_data.clear()
        await update.message.reply_text(
            "اختر القسم:",
            reply_markup=main_menu(),
        )
        return

    # طلب كتاب غير موجود
    if text == REQUEST_BUTTON:
        await update.message.reply_text(
            "📩 طلب كتاب غير موجود\n\n"
            "إذا لم تجد كتابك في القوائم، أرسل في رسالة واحدة:\n"
            "• اسم المقرر\n"
            "• اسم الكتاب\n"
            "• رقم الطبعة (Edition) إن وجد\n\n"
            "على قناتنا في تليقرام:\n"
            "@universitiesbooks",
            reply_markup=main_menu(),
        )
        return

    # اختيار قسم
    if text in SECTION_BUTTONS:
        sec_key = SECTION_BUTTONS[text]
        context.user_data["section"] = sec_key
        await update.message.reply_text(
            f"اختر الكتاب من قسم {BOOKS[sec_key]['title']} {BOOKS[sec_key]['emoji']}:",
            reply_markup=section_menu(sec_key),
        )
        return

    # اختيار كتاب
    if text in BOOK_BUTTONS:
        sec_key, book_title = BOOK_BUTTONS[text]
        files = BOOKS[sec_key]["items"][book_title]["files"]

        if not files:
            await update.message.reply_text(
                f"الكتاب «{book_title}» غير مضاف حاليًا أو يحتاج تحديث.",
                reply_markup=section_menu(sec_key),
            )
            return

        await update.message.reply_text(
            f"📚 جاري إرسال: {book_title}",
            reply_markup=section_menu(sec_key),
        )

        for fid in files:
            try:
                await context.bot.send_document(
                    chat_id=update.effective_chat.id,
                    document=fid,
                )
            except Exception as e:
                logger.error("Error sending %s: %s", book_title, e)
                await update.message.reply_text(
                    "حدث خطأ أثناء إرسال الملف.\n"
                    "إذا تكرر الخطأ، راسلنا على قناتنا في تليقرام:\n"
                    "@universitiesbooks",
                    reply_markup=section_menu(sec_key),
                )
                break
        return

    # أي نص آخر
    await update.message.reply_text(
        "اختر القسم أو الكتاب من الأزرار في الأسفل.\n"
        f"أو اضغط «{BACK_BUTTON}» للعودة للقائمة الرئيسية.",
        reply_markup=main_menu(),
    )


# =========================
# ADMIN: استخراج file_id لأي ملف
# =========================

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """عندما يرسل الأدمن ملفًا للبوت يرجع له الـ file_id."""
    user_id = update.effective_user.id if update.effective_user else None
    if user_id != ADMIN_ID:
        # أي مستخدم عادي يرسل ملف → نتجاهله (لا نرد)
        return

    doc = update.message.document
    if not doc:
        return

    file_id = doc.file_id
    file_name = doc.file_name or "بدون اسم"

    logger.info("ADMIN %s sent document: %s (%s)", user_id, file_name, file_id)

    await update.message.reply_text(
        f"👑 ADMIN MODE\n"
        f"File name: {file_name}\n\n"
        f"file_id:\n{file_id}"
    )


# =========================
# main
# =========================

def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    # هاندلر الملفات (Document) للأدمن
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    logger.info("Bot started…")
    app.run_polling()


if __name__ == "__main__":
    main()


