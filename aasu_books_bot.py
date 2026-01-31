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

# إعداد اللوج
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# توكن البوت من متغير البيئة
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Environment variable BOT_TOKEN is not set.")


# =========================
# بيانات الكتب
# =========================

BOOKS: Dict[str, Dict[str, Any]] = {
    "ENGLISH": {
        "title": "ENGLISH",
        "emoji": "📘",
        "items": {
            "IEP098": {
                "title": "IEP098",
                "files": [
                    "BQACAgQAAxkBAAIL3Gl-EzrZzs2g07czYxViZnFQUmuMAAIdGwAC8nHxUxzXjXFnArCtOAQ",
                    "BQACAgQAAxkBAAIL3Wl-EzoDyNzQ5XjTE_FRGbrVuotoAAIeGwAC8nHxU3nuGyUha9KHOAQ",
                ],
            },
            "IEP099": {
                "title": "IEP099",
                # ضع هنا file_id الصحيح لملفات IEP099 عندما تحصل عليهما
                # مثال:
                # "files": ["id_1", "id_2"],
                "files": [],
            },
            "ENL101": {
                "title": "ENL101",
                "files": [
                    "BQACAgQAAxkBAAIMGWl-FOUnbh4wOGsNbtLngKoYyPtuAAIjGwAC8nHxU0Y7oQvq1Z2NOAQ"
                ],
            },
            "ENL102": {
                "title": "ENL102",
                "files": [
                    "BQACAgQAAxkBAAIMHWl-FQXlddgKlr3P5iYirVVA9rNrAAIkGwAC8nHxU2BsDB5e1iDjOAQ"
                ],
            },
            "ENL201": {
                "title": "ENL201",
                "files": [
                    "BQACAgQAAxkBAAIMIWl-FQ_weESJKCt12xhL4jhS_qGWAAIlGwAC8nHxU1b2DjPqD5tVOAQ"
                ],
            },
        },
    },
    "MATHEMATICS": {
        "title": "MATHEMATICS",
        "emoji": "📕",
        "items": {
            "IMP098": {
                "title": "IMP098",
                "files": [
                    "BQACAgQAAxkBAAILz2l-ECGbiXh0jlcNWQAB4rH6wVDivgACERsAAvJx8VOGbCjs9abLrjgE"
                ],
            },
            "IMP099": {
                "title": "IMP099",
                "files": [
                    "BQACAgQAAxkBAAIL0Gl-ECHaJnh4p1bVl_2xEYmrvF5zAAITGwAC8nHxUws9ZXV3xq5fOAQ"
                ],
            },
            "MAT120": {
                "title": "MAT120",
                "files": [
                    "BQACAgQAAxkBAAIL0Wl-ECGAbAkm5fcbYxKLUQWTmAABBwACFBsAAvJx8VO5FMY6jCWnFzgE"
                ],
            },
            "MAT202": {
                "title": "MAT202",
                "files": [
                    "BQACAgQAAxkBAAIL0ml-ECF-irXDHPkbWBXHC8KIb-WnAAIWGwAC8nHxU58M0c9N4NY1OAQ",
                    "BQACAgQAAxkBAAIL02l-ECEG1xtclFYQE9nfddmOy-iTAAIXGwAC8nHxU5KDFOw2KgrAOAQ",
                ],
            },
            "MAT240": {
                "title": "MAT240",
                "files": [
                    "BQACAgQAAxkBAAIL1Gl-ECGkSQWzVoimStRO2izZYIsaAAIYGwAC8nHxU1w3q6vTihc5OAQ"
                ],
            },
            "CALC143_14": {
                "title": "CALCULUS 1+2+3, 14th edition",
                "files": [
                    "BQACAgQAAxkBAAIL1Wl-ECGdFc_Jd6jbsEF47J-lJ950AAIZGwAC8nHxU5s8Au3aPqiYOAQ",
                    "BQACAgQAAxkBAAIL1ml-ECHDd_INapp0zO-nyGOJxgltAAIbGwAC8nHxU6ngDlvpZT7LOAQ",
                ],
            },
            "CALC143_15": {
                "title": "CALCULUS 1+2+3, 15th edition",
                "files": [
                    "BQACAgQAAxkBAAIL12l-ECGz_nLCgUr0F48_s5H3D0h0AAIcGwAC8nHxU5DyCjnsOA1-OAQ"
                ],
            },
        },
    },
    "SCIENCE": {
        "title": "SCIENCE",
        "emoji": "📙",
        "items": {
            "CHEMISTRY": {
                "title": "CHEMISTRY",
                "files": [
                    "BQACAgQAAxkBAAIMKWl-FSTI_dUM8mdsOuzXqvtE6mjVAAInGwAC8nHxU3X8S6YnxBvtOAQ"
                ],
            },
            "BIOLOGY": {
                "title": "BIOLOGY",
                "files": [
                    "BQACAgQAAxkBAAIMJWl-FRvYNe_GWcR8xfQdSERQlH8jAAImGwAC8nHxU7fqnRfcBL-JOAQ"
                ],
            },
            "PHYSICS12": {
                "title": "PHYSICS 1+2",
                "files": [
                    "BQACAgQAAxkBAAIMLWl-FS4D6E8WOw4ye7VsWm-qwt6xAAIoGwAC8nHxU5UX0CLUbH48OAQ",
                    "BQACAgQAAxkBAAIMMWl-FUB--sIR3Kbp21uT4JkvZsKIAAIpGwAC8nHxU-ExZbt3dQsfOAQ",
                ],
            },
        },
    },
    "ENGINEERING": {
        "title": "ENGINEERING",
        "emoji": "📗",
        "items": {
            "SUSTAINABLE_ENERGY": {
                "title": "Sustainable Energy",
                "files": [
                    "BQACAgQAAxkBAAIMNml-FVAYIXNs2KPC9RyyeIYurThDAAIqGwAC8nHxU5AOCer6Uom2OAQ"
                ],
            },
            "NUMERICAL_METHODS": {
                "title": "Numerical Methods",
                "files": [
                    "BQACAgQAAxkBAAIMOml-FXN2tvwsnyz2Kki8Lz_4aZzmAAIrGwAC8nHxU-2B7iedfCcLOAQ"
                ],
            },
            "STATS_PROB": {
                "title": "Statistics and Probability",
                "files": [
                    "BQACAgQAAxkBAAIMPml-FYWsXRClTnrowVJWTd6T1rGmAAIsGwAC8nHxU0RW_VA4ghQtOAQ"
                ],
            },
            "STATICS": {
                "title": "STATICS AND ENGINEERING",
                "files": [
                    "BQACAgQAAxkBAAIMQml-FZjPOxYp9ZmOOyCeaNZjQ6B0AAItGwAC8nHxUw2FATSwcdEyOAQ"
                ],
            },
            "POWER_ELECTRONICS": {
                "title": "Power Electronics",
                "files": [
                    "BQACAgQAAxkBAAIMRml-FaVOtMx3sENUGqGq5yVXAu9xAAIuGwAC8nHxU00l9Cv3g8z-OAQ"
                ],
            },
            "THERMODYNAMICS": {
                "title": "Thermodynamics",
                "files": [
                    "BQACAgQAAxkBAAIMSml-FbLrrmYkgzQnziGSNi9W_dgrAAIvGwAC8nHxUwpE1g0nEDKWOAQ",
                    "BQACAgQAAxkBAAIMTml-FbkUe9Fjhce70kH6fhTOV0RDAAIwGwAC8nHxU1BgiE_TMfeBOAQ",
                ],
            },
        },
    },
    "COMPUTING": {
        "title": "COMPUTING",
        "emoji": "💻",
        "items": {
            "DIGITAL_LOGIC": {
                "title": "Digital Logic",
                "files": [
                    "BQACAgQAAxkBAAIMUml-FcOEj8C3sprkk8wr4HUwy7dLAAIxGwAC8nHxU8K0a9dzrH-mOAQ"
                ],
            },
            "JAVA": {
                "title": "JAVA",
                "files": [
                    "BQACAgQAAxkBAAIMWml-FeEMdZcvxOrd_PyfhFaxmBu5AAIzGwAC8nHxU-kZyqo6BeDNOAQ"
                ],
            },
            "CPP": {
                "title": "C++",
                "files": [
                    "BQACAgQAAxkBAAIMVml-FdX5yUdk6QK3xlmgmYXrlL94AAIyGwAC8nHxUxgG1qHRu715OAQ"
                ],
            },
        },
    },
    "BUSINESS": {
        "title": "BUSINESS",
        "emoji": "💼",
        "items": {
            "INT_ECON": {
                "title": "International Economics",
                "files": [
                    "BQACAgQAAxkBAAIMXml-FevL7ZdBcXOeIIy8zQlYZGozAAI0GwAC8nHxU7X3vLUkvyKcOAQ"
                ],
            },
        },
    },
    "GENERAL": {
        "title": "GENERAL",
        "emoji": "📚",
        "items": {
            "INF": {
                "title": "INF",
                "files": [
                    "BQACAgQAAxkBAAIMYml-FfV_XIgV2ywjRO5J12Vb6NuQAAI1GwAC8nHxU8QtFQABNpq81jgE"
                ],
            },
            "ETHICS": {
                "title": "ETHICS",
                "files": [
                    "BQACAgQAAxkBAAIMZml-Ff7ymjnq3qdBttRPIvXqLXfoAAI2GwAC8nHxU3d75xq1hwvuOAQ"
                ],
            },
        },
    },
}

# سيتم ملؤها آليًا بعد تعريف BOOKS
SECTION_BUTTONS: Dict[str, str] = {}
BOOK_BUTTONS: Dict[str, tuple] = {}


def _build_button_maps() -> None:
    """تحضير القوائم من BOOKS."""
    SECTION_BUTTONS.clear()
    BOOK_BUTTONS.clear()

    for sec_key, sec_data in BOOKS.items():
        sec_button = f"{sec_data['title']} {sec_data['emoji']}"
        SECTION_BUTTONS[sec_button] = sec_key

        for book_key, book_data in sec_data["items"].items():
            book_button = book_data["title"]
            BOOK_BUTTONS[book_button] = (sec_key, book_key)


# استدعاء مرة واحدة عند التشغيل
_build_button_maps()

MAIN_REQUEST_BUTTON = "طلب كتاب غير موجود ✉️"
MAIN_BACK_BUTTON = "القائمة الرئيسية ⬅️ BACK"


def build_main_menu() -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text)] for text in SECTION_BUTTONS.keys()]
    rows.append([KeyboardButton(MAIN_REQUEST_BUTTON)])
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)


async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id

    text = (
        "مرحبًا بك في بوت الكتب غير الرسمي لجامعة عبدالله السالم AASU Books Bot.\n\n"
        "⚠️ البوت غير تابع رسميًا للجامعة.\n\n"
        "طريقة الاستخدام:\n"
        "1️⃣ اختر القسم من الأزرار بالأسفل.\n"
        "2️⃣ اختر اسم الكتاب الذي تريده.\n"
        "3️⃣ سيصلك الكتاب مباشرة كملف PDF.\n\n"
        "إذا لم تجد كتابك، اضغط الزر:\n"
        f"«{MAIN_REQUEST_BUTTON}» لطلب إضافة كتاب جديد.\n"
    )

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=build_main_menu(),
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_welcome(update, context)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (update.message.text or "").strip()

    # رجوع للقائمة الرئيسية
    if text == MAIN_BACK_BUTTON or text.lower() in {"/menu", "main menu"}:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="اختر القسم:",
            reply_markup=build_main_menu(),
        )
        return

    # زر طلب كتاب غير موجود
    if text == MAIN_REQUEST_BUTTON:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                "إذا لم تجد كتابك في القوائم، أرسل لنا اسم المقرر، اسم الكتاب، "
                "والطبعة على تيليقرام:\n"
                "@BOOKADVISORS\n\n"
                "أو اكتبها هنا كرسالة وسنحاول إضافته في أقرب وقت."
            ),
        )
        return

    # اختيار قسم
    if text in SECTION_BUTTONS:
        sec_key = SECTION_BUTTONS[text]
        await send_section_books(sec_key, update, context)
        return

    # اختيار كتاب
    if text in BOOK_BUTTONS:
        sec_key, book_key = BOOK_BUTTONS[text]
        await send_book_files(sec_key, book_key, update, context)
        return

    # نص عشوائي
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="استخدم الأزرار بالأسفل لاختيار القسم أو الكتاب.",
    )


async def send_section_books(
    section_key: str, update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    chat_id = update.effective_chat.id
    sec = BOOKS[section_key]

    rows = [
        [KeyboardButton(book_data["title"])]
        for book_data in sec["items"].values()
    ]
    rows.append([KeyboardButton(MAIN_BACK_BUTTON)])
    rows.append([KeyboardButton(MAIN_REQUEST_BUTTON)])

    reply_markup = ReplyKeyboardMarkup(rows, resize_keyboard=True)

    await context.bot.send_message(
        chat_id=chat_id,
        text=f"اختر الكتاب من قسم:\n{sec['title']} {sec['emoji']}",
        reply_markup=reply_markup,
    )


async def send_book_files(
    section_key: str, book_key: str, update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    chat_id = update.effective_chat.id
    book = BOOKS[section_key]["items"][book_key]
    files = book.get("files") or []

    if not files:
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                f"الكتاب «{book['title']}» غير مضاف حاليًّا أو أن الرابط يحتاج تحديثًا.\n"
                "سيتم رفعه قريبًا إن شاء الله."
            ),
        )
        return

    await context.bot.send_message(
        chat_id=chat_id,
        text=f"📚 جاري إرسال: {book['title']}",
    )

    try:
        for file_id in files:
            await context.bot.send_document(
                chat_id=chat_id,
                document=file_id,
            )
    except Exception as e:
        logger.exception("Error while sending file for %s - %s", section_key, book_key)
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "حدث خطأ أثناء إرسال الملف.\n"
                "رسالة النظام من تيليجرام:\n"
                f"{e}\n\n"
                "إذا تكرر الخطأ، راسلنا على إنستغرام:\n"
                "@BOOKADVISORS"
            ),
        )


def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("Bot is starting...")
    application.run_polling()


if __name__ == "__main__":
    main()
