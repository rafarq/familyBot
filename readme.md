# Bot Familiar - Telegram Bot

Este es un bot de Telegram diseñado para enviar mensajes automáticos en fechas específicas. El bot está configurado para leer fechas y mensajes desde un archivo TSV (`fechas.tsv`) y enviar mensajes a grupos o personas específicas según la configuración proporcionada en `config.json`. Además, responde al mensaje "hola" con un mensaje de confirmación.

## Requisitos

- Python 3.7 o superior.
- Librerías necesarias: `csv`, `datetime`, `json`, `asyncio`, `schedule`, `time`, `python-telegram-bot`.

## Instalación

1. Clona este repositorio en tu máquina local:

   ```bash
   git clone https://github.com/tuusuario/bot-familiar.git
   cd bot-familiar
   ```

Instala las dependencias necesarias:

2. ```bash
   pip install -r requirements.txt
   ```
3. Configura el archivo `config.json` con los datos necesarios:

   ```json
   {
       "token": "TU_TOKEN_DE_TELEGRAM",
       "grupos": {
           "nombre_grupo": "ID_GRUPO"
       },
       "personas": {
           "nombre_persona": "ID_PERSONA"
       },
       "hora_envio": "HH:MM"
   }
   ```

   - `token`: El token de tu bot de Telegram.
   - `grupos`: Un diccionario que mapea nombres de grupos a sus respectivos IDs.
   - `personas`: Un diccionario que mapea nombres de personas a sus respectivos IDs.
   - `hora_envio`: La hora en la que se enviarán los mensajes programados (formato "HH:MM").
4. Prepara el archivo `fechas.tsv` con las fechas y mensajes que deseas enviar:

   ```
   dia_mes	mensaje	destinatarios
   01/01	¡Feliz Año Nuevo!	grupo_familia,amigo1
   15/03	¡Feliz Cumpleaños!	amigo2
   ```

   - `dia_mes`: La fecha en formato "DD/MM".
   - `mensaje`: El mensaje que se enviará en esa fecha.
   - `destinatarios`: Una lista separada por comas de los destinatarios (grupos o personas).

## Ejecución

Para ejecutar el bot, simplemente corre el siguiente comando:

```bash
python bot.py
```

El bot se ejecutará en segundo plano y enviará los mensajes según la programación establecida. Además, responderá al mensaje "hola" con `"familyBot.py está funcionando correctamente."`.

## Funcionalidades

- **Mensajes Programados**: El bot enviará mensajes en las fechas especificadas en `fechas.tsv` a los destinatarios correspondientes.
- **Respuesta a "hola"**: El bot responde al mensaje "hola" con un mensaje de confirmación.

## Detener el Bot

Para detener el bot, presiona `Ctrl + C` en la terminal donde se está ejecutando.

## Contribuciones

Si deseas contribuir a este proyecto, por favor abre un issue o envía un pull request. ¡Todas las contribuciones son bienvenidas!

## Licencia

Este proyecto está bajo la licencia MIT. Para más detalles, consulta el archivo [LICENSE](LICENSE).

---

¡Gracias por usar el Bot Familiar! Si tienes alguna pregunta o necesitas ayuda, no dudes en contactarme.
