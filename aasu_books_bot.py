import os
import logging

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
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

# ==========================
# إعداد الـ Logging
# ==========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ==========================
# توكن البوت من Environment
# ==========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Environment variable BOT_TOKEN is not set")

# ==========================
# الأزرار الثابتة
# ==========================
BACK_BUTTON = "🔙 القائمة الرئيسية"
REQUEST_BOOK_BUTTON = "📩 طلب كتاب غير موجود"

# أزرار الأقسام في الكيبورد السفلية (ReplyKeyboard)
CATEGORY_BUTTONS = {
    "ENGLISH 📘": "ENGLISH",
    "MATHEMATICS 📕": "MATHEMATICS",
    "SCIENCE 📙": "SCIENCE",
    "ENGINEERING 📗": "ENGINEERING",
    "COMPUTING 💻": "COMPUTING",
    "BUSINESS 💼": "BUSINESS",
    "GENERAL 📚": "GENERAL",
}

# ==========================
# بيانات الكتب + File IDs
# ==========================
BOOKS = {
    "ENGLISH": {
        "IEP098": [
            "BQACAgQAAxkBAAIL3Gl-EzrZzs2g07czYxViZnFQUmuMAAIdGwAC8nHxUxzXjXFnArCtOAQ",
            "BQACAgQAAxkBAAIL3Wl-EzoDyNzQ5XjTE_FRGbrVuotoAAIeGwAC8nHxU3nuGyUha9KHOAQ",
        ],
        "IEP099": [
            "BQACAgQAAxkBAAIMEWl-FNLQ7CV-qOpJ6NL-r412lwmHAAIhGwAC8nHxU4rMrWQVI3_Uoaq",
            "BQACAgQAAxkBAAIMFWl-FNw65ZKvj2cUhl4nVWQn80d9AAIiGwAC8nHxU_XTBdumCrE1OAQ",
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
    "MATHEMATICS": {
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
        "CALCULUS 1+2+3, 14th edition": [
            "BQACAgQAAxkBAAIL1Wl-ECGdFc_Jd6jbsEF47J-lJ950AAIZGwAC8nHxU5s8Au3aPqiYOAQ",
            "BQACAgQAAxkBAAIL1ml-ECHDd_INapp0zO-nyGOJxgltAAIbGwAC8nHxU6ngDlvpZT7LOAQ",
        ],
        "CALCULUS 1+2+3, 15th edition": [
            "BQACAgQAAxkBAAIL12l-ECGz_nLCgUr0F48_s5H3D0h0AAIcGwAC8nHxU5DyCjnsOA1-OAQ",
        ],
    },
    "SCIENCE": {
        "CHEMISTRY": [
            "BQACAgQAAxkBAAIMKWl-FSTI_dUM8mdsOuzXqvtE6mjVAAInGwAC8nHxU3X8S6YnxBvtOAQ",
        ],
        "BIOLOGY": [
            "BQACAgQAAxkBAAIMJWl-FRvYNe_GWcR8xfQdSERQlH8jAAImGwAC8nHxU7fqnRfcBL-JOAQ",
        ],
        "PHYSICS 1+2": [
            "BQACAgQAAxkBAAIMLWl-FS4D6E8WOw4ye7VsWm-qwt6xAAIoGwAC8nHxU5UX0CLUbH48OAQ",
            "BQACAgQAAxkBAAIMMWl-FUB--sIR3Kbp21uT4JkvZsKIAAIpGwAC8nHxU-ExZbt3dQsfOAQ",
        ],
    },
    "ENGINEERING": {
        "Sustainable Energy": [
            "BQACAgQAAxkBAAIMNml-FVAYIXNs2KPC9RyyeIYurThDAAIqGwAC8nHxU5AOCer6Uom2OAQ",
        ],
        "Numerical Methods": [
            "BQACAgQAAxkBAAIMOml-FXN2tvwsnyz2Kki8Lz_4aZzmAAIrGwAC8nHxU-2B7iedfCcLOAQ",
        ],
        "Statistics and Probability": [
            "BQACAgQAAxkBAAIMPml-FYWsXRClTnrowVJWTd6T1rGmAAIsGwAC8nHxU0RW_VA4ghQtOAQ",
        ],
        "Statics and Strength of Materials": [
            "BQACAgQAAxkBAAIMQml-FZjPOxYp9ZmOOyCeaNZjQ6B0AAItGwAC8nHxUw2FATSwcdEyOAQ",
        ],
        "Power Electronics": [
            "BQACAgQAAxkBAAIMRml-FaVOtMx3sENUGqGq5yVXAu9xAAIuGwAC8nHxU00l9Cv3g8z-OAQ",
        ],
        "Thermodynamics": [
            "BQACAgQAAxkBAAIMSml-FbLrrmYkgzQnziGSNi9W_dgrAAIvGwAC8nHxUwpE1g0nEDKWOAQ",
            "BQACAgQAAxkBAAIMTml-FbkUe9Fjhce70kH6fhTOV0RDAAIwGwAC8nHxU1BgiE_TMfeBOAQ",
        ],
    },
    "COMPUTING": {
        "Digital Logic": [
            "BQACAgQAAxkBAAIMUml-FcOEj8C3sprkk8wr4HUwy7dLAAIxGwAC8nHxU8K0a9dzrH-mOAQ",
        ],
        "JAVA": [
            "BQACAgQAAxkBAAIMWml-FeEMdZcvxOrd_PyfhFaxmBu5AAIzGwAC8nHxU-kZyqo6BeDNOAQ",
        ],
        "C++": [
            "BQACAgQAAxkBAAIMVml-FdX5yUdk6QK3xlmgmYXrlL94AAIyGwAC8nHxUxgG1qHRu715OAQ",
        ],
    },
    "BUSINESS": {
        "International Economics": [
            "BQACAgQAAxkBAAIMXml-FevL7ZdBcXOeIIy8zQlYZGozAAI0GwAC8nHxU7X3vLUkvyKcOAQ",
        ],
    },
    "GENERAL": {
        "INF": [
            "BQACAgQAAxkBAAIMYml-FfV_XIgV2ywjRO5J12Vb6NuQAAI1GwAC8nHxU8QtFQABNpq81jgE",
        ],
        "ETHICS": [
            "BQACAgQAAxkBAAIMZml-Ff7ymjnq3qdBttRPIvXqLXfoAAI2GwAC8nHxU3d75xq1hwvuOAQ",
        ],
    },
}

# ==========================
# دوال الكيبوردات
# ==========================


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    rows = [
        [KeyboardButton("ENGLISH 📘")],
        [KeyboardButton("MATHEMATICS 📕")],
        [KeyboardButton("SCIENCE 📙")],
        [KeyboardButton("ENGINEERING 📗")],
        [KeyboardButton("COMPUTING 💻")],
        [KeyboardButton("BUSINESS 💼")],
        [KeyboardButton("GENERAL 📚")],
        [KeyboardButton(REQUEST_BOOK_BUTTON)],
    ]
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)


def category_keyboard(category: str) -> InlineKeyboardMarkup:
    buttons = []
    for book_name in BOOKS.get(category, {}):
        buttons.append(
            [InlineKeyboardButton(book_name, callback_data=f"{category}|{book_name}")]
        )

    # زر العودة للقائمة الرئيسية كـ Inline
    buttons.append([InlineKeyboardButton(BACK_BUTTON, callback_data="BACK_TO_MAIN")])

    return InlineKeyboardMarkup(buttons)


# ==========================
# Handlers
# ==========================


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["state"] = "MAIN_MENU"
    context.user_data["category"] = None

    text = (
        "مرحباً بك في AASU BOOKS BOT 📚\n\n"
        "بوت غير رسمي لمساعدة طلاب جامعة عبدالله السالم في الوصول إلى الكتب والمراجع بسهولة.\n\n"
        "طريقة الاستخدام:\n"
        "1️⃣ اختر القسم (ENGLISH, MATHEMATICS, …) من الأزرار في الأسفل.\n"
        "2️⃣ اختر اسم المقرر/الكتاب من القائمة التالية.\n"
        "3️⃣ سيصلك الكتاب مباشرة بصيغة PDF.\n\n"
        f"إذا لم تجد كتابك اضغط الزر «{REQUEST_BOOK_BUTTON}» في الأسفل لطلب إضافة الكتاب."
    )

    await update.message.reply_text(text, reply_markup=main_menu_keyboard())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "استخدم /start لعرض القائمة الرئيسية ثم اختر القسم والكتاب المطلوب.\n"
        f"لطلب كتاب غير موجود اضغط «{REQUEST_BOOK_BUTTON}» من القائمة."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()
    state = context.user_data.get("state", "MAIN_MENU")

    # زر الرجوع من الكيبورد السفلية (لو استُخدم مستقبلاً)
    if text == BACK_BUTTON:
        context.user_data["state"] = "MAIN_MENU"
        context.user_data["category"] = None
        await update.message.reply_text(
            "اختر القسم:", reply_markup=main_menu_keyboard()
        )
        return

    # زر طلب كتاب غير موجود
    if text == REQUEST_BOOK_BUTTON:
        await update.message.reply_text(
            "📩 طلب كتاب غير موجود\n\n"
            "إذا لم تجد كتابك في القوائم، أرسل في رسالة واحدة المعلومات التالية:\n"
            "• اسم المقرر (بالإنجليزي كما في الخطة)\n"
            "• اسم الكتاب الكامل\n"
            "• رقم الإصدار (Edition) إن وجد\n\n"
            "أو يمكنك التواصل مباشرة مع مشرف البوت:\n"
            "@YourUser\n\n"
            "بعد إرسال الطلب سيتم مراجعته وإضافة الكتاب للقائمة قدر المستطاع."
        )
        return

    # حالة القائمة الرئيسية
    if state == "MAIN_MENU":
        category = CATEGORY_BUTTONS.get(text)
        if not category:
            await update.message.reply_text(
                "اختر القسم من الأزرار في الأسفل.", reply_markup=main_menu_keyboard()
            )
            return

        # الانتقال إلى حالة اختيار كتاب
        context.user_data["state"] = "CATEGORY"
        context.user_data["category"] = category

        await update.message.reply_text(
            f"اختر الكتاب من قسم {category}:", reply_markup=category_keyboard(category)
        )
        return

    # حالة اختيار كتاب (المستخدم يضغط Inline Buttons وليس يكتب نص)
    if state == "CATEGORY":
        category = context.user_data.get("category")
        if not category:
            context.user_data["state"] = "MAIN_MENU"
            await update.message.reply_text(
                "حدث خطأ بسيط، تم إعادتك للقائمة الرئيسية.",
                reply_markup=main_menu_keyboard(),
            )
            return

        await update.message.reply_text(
            "اختر الكتاب من الأزرار الظاهرة فوق الرسائل.", reply_markup=category_keyboard(category)
        )
        return


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data

    # زر الرجوع للقائمة الرئيسية من الـ Inline Keyboard
    if data == "BACK_TO_MAIN":
        context.user_data["state"] = "MAIN_MENU"
        context.user_data["category"] = None
        await query.message.reply_text(
            "اختر القسم:", reply_markup=main_menu_keyboard()
        )
        return

    # بيانات الكتاب: CATEGORY|BOOK_NAME
    try:
        category, book_name = data.split("|", maxsplit=1)
    except ValueError:
        return

    files = BOOKS.get(category, {}).get(book_name)
    if not files:
        await query.message.reply_text("لم يتم العثور على هذا الكتاب حالياً.")
        return

    # إرسال كل الملفات المرتبطة بالكتاب (كتاب + Solutions مثلاً)
    first = True
    for file_id in files:
        if first:
            await context.bot.send_document(
                chat_id=query.message.chat_id,
                document=file_id,
                caption=f"{book_name}",
            )
            first = False
        else:
            await context.bot.send_document(
                chat_id=query.message.chat_id,
                document=file_id,
            )


# ==========================
# Main
# ==========================


def main() -> None:
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .read_timeout(30)
        .write_timeout(30)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    application.add_handler(CallbackQueryHandler(handle_callback))

    logger.info("AASU Books Bot started.")
    application.run_polling()


if __name__ == "__main__":
    main()
