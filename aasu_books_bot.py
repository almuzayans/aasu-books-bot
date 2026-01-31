import os
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ============= إعداد الأزرار =============

BACK_BUTTON = "🔙 القائمة الرئيسية"
REQUEST_BOOK_BUTTON = "📩 طلب كتاب غير موجود"

# CATEGORIES: كل قسم يحتوي كتب + قائمة الـ file_id لكل كتاب
CATEGORIES = {
    "ENGLISH 📘": {
        "IEP098": [
            "BQACAgQAAxkBAANeaX5DhKElVq3fMBxlGEbgGvcqcjwAAh0bAALycfFT9BoAAUXJL5S4OAQ",
            "BQACAgQAAxkBAANgaX5DjPtZvQJ1f97skcmc8_GDAXIAAh4bAALycfFT5GMrDI8u7wU4BA",
        ],
        "IEP099": [
            "BQACAgQAAxkBAANiaX5DlJuH3ba_Ayl9T2Tf3gOfqdMAAiEbAALycfFTpy3dulVQaRw4BA",
            "BQACAgQAAxkBAANkaX5DnKijQjw-ZL2xUrQEgwV6kCAAAiIbAALycfFTg7sY1hTGlJ44BA",
        ],
        "ENL101": [
            "BQACAgQAAxkBAANmaX5DoaPcTqVf2DH4TewM8EMZetMAAiMbAALycfFTk1YxE2Opeyk4BA",
        ],
        "ENL102": [
            "BQACAgQAAxkBAANoaX5DpDgsISuxIOX8huMpAQqckDkAAiQbAALycfFT3tRwYVSpZmg4BA",
        ],
        "ENL201": [
            "BQACAgQAAxkBAANqaX5DpyY3cXce9IqeglPbmybTwMQAAiUbAALycfFTs1G44mXYJSY4BA",
        ],
    },

    "MATHEMATICS 📕": {
        "IMP098": [
            "BQACAgQAAxkBAANMaX5C3-WU-9eRhjfOt_0TqdfH3X8AAhEbAALycfFTMHq5VYmQzvE4BA",
        ],
        "IMP099": [
            "BQACAgQAAxkBAANOaX5DAu1cHa3-AiuqRBIaV--yhjkAAhMbAALycfFTfNO4uXFsV9o4BA",
        ],
        "MAT120": [
            "BQACAgQAAxkBAANQaX5DCNSSyX0DH1qRpDQnyWC_I4kAAhQbAALycfFTNNcZ2GMWaGw4BA",
        ],
        "MAT202": [
            "BQACAgQAAxkBAANSaX5DELOJ_d0NWzISHplFEPvGlCwAAhYbAALycfFT_q1WURHg0Dk4BA",
            "BQACAgQAAxkBAANUaX5DJZ8Fr2hbcbUhme5rTywJNQUAAhcbAALycfFTr15SrbMrbJw4BA",
        ],
        "MAT240": [
            "BQACAgQAAxkBAANWaX5DLdLx7S_CtqajctIFvxTKfuMAAhgbAALycfFTnxqt4fRCfj04BA",
        ],
        "CALCULUS 1+2+3, 14th edition": [
            "BQACAgQAAxkBAANYaX5DMoTQJmYXVwb_S9Y1jhhnadwAAhkbAALycfFT47dPGDOwyYg4BA",
            "BQACAgQAAyEFAATd7DxXAANTaX5DY7ci7lyPxrsSDlyclYPdEmMAAhsbAALycfFTez66ahxP7Vs4BA",
        ],
        "CALCULUS 1+2+3, 15th edition": [
            "BQACAgQAAxkBAANcaX5DfqkAAXmt2grbQfGoGoxPRuJgAAIcGwAC8nHxU-9rxxOsCx3eOAQ",
        ],
    },

    "SCIENCE 📙": {
        "CHEMISTRY": [
            # ملاحظة: هذا نفس ID حق ENL201 كما أرسلته أنت. لو كان خطأ، استخرج واحد جديد لـ Chemistry واستبدله هنا.
            "BQACAgQAAxkBAANqaX5DpyY3cXce9IqeglPbmybTwMQAAiUbAALycfFTs1G44mXYJSY4BA",
        ],
        "BIOLOGY": [
            "BQACAgQAAxkBAANsaX5Dqth2_8VnAAHWxAJdWGQfoiyxAAImGwAC8nHxUxLrGa5bxwocOAQ",
        ],
        "PHYSICS 1+2": [
            "BQACAgQAAxkBAANwaX5Dsj3Xc2Ef6um7xSWT3nFduUwAAigbAALycfFT3dAcaZaAxJo4BA",
            "BQACAgQAAxkBAANyaX5D1aR6gB30_YrTRZfk8B8piFoAAikbAALycfFTSew7BD93KTo4BA",
        ],
    },

    "ENGINEERING 📗": {
        "Sustainable Energy": [
            "BQACAgQAAxkBAAN0aX5D2aFDNfKVK8mUatYEtSs4WdAAAiobAALycfFTkMQdzWQTids4BA",
        ],
        "Numerical Methods": [
            "BQACAgQAAxkBAAN2aX5D3ep5Wyk1fVtxDqsUhL_zlKAAAisbAALycfFTyCNa1b5r-_Q4BA",
        ],
        "Statistics and Probability": [
            "BQACAgQAAxkBAAN4aX5D8qd25WaT9RwHvHkutGjrSDUAAiwbAALycfFTRDpTGSb4Wdo4BA",
        ],
        "STATICS AND ENGINEERING": [
            "BQACAgQAAxkBAAN6aX5D9qaP2WcKl8zwDG5VGW92b2kAAi0bAALycfFTMctxbY8fzKk4BA",
        ],
        "Power Electronics": [
            "BQACAgQAAxkBAAN8aX5D-lfxE9Ak8u-8tYueiQ_lOHUAAi4bAALycfFT60ojbVjVR-Y4BA",
        ],
        "Thermodynamics": [
            "BQACAgQAAxkBAAN-aX5EAYfNr6nG9VXUAU5QSXVFuRAAAi8bAALycfFTHZzcdQ6MfOc4BA",
            "BQACAgQAAxkBAAOAaX5ECpTBcWN6LCSMXc44dSZzw50AAjAbAALycfFTHpWcivSKxvw4BA",
        ],
    },

    "COMPUTING 💻": {
        "Digital Logic": [
            "BQACAgQAAxkBAAOCaX5EDw-ndnnCb81VUNTyk5mvkXMAAjEbAALycfFT8wg371fy31I4BA",
        ],
        "JAVA": [
            "BQACAgQAAxkBAAOGaX5EHxfIL0XjswFLyaZ65bz9jw8AAjMbAALycfFTJrXTO1gNbns4BA",
        ],
        "C++": [
            "BQACAgQAAxkBAAOEaX5EE1KkQtBG3q35tgarkgadHgwAAjIbAALycfFTulRfrLFL5W04BA",
        ],
    },

    "BUSINESS 💼": {
        "International Economics": [
            "BQACAgQAAxkBAAOIaX5EJxw6xSfE3ZU39QKNyAOi-JsAAjQbAALycfFT66_9SZ33KcQ4BA",
        ],
    },

    "GENERAL 📚": {
        "INF": [
            "BQACAgQAAxkBAAOKaX5EMwndtD6s5DmqfWvdsR6JNYEAAjUbAALycfFT6tIrOpfEvIQ4BA",
        ],
        "ETHICS": [
            "BQACAgQAAxkBAAOMaX5EN4xrQ1F3TrK_RpL79AZKzfgAAjYbAALycfFTRRE-1RxQLRw4BA",
        ],
    },
}


# ============= بناء الكيبورد =============

def main_menu_keyboard() -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(name)] for name in CATEGORIES.keys()]
    rows.append([KeyboardButton(REQUEST_BOOK_BUTTON)])
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)


def category_keyboard(category_key: str) -> ReplyKeyboardMarkup:
    books = list(CATEGORIES[category_key].keys())
    rows = [[KeyboardButton(title)] for title in books]
    rows.append([KeyboardButton(BACK_BUTTON)])
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)


# ============= Handlers =============

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["state"] = "MAIN_MENU"
    context.user_data["category"] = None

    text = (
        "مرحباً بك في AASU BOOKS BOT 📚\n\n"
        "بوت غير رسمي يساعد طلاب جامعة عبدالله السالم في الوصول للكتب والمراجع بصيغة PDF.\n\n"
        "طريقة الاستخدام:\n"
        "1️⃣ اختر القسم (ENGLISH, MATHEMATICS, …) من الأزرار بالأسفل.\n"
        "2️⃣ اختر اسم المقرر/الكتاب.\n"
        "3️⃣ سيصلك الكتاب مباشرة.\n\n"
        f"إذا لم تجد كتابك اضغط الزر «{REQUEST_BOOK_BUTTON}» لطلب إضافته."
    )

    await update.message.reply_text(
        text,
        reply_markup=main_menu_keyboard(),
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (update.message.text or "").strip()
    state = context.user_data.get("state", "MAIN_MENU")
    current_category = context.user_data.get("category")

    # زر الرجوع
    if text == BACK_BUTTON:
        context.user_data["state"] = "MAIN_MENU"
        context.user_data["category"] = None
        await update.message.reply_text(
            "اختر القسم:",
            reply_markup=main_menu_keyboard(),
        )
        return

    # زر طلب كتاب غير موجود
    if text == REQUEST_BOOK_BUTTON:
        await update.message.reply_text(
            "📩 طلب كتاب غير موجود\n\n"
            "إذا لم تجد الكتاب الذي تبحث عنه، أرسل في رسالة واحدة:\n"
            "• اسم المقرر (بالإنجليزي كما في الخطة)\n"
            "• اسم الكتاب الكامل\n"
            "• رقم الإصدار (Edition) إن وجد\n\n"
            "أو تواصل مع مشرف البوت على إنستغرام:\n"
            "@BOOKADVISORS",
            reply_markup=main_menu_keyboard(),
        )
        return

    # /start في أي وقت
    if text.startswith("/start"):
        await start(update, context)
        return

    # اختيار قسم في أي حالة
    if text in CATEGORIES:
        context.user_data["state"] = "CATEGORY"
        context.user_data["category"] = text
        await update.message.reply_text(
            f"اختر الكتاب من قسم:\n{text}",
            reply_markup=category_keyboard(text),
        )
        return

    # داخل قسم: اختيار كتاب
    if state == "CATEGORY" and current_category in CATEGORIES:
        books = CATEGORIES[current_category]

        if text in books:
            file_ids = books[text]

            await update.message.reply_text(f"جاري إرسال: {text} 📚")

            for fid in file_ids:
                try:
                    await update.message.bot.send_document(
                        chat_id=update.effective_chat.id,
                        document=fid,
                    )
                except Exception as e:
                    # لو حصل خطأ من تليجرام
                    print(f"Error sending {text} with file_id {fid}: {e}")
                    await update.message.reply_text(
                        "حدث خطأ أثناء إرسال الملف.\n"
                        "إذا تكرر الخطأ، راسلنا على إنستغرام: @BOOKADVISORS",
                        reply_markup=category_keyboard(current_category),
                    )
                    return

            await update.message.reply_text(
                "يمكنك اختيار كتاب آخر من نفس القسم، أو الضغط على "
                f"«{BACK_BUTTON}» للعودة للقائمة الرئيسية.",
                reply_markup=category_keyboard(current_category),
            )
        else:
            # ضغط شيء غير موجود في هذا القسم
            await update.message.reply_text(
                "من فضلك اختر اسم الكتاب من الأزرار، "
                f"أو اضغط «{BACK_BUTTON}» للعودة.",
                reply_markup=category_keyboard(current_category),
            )
        return

    # أي نص غير معروف
    context.user_data["state"] = "MAIN_MENU"
    context.user_data["category"] = None
    await update.message.reply_text(
        "اختر القسم من الأزرار في الأسفل، أو اكتب /start للعودة للبداية.",
        reply_markup=main_menu_keyboard(),
    )


# ============= تشغيل البوت =============

def main() -> None:
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise RuntimeError("Environment variable BOT_TOKEN is not set")

    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()
