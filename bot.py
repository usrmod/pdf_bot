import io

from telegram import Update
from telegram.ext import ContextTypes

from image_to_pdf import images_to_pdf  # , single_image_to_pdf


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


# For testing, later will be integrated with othre functions or features


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! my favourite freeloader!\n\nUse /start_pdf to create PDF from a single or multiple images"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """📖 Commands:

📄 PDF Creation:
/start_pdf - Begin collecting images for PDF
/finish - Create PDF from collected images
/cancel - Cancel and clear images

ℹ️ General:
/start - Welcome
/help - This message"""
    )


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is working!")


async def start_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Start collecting images for PDF creation
    """
    # Initialize empty list to store image bytes
    context.user_data["collecting_images"] = True
    context.user_data["image_bytes_list"] = []

    await update.message.reply_text(
        "📸 Send me images one by one.\n"
        "I'll keep them in the order you send them.\n\n"
        "When done, use the LAST /finish to create PDF\n"
        "Use /cancel to cancel"
    )


async def collect_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Collect photos sent by user
    """
    # Check if user is collecting images
    if not context.user_data.get("collecting_images"):
        await update.message.reply_text(
            "⚠️ Use /start_pdf first to begin collecting images"
        )
        return

    try:
        # Get photo
        photo = update.message.photo[-1]
        photo_file = await context.bot.get_file(photo.file_id)

        # Download to memory
        photo_bytes = io.BytesIO()
        await photo_file.download_to_memory(photo_bytes)

        # Store bytes in list (maintains order)
        context.user_data["image_bytes_list"].append(photo_bytes.getvalue())

        # Confirm to user
        count = len(context.user_data["image_bytes_list"])
        await update.message.reply_text(
            f"✅ Image {count} added!\nSend more or use /finish"
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def finish_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Create PDF from all collected images
    """
    # Get collected images
    image_bytes_list = context.user_data.get("image_bytes_list", [])

    if not image_bytes_list:
        await update.message.reply_text(
            "❌ No images collected!\nUse /start_pdf to begin"
        )
        return

    count = len(image_bytes_list)
    await update.message.reply_text(f"📄 Creating PDF from {count} image(s)...")

    try:
        # Create PDF from all images
        pdf_output = images_to_pdf(image_bytes_list)

        # Send PDF to user
        await update.message.reply_document(
            document=pdf_output,
            filename=f"combined_{count}_pages.pdf",
            caption=f"""
            ✅ PDF created with {count} page(s)!

Wish to make another pdf?
Use /start_pdf again""",
        )

        # Clear collected images
        context.user_data["collecting_images"] = False
        context.user_data["image_bytes_list"] = []

    except Exception as e:
        await update.message.reply_text(f"❌ Error creating PDF: {str(e)}")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Cancel image collection
    """
    # Clear stored data
    context.user_data["collecting_images"] = False
    context.user_data["image_bytes_list"] = []

    await update.message.reply_text(
        "❌ Cancelled. All images cleared.\nUse /start_pdf to begin again"
    )
