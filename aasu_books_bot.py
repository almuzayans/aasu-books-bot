import os
import logging
from typing import Dict, List

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

# =========================
# إعداد اللوجينغ
# =========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# =========================
# متغيّر التوكن من بيئة التشغيل
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")


# =========================
# القوائم والأزرار
# =========================

MAIN_MENU_BUTTONS = [
    ["ENGLISH 📘"],
    ["MATHEMATICS 📕"],
    ["SCIENCE 📙"],
    ["ENGINEERING 📗"],
    ["COMPUTING 💻"],
    ["BUSINESS 💼"],
    ["GENERAL 📚"],
]

REQUEST_BUTTON = "طلب كتاب غير موجود 📩"
BACK_BUTTON = "القائمة الرئيسية ⬅️"

CATEGORY_KEY_BY_BUTTON: Dict[str, str] = {
    "ENGLISH 📘": "ENGLISH",
    "MATHEMATICS 📕": "MATHEMATICS",
    "SCIENCE 📙": "SCIENCE",
    "ENGINEERING 📗": "ENGINEERING",
    "COMPUTING 💻": "COMPUTING",
    "BUSINESS 💼": "BUSINESS",
    "GENERAL 📚": "GENERAL",
}

BOOK_MENU_BUTTONS: Dict[str, List[List[str]]] = {
    "ENGLISH": [
        ["IEP098"],
        ["IEP099"],
        ["ENL101"],
        ["ENL102"],
        ["ENL201"],
        [BACK_BUTTON],
    ],
    "MATHEMATICS": [
        ["IMP098"],
        ["IMP099"],
        ["MAT120"],
        ["MAT202"],
        ["MAT240"],
        ["CALCULUS 1+2+3, 14th edition"],
        ["CALCULUS 1+2+3, 15th edition"],
        [BACK_BUTTON],
    ],
    "SCIENCE": [
        ["CHEMISTRY"],
        ["BIOLOGY"],
        ["PHYSICS 1+2"],
        [BACK_BUTTON],
    ],
    "ENGINEERING": [
        ["Sustainable Energy"],
        ["Numerical Methods"],
        ["Statistics and Probability"],
        ["STATICS AND ENGINEERING"],
        ["Power Electronics"],
        ["Thermodynamics"],
        [BACK_BUTTON],
    ],
    "COMPUTING": [
        ["Digital Logic"],
        ["JAVA"],
        ["C++"],
        [BACK_BUTTON],
    ],
    "BUSINESS": [
        ["International Economics"],
        [BACK_BUTTON],
    ],
    "GENERAL": [
        ["INF"],
        ["ETHICS"],
        [BACK_BUTTON],
    ],
}

# =========================
# ملفّات الكتب (FILE_IDs)
# =========================

BOOK_FILES: Dict[str, List[str]] = {
    # ---------- ENGLISH ----------
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

    # ---------- MATHEMATICS ----------
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

    # ---------- SCIENCE ----------
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

    # ---------- ENGINEERING ----------
    "Sustainable Energy": [
        "BQACAgQAAxkBAAIMNml-FVAYIXNs2KPC9RyyeIYurThDAAIqGwAC8nHxU5AOCer6Uom2OAQ",
    ],
    "Numerical Methods": [
        "BQACAgQAAxkBAAIMOml-FXN2tvwsnyz2Kki8Lz_4aZzmAAIrGwAC8nHxU-2B7iedfCcLOAQ",
    ],
    "Statistics and Probability": [
        "BQACAgQAAxkBAAIMPml-FYWsXRClTnrowVJWTd6T1rGmAAIsGwAC8nHxU0RW_VA4ghQtOAQ",
    ],
    "STATICS AND ENGINEERING": [
        "BQACAgQAAxkBAAIMQml-FZjPOxYp9ZmOOyCeaNZjQ6B0AAItGwAC8nHxUw2FATSwcdEyOAQ",
    ],
    "Power Electronics": [
        "BQACAgQAAxkBAAIMRml-FaVOtMx3sENUGqGq5yVXAu9xAAIuGwAC8nHxU00l9Cv3g8z-OAQ",
    ],
    "Thermodynamics": [
        "BQACAgQAAxkBAAIMSml-FbLrrmYkgzQnziGSNi9W_dgrAAIvGwAC8nHxUwpE1g0nEDKWOAQ",
        "BQACAgQAAxkBAAIMTml-FbkUe9Fjhce70kH6fhTOV0RDAAIwGwAC8nHxU1BgiE_TMfeBOAQ",
    ],

    # ---------- COMPUTING ----------
    "Digital Logic": [
        "BQACAgQAAxkBAAIMUml-FcOEj8C3sprkk8wr4HUwy7dLAAIxGwAC8nHxU8K0a9dzrH-mOAQ",
    ],
    "JAVA": [
        "BQACAgQAAxkBAAIMWml-FeEMdZcvxOrd_PyfhFaxmBu5AAIzGwAC8nHxU-kZyqo6BeDNOAQ",
    ],
    "C++": [
        "BQACAgQAAxkBAAIMVml-FdX5yUdk6QK3xlmgmYXrlL94AAIyGwAC8nHxUxgG1qHRu715OAQ",
    ],

    # ---------- BUSINESS ----------
    "International Economics": [
        "BQACAgQAAxkBAAIMXml-FevL7ZdBcXOeIIy8zQlYZGozAAI0GwAC8nHxU7X3vLUkvyKcOAQ",
    ],

    # ---------- GENERAL ----------
    "INF": [
        "BQACAgQAAxkBAAIMYml-FfV_XIgV2ywjRO5J12Vb6NuQAAI1GwAC8nHxU8QtFQABNpq81jgE",
    ],
    "ETHICS": [
        "BQACAgQAAxkBAAIMZml-Ff7ymjnq3qdBttRPIvXqLXfoAAI2GwAC8nHxU3d75xq1hwvuOAQ",
    ],
}


# =========================
# دوال إرسال القوائم
# =========================

def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        MAIN_MENU_BUTTONS + [[REQUEST_BUTTON]],
        resize_keyboard=True,
    )


def category_keyboard(category_key: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        BOOK_MENU_BUTTONS[category_key] + [[REQUEST_BUTTON]],
        resize_keyboard=True,
    )


# =========================
# Handlers
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.clear()
    context.user_data["mode"] = "CATEGORY"

    text = (
        "مرحبًا بك في بوت الكتب غير الرسمي لجامعة عبدالله السالم (AASU Books).\n\n"
        "طريقة الاستخدام:\n"
        "1️⃣ اختر القسم من الأزرار بالأسفل.\n"
        "2️⃣ اختر اسم الكتاب المطلوب.\n"
        "3️⃣ سيصلك الكتاب مباشرة كملف PDF.\n\n"
        "إذا لم تجد كتابك، اضغط الزر «طلب كتاب غير موجود 📩» في الأسفل.\n"
    )

    await update.message.reply_text(
        text,
        reply_markup=main_menu_keyboard(),
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None or update.message.text is None:
        return

    text = update.message.text.strip()

    # زر الرجوع للقائمة الرئيسية
    if text == BACK_BUTTON:
        context.user_data["mode"] = "CATEGORY"
        context.user_data.pop("category", None)
        await update.message.reply_text(
            "اختر القسم:",
            reply_markup=main_menu_keyboard(),
        )
        return

    # زر طلب كتاب غير موجود
    if text == REQUEST_BUTTON:
        await update.message.reply_text(
            "إذا لم تجد كتابك:\n"
            "1️⃣ اكتب اسم المقرر + الكود (إن وُجد).\n"
            "2️⃣ اكتب اسم الكتاب والإصدار (Edition).\n"
            "3️⃣ أرسل الطلب في رسالة واحدة هنا أو تواصل معنا على إنستغرام:\n"
            "@BOOKADVISORS\n\n"
            "سنحاول إضافته في أسرع وقت ممكن.",
            reply_markup=main_menu_keyboard()
        )
        return

    mode = context.user_data.get("mode", "CATEGORY")

    # اختيار قسم من القائمة الرئيسية
    if text in CATEGORY_KEY_BY_BUTTON:
        category_key = CATEGORY_KEY_BY_BUTTON[text]
        context.user_data["mode"] = "BOOK"
        context.user_data["category"] = category_key

        await update.message.reply_text(
            "اختر الكتاب من القسم:",
            reply_markup=category_keyboard(category_key),
        )
        return

    # اختيار كتاب من داخل قسم
    if mode == "BOOK":
        category_key = context.user_data.get("category")

        if category_key and text in BOOK_FILES:
            await update.message.reply_text(f"📚 جاري إرسال: {text}")

            files = BOOK_FILES[text]
            for file_id in files:
                try:
                    # هنا كان الخطأ: يجب استخدام context.bot وليس update.message.bot
                    await context.bot.send_document(
                        chat_id=update.effective_chat.id,
                        document=file_id,
                        caption=text,
                    )
                except Exception as e:
                    logger.error("Telegram error while sending %s: %s", text, e)
                    await update.message.reply_text(
                        "حدث خطأ أثناء إرسال الملف.\n"
                        "رسالة النظام من تيليجرام:\n"
                        f"{e}\n\n"
                        "إذا تكرر الخطأ، راسلنا على إنستغرام:\n"
                        "@BOOKADVISORS"
                    )
                    break
            return

    # أي شيء آخر
    await update.message.reply_text(
        "استخدم الأزرار في الأسفل لاختيار القسم أو الكتاب.\n"
        "للعودة اضغط «القائمة الرئيسية ⬅️».",
        reply_markup=main_menu_keyboard(),
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling an update: %s", context.error)


# =========================
# main()
# =========================

def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("متغيّر البيئة BOT_TOKEN غير موجود.")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
    )

    application.add_error_handler(error_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
