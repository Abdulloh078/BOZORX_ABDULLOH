import os
import django
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# Django muhitini ulash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.products.models import Product

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# SOZLAMALAR
TOKEN = "8934711690:AAHM0IG9Di6n_0N2Wew8e19uT3osOol1w38"
ADMIN_TELEGRAM_ID = 8328359338


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id == ADMIN_TELEGRAM_ID:
        await update.message.reply_text("👑 **Siz adminsiz!** Bot to'lovlarni qabul qilishga va sizga yuborishga tayyor.")
    else:
        await update.message.reply_text(
            "Salom! **Bozorix** to'lov tasdiqlash botiga xush kelibsiz.\n\n"
            "📸 Saytdan to'lovni amalga oshirgach, **chek rasmini** shu botga yuboring.\n"
            "💬 Izohiga e'loningizning **#ID** raqamini yozing (Masalan: `#7`)."
        )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    photo = update.message.photo[-1]
    caption_text = update.message.caption or ""

    # ID raqamini ajratib olish
    product_id = None
    for word in caption_text.split():
        clean_word = word.replace('#', '').strip()
        if clean_word.isdigit():
            product_id = int(clean_word)
            break

    product = None
    if product_id:
        product = Product.objects.filter(id=product_id).first()

    if not product:
        product = Product.objects.order_by('-created_at').first()

    if product:
        prod_info = (
            f"📦 **E'lon ID:** #{product.id}\n"
            f"🏷 **Nomi:** {product.title}\n"
            f"💰 **Narxi:** {product.price} so'm\n"
            f"📊 **Holati:** `{product.status}`"
        )
        p_id = product.id
    else:
        prod_info = "⚠️ Bazadan mos e'lon topilmadi!"
        p_id = 0

    # Adminga tasdiqlash tugmalari (callback_data ichiga foydalanuvchi ID sini ham joylaymiz)
    keyboard = [
        [
            InlineKeyboardButton("✅ Tasdiqlash (Saytga chiqarish)", callback_data=f"approve_{p_id}_{user.id}"),
            InlineKeyboardButton("❌ Rad etish", callback_data=f"reject_{p_id}_{user.id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    admin_message = (
        f"📩 **YANGI TO'LOV CHEKI KELDI!**\n\n"
        f"👤 **Foydalanuvchi:** @{user.username or 'Username_yoq'} ({user.full_name})\n"
        f"🆔 **Telegram ID:** `{user.id}`\n\n"
        f"{prod_info}\n\n"
        f"💬 **Izoh:** {caption_text if caption_text else 'Izoh yoq'}"
    )

    # Adminga yuborish
    try:
        await context.bot.send_photo(
            chat_id=ADMIN_TELEGRAM_ID,
            photo=photo.file_id,
            caption=admin_message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        if user.id != ADMIN_TELEGRAM_ID:
            await update.message.reply_text("✅ Chekingiz adminga yuborildi! Tekshirilib, e'loningiz tez orada saytda faollashtiriladi.")
    except Exception as e:
        logger.error(f"Adminga yuborishda xatolik: {e}")
        await update.message.reply_text("⚠️ Xatolik: Admin botni hali ishga tushirmagan. Admin botga kirib /start bosishi kerak.")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split('_')
    action = data[0]
    product_id = int(data[1])
    user_id = int(data[2]) if len(data) > 2 else None

    if product_id == 0:
        await query.message.reply_text("❌ Xatolik: E'lon ID si topilmadi!")
        return

    try:
        product = Product.objects.get(id=product_id)

        if action == 'approve':
            # Django bazasida statusni ACTIVE qilish
            try:
                product.status = Product.Status.ACTIVE
            except AttributeError:
                product.status = 'ACTIVE'
            
            product.save()

            # Admin xabarini yangilash
            await query.edit_message_caption(
                caption=query.message.caption + "\n\n✅ **HOLAT: Tasdiqlandi va e'lon SAYTGA CHIQARILDI!**",
                parse_mode="Markdown"
            )

            # Foydalanuvchiga xabar yuborish
            if user_id:
                try:
                    await context.bot.send_message(
                        chat_id=user_id,
                        text=f"🎉 **Xushxabar!** #{product.id}-sonli e'loningiz to'lovi tasdiqlandi va saytga chiqarildi!"
                    )
                except Exception as e:
                    logger.error(f"Foydalanuvchiga xabar yuborishda xatolik: {e}")

        elif action == 'reject':
            await query.edit_message_caption(
                caption=query.message.caption + "\n\n❌ **HOLAT: Admin tomonidan rad etildi.**",
                parse_mode="Markdown"
            )

            # Foydalanuvchiga rad etilgani haqida xabar
            if user_id:
                try:
                    await context.bot.send_message(
                        chat_id=user_id,
                        text=f"❌ #{product.id}-sonli e'loningiz uchun yuborilgan to'lov cheki rad etildi."
                    )
                except Exception as e:
                    logger.error(f"Foydalanuvchiga xabar yuborishda xatolik: {e}")

    except Product.DoesNotExist:
        await query.message.reply_text("❌ Xatolik: E'lon bazadan topilmadi!")
    except Exception as e:
        await query.message.reply_text(f"❌ Xatolik yuz berdi: {e}")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("🤖 Bot ishga tushdi...")
    app.run_polling()


if __name__ == '__main__':
    main()