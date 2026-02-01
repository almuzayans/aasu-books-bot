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
                    "BQACAgQAAxkBAAIBUWl_byuotOYZkiiyaKr1vOuJYnqVAALgHAAC7j0AAVDQ9an6p0Nr3TgE",
                    "BQACAgQAAxkBAAIBU2l_b4noaBgB8q2G9e7wePSXsYf6AALjHAAC7j0AAVC4sLHn-hv1JjgE",
                ]
            },
            "IEP099": {
                "files": [
                    "BQACAgQAAxkBAAIBVWl_b_-4KyHV__R56ow2Dahq7InOAALnHAAC7j0AAVDlzd3MqRFTiTgE",
                    "BQACAgQAAxkBAAIBV2l_cF6kPvAUtRXkQkya4iG8g3WwAALoHAAC7j0AAVAXV2Tyjtqf-jgE",
                ]
            },
            "ENL101": {
                "files": [
                    "BQACAgQAAxkBAAIBWWl_cQgZ4508o4_S6Vo_KzgE9-mdAALpHAAC7j0AAVDqxGQ3d_YIKzgE"
                ]
            },
            "ENL102": {
                "files": [
                    "BQACAgQAAxkBAAIBW2l_cVL70eZ2yPP3Id-YLSbFi1UtAALqHAAC7j0AAVCAfGx1Us3DcDgE"
                ]
            },
            "ENL201": {
                "files": [
                    "BQACAgQAAxkBAAIBXWl_cW8o7qNxaaj-GCkIEtb05bPjAALrHAAC7j0AAVApCeyoQuwCkTgE"
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
                    "BQACAgQAAxkBAAIBX2l_cfKXZe0liDR42YH-FvXRs-xIAALtHAAC7j0AAVDFT9tHIvqySjgE"
                ]
            },
            "IMP099": {
                "files": [
                    "BQACAgQAAxkBAAIBYWl_ckSqgrx00518CPCspoRSIkMqAALuHAAC7j0AAVBLQCnoLzpfgTgE"
                ]
            },
            "MAT120": {
                "files": [
                    "BQACAgQAAxkBAAIBY2l_cl5Z_M-lNCNAJQUqaVD7046QAALvHAAC7j0AAVDoY7Kp-wYAAQU4BA"
                ]
            },
            "MAT202": {
                "files": [
                    "BQACAgQAAxkBAAIBZWl_cofNMYaVjTaMIIUU9BW-t_fnAALwHAAC7j0AAVBY9Uvn-EsILDgE",
                    "BQACAgQAAxkBAAIBZ2l_cpJAoGyR8kUc8CAjjqsG8Yx5AALxHAAC7j0AAVBgLpV8bDeh5TgE",
                ]
            },
            "MAT240": {
                "files": [
                    "BQACAgQAAxkBAAIBaWl_cr4GDS0NO2rw_SQMrAPLUcr2AALyHAAC7j0AAVBLCiRAMVUD-TgE"
                ]
            },
            "CALCULUS 1+2+3, 14th edition": {
                "files": [
                    "BQACAgQAAxkBAAIBbWl_cwa_-e020EWVFz1HtbulQChgAAL1HAAC7j0AAVDT8lJqZ3RBkzgE",
                    "BQACAgQAAxkBAAIBa2l_cvbFviT3gx1fA4mtksjbqj39AALzHAAC7j0AAVDehN0FRg7XZTgE",
                ]
            },
            "CALCULUS 1+2+3, 15th edition": {
                "files": [
                    "BQACAgQAAxkBAAIBb2l_c0KGLjTYAYmOE0R_GzuZUGl4AAL2HAAC7j0AAVBz3ifn4truUDgE"
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
                    "BQACAgQAAxkBAAIBcWl_c3pUW_ng5coBTIzbkTYB4Eb3AAL3HAAC7j0AAVCFO_BAQVsxrTgE"
                ]
            },
            "BIOLOGY": {
                "files": [
                    "BQACAgQAAxkBAAIBc2l_c_Up2pgXQEIT7WEoSkxhbY1LAAL4HAAC7j0AAVDEgPTLDr41KTgE"
                ]
            },
            "PHYSICS 1+2": {
                "files": [
                    "BQACAgQAAxkBAAIBdWl_dIe9Vh9utJLhbSDb4-tfk28TAAL6HAAC7j0AAVDPzbOWsjiXgDgE",
                    "BQACAgQAAxkBAAIBd2l_dKE_YU2pcFh9Z9r_DH7aphomAAL7HAAC7j0AAVCeJbeoyQzgxjgE",
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
                    "BQACAgQAAxkBAAIBeWl_dNNrfxKbelHxp67hA03iIOZuAAL8HAAC7j0AAVBC6O7b8opm_jgE"
                ]
            },
            "Numerical Methods": {
                "files": [
                    "BQACAgQAAxkBAAIBe2l_dPWaPkegmF8bsYDOo1ZyrFAIAAL9HAAC7j0AAVDyeO3qhIMqZTgE"
                ]
            },
            "Statistics and Probability": {
                "files": [
                    "BQACAgQAAxkBAAIBf2l_dWFoJBEX5meC2Iy9lD1oAg7cAAL_HAAC7j0AAVAT3h96NkNoUDgE"
                ]
            },
            "STATICS AND ENGINEERING": {
                "files": [
                    "BQACAgQAAxkBAAIBfWl_dSvWe-NrsAABqLoiwnyrxWtvygAC_hwAAu49AAFQD6yDliuYeWE4BA"
                ]
            },
            "Power Electronics": {
                "files": [
                    "BQACAgQAAxkBAAIBgWl_dZwCFzj0gMz66NeBi5s9dc8bAAMdAALuPQABUBpdy0nfu08wOAQ"
                ]
            },
            "Thermodynamics": {
                "files": [
                    "BQACAgQAAxkBAAIBhWl_ddif8UgcaUYGhx9b9WLtcahiAAICHQAC7j0AAVB8enEpdAJCcjgE",
                    "BQACAgQAAxkBAAIBg2l_dcvUiM-B6xqCHarjMgjZhs-1AAIBHQAC7j0AAVCmmVElDXdu-jgE",
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
                    "BQACAgQAAxkBAAIBh2l_dfW1BsAX6wxd1Mz2rDTvUPm3AAIDHQAC7j0AAVAczh001hUPbDgE"
                ]
            },
            "JAVA": {
                "files": [
                    "BQACAgQAAxkBAAIBiWl_dgOr3ZKF6MN-yMtLXu-mk0CFAAIEHQAC7j0AAVAEJr1HEDJ0OTgE"
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
                    "BQACAgQAAxkBAAIBjWl_dj49CQoMHkSrnOZAXAABvEOmFAACBx0AAu49AAFQMdVRhorDo984BA"
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
                    "BQACAgQAAxkBAAIBj2l_dmY_mOjpWctRhzkc5VGiAr7cAAIIHQAC7j0AAVA8Znv01gABgiA4BA"
                ]
            },
            "ETHICS": {
                "files": [
                    "BQACAgQAAxkBAAIBkWl_dmpBZMrht0RUJmP2ikglAAEXcAACCR0AAu49AAFQXZOMbGq74FE4BA"
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
