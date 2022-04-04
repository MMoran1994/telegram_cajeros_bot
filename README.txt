CajerosBot

Versión de Python utilizada: 3.6.5

Requerimientos previos:
	Instalar/Contar con las siguientes bibiliotecas:
		- pyTelegramBotAPI (https://pypi.org/project/pyTelegramBotAPI/)(Implementacion en Python de la Telegram Bot API)
		- scikit-learn (https://scikit-learn.org/stable/install.html)(Contiene una implementación del BallTree utilizado)
		- urllib (https://pypi.org/project/urllib3/)(Permite obtener archivos de páginas de internet. Utilizado para descargar el dataset de https://data.buenosaires.gob.ar/dataset/cajeros-automaticos)
		- staticmap (https://github.com/komoot/staticmap)(Creador del mapa y sus marcadores)

IMPORTANTE:
	Antes de iniciar el bot, correr el script crear_registro.py en una terminal mediante el comando 'python crear_registro.py'. El mismo genera un json que llevará un conteo de las extracciones estimadas hechas por los usuarios.

Iniciar el bot:
	- Desde una terminal, ejecutar el comando 'python cajeros_bot.py'. Asegurarse de tener conexión a internet para que el bot pueda recibir mensajes del servidor de Telegram. 
	- Una vez inicializado, el bot realizará un polling constante a la espera de nuevos mensajes.
	- En Telegram, buscar e ingresar al canal del bot @CajerosDeLaCiudadBot.
	- Seguir las instrucciones detalladas en el canal para hacer uso del bot.
	
	Detalles extras:
		- El bot utiliza un thread extra para llevar a cabo el reinicio del registro de extracciones en la hora especificada. Por lo tanto, podría ser necesario cerrar varios procesos para apagar el bot.
		- En el código se provee una coordenada ubicada en CABA ((-34.577318, -58.429110)) utilizada a modo de testeo. Para utilizarla, descomentar la línea 62 y comentar la línea 64 del código del archivo cajeros_bot.py


Bot creado por: Martín Morán
Dudas o comentarios escribir a: martinmoran1994@gmail.com