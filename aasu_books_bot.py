from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes


# ضع توكن البوت الذي أخذته من BotFather هنا:
import os
TOKEN = os.environ.get("BOT_TOKEN")


BOOKS = {
    "english": {
        "title": "ENGLISH",
        "items": {
            "iep098": {
                "title": "IEP098",
                "files": [
                    "BQACAgQAAxkBAAIL3Gl-EzrZzs2g07czYxViZnFQUmuMAAIdGwAC8nHxUxzXjXFnArCtOAQ",
                    "BQACAgQAAxkBAAIL3Wl-EzoDyNzQ5XjTE_FRGbrVuotoAAIeGwAC8nHxU3nuGyUha9KHOAQ",
                ],
            },
            "iep099": {
                "title": "IEP099",
                "files": [
                    "BQACAgQAAxkBAAIMEWl-FNLQ7CV-qOpJ6NL-r412lwmHAAIhGwAC8nHxU4rMrWQVI3_Uoaq",
                    "BQACAgQAAxkBAAIMFWl-FNw65ZKvj2cUhl4nVWQn80d9AAIiGwAC8nHxU_XTBdumCrE1OAQ",
                ],
            },
            "enl101": {
                "title": "ENL101",
                "files": [
                    "BQACAgQAAxkBAAIMGWl-FOUnbh4wOGsNbtLngKoYyPtuAAIjGwAC8nHxU0Y7oQvq1Z2NOAQ",
                ],
            },
            "enl102": {
                "title": "ENL102",
                "files": [
                    "BQACAgQAAxkBAAIMHWl-FQXlddgKlr3P5iYirVVA9rNrAAIkGwAC8nHxU2BsDB5e1iDjOAQ",
                ],
            },
            "enl201": {
                "title": "ENL201",
                "files": [
                    "BQACAgQAAxkBAAIMIWl-FQ_weESJKCt12xhL4jhS_qGWAAIlGwAC8nHxU1b2DjPqD5tVOAQ",
                ],
            },
        },
    },

    "math": {
        "title": "MATHMATICS",
        "items": {
            "imp098": {
                "title": "IMP098",
                "files": [
                    "BQACAgQAAxkBAAILz2l-ECGbiXh0jlcNWQAB4rH6wVDivgACERsAAvJx8VOGbCjs9abLrjgE",
                ],
            },
            "imp099": {
                "title": "IMP099",
                "files": [
                    "BQACAgQAAxkBAAIL0Gl-ECHaJnh4p1bVl_2xEYmrvF5zAAITGwAC8nHxUws9ZXV3xq5fOAQ",
                ],
            },
            "mat120": {
                "title": "MAT120",
                "files": [
                    "BQACAgQAAxkBAAIL0Wl-ECGAbAkm5fcbYxKLUQWTmAABBwACFBsAAvJx8VO5FMY6jCWnFzgE",
                ],
            },
            "mat202": {
                "title": "MAT202",
                "files": [
                    "BQACAgQAAxkBAAIL0ml-ECF-irXDHPkbWBXHC8KIb-WnAAIWGwAC8nHxU58M0c9N4NY1OAQ",
                    "BQACAgQAAxkBAAIL02l-ECEG1xtclFYQE9nfddmOy-iTAAIXGwAC8nHxU5KDFOw2KgrAOAQ",
                ],
            },
            "mat240": {
                "title": "MAT240",
                "files": [
                    "BQACAgQAAxkBAAIL1Gl-ECGkSQWzVoimStRO2izZYIsaAAIYGwAC8nHxU1w3q6vTihc5OAQ",
                ],
            },
            "calc14": {
                "title": "CALCULUS 1+2+3, 14th edition",
                "files": [
                    "BQACAgQAAxkBAAIL1Wl-ECGdFc_Jd6jbsEF47J-lJ950AAIZGwAC8nHxU5s8Au3aPqiYOAQ",
                    "BQACAgQAAxkBAAIL1ml-ECHDd_INapp0zO-nyGOJxgltAAIbGwAC8nHxU6ngDlvpZT7LOAQ",
                ],
            },
            "calc15": {
                "title": "CALCULUS 1+2+3, 15th edition",
                "files": [
                    "BQACAgQAAxkBAAIL12l-ECGz_nLCgUr0F48_s5H3D0h0AAIcGwAC8nHxU5DyCjnsOA1-OAQ",
                ],
            },
        },
    },

    "science": {
        "title": "SCIENCE",
        "items": {
            "chemistry": {
                "title": "CHEMISTRY",
                "files": [
                    "BQACAgQAAxkBAAIMKWl-FSTI_dUM8mdsOuzXqvtE6mjVAAInGwAC8nHxU3X8S6YnxBvtOAQ",
                ],
            },
            "biology": {
                "title": "BIOLOGY",
                "files": [
                    "BQACAgQAAxkBAAIMJWl-FRvYNe_GWcR8xfQdSERQlH8jAAImGwAC8nHxU7fqnRfcBL-JOAQ",
                ],
            },
            "physics": {
                "title": "PHYSICS 1+2",
                "files": [
                    "BQACAgQAAxkBAAIMLWl-FS4D6E8WOw4ye7VsWm-qwt6xAAIoGwAC8nHxU5UX0CLUbH48OAQ",
                    "BQACAgQAAxkBAAIMMWl-FUB--sIR3Kbp21uT4JkvZsKIAAIpGwAC8nHxU-ExZbt3dQsfOAQ",
                ],
            },
        },
    },

    "engineering": {
        "title": "ENGINEERING",
        "items": {
            "sustainable_energy": {
                "title": "Sustainable Energy",
                "files": [
                    "BQACAgQAAxkBAAIMNml-FVAYIXNs2KPC9RyyeIYurThDAAIqGwAC8nHxU5AOCer6Uom2OAQ",
                ],
            },
            "numerical_methods": {
                "title": "Numerical Methods",
                "files": [
                    "BQACAgQAAxkBAAIMOml-FXN2tvwsnyz2Kki8Lz_4aZzmAAIrGwAC8nHxU-2B7iedfCcLOAQ",
                ],
            },
            "statistics_probability": {
                "title": "Statistics and Probability",
                "files": [
                    "BQACAgQAAxkBAAIMPml-FYWsXRClTnrowVJWTd6T1rGmAAIsGwAC8nHxU0RW_VA4ghQtOAQ",
                ],
            },
            "statics_engineering": {
                "title": "STATICS AND ENGINEERING",
                "files": [
                    "BQACAgQAAxkBAAIMQml-FZjPOxYp9ZmOOyCeaNZjQ6B0AAItGwAC8nHxUw2FATSwcdEyOAQ",
                ],
            },
            "power_electronics": {
                "title": "Power Electronics",
                "files": [
                    "BQACAgQAAxkBAAIMRml-FaVOtMx3sENUGqGq5yVXAu9xAAIuGwAC8nHxU00l9Cv3g8z-OAQ",
                ],
            },
            "thermodynamics": {
                "title": "Thermodynamics",
                "files": [
                    "BQACAgQAAxkBAAIMSml-FbLrrmYkgzQnziGSNi9W_dgrAAIvGwAC8nHxUwpE1g0nEDKWOAQ",
                    "BQACAgQAAxkBAAIMTml-FbkUe9Fjhce70kH6fhTOV0RDAAIwGwAC8nHxU1BgiE_TMfeBOAQ",
                ],
            },
        },
    },

    "computing": {
        "title": "COMPUTING",
        "items": {
            "digital_logic": {
                "title": "Digital Logic",
                "files": [
                    "BQACAgQAAxkBAAIMUml-FcOEj8C3sprkk8wr4HUwy7dLAAIxGwAC8nHxU8K0a9dzrH-mOAQ",
                ],
            },
            "java": {
                "title": "JAVA",
                "files": [
                    "BQACAgQAAxkBAAIMWml-FeEMdZcvxOrd_PyfhFaxmBu5AAIzGwAC8nHxU-kZyqo6BeDNOAQ",
                ],
            },
            "cpp": {
                "title": "C++",
                "files": [
                    "BQACAgQAAxkBAAIMVml-FdX5yUdk6QK3xlmgmYXrlL94AAIyGwAC8nHxUxgG1qHRu715OAQ",
                ],
            },
        },
    },

    "business": {
        "title": "BUSINESS",
        "items": {
            "international_economics": {
                "title": "International Economics",
                "files": [
                    "BQACAgQAAxkBAAIMXml-FevL7ZdBcXOeIIy8zQlYZGozAAI0GwAC8nHxU7X3vLUkvyKcOAQ",
                ],
            },
        },
    },

    "general": {
        "title": "GENERAL",
        "items": {
            "inf": {
                "title": "INF",
                "files": [
                    "BQACAgQAAxkBAAIMYml-FfV_XIgV2ywjRO5J12Vb6NuQAAI1GwAC8nHxU8QtFQABNpq81jgE",
                ],
            },
            "ethics": {
                "title": "ETHICS",
                "files": [
                    "BQACAgQAAxkBAAIMZml-Ff7ymjnq3qdBttRPIvXqLXfoAAI2GwAC8nHxU3d75xq1hwvuOAQ",
                ],
            },
        },
    },
}


def build_main_menu() -> InlineKeyboardMarkup:
    rows = []
    for cat_key, cat_data in BOOKS.items():
        rows.append([
            InlineKeyboardButton(cat_data["title"], callback_data=f"cat:{cat_key}")
        ])
    return InlineKeyboardMarkup(rows)


def build_category_menu(cat_key: str) -> InlineKeyboardMarkup:
    items = BOOKS[cat_key]["items"]
    rows = []
    for book_key, book_data in items.items():
        rows.append([
            InlineKeyboardButton(book_data["title"], callback_data=f"book:{cat_key}:{book_key}")
        ])
    rows.append([
        InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data="back:main")
    ])
    return InlineKeyboardMarkup(rows)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📚 أهلاً بك في AASU BOOKS BOT (غير رسمي)\n\n"
        "اختر القسم من القائمة:"
    )
    await update.message.reply_text(text, reply_markup=build_main_menu())


async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back:main":
        await query.edit_message_text(
            "📚 اختر القسم:",
            reply_markup=build_main_menu()
        )
        return

    if data.startswith("cat:"):
        _, cat_key = data.split(":", 1)
        await query.edit_message_text(
            f"{BOOKS[cat_key]['title']}\n\nاختر الكتاب:",
            reply_markup=build_category_menu(cat_key)
        )
        return

    if data.startswith("book:"):
        _, cat_key, book_key = data.split(":")
        book = BOOKS[cat_key]["items"][book_key]
        title = book["title"]
        file_ids = book["files"]

        first = True
        for fid in file_ids:
            caption = f"📖 {title}" if first else None
            await query.message.reply_document(document=fid, caption=caption)
            first = False

        return


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_button))

    app.run_polling()


if __name__ == "__main__":
    main()
