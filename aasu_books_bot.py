import os
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ========================
# 1) إعداد القوائم
# ========================

MAIN_MENU_BUTTONS = [
    ["ENGLISH 📘"],
    ["MATHEMATICS 📕"],
    ["SCIENCE 📙"],
    ["ENGINEERING 📗"],
    ["COMPUTING 💻"],
    ["BUSINESS 💼"],
    ["GENERAL 📚"],
]

SECTION_BOOKS = {
    "ENGLISH 📘": ["IEP098", "IEP099", "ENL101", "ENL102", "ENL201"],
    "MATHEMATICS 📕": ["IMP098", "IMP099", "MAT120", "MAT202", "MAT240",
                       "CALCULUS 1+2+3, 14th edition", "CALCULUS 1+2+3, 15th edition"],
    "SCIENCE 📙": ["CHEMISTRY", "BIOLOGY", "PHYSICS 1+2"],
    "ENGINEERING 📗": ["Sustainable Energy", "Numerical Methods",
                       "Statistics and Probability", "STATICS AND ENGINEERING",
                       "Power Electronics", "Thermodynamics"],
    "COMPUTING 💻": ["Digital Logic", "JAVA", "C++"],
    "BUSINESS 💼": ["International Economics"],
    "GENERAL 📚": ["INF", "ETHICS"],
}

# هنا ضع الـ file_id الصحيحة لاحقاً بعد أن تستخرجها من البوت نفسه
BOOK_FILES = {
    "IEP098": [
        "BQACAgQAAxkBAAIL3Gl-EzrZzs2g07czYxViZnFQUmuMAAIdGwAC8nHxUxzXjXFnArCtOAQ",
        "BQACAgQAAxkBAAIL3Wl-EzoDyNzQ5XjTE_FRGbrVuotoAAIeGwAC8nHxU3nuGyUha9KHOAQ",
    ],
    "IEP099": [
        "BQACAgQAAxkBAAIMEWl-FNLQ7CV-qOpJ6NL-r412lwmHAAIhGwAC8nHxU4rMrWQVI3_Uoaq",
        "BQACAgQAAxkBAAIMFWl-FNw65ZKvj2cUhl4nVWQn80d9AAIiGwAC8nHxU_XTBdumCrE1OAQ",
    ],
    "ENL101": ["BQACAgQAAxkBAAIMGWl-FOUnbh4wOGsNbtLngKoYyPtuAAIjGwAC8nHxU0Y7oQvq1Z2NOAQ"],
    "ENL102": ["BQACAgQAAxkBAAIMHWl-FQXlddgKlr3P5iYirVVA9rNrAAIkGwAC8nHxU2BsDB5e1iDjOAQ"],
    "ENL201": ["BQACAgQAAxkBAAIMIWl-FQ_weESJKCt12xhL4jhS_qGWAAIlGwAC8nHxU1b2DjPqD5tVOAQ"],

    "IMP098": ["BQACAgQAAxkBAAILz2l-ECGbiXh0jlcNWQAB4rH6wVDivgACERsAAvJx8VOGbCjs9abLrjgE"],
    "IMP099": ["BQACAgQAAxkBAAIL0Gl-ECHaJnh4p1bVl_2xEYmrvF5zAAITGwAC8nHxUws9ZXV3xq5fOAQ"],
    "MAT120": ["BQACAgQAAxkBAAIL0Wl-ECGAbAkm5fcbYxKLUQWTmAABBwACFBsAAvJx8VO5FMY6jCWnFzgE"],
    "MAT202": [
        "BQACAgQAAxkBAAIL0ml-ECF-irXDHPkbWBXHC8KIb-WnAAIWGwAC8nHxU58M0c9N4NY1OAQ",
        "BQACAgQAAxkBAAIL02l-ECEG1xtclFYQE9nfddmOy-iTAAIXGwAC8nHxU5KDFOw2KgrAOAQ",
    ],
    "MAT240": ["BQACAgQAAxkBAAIL1Gl-ECGkSQWzVoimStRO2izZYIsaAAIYGwAC8nHxU1w3q6vTihc5OAQ"],
    "CALCULUS 1+2+3, 14th edition": [
        "BQACAgQAAxkBAAIL1Wl-ECGdFc_Jd6jbsEF47J-lJ950AAIZGwAC8nHxU5s8Au3aPqiYOAQ",
        "BQACAgQAAxkBAAIL1ml-ECHDd_INapp0zO-nyGOJxgltAAIbGwAC8nHxU6ngDlvpZT7LOAQ",
    ],
    "CALCULUS 1+2+3, 15th edition": [
        "BQACAgQAAxkBAAIL12l-ECGz_nLCgUr0F48_s5H3D0h0AAIcGwAC8nHxU5DyCjnsOA1-OAQ"
    ],

    "CHEMISTRY": ["BQACAgQAAxkBAAIMKWl-FSTI_dUM8mdsOuzXqvtE6mjVAAInGwAC8nHxU3X8S6YnxBvtOAQ"],
    "BIOLOGY": ["BQACAgQAAxkBAAIMJWl-FRvYNe_GWcR8xfQdSERQlH8jAAImGwAC8nHxU7fqnRfcBL-JOAQ"],
    "PHYSICS 1+2": [
        "BQACAgQAAxkBAAIMLWl-FS4D6E8WOw4ye7VsWm-qwt6xAAIoGwAC8nHxU5UX0CLUbH48OAQ",
        "BQACAgQAAxkBAAIMMWl-FUB--sIR3Kbp21uT4JkvZsKIAAIpGwAC8nHxU-ExZbt3dQsfOAQ",
    ],

    "Sustainable Energy": ["BQACAgQAAxkBAAIMNml-FVAYIXNs2KPC9RyyeIYurThDAAIqGwAC8nHxU5AOCer6Uom2OAQ"],
    "Numerical Methods": ["BQACAgQAAxkBAAIMOml-FXN2tvwsnyz2Kki8Lz_4aZzmAAIrGwAC8nHxU-2B7iedfCcLOAQ"],
    "Statistics and Probability": ["BQACAgQAAxkBAAIMPml-FYWsXRClTnrowVJWTd6T1rGmAAIsGwAC8nHxU0RW_VA4ghQtOAQ"],
    "STATICS AND ENGINEERING": ["BQACAgQAAxkBAAIMQml-FZjPOxYp9ZmOOyCeaNZjQ6B0AAItGwAC8nHxUw2FATSwcdEyOAQ"],
    "Power Electronics": ["BQACAgQAAxkBAAIMRml-FaVOtMx3sENUGqGq5yVXAu9xAAIuGwAC8nHxU00l9Cv3g8z-OAQ"],
    "Thermodynamics": [
        "BQACAgQAAxkBAAIMSml-FbLrrmYkgzQnziGSNi9W_dgrAAIvGwAC8nHxUwpE1g0nEDKWOAQ",
        "BQACAgQAAxkBAAIMTml-FbkUe9Fjhce70kH6fhTOV0RDAAIwGwAC8nHxU1BgiE_TMfeBOAQ",
    ],

    "Digital Logic": ["BQACAgQAAxkBAAIMUml-FcOEj8C3sprkk8wr4HUwy7dLAAIxGwAC8nHxU8K0a9dzrH-mOAQ"],
    "JAVA": ["BQACAgQAAxkBAAIMWml-FeEMdZcvxOrd_PyfhFaxmBu5AAIzGwAC8nHxU-kZyqo6BeDNOAQ"],
    "C++": ["BQACAgQAAxkBAAIMVml-FdX5yUdk6QK3xlmgmYXrlL94AAIyGwAC8nHxUxgG1qHRu715OAQ"],

    "International Economics": ["BQACAgQAAxkBAAIMXml-FevL7ZdBcXOeIIy8zQlYZGozAAI0GwAC8nHxU7X3vLUkvyKcOAQ"],

    "INF": ["BQACAgQAAxkBAAIMYml-FfV_XIgV2ywjRO5J12Vb6NuQAAI1GwAC8nHxU8QtFQABNpq81jgE"],
    "ETHICS": ["BQACAgQAAxkBAAIMZml-Ff7ymjnq3qdBttRPIvXqLXfoAAI2GwAC8nHxU3d75xq1hwvuOAQ"],
}

BACK_TO_MAIN = "⬅️ رجوع للقائمة الرئيسية"
MAIN_MENU_TEXT = "القائمة الرئيسية"

# ========================
# 2) دوال المساعدة
# ========================

def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        MAIN_MENU_BUTTONS,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

def section_keyboard(section: str):
    buttons = [[name] for name in SECTION_BOOKS.get(section, [])]
    buttons.append([BACK_TO_MAIN])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=False)

# ========================
# 3) الأوامر الأساسية
# ========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "مرحباً بك في مكتبة AASU للكتب الدراسية.\n\n"
        "اختر القسم المطلوب من الأزرار في الأسفل."
    )
    await update.message.reply_text(text, reply_markup=main_menu_keyboard())

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()

    # رجوع للقائمة الرئيسية
    if text in [BACK_TO_MAIN, MAIN_MENU_TEXT, "/menu"]:
        await update.message.reply_text("اختر القسم:", reply_markup=main_menu_keyboard())
        return

    # اختيار قسم
    if text in SECTION_BOOKS:
        await update.message.reply_text(
            f"الكتب المتاحة في قسم {text}:\nاختر الكتاب من الأزرار.",
            reply_markup=section_keyboard(text),
        )
        return

    # اختيار كتاب
    if text in BOOK_FILES:
        files = BOOK_FILES[text]
        for fid in files:
            try:
                await update.message.reply_document(
                    document=fid,
                    caption=text,
                    reply_markup=section_keyboard(
                        next(section for section, books in SECTION_BOOKS.items() if text in books)
                    ),
                )
            except Exception as e:
                # رسالة خطأ للمستخدم
                await update.message.reply_text(
                    "حدث خطأ أثناء إرسال الملف.\n"
                    "إذا تكرر الخطأ، راسل مشرف البوت.",
                    reply_markup=section_keyboard(
                        next(section for section, books in SECTION_BOOKS.items() if text in books)
                    ),
                )
                # تسجيل الخطأ في اللوج لنعرف السبب الحقيقي
                print(f"Error sending {text} with file_id {fid}: {e}")
        return

    # أي نص آخر
    await update.message.reply_text(
        "اختر من الأزرار في الأسفل، أو اكتب /start لعرض القائمة.",
        reply_markup=main_menu_keyboard(),
    )

# ========================
# 4) استخراج file_id لأي ملف (أداة لك فقط)
# ========================

async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    أي ملف PDF ترسله للبوت سيرد عليك بالـ file_id الخاص بـ «هذا البوت».
    استخدم هذه القيم لتحديث BOOK_FILES ثم أعد نشر الكود.
    """
    if not update.message.document:
        return
    doc = update.message.document
    await update.message.reply_text(
        f"file_id لهذا الملف:\n\n{doc.file_id}"
    )
    print(f"Got file_id from user {update.effective_user.id}: {doc.file_id}")

# ========================
# 5) تشغيل البوت
# ========================

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN env var is not set")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", start))

    # استقبال أي نص للتعامل مع القوائم
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # استقبال أي مستند PDF لإرجاع file_id (أداة مساعدة)
    app.add_handler(MessageHandler(filters.Document.ALL, get_file_id))

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
