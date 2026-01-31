import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultCachedDocument,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    InlineQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

# =========================
# 📚 DATABASE
# =========================

BOOKS = {
    "SCIENCE": {
        "title": "SCIENCE 📙",
        "items": {
            "BIOLOGY": {
                "title": "BIOLOGY",
                "files": [
                    "FILE_ID_HERE",
                ],
            },
            "CHEMISTRY": {
                "title": "CHEMISTRY",
                "files": [
                    "FILE_ID_HERE",
                ],
            },
        },
    },

    "COMPUTING": {
        "title": "COMPUTING 💻",
        "items": {
            "JAVA": {
                "title": "JAVA",
                "files": [
                    "FILE_ID_HERE",
                ],
            },
            "IEP099": {
                "title": "IEP099",
                "files": [
                    "FILE_ID_HERE",  # هذا يعمل عندك
                ],
            },
        },
    },
}

# =========================
# 🟢 START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(cat["title"], callback_data=f"CAT|{key}")]
        for key, cat in BOOKS.items()
    ]

    await update.message.reply_text(
        "👋 أهلاً بك في *AASU Books Bot*\n\n"
        "📚 اختر القسم وسيصلك الكتاب مباشرة.\n\n"
        "❗ القناة غير رسمية.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# =========================
# 🟡 BUTTON HANDLER
# =========================

async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split("|")

    # --- Category ---
    if data[0] == "CAT":
        cat_key = data[1]
        cat = BOOKS.get(cat_key)

        keyboard = [
            [InlineKeyboardButton(book["title"], callback_data=f"BOOK|{cat_key}|{book_key}")]
            for book_key, book in cat["items"].items()
        ]

        keyboard.append(
            [InlineKeyboardButton("⬅️ القائمة الرئيسية", callback_data="BACK")]
        )

        await query.edit_message_text(
            f"📘 اختر الكتاب من قسم:\n*{cat['title']}*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # --- Book ---
    elif data[0] == "BOOK":
        cat_key, book_key = data[1], data[2]
        book = BOOKS[cat_key]["items"][book_key]

        await query.edit_message_text(
            f"📚 جاري إرسال: *{book['title']}*",
            parse_mode="Markdown",
        )

        for file_id in book["files"]:
            try:
                await query.message.reply_document(document=file_id)
            except Exception as e:
                await query.message.reply_text(
                    "❌ حدث خطأ أثناء إرسال الملف.\n"
                    "إذا تكرر الخطأ، راسلنا على إنستغرام:\n"
                    "@BOOKADVISORS"
                )
                print(e)

    # --- Back ---
    elif data[0] == "BACK":
        await start(update, context)

# =========================
# 🔍 INLINE MODE (حل الآيفون)
# =========================

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.lower().strip()
    if not query:
        return

    results = []

    for cat_key, cat in BOOKS.items():
        for book_key, book in cat["items"].items():
            if query in book["title"].lower():
                for i, file_id in enumerate(book["files"], start=1):
                    results.append(
                        InlineQueryResultCachedDocument(
                            id=f"{cat_key}_{book_key}_{i}",
                            title=book["title"],
                            document_file_id=file_id,
                            description="AASU Books Bot",
                        )
                    )

    await update.inline_query.answer(
        results[:50],
        cache_time=0,
        is_personal=True,
    )

# =========================
# 🚀 MAIN
# =========================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_button))
    app.add_handler(InlineQueryHandler(inline_query))

    app.run_polling()

if __name__ == "__main__":
    main()
