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
# بيانات الكتب (كل الأقسام)
# =========================

BOOKS: Dict[str, Dict[str, Any]] = {
    "ENGLISH": {
        "title": "ENGLISH",
        "emoji": "📘",
        "items": {
            "IEP098": {
                "files": [
                    "BQACAgQAAxkBAAIL3Gl-EzrZzs2g07czYxViZnFQUmuMAAIdGwAC8nHxUxzXjXFnArCtOAQ",
                    "BQACAgQAAxkBAAIL3Wl-EzoDyNzQ5XjTE_FRGbrVuotoAAIeGwAC8nHxU3nuGyUha9KHOAQ",
                ]
            },
            "IEP099": {
                "files": [
                    "BQACAgQAAxkBAANiaX5DlJuH3ba_Ayl9T2Tf3gOfqdMAAiEbAALycfFTpy3dulVQaRw4BA",
                    "BQACAgQAAxkBAANkaX5DnKijQjw-ZL2xUrQEgwV6kCAAAiIbAALycfFTg7sY1hTGlJ44BA",
                ]
            },
            "ENL101": {
                "files": [
                    "BQACAgQAAxkBAAIMGWl-FOUnbh4wOGsNbtLngKoYyPtuAAIjGwAC8nHxU0Y7oQvq1Z2NOAQ"
                ]
            },
            "ENL102": {
                "files": [
                    "BQACAgQAAxkBAAIMHWl-FQXlddgKlr3P5iYirVVA9rNrAAIkGwAC8nHxU2BsDB5e1iDjOAQ"
                ]
            },
            "ENL201": {
                "files": [
                    "BQACAgQAAxkBAAIMIWl-FQ_weESJKCt12xhL4jhS_qGWAAIlGwAC8nHxU1b2DjPqD5tVOAQ"
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
                    "BQACAgQAAxkBAAILz2l-ECGbiXh0jlcNWQAB4rH6wVDivgACERsAAvJx8VOGbCjs9abLrjgE"
                ]
            },
            "IMP099": {
                "files": [
                    "BQACAgQAAxkBAAIL0Gl-ECHaJnh4p1bVl_2xEYmrvF5zAAITGwAC8nHxUws9ZXV3xq5fOAQ"
                ]
            },
            "MAT120": {
                "files": [
                    "BQACAgQAAxkBAAIL0Wl-ECGAbAkm5fcbYxKLUQWTmAABBwACFBsAAvJx8VO5FMY6jCWnFzgE"
                ]
            },
            "MAT202": {
                "files": [
                    "BQACAgQAAxkBAAIL0ml-ECF-irXDHPkbWBXHC8KIb-WnAAIWGwAC8nHxU58M0c9N4NY1OAQ",
                    "BQACAgQAAxkBAAIL02l-ECEG1xtclFYQE9nfddmOy-iTAAIXGwAC8nHxU5KDFOw2KgrAOAQ",
                ]
            },
            "MAT240": {
                "files": [
                    "BQACAgQAAxkBAAIL1Gl-ECGkSQWzVoimStRO2izZYIsaAAIYGwAC8nHxU1w3q6vTihc5OAQ"
                ]
            },
            "CALCULUS 1+2+3, 14th edition": {
                "files": [
                    "BQACAgQAAxkBAAIL1Wl-ECGdFc_Jd6jbsEF47J-lJ950AAIZGwAC8nHxU5s8Au3aPqiYOAQ",
                    "BQACAgQAAxkBAAIL1ml-ECHDd_INapp0zO-nyGOJxgltAAIbGwAC8nHxU6ngDlvpZT7LOAQ",
                ]
            },
            "CALCULUS 1+2+3, 15th edition": {
                "files": [
                    "BQACAgQAAxkBAAIL12l-ECGz_nLCgUr0F48_s5H3D0h0AAIcGwAC8nHxU5DyCjnsOA1-OAQ"
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
                    "BQACAgQAAxkBAAIMKWl-FSTI_dUM8mdsOuzXqvtE6mjVAAInGwAC8nHxU3X8S6YnxBvtOAQ"
                ]
            },
            "BIOLOGY": {
                "files": [
                    "BQACAgQAAxkBAAIMJWl-FRvYNe_GWcR8xfQdSERQlH8jAAImGwAC8nHxU7fqnRfcBL-JOAQ"
                ]
            },
            "PHYSICS 1+2": {
                "files": [
                    "BQACAgQAAxkBAAIMLWl-FS4D6E8WOw4ye7VsWm-qwt6xAAIoGwAC8nHxU5UX0CLUbH48OAQ",
                    "BQACAgQAAxkBAAIMMWl-FUB--sIR3Kbp21uT4JkvZsKIAAIpGwAC8nHxU-ExZbt3dQsfOAQ",
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
                    "BQACAgQAAxkBAAIMNml-FVAYIXNs2KPC9RyyeIYurThDAAIqGwAC8nHxU5AOCer6Uom2OAQ"
                ]
            },
            "Numerical Methods": {
                "files": [
                    "BQACAgQAAxkBAAIMOml-FXN2tvwsnyz2Kki8Lz_4aZzmAAIrGwAC8nHxU-2B7iedfCcLOAQ"
                ]
            },
            "Statistics and Probability": {
                "files": [
                    "BQACAgQAAxkBAAIMPml-FYWsXRClTnrowVJWTd6T1rGmAAIsGwAC8nHxU0RW_VA4ghQtOAQ"
                ]
            },
            "STATICS AND ENGINEERING": {
                "files": [
                    "BQACAgQAAxkBAAIMQml-FZjPOxYp9ZmOOyCeaNZjQ6B0AAItGwAC8nHxUw2FATSwcdEyOAQ"
                ]
            },
            "Power Electronics": {
                "files": [
                    "BQACAgQAAxkBAAIMRml-FaVOtMx3sENUGqGq5yVXAu9xAAIuGwAC8nHxU00l9Cv3g8z-OAQ"
                ]
            },
            "Thermodynamics": {
                "files": [
                    "BQACAgQAAxkBAAIMSml-FbLrrmYkgzQnziGSNi9W_dgrAAIvGwAC8nHxUwpE1g0nEDKWOAQ",
                    "BQACAgQAAxkBAAIMTml-FbkUe9Fjhce70kH6fhTOV0RDAAIwGwAC8nHxU1BgiE_TMfeBOAQ",
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
                    "BQACAgQAAxkBAAIMUml-FcOEj8C3sprkk8wr4HUwy7dLAAIxGwAC8nHxU8K0a9dzrH-mOAQ"
                ]
            },
            "JAVA": {
                "files": [
                    "BQACAgQAAxkBAAIMWml-FeEMdZcvxOrd_PyfhFaxmBu5AAIzGwAC8nHxU-kZyqo6BeDNOAQ"
                ]
            },
            "C++": {
                "files": [
                    "BQACAgQAAxkBAAIMVml-FdX5yUdk6QK3xlmgmYXrlL94AAIyGwAC8nHxUxgG1qHRu715OAQ"
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
                    "BQACAgQAAxkBAAIMXml-FevL7ZdBcXOeIIy8zQlYZGozAAI0GwAC8nHxU7X3vLUkvyKcOAQ"
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
                    "BQACAgQAAxkBAAIMYml-FfV_XIgV2ywjRO5J12Vb6NuQAAI1GwAC8nHxU8QtFQABNpq81jgE"
                ]
            },
            "ETHICS": {
                "files": [
                    "BQACAgQAAxkBAAIMZml-Ff7ymjnq3qdBttRPIvXqLXfoAAI2GwAC8nHxU3d75xq1hwvuOAQ"
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
        "مرحبًا بك في AASU BOOKS BOT 📚\n\n"
        "بوت غير رسمي لمساعدة طلاب جامعة عبدالله السالم على الوصول للكتب.\n\n"
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
            "أو راسلنا على تليقرام:\n"
            "@BOOKADVISORS",
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
                    "إذا تكرر الخطأ، راسلنا على تليقرام:\n"
                    "@BOOKADVISORS",
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
# main
# =========================

def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("Bot started…")
    app.run_polling()


if __name__ == "__main__":
    main()

