import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from PyPDF2 import PdfReader, PdfWriter
import zipfile

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    await file.download_to_drive("input.pdf")

    reader = PdfReader("input.pdf")
    files = []

    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        name = f"page_{i}.pdf"

        with open(name, "wb") as f:
            writer.write(f)

        files.append(name)

    with zipfile.ZipFile("out.zip", "w") as zipf:
        for f in files:
            zipf.write(f)

    await update.message.reply_document(open("out.zip", "rb"))

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))
app.run_polling()
