# aasu_books_bot.py
import os
import logging
from typing import Dict, List, Union

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# ----------------- الإعدادات العامة -----------------

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Environment variable BOT_TOKEN is not set")

# ----------------- بيانات الكتب -----------------

# النوع: Dict[category_key, Dict[book_name, Union[str, List[str]]]]
# إذا كان الكتاب في ملفين، ضع list من file_id
BOOKS: Dict[str, Dict[str, Union[str, List[str]]]] = {
    "ENGLISH": {
        "IEP098": [
            "BQACAgQAAxkBAAIL3Gl-EzrZzs2g07czYxViZnFQUmuMAAIdGwAC8nHxUxzXjXFnArCtOAQ",
            "BQACAgQAAxkBAAIL3Wl-EzoDyNzQ5XjTE_FRGbrVuotoAAIeGwAC8nHxU3nuGyUha9KHOAQ",
        ],
        "IEP099": [
            "BQACAgQAAxkBAAIMEWl-FNLQ7CV-qOpJ6NL-r412lwmHAAIhGwAC8nHxU4rMrWQVI3_Uoaq",
            "BQACAgQAAxkBAAIMFWl-FNw65ZKvj2cUhl4nVWQn80d9AAIiGwAC8nHxU_XTBdumCrE1OAQ",
        ],
        "ENL101": "BQACAgQAAxkBAAIMGWl-FOUnbh4wOGsNbtLngKoYyPtuAAIjGwAC8nHxU0Y7oQvq1Z2NOAQ",
        "ENL102": "BQACAgQAAxkBAAIMHWl-FQXlddgKlr3P5iYirVVA9rNrAAIkGwAC8nHxU2BsDB5e1iDjOAQ",
        "ENL201": "BQACAgQAAxkBAAIMIWl-FQ_weESJKCt12xhL4jhS_qGWAAIlGwAC8nHxU1b2DjPqD5tVOAQ",
    },
    "MATHEMATICS": {
        "IMP098": "BQACAgQAAxkBAAILz2l-ECGbiXh0jlcNWQAB4rH6wVDivgACERsAAvJx8VOGbCjs9abLrjgE",
        "IMP099": "BQACAgQAAxkBAAIL0Gl-ECHaJnh4p1bVl_2xEYmrvF5zAAITGwAC8nHxUws9ZXV3xq5fOAQ",
        "MAT120": "BQACAgQAAxkBAAIL0Wl-ECGAbAkm5fcbYxKLUQWTmAABBwACFBsAAvJx8VO5FMY6jCWnFzgE",
        "MAT202": [
            "BQACAgQAAxkBAAIL0ml-ECF-irXDHPkbWBXHC8KIb-WnAAIWGwAC8nHxU58M0c9N4NY1OAQ",
            "BQACAgQAAxkBAAIL02l-ECEG1xtclFYQE9nfddmOy-iTAAIXGwAC8nHxU5KDFOw2KgrAOAQ",
        ],
        "MAT240": "BQACAgQAAxkBAAIL1Gl-ECGkSQWzVoimStRO2izZYIsaAAIYGwAC8nHxU1w3q6vTihc5OAQ",
        "CALCULUS 1+2+3, 14th edition": [
            "BQACAgQAAxkBAAIL1Wl-ECGdFc_Jd6jbsEF47J-lJ950AAIZGwAC8nHxU5s8Au3aPqiYOAQ",
            "BQACAgQAAxkBAAIL1ml-ECHDd_INapp0zO-nyGOJxgltAAIbGwAC8nHxU6ngDlvpZT7LOAQ",
        ],
        "CALCULUS 1+2+3, 15th edition": "BQACAgQAAxkBAAIL12l-ECGz_nLCgUr0F48_s5H3D0h0AAIcGwAC8nHxU5DyCjnsOA1-OAQ",
    },
    "SCIENCE": {
        "CHEMISTRY": "BQACAgQAAxkBAAIMKWl-FSTI_dUM8mdsOuzXqvtE6mjVAAInGwAC8nHxU3X8S6YnxBvtOAQ",
        "BIOLOGY": "BQACAgQAAxkBAAIMJWl-FRvYNe_GWcR8xfQdSERQlH8jAAImGwAC8nHxU7fqnRfcBL-JOAQ",
        "PHYSICS 1+2": [
            "BQACAgQAAxkBAAIMLWl-FS4D6E8WOw4ye7VsWm-qwt6xAAIoGwAC8nHxU5UX0CLUbH48OAQ",
            "BQACAgQAAxkBAAIMMWl-FUB--sIR3Kbp21uT4JkvZsKIAAIpGwAC8nHxU-ExZbt3dQsfOAQ",
        ],
    },
    "ENGINEERING": {
        "Sustainable Energy": "BQACAgQAAxkBAAIMNml-FVAYIXNs2KPC9RyyeIYurThDAAIqGwAC8nHxU5AOCer6Uom2OAQ",
        "Numerical Methods": "BQACAgQAAxkBAAIMOml-FXN2tvwsnyz2Kki8Lz_4aZzmAAIrGwAC8nHxU-2B7iedfCcLOAQ",
        "Statistics and Probability": "BQACAgQAAxkBAAIMPml-FYWsXRClTnrowVJWTd6T1rGmAAIsGwAC8nHxU0RW_VA4ghQtOAQ",
        "STATICS AND ENGINEERING": "BQACAgQAAxkBAAIMQml-FZjPOxYp9ZmOOyCeaNZjQ6B0AAItGwAC8nHxUw2FATSwcdEyOAQ",
        "Power Electronics": "BQACAgQAAxkBAAIMRml-FaVOtMx3sENUGqGq5yVXAu9xAAIuGwAC8nHxU00l9Cv3g8z-OAQ",
        "Thermodynamics": [
            "BQACAgQAAxkBAAIMSml-FbLrrmYkgzQnziGSNi9W_dgrAAIvGwAC8nHxUwpE1g0nEDKWOAQ",
            "BQACAgQAAxkBAAIMTml-FbkUe9Fjhce70kH6fhTOV0RDAAIwGwAC8nHxU1BgiE_TMfeBOAQ",
        ],
    },
    "COMPUTING": {
        "Digital Logic": "BQACAgQAAxkBAAIMUml-FcOEj8C3sprkk8wr4HUwy7dLAAIxGwAC8nHxU8K0a9dzrH-mOAQ",
        "JAVA": "BQACAgQAAxkBAAIMWml-FeEMdZcvxOrd_PyfhFaxmBu5AAIzGwAC8nHxU-kZyqo6BeDNOAQ",
        "C++": "BQACAgQAAxkBAAIMVml-FdX5yUdk6QK3xlmgmYXrlL94AAIyGwAC8nHxUxgG1qHRu715OAQ",
    },
    "BUSINESS": {
        "International Economics": "BQACAgQAAxkBAAIMXml-FevL7ZdBcXOeIIy8zQlYZGozAAI0GwAC8nHxU7X3vLUkvyKcOAQ",
    },
    "GENERAL": {
        "INF": "BQACAgQAAxkBAAIMYml-FfV_XIgV2ywjRO5J12Vb6NuQAAI1GwAC8nHxU8QtFQABNpq81jgE",
        "ETHICS": "BQACAgQAAxkBAAIMZml-Ff7ymjnq3qdBttRPIvXqLXfoAAI2GwAC8nHxU3d75xq1hwvuOAQ",
    },
}

# أزرار القائمة الرئيسية: (النص الظاهر, المفتاح في BOOKS)
CATEGORIES = [
    ("ENGLISH 📘", "ENGLISH"),
    ("MATHEMATICS 📕", "MATHEMATICS"),
    ("SCIENCE 📙", "SCIENCE"),
    ("ENGINEERING 📗", "ENGINEERING"),
    ("COMPUTING 💻", "COMPUTING"),
    ("BUSINESS 💼", "BUSINESS"),
    ("GENERAL 📚", "GENERAL"),
]


# ----------------- لوحات الأزرار -----------------


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    rows = [[text] for text, _ in CATEGORIES]
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)


def category_keyboard(category_key: str) -> InlineKeyboardMarkup:
    books = BOOKS.get(category_key, {})
    buttons: List[List[InlineKeyboardButton]] = []

    for book_name in books.keys():
        # callback_data = "CATEGORY|BOOK_NAME"
        data = f"{category_key}|{book_name}"
        buttons.append([InlineKeyboardButton(book_name, callback_data=data)])

    # زر دعم إنستغرام في أخر القائمة
    buttons.append(
        [
            InlineKeyboardButton(
                "هذا الكتاب غير موجود؟ راسلنا على @BOOKADVISORS",
                url="https://www.instagram.com/BOOKADVISORS",
            )
        ]
    )

    return InlineKeyboardMarkup(buttons)


# ----------------- الهاندلرز -----------------


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "مرحبًا بك في AASU Books Bot 📚\n\n"
        "اختر القسم من القائمة السفلية، ثم اختر المقرر ليصلك الكتاب بصيغة PDF مباشرة.\n\n"
        "إذا لم تجد كتابك، يمكنك دائمًا مراسلتنا على إنستغرام:\n"
        "@BOOKADVISORS"
    )
    await update.message.reply_text(text, reply_markup=main_menu_keyboard())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "طريقة استخدام البوت:\n"
        "1️⃣ من القائمة السفلية اختر القسم (ENGLISH, MATHEMATICS …).\n"
        "2️⃣ ستظهر لك قائمة بالمواد داخل هذا القسم.\n"
        "3️⃣ اضغط على اسم المادة ليصلك الكتاب PDF.\n\n"
        "إن لم تجد الكتاب المطلوب، راسلنا على إنستغرام: @BOOKADVISORS"
    )
    await update.message.reply_text(text, reply_markup=main_menu_keyboard())


async def send_category(update: Update, category_key: str) -> None:
    books = BOOKS.get(category_key)
    if not books:
        await update.message.reply_text(
            "لا توجد كتب مسجّلة لهذا القسم حاليًا.",
            reply_markup=main_menu_keyboard(),
        )
        return

    await update.message.reply_text(
        "اختر المقرر المطلوب:",
        reply_markup=category_keyboard(category_key),
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    text = (update.message.text or "").strip()

    # 1) إذا ضغط زر من القائمة الرئيسية
    for button_text, category_key in CATEGORIES:
        if text == button_text:
            await send_category(update, category_key)
            return

    # 2) أي شيء آخر = مساعدة
    await help_command(update, context)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return

    await query.answer()

    data = query.data or ""
    if "|" not in data:
        return

    category_key, book_name = data.split("|", 1)
    books = BOOKS.get(category_key, {})
    file_value = books.get(book_name)

    if not file_value:
        await query.message.reply_text(
            "لم يتم العثور على هذا الملف.\n"
            "إن لم يكن الكتاب متوفرًا، راسلنا على إنستغرام: @BOOKADVISORS"
        )
        return

    chat_id = query.message.chat.id  # مهم: chat.id في الإصدارات الحديثة

    # كتاب واحد أو أكثر من ملف
    if isinstance(file_value, list):
        for idx, fid in enumerate(file_value, start=1):
            caption = f"{book_name} (جزء {idx})" if len(file_value) > 1 else book_name
            await context.bot.send_document(
                chat_id=chat_id,
                document=fid,
                caption=caption,
            )
    else:
        await context.bot.send_document(
            chat_id=chat_id,
            document=file_value,
            caption=book_name,
        )


# ----------------- نقطة التشغيل -----------------


def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("AASU Books Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
