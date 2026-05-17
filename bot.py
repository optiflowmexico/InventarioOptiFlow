import os
import tempfile
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from catalogo_core import analizar_y_limpiar_excel


# Cómo usar:
#
# 1. Crea tu bot en BotFather y obtén el token.
# 2. Define BOT_TOKEN en tu entorno:
#
#    - Linux/macOS:
#        export BOT_TOKEN=123456789:ABC...
#
#    - Windows (CMD):
#        set BOT_TOKEN=123456789:ABC...
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"Hola {user_name}.\n\n"
        "Envíame un archivo Excel (.xlsx) de tu catálogo de productos y "
        "te devolveré un catálogo analizado y limpio."
    )


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    if not doc.file_name.lower().endswith(".xlsx"):
        await update.message.reply_text("Por favor envía un archivo en formato .xlsx.")
        return

    # Descargamos el documento desde Telegram
    file = await context.bot.get_file(doc.file_id)

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, doc.file_name)
        output_path = os.path.join(tmpdir, f"CATALOGO_LIMPIO_{doc.file_name}")

        # Guardamos el archivo del usuario
        await file.download_to_drive(custom_path=input_path)

        # Usamos el núcleo compartido (el mismo que Streamlit)
        resumen = analizar_y_limpiar_excel(input_path, output_path)

        # Enviamos el resumen de problemas
        await update.message.reply_text(resumen)

        # Enviamos el archivo Excel limpio como documento adjunto
        with open(output_path, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename="catalogo_limpio.xlsx",
                caption="✨ Catálogo de productos limpio y listo para tu ERP."
            )


def main():
    if not BOT_TOKEN:
        print("Error: define BOT_TOKEN en tu entorno.")
        print("Ejemplo: export BOT_TOKEN=123456789:ABC...")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    print("Bot iniciado. Presiona CTRL+C para detenerlo.")
    app.run_polling()


if __name__ == "__main__":
    main()
