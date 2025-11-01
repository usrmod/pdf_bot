import io

from telegram import Update
from telegram.ext import ContextTypes

from bg_rem import rem_image
from image_to_pdf import single_image_to_pdf


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Util Bot here")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """Commnads list:
/start - just a hello
/help - list commands
/test - testing, might be broken
/image_to_pdf - converts single image to a pdf file"""
    )


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a test")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Access arguments via context.args
    if context.args:
        message = " ".join(context.args)
        await update.message.reply_text(f"You said: {message}")
    else:
        await update.message.reply_text("Usage: /echo <message>")


async def remove_bg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Removing background from your image...")

    try:
        picture = update.message.photo[-1]
        picture_id = await context.bot.get_file(picture.file_id)

        picture_bytes = io.BytesIO()
        await picture_id.download_to_memory(picture_bytes)

        output = rem_image(picture_bytes.getvalue())

        await context.bot.send_document(
            chat_id=update.message.chat_id,
            document=output,
            filename="no_bg.png",
            caption="Completed!",
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def img_to_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("converting your single image to a pdf")

    try:
        picture = update.message.photo[-1]
        picture_id = await context.bot.get_file(picture.file_id)

        picture_bytes = io.BytesIO()
        await picture_id.download_to_memory(picture_bytes)

        pdf_output = single_image_to_pdf(picture_bytes.getvalue())

        await update.message.reply_document(
            document=pdf_output, filename="from_image.pdf", caption="Here is your pdf"
        )
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
