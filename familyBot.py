import csv
import datetime
import json
import asyncio
import schedule
import time
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Cargar configuración desde el archivo config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Datos de configuración
TOKEN = config["token"]
GRUPOS = config["grupos"]
PERSONAS = config["personas"]
HORA_ENVIO = config["hora_envio"]  # Hora en formato "HH:MM"

# Crear instancia del bot
bot = Bot(token=TOKEN)

# Función para leer fechas y mensajes del archivo TSV
def leer_fechas():
    with open('fechas.tsv', newline='', encoding='utf-8') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        fechas = []
        for row in reader:
            # Validar que la fila tiene las claves esperadas
            if not all(key in row for key in ["dia_mes", "mensaje", "destinatarios"]):
                print(f"Advertencia: Fila mal formada o con claves faltantes: {row}")
                continue
            # Validar valores no vacíos
            if not row["dia_mes"] or not row["mensaje"]:
                print(f"Advertencia: Fila con valores vacíos detectada: {row}")
                continue
            fechas.append({
                "dia_mes": row["dia_mes"],
                "mensaje": row["mensaje"],
                "destinatarios": row["destinatarios"].split(",") if row["destinatarios"] else []
            })
        return fechas

# Función asíncrona para enviar mensajes
async def enviar_mensajes():
    hoy = datetime.date.today().strftime('%d/%m')  # Formato DD/MM
    fechas = leer_fechas()
    for evento in fechas:
        if evento["dia_mes"] == hoy:
            for destinatario in evento["destinatarios"]:
                destinatario = destinatario.strip()
                grupo_id = GRUPOS.get(destinatario)
                persona_id = PERSONAS.get(destinatario)

                print(f"Procesando destinatario: {destinatario}")
                print(f"Grupo ID: {grupo_id}, Persona ID: {persona_id}")
                
                try:
                    if grupo_id:
                        await bot.send_message(chat_id=grupo_id, text=evento["mensaje"])
                    elif persona_id:
                        await bot.send_message(chat_id=persona_id, text=evento["mensaje"])
                    else:
                        print(f"Error: Destinatario '{destinatario}' no encontrado en config.json")
                except Exception as e:
                    print(f"Error al enviar mensaje a {destinatario}: {e}")

# Función para ejecutar la tarea programada
def ejecutar_tarea_programada():
    print(f"Ejecutando tarea programada a las {datetime.datetime.now().strftime('%H:%M:%S')}")
    asyncio.run(enviar_mensajes())

# Configurar las tareas en schedule
def configurar_schedule(hora_envio):
    schedule.every().day.at(hora_envio).do(ejecutar_tarea_programada)
    print(f"Tarea programada para ejecutarse todos los días a las {hora_envio}.")

# Función para manejar el comando /start o el mensaje "hola"
async def handle_message(update: Update, context):
    text = update.message.text.lower()
    if text == "hola":
        await update.message.reply_text("familyBot.py está funcionando correctamente.")

# Bucle principal
if __name__ == "__main__":
    print("Bot ejecutándose...")

    # Configurar las tareas con la hora especificada
    configurar_schedule(HORA_ENVIO)

    # Crear la aplicación de Telegram
    application = Application.builder().token(TOKEN).build()

    # Registrar el manejador de mensajes
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Iniciar el bot en segundo plano
    application.run_polling()

    # Inicia el bucle de schedule
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)  # Evita alto uso de CPU
    except KeyboardInterrupt:
        print("Bot detenido manualmente.")