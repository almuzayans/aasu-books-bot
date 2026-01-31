import os
from typing import Dict, List

from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# =========================
# إعداد التوكن من Environment
# =========================
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set")

# =========================
# بيانات الكتب
# =========================

# الهيكل:
# BOOKS[category][code] = {"title": "نص يظهر للمستخدم", "files": [file_id1, file_id2, ...]}
BOOKS: Dict[str, Dict[str, Dict[str, List[str]]]] = {
    "ENGLISH": {
        "IEP098": {
            "title": "IEP098 (R&W + L&S)",
            "files": [
                "BQACAgQAAxkBAAIL3Gl-EzrZzs2g07czYxViZnFQUmuMAAIdGwAC8nHxUxzXjXFnArCtOAQ",
                "BQACAgQAAxkBAAIL3Wl-EzoDyNzQ5XjTE_FRGbrVuotoAAIeGwAC8nHxU3nuGyUha9KHOAQ",
            ],
        },
        "IEP099": {
            "title": "IEP099 (R&W + L&S)",
            "files": [
                "BQACAgQAAxkBAAIMEWl-FNLQ7CV-qOpJ6NL-r412lwmHAAIhGwAC8nHxU4rMrWQVI3_Uoaq",
                "BQACAgQAAxkBAAIMFWl-FNw65ZKvj2cUhl4nVWQn80d9AAIiGwAC8nHxU_XTBdumCrE1OAQ",
            ],
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
    "MATHEMATICS": {
        "IMP098": {
            "title": "IMP098 – Intermediate Algebra",
            "files": [
                "BQACAgQAAxkBAAILz2l-ECGbiXh0jlcNWQAB4rH6wVDivgACERsAAvJx8VOGbCjs9abLrjgE"
            ],
        },
        "IMP099": {
            "title": "IMP099 – Precalculus",
            "files": [
                "BQACAgQAAxkBAAIL0Gl-ECHaJnh4p1bVl_2xEYmrvF5zAAITGwAC8nHxUws9ZXV3xq5fOAQ"
            ],
        },
        "MAT120": {
            "title": "MAT120 – Discrete Mathematics",
            "files": [
                "BQACAgQAAxkBAAIL0Wl-ECGAbAkm5fcbYxKLUQWTmAABBwACFBsAAvJx8VO5FMY6jCWnFzgE"
            ],
        },
        "MAT202": {
            "title": "MAT202 – Linear Algebra (+ Solutions)",
            "files": [
                "BQACAgQAAxkBAAIL0ml-ECF-irXDHPkbWBXHC8KIb-WnAAIWGwAC8nHxU58M0c9N4NY1OAQ",
                "BQACAgQAAxkBAAIL02l-ECEG1xtclFYQE9nfddmOy-iTAAIXGwAC8nHxU5KDFOw2KgrAOAQ",
            ],
        },
        "MAT240": {
            "title": "MAT240 – Differential Equations",
            "files": [
                "BQACAgQAAxkBAAIL1Gl-ECGkSQWzVoimStRO2izZYIsaAAIYGwAC8nHxU1w3q6vTihc5OAQ"
            ],
        },
        "CALC14": {
            "title": "Calculus 1+2+3 – 14th Ed (+ Solutions)",
            "files": [
                "BQACAgQAAxkBAAIL1Wl-ECGdFc_Jd6jbsEF47J-lJ950AAIZGwAC8nHxU5s8Au3aPqiYOAQ",
                "BQACAgQAAxkBAAIL1ml-ECHDd_INapp0zO-nyGOJxgltAAIbGwAC8nHxU6ngDlvpZT7LOAQ",
            ],
        },
        "CALC15": {
            "title": "Calculus 1+2+3 – 15th Ed",
            "files": [
                "BQACAgQAAxkBAAIL12l-ECGz_nLCgUr0F48_s5H3D0h0AAIcGwAC8nHxU5DyCjnsOA1-OAQ"
            ],
        },
    },
    "SCIENCE": {
        "CHEM": {
            "title": "Chemistry",
            "files": [
                "BQACAgQAAxkBAAIMKWl-FSTI_dUM8mdsOuzXqvtE6mjVAAInGwAC8nHxU3X8S6YnxBvtOAQ"
            ],
        },
        "BIO": {
            "title": "Biology",
            "files": [
                "BQACAgQAAxkBAAIMJWl-FRvYNe_GWcR8xfQdSERQlH8jAAImGwAC8nHxU7fqnRfcBL-JOAQ"
            ],
        },
        "PHYS": {
            "title": "Physics 1+2 (+ Solutions)",
            "files": [
                "BQACAgQAAxkBAAIMLWl-FS4D6E8WOw4ye7VsWm-qwt6xAAIoGwAC8nHxU5UX0CLUbH48OAQ",
                "BQACAgQAAxkBAAIMMWl-FUB--sIR3Kbp21uT4JkvZsKIAAIpGwAC8nHxU-ExZbt3dQsfOAQ",
            ],
        },
    },
    "ENGINEERING": {
        "SUST": {
            "title": "Introduction to Energy & Sustainability",
            "files": [
                "BQACAgQAAxkBAAIMNml-FVAYIXNs2KPC9RyyeIYurThDAAIqGwAC8nHxU5AOCer6Uom2OAQ"
            ],
        },
        "NUM": {
            "title": "Numerical Methods",
            "files": [
                "BQACAgQAAxkBAAIMOml-FXN2tvwsnyz2Kki8Lz_4aZzmAAIrGwAC8nHxU-2B7iedfCcLOAQ"
            ],
        },
        "STATPROB": {
            "title": "Engineering Probability & Statistics",
            "files": [
                "BQACAgQAAxkBAAIMPml-FYWsXRClTnrowVJWTd6T1rGmAAIsGwAC8nHxU0RW_VA4ghQtOAQ"
            ],
        },
        "STATICS": {
            "title": "Statics and Strength of Materials",
            "files": [
                "BQACAgQAAxkBAAIMQml-FZjPOxYp9ZmOOyCeaNZjQ6B0AAItGwAC8nHxUw2FATSwcdEyOAQ"
            ],
        },
        "POWER": {
            "title": "Industrial / Power Electronics",
            "files": [
                "BQACAgQAAxkBAAIMRml-FaVOtMx3sENUGqGq5yVXAu9xAAIuGwAC8nHxU00l9Cv3g8z-OAQ"
            ],
        },
        "THERMO": {
            "title": "Thermodynamics (+ Solutions)",
            "files": [
                "BQACAgQAAxkBAAIMSml-FbLrrmYkgzQnziGSNi9W_dgrAAIvGwAC8nHxUwpE1g0nEDKWOAQ",
                "BQACAgQAAxkBAAIMTml-FbkUe9Fjhce70kH6fhTOV0RDAAIwGwAC8nHxU1BgiE_TMfeBOAQ",
            ],
        },
    },
    "COMPUTING": {
        "DIGITAL": {
            "title": "Digital Logic",
            "files": [
                "BQACAgQAAxkBAAIMUml-FcOEj8C3sprkk8wr4HUwy7dLAAIxGwAC8nHxU8K0a9dzrH-mOAQ"
            ],
        },
        "JAVA": {
            "title": "Java (CCS220)",
            "files": [
                "BQACAgQAAxkBAAIMWml-FeEMdZcvxOrd_PyfhFaxmBu5AAIzGwAC8nHxU-kZyqo6BeDNOAQ"
            ],
        },
        "CPP": {
            "title": "C++ (CCS120)",
            "files": [
                "BQACAgQAAxkBAAIMVml-FdX5yUdk6QK3xlmgmYXrlL94AAIyGwAC8nHxUxgG1qHRu715OAQ"
            ],
        },
    },
    "BUSINESS": {
        "INT_ECON": {
            "title": "Global Economic & Trade (International Economics)",
            "files": [
                "BQACAgQAAxkBAAIMXml-FevL7ZdBcXOeIIy8zQlYZGozAAI0GwAC8nHxU7X3vLUkvyKcOAQ"
            ],
        },
    },
    "GENERAL": {
        "INF": {
            "title": "INF – Information Technology",
            "files": [
                "BQACAgQAAxkBAAIMYml-FfV_XIgV2ywjRO5J12Vb6NuQAAI1GwAC8nHxU8QtFQABNpq81jgE"
            ],
        },
        "ETHICS": {
            "title": "Ethics",
            "files": [
                "BQACAgQAAxkBAAIMZml-Ff7ymjnq3qdBttRPIvXqLXfoAAI2GwAC8nHxU3d75xq1hwvuOAQ"
            ],
        },
    },
}

# عناوين القوائم الرئيسية (للعرض)
CATEGORY_TITLES = {
    "ENGLISH": "ENGLISH 📘",
    "MATHEMATICS": "MATHEMATICS 📕",
    "SCIENCE": "SCIENCE 📙",
    "ENGINEERING": "ENGINEERING 📗",
    "COMPUTING": "COMPUTING 💻",
    "BUSINESS": "BUSINESS 💼",
    "GENERAL": "GENERAL 📚",
}

# =========================
# بناء القوائم
# =========================


def build_main_menu() -> InlineKeyboardMarkup:
    buttons = []
    for cat_key in [
        "ENGLISH",
        "MATHEMATICS",
        "SCIENCE",
        "ENGINEERING",
        "COMPUTING",
        "BUSINESS",
        "GENERAL",
    ]:
        buttons.append(
            [InlineKeyboardButton(CATEGORY_TITLES[cat_key], callback_data=f"CAT:{cat_key}")]
        )
    return InlineKeyboardMarkup(buttons)


def build_category_menu(category: str) -> InlineKeyboardMarkup:
    books = BOOKS.get(category, {})
    buttons: List[List[InlineKeyboardButton]] = []

    for code, meta in books.items():
        title = meta["title"]
        buttons.append(
            [
                InlineKeyboardButton(
                    text=title, callback_data=f"BOOK:{category}:{code}"
                )
            ]
        )

    # زر رجوع
    buttons.append(
        [InlineKeyboardButton("⬅ Back to Main Menu", callback_data="MAIN")]
    )
    return InlineKeyboardMarkup(buttons)


# =========================
# Handlers
# =========================


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "مرحبًا بك في AASU Books Bot 📚\n\n"
        "بوت غير رسمي لمساعدة طلاب جامعة عبدالله السالم في الوصول للكتب بسهولة.\n\n"
        "اختر القسم من القائمة التالية:"
    )
    await update.message.reply_text(text, reply_markup=build_main_menu())


async def handle_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data or ""

    # الرجوع للقائمة الرئيسية
    if data == "MAIN":
        await query.edit_message_text(
            "اختر القسم:", reply_markup=build_main_menu()
        )
        return

    # فتح قائمة قسم
    if data.startswith("CAT:"):
        _, category = data.split(":", 1)
        if category not in BOOKS:
            await query.answer("القسم غير موجود.", show_alert=True)
            return

        await query.edit_message_text(
            text=f"اختر الكتاب من قسم {CATEGORY_TITLES.get(category, category)}:",
            reply_markup=build_category_menu(category),
        )
        return

    # إرسال كتاب
    if data.startswith("BOOK:"):
        try:
            _, category, code = data.split(":", 2)
        except ValueError:
            await query.answer("طلب غير مفهوم.", show_alert=True)
            return

        category_books = BOOKS.get(category, {})
        meta = category_books.get(code)
        if not meta:
            await query.answer("الكتاب غير موجود.", show_alert=True)
            return

        chat_id = query.message.chat_id
        title = meta["title"]
        file_ids = meta["files"]

        # إرسال كل ملف في الكتاب
        for fid in file_ids:
            await context.bot.send_document(chat_id=chat_id, document=fid, caption=title)

        # إبقاء نفس القائمة بعد الإرسال
        await query.answer("تم إرسال الكتاب ✅")
        return


# =========================
# نقطة تشغيل البوت
# =========================


def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callbacks))

    application.run_polling()


if __name__ == "__main__":
    main()
