import telebot
from telebot import types
import auxiliares
from red_de_cajeros import RedDeCajeros
import json
import threading


bot = telebot.TeleBot('5276948681:AAFndSvuna6J7EdDAdTUz4GgeSNRM-GyU_Q')

dataset_link, dataset_banelco = auxiliares.obtener_dataset()

red_banelco = RedDeCajeros(dataset_banelco)
red_link = RedDeCajeros(dataset_link)

@bot.message_handler(commands=["start"])
def start (message):
    bot.send_message(message.chat.id, 
        "Este bot te mostrará información de hasta tres cajeros automáticos "+"con extracción disponible "+
        "próximos a tu ubicación, en un radio de 500m. "+
        "Además se te mostrará un mapa de la zona con los cajeros. Utiliza los comandos "+
        "/link o /banelco de acuerdo a la red que busques.")

@bot.message_handler(commands=["help"])
def help (message):
    bot.send_message(message.chat.id, 
        "Utiliza /link para mostrar cajeros de la red Link y /banelco para los de la red Banelco.")

@bot.message_handler(commands=["link"])
def link (message):
    pedir_ubicacion(message.chat.id)
    bot.register_next_step_handler(message, link_location)

@bot.message_handler(commands=["banelco"])
def banelco (message):
    pedir_ubicacion(message.chat.id)
    bot.register_next_step_handler(message, banelco_location)

def pedir_ubicacion(chat_id):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    msg = "Por favor, comparte tu ubicación actual"
    button_geo = types.KeyboardButton(text="Enviar ubicación", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(chat_id, msg, reply_markup=keyboard)


def link_location(message):

    buscar_cercanos_a_red(message, red_link)


def banelco_location(message):

    buscar_cercanos_a_red(message, red_banelco)


def buscar_cercanos_a_red(message, red_bancaria):
    
    if message.location is not None:
        
        #Coordenadas de testeo (dentro de CABA)
        #coords_del_usuario = (-34.577318, -58.429110)
        
        coords_del_usuario = (message.location.latitude, message.location.longitude)
        cajeros_en_rango = red_bancaria.k_mas_cercanos(coords_del_usuario, 3)
        
        registro_de_extracciones = auxiliares.obtener_registros_extraccion()

        cajeros_en_rango = auxiliares.filtrar_cajeros(cajeros_en_rango, registro_de_extracciones)

        if len(cajeros_en_rango) == 0:
            bot.send_message(message.chat.id,"No hay bancos en rango", reply_markup=types.ReplyKeyboardRemove())
        else:
            #Notificar de extracción
            auxiliares.modificar_registro(cajeros_en_rango, registro_de_extracciones)
            respuesta = auxiliares.construir_respuesta_con(cajeros_en_rango)
            mapa = auxiliares.construir_mapa((coords_del_usuario[1], coords_del_usuario[0]), cajeros_en_rango)
            bot.send_message(message.chat.id,respuesta, reply_markup=types.ReplyKeyboardRemove())
            bot.send_photo(message.chat.id, mapa, 
                caption="Punto rojo: posición actual\n"+
                        "Punto/os amarillo/os: cajeros cercanos")

            
    else:
        bot.send_message(message.chat.id, 
            "Parece que algo ha salido mal.\n"+
            "Por favor asegurese de enviar "+
            "su ubicación e intentelo de nuevo.",
             reply_markup=types.ReplyKeyboardRemove())


#Crear un thread que se encargue de reiniciar el registro de extracciones
reiniciador = threading.Thread(target=auxiliares.reiniciar_registro)
reiniciador.start()


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.infinity_polling()