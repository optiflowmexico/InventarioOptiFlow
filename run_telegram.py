import os
import streamlit as st
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# Importamos tus funciones de bot.py para procesar el Excel
from bot import procesar_catalogo, procesar_materias_primas

# 1. CARGA SEGURA DEL TOKEN
# En local lee el archivo .env. En Streamlit Cloud leerá la sección "Secrets".
load_dotenv()
TOKEN = os.environ.get("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("❌ ERROR: No se configuró la variable TELEGRAM_TOKEN")

# 2. LÓGICA DEL BOT DE TELEGRAM
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde al comando /start"""
    await update.message.reply_text(
        "🤖 ¡Hola! Bienvenido al asistente de OptiFlow ERP.\n\n"
        "Envíame un archivo de Excel (.xlsx) con tu catálogo de Productos o de Materias Primas "
        "y te lo devolveré completamente limpio y formateado. 🚀"
    )

async def manejar_documento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recibe y procesa el archivo Excel enviado por el usuario"""
    documento = update.message.document
    
    # Validar que sea un archivo Excel
    if not documento.file_name.endswith('.xlsx'):
        await update.message.reply_text("⚠️ Por favor, asegúrate de enviar un archivo con extensión .xlsx")
        return

    await update.message.reply_text("📥 Archivo recibido. Procesando y aplicando reglas de OptiFlow ERP... Por favor espera.")
    
    # Descargar el archivo que envió el usuario
    archivo_telegram = await context.bot.get_file(documento.file_id)
    ruta_temporal = os.path.join(os.getcwd(), documento.file_name)
    await archivo_telegram.download_to_drive(ruta_temporal)

    # Aquí decidirás qué función usar (por simplicidad, un ejemplo con catálogo de productos)
    # En una versión avanzada puedes preguntarle al usuario o leer el contenido para identificarlo
    exito, resultado, df = procesar_catalogo(ruta_temporal)

    if exito:
        # Enviar de vuelta el archivo limpio al usuario
        with open(resultado, 'rb') as archivo_limpio:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=archivo_limpio,
                filename=os.path.basename(resultado),
                caption="✅ ¡Listo! Aquí tienes tu catálogo limpio y optimizado para el ERP. 📦"
            )
    else:
        await update.message.reply_text(f"❌ Hubo un problema al procesar el archivo: {resultado}")
    
    # Limpieza: Borrar el archivo temporal de nuestra computadora
    if os.path.exists(ruta_temporal):
        os.remove(ruta_temporal)

# 3. ARRANQUE DEL SERVIDOR DEL BOT
def main():
    print("🤖 El Bot de Telegram de OptiFlow está escuchando mensajes...")
    app = Application.builder().token(TOKEN).build()
    
    # Comandos y manejadores
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, manejar_documento))
    
    # Ejecutar el bot (Polling clásico)
    app.run_polling()

if __name__ == '__main__':
    main()