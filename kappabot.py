import asyncio
import time
import logging
import json
import urllib.request
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    CallbackContext,
    Filters,
    CallbackQueryHandler,
    )
from Nasty_words_filter_back import bad_language_filter
from map_code import map_code

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

CONSULT_TIME = 0
jsons = []
idiom = ""
id_verifier_var = "Initially_non_verified"
#
## Internal functions
#

def jsons_catg_subcatg():
    "Return all information of categories and subcategories."
    subcatgs = []
    data_j0_en = []
    data_j0_es = []
    subcatgs_en = []
    subcatgs_es = []
    
    catg_plain = get_json("https://kappasw.org/kappa/categories")
    catgs = categories_processed(catg_plain)
    data = subcategory_processed(catgs)

    for x in data:
        data_j0_en.append(j0_en(x))
        data_j0_es.append(j0_es(x))

    good_catgs_en = categories_idioms(data_j0_en)
    good_catgs_es = categories_idioms(data_j0_es)
    good_catgs_en.append(["Add a new category", "newCategory"])
    good_catgs_es.append(["Agregar nueva categoría", "nuevaCategoria"])

    for sub_en in data_j0_en:
        subcatgs_en.append(sub_en[2])
    subcatgs_en_onelist = subcategories_to_onelist_en(subcatgs_en)
        
    for sub_es in data_j0_es:
        subcatgs_es.append(sub_es[2])
    subcatgs_es_onelist = subcategories_to_onelist_es(subcatgs_es)
    
    return [[data_j0_en, data_j0_es], [good_catgs_en, good_catgs_es], [subcatgs_en_onelist, subcatgs_es_onelist]]

def subcategories_to_onelist_en(subcatgs_en):
    subcatgs_one_list = []
    for i in subcatgs_en:
        for j in i:
            if j[1] == "newSubcategory":
                continue
            subcatgs_one_list.append(j)
    subcatgs_one_list.append(["Add a new subcategory", "newSubcategory"])
    return subcatgs_one_list

def subcategories_to_onelist_es(subcatgs_es):
    subcatgs_one_list = []
    for i in subcatgs_es:
        for j in i:
            if j[1] == "nuevaSubcategoria":
                continue
            subcatgs_one_list.append(j)
    subcatgs_one_list.append(["Agregar nueva subcategoría", "nuevaSubcategoria"])
    return subcatgs_one_list

def categories_idioms(json_en_or_es):
    catgs_en = []
    for i in json_en_or_es:
        catgs_en.append([i[0], i[1]])
    return catgs_en

def categories_processed(lst_jsons):
    "Build the plain categories."
    new_json = []
    for i in lst_jsons:
        new_json.append([i['Name_en'], i['Name_es'], i['_id']])
    return new_json

def subcategory_processed(lst_categories):
    '''Build the list of categories with list of subcategories. if the category dont have subcategory, add the list for
build a new subcategory.'''
    subcategories = []
    cat_with_subcats = []
    for i in lst_categories:
        all_subcategories = get_json('https://kappasw.org/kappa/subcategories/category/' + i[2])
        if all_subcategories == []:
            cat_with_subcats.append([i[0], i[1], i[2], [["Add a new subcategory", "newSubcategory"], ["Agregar nueva subcategoría", "nuevaSubcategoria"]]])
        else:
            for j in all_subcategories:
                subcategories.append([j['Name_en'], j['Name_es'], j['_id']])
            subcategories.append(["Add a new subcategory", "newSubcategory"])
            subcategories.append(["Agregar nueva subcategoría", "nuevaSubcategoria"])
            cat_with_subcats.append([i[0], i[1], i[2], subcategories])
            subcategories = []
    return cat_with_subcats

def subcatgs_of_catg(id_category):
    '''Input an ID Category, and return the list of subcategories.
       With name and id.'''
    if idiom == "es":
        for i in jsons[0][1]:
            if i[1] == id_category:
                return i[2]
    else:
        for i in jsons[0][0]:
            if i[1] == id_category:
                return i[2]

def j0_en(json0):
    "Build the json0, categories with subcategories in english."
    json_0_en = []
    internal = []
    json_0_en.append(json0[0])
    json_0_en.append(json0[2])
    for i in json0[3]:
        if i[1] == "nuevaCategoria":
            continue
        if i[1] == "newSubcategory":
            internal.append([i[0], i[1]])
        if len(i) == 3:
            internal.append([i[0], i[2]])
    json_0_en.append(internal)
    return json_0_en

def j0_es(json0):
    "Build the json0, categories with subcategories in spanish."
    json_0_es = []
    internal = []
    json_0_es.append(json0[1])
    json_0_es.append(json0[2])
    for i in json0[3]:
        if i[1] == "newSubcategory":
            continue
        if i[1] == "nuevaSubcategoria":
            internal.append([i[0], i[1]])
        if len(i) == 3:
            internal.append([i[1], i[2]])
    json_0_es.append(internal)
    return json_0_es

def json_skel_map(id_subcategory, comment, lat, lng):
    "Build the skel for json user location."
    return {"type":"Feature", "properties":{"Subcategory":id_subcategory, "Popup_en":comment, "Popup_es":comment}, "geometry":{ "coordinates":[lat, lng]}}

def json_post(url, input_json):
    "Call the plain data jsons."
    url_post = url
    reqst = urllib.request.Request(url_post)
    reqst.add_header('Content-type', 'application/json; charset=utf-8')
    normalization_json = json.dumps(input_json)
    json_encode = normalization_json.encode('utf-8')
    json_complete = reqst.add_header('Content-length', len(json_encode))
    to_send = urllib.request.urlopen(reqst, json_encode)

def user_post(url, json_usr_post):
    "Send a post request for user information."
    request = Request(url, urlencode(json_usr_post).encode())
    json_usr = urlopen(request).read().decode()
    return json_usr

def get_json(url):
    "GET json."
    geted_url = urllib.request.urlopen(url)
    data_from_url = geted_url.read()
    encoding_data = geted_url.info().get_content_charset('utf-8')
    information = json.loads(data_from_url.decode(encoding_data))
    return information

def build_new_category(category_name):
    "Send a post for build a new category."
    new_category = user_post("https://kappasw.org/kappa/categories", {"Name_en": category_name, "Name_es": category_name, "Nickname": ""})
    ## type(new_category) == str
    return new_category[-297:-273]

def build_new_subcategory(id_category, name):
    new_subcategory = user_post("https://kappasw.org/kappa/subcategories", {"Category": id_category, "Name_en": name, "Name_es": name, "Icon": ""})
    return new_subcategory

def keyboard_skel(show_text, callback):
    "Return a small keyboard."
    return InlineKeyboardButton(show_text, callback_data=callback)

def build_vert_keyboards(list_of_lists):
    "Build vertical keyboards from a `list_of_list`."
    keyboards = []
    for i in list_of_lists:
        skels = []
        for j in i:
            skels.append(keyboard_skel(j[0], j[1]))
        keyboards.append(skels)
        skels = []
    return keyboards

def get_three(some_list):
    """Input a list of list and return a list with sublist with three elements
and rest."""
    all_keyboards = []
    first = 0
    end = 3
    while True:
        keyboard = some_list[first:end]
        if len(keyboard) < 3:
            all_keyboards.append(keyboard)
            break
        first += 3
        end += 3
        all_keyboards.append(keyboard)
    return all_keyboards

async def get_jsons_async():
    "Asynchronous call for jsons."
    await asyncio.sleep(1)
    time.sleep(3600)
    jsons_next_time()
    
def jsons_first_time():
    "First call for jsons."
    global CONSULT_TIME
    if CONSULT_TIME == 0:
        jsons = jsons_catg_subcatg()
        print(jsons, "\n")
        print("Data or json[0] \n", jsons[0], "\n")
        print("Categories: or json[1] \n", jsons[1], "\n")
        print("Subcategories: or json[2] \n", jsons[2], "\n")
        CONSULT_TIME = 1
    return jsons

def jsons_next_time():
    "Consecutive calls for jsons."
    global CONSULT_TIME
    if CONSULT_TIME == 1:
        jsons = jsons_catg_subcatg()
        print(jsons, "\n")
        print("Data or json[0] \n", jsons[0], "\n")
        print("Categories: or json[1] \n", jsons[1], "\n")
        print("Subcategories: or json[2] \n", jsons[2], "\n")
    return jsons

async def loop_tasks():
    "Asynchronous tasks for call jsons."
    tasks = []
    for i in range(0, 121):
        tasks.append(120)
    tasks_loop = [get_jsons_async() for num in tasks]
    await asyncio.wait(tasks_loop)


#
## Telegram functions
#

def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user_data = context.user_data
    category = 'Chat_id'
    user_data[category] = chat_id

    to_reply = [("Español", "Spanish"), ("English", "English")]
    reply_keyboards = get_three(to_reply)
    keyboards = build_vert_keyboards(reply_keyboards)
    reply_markup = InlineKeyboardMarkup(keyboards)
    update.message.reply_text(
        ''' ¡Hola, bienvenido a los servicios de geolocalización de Kappa! \nPor favor, selecciona tu idioma.
           \n\nHello, welcome to Kappa geolocation services! \nPlease select your language.''', reply_markup=reply_markup)

def to_do(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("Register a new location", callback_data="Location")],
    [InlineKeyboardButton("Looking for a location", callback_data='Search')]]
    markup_to_send = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('What do you want to do now?', reply_markup=markup_to_send)

def hacer(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("Registrar una nueva localización", callback_data="Localizacion")],
                [InlineKeyboardButton("Visualizar una localización", callback_data='Buscar')]]
    markup_to_send = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('¿Qué deseas hacer ahora?', reply_markup=markup_to_send)

def build_category(update: Update, context: CallbackContext):
    all_information = update.message.text
    get_new_category = all_information.split(" ")[1]

    in_message = bad_language_filter(get_new_category)

    cond_1 = (in_message[0] == 'Thank you') and (in_message[1] == 'Gracias') and (id_verifier_var == 'Verified_User')
    cond_2 = (in_message[0] == 'Thank you') and (in_message[1] == 'Gracias') and (id_verifier_var != 'Verified_User')
    cond_3 = (in_message[0] != 'Thank you') or (in_message[1] != 'Gracias')

    if cond_1:
        id_new_category = build_new_category(get_new_category)
        user_data = context.user_data
        category = 'idNewCategory'
        user_data[category] = id_new_category
        update.message.reply_text('''Please type "/subcategory" followed by the name of the subcategory you want to add (it must have only one word).
                    \n Example:\n/subcategory Public''')
    elif cond_2:
        update.message.reply_text('''It seems you did not accept our Terms of Use and Privacy Policy. To create a new category you must accept. To do so, please restart your interaction with the bot by pressing here /start''')

    elif cond_3:
        update.message.reply_text('Inappropriate use of language detected, please remove any word that could be considered indecent or offensive.')


def construir_categoria(update: Update, context: CallbackContext):
    all_information = update.message.text
    get_new_category = all_information.split(" ")[1]

    in_message = bad_language_filter(get_new_category)

    cond_1 = (in_message[0] == 'Thank you') and (in_message[1] == 'Gracias') and (id_verifier_var == 'Verified_User')
    cond_2 = (in_message[0] == 'Thank you') and (in_message[1] == 'Gracias') and (id_verifier_var != 'Verified_User')
    cond_3 = (in_message[0] != 'Thank you') or (in_message[1] != 'Gracias')

    if cond_1:
        id_new_category = build_new_category(get_new_category)
        user_data = context.user_data
        category = 'idNewCategory'
        user_data[category] = id_new_category
        update.message.reply_text('''Por favor escribe "/subcategoria" seguido del nombre de la subcategoría que deseas agregar (usa una sola palabra).
                \nEjemplo:\n/subcategoria Públicas''')
        
    elif cond_2:
        update.message.reply_text('''Parece que no has aceptado nuestros Términos de uso y Políticas de Privacidad. Crear una nueva categoría requiere que aceptes  nuestros términos y políticas, para esto, reinicia tu interacción con el bot presionando aqui /iniciar''')
        
    elif cond_3:
        update.message.reply_text('Uso inapropiado de lenguaje, por favor remueve cualquier palabra que pueda ser considerada indecente u ofensiva.')
        

def build_subcategory(update: Update, context: CallbackContext):
    all_information = update.message.text
    new_subcategory = all_information.split(" ")[1]

    in_message = bad_language_filter(new_subcategory)

    if ((in_message[0] == 'Thank you') and (in_message[1] == 'Gracias')):
        if id_verifier_var == 'Verified_User':
            id_owner_category = context.user_data['idNewCategory']
            build_new_subcategory(id_owner_category, new_subcategory)
            global jsons
            jsons = jsons_next_time()
            update.message.reply_text('''Congratulations! the new category/subcategory is updated, but the point is not registered on the map yet.
                                 \nTo actually register the location, please, restart the process by pressing here /ToDo''')
        else:
            update.message.reply_text('''It seems you did not accept our Terms of Use and Privacy Policy. To create a new subcategory you must accept. To do so, please restart your interaction with the bot by pressing here /start ''')


    elif ((in_message[0] != 'Thank you') or (in_message[1] != 'Gracias')):
        update.message.reply_text('Inappropriate use of language detected, please remove any word that could be considered indecent or offensive.')


def construir_subcategoria(update: Update, context: CallbackContext):
    all_information = update.message.text
    new_subcategory = all_information.split(" ")[1]

    in_message = bad_language_filter(new_subcategory)

    if ((in_message[0] == 'Thank you') and (in_message[1] == 'Gracias')):
        if id_verifier_var == 'Verified_User':
            id_owner_category = context.user_data['idNewCategory']
            build_new_subcategory(id_owner_category, new_subcategory)
            global jsons
            jsons = jsons_next_time()
            update.message.reply_text('''¡Felicidades! La nueva categoría/subcategoría ha sido creada, pero la localización todavía no se ha registrado en el mapa. 
                    \nPara registrar la localización, por favor reinicia el proceso presionando este vínculo /Hacer.''')
            
        else:
            update.message.reply_text('''Parece que no has aceptado nuestros Términos de uso y Políticas de Privacidad. Crear una nueva subcategoría requiere que aceptes  nuestros términos y políticas, para esto, reinicia tu interacción con el bot presionando aqui /iniciar ''')
            
    elif ((in_message[0] != 'Thank you') or (in_message[1] != 'Gracias')):
        update.message.reply_text('Uso inapropiado de lenguaje, por favor remueve cualquier palabra que pueda ser considerada indecente u ofensiva.')
        


def interface(update: Update, context: CallbackContext):
    id_categories = []
    id_subcategories = []


    query = update.callback_query

    if f'{query.data}' == "Spanish":
        global idiom
        idiom = "es"
        to_reply = [["Aceptar", "Aceptar"], ["Rechazar", "Rechazar"]]
        reply_keyboards = get_three(to_reply)
        keyboards = build_vert_keyboards(reply_keyboards)
        reply_markup = InlineKeyboardMarkup(keyboards)
        query.edit_message_text('''Para usar nuestros servicios, debes aceptar los Términos de Uso y Política de Privacidad que puedes leer en el siguiente enlace: https://kappasw.org/disclaimer.
                                \nAhora, ¿declaras haber leído, y aceptas los Términos de Uso y Política de Privacidad de Kappa Software?''',
                                reply_markup = reply_markup)

    elif f'{query.data}' == "English":
        idiom = "en"
        to_reply = [["Accept", "Accept"], ["Reject", "Reject"]]
        reply_keyboards = get_three(to_reply)
        keyboards = build_vert_keyboards(reply_keyboards)
        reply_markup = InlineKeyboardMarkup(keyboards)
        query.edit_message_text(
            '''To use our services, you must accept the Terms of Use and Privacy Policy that you can find through https://kappasw.org/disclaimer
            \nNow, do you declare that you read and accept Kappa Software's Terms of Use and Privacy Policy?''',
            reply_markup = reply_markup)

    if idiom == "es":
        for i in jsons[1][1]:
            id_categories.append(i[1])
    else:
        for i in jsons[1][0]:
            id_categories.append(i[1])

    if idiom == "es":
        for k in jsons[2][1]:
            id_subcategories.append(k[1])
        id_subcategories.pop()
    else:
        for k in jsons[2][0]:
            id_subcategories.append(k[1])
        id_subcategories.pop()


    if f'{query.data}' == 'Accept':
        chat_id_send = context.user_data['Chat_id']
        print(chat_id_send)
        #print(chat_id, type(chat_id)) ## type = integer
        user_id_verify_url = get_json("https://kappasw.org/kappa/telegramusers/" + f'{chat_id_send}')
        #print(type(user_id_verify_url)) ## type dictionary
        global id_verifier_var

        if user_id_verify_url.get('_id') != None:
            id_verifier_var = "Verified_User"
        else:
            post_id = user_post("https://kappasw.org/kappa/telegramusers", {"idTelegram":  chat_id_send})
            print(post_id)
            id_verifier_var = "Verified_User"
        query.edit_message_text('''Thank you for accepting our terms and policies! To choose what you want to do now, please press here /ToDo''')


    if f'{query.data}' == 'Aceptar':
        chat_id_send = context.user_data['Chat_id']
        print(chat_id_send)
        #print(chat_id, type(chat_id)) ## type = integer
        user_id_verify_url = get_json("https://kappasw.org/kappa/telegramusers/" + f'{chat_id_send}')
        #print(type(user_id_verify_url)) ## type dictionary

        if user_id_verify_url.get('_id') != None:
            id_verifier_var = "Verified_User"
        else:
            post_id = user_post("https://kappasw.org/kappa/telegramusers", {"idTelegram":  chat_id_send})
            print(post_id)
            id_verifier_var = "Verified_User"
        query.edit_message_text('''¡Gracias por aceptar nuestros términos y políticas! Para seleccionar lo que quieres hacer ahora, por favor presiona aquí: /Hacer''')
      

    if f'{query.data}' == 'Rechazar':
        query.edit_message_text('''Los servicios de Kappa Software sólo estarán disponibles después de que aceptes nuestros términos y políticas.
                                \nPara aceptar los términos y políticas de Kappa Software debes reiniciar tu interacción con el bot presionando aqui  /iniciar ''')


    if f'{query.data}' == 'Reject':
        query.edit_message_text('''To use Kappa Software's services you must accept our terms and policies.
                                \nPlease, read it again, we are sure you will accept them, our services worth it!
                                \nTo accept our terms and policies you must restart the process by pressing here /start ''')

    if f'{query.data}' == 'Buscar':

        query.edit_message_text('''Por favor presiona aquí /buscar para activar esta opción''')
        
    if f'{query.data}' == 'Search':
        query.edit_message_text('''Please type here /search to activate this option''')

    if f'{query.data}' == 'Localizacion':
        query.edit_message_text('''Por favor, envíame la localización del lugar o evento que quieres registrar. Para esto, utiliza la opción de Telegram "Compartir Localización" y ubica el marcador encima del lugar que quieres mapear. ''')

    if f'{query.data}' == 'Location':
        query.edit_message_text('''Now please send me the location of the place or event you want to register. To complete this action, use Telegram's "Share location" option and place the marker on the location you want to map.''')


    if f'{query.data}' == 'nuevaCategoria':
        query.edit_message_text('''Por favor escribe "/categoria" seguida del nombre de la categoría que quieres agregar.
                                \nPor favor usa una palabra que sea auto-explicativa, por ejemplo:
                                \n/categoria Escuelas''')
        
    if f'{query.data}' == 'newCategory':
        query.edit_message_text('''Please write "/category" followed by the name of the category you want to register.
                                   \nPlease use one unique, self-explicative word, for example:
                                   \n/category Schools''')

    if f'{query.data}' == 'nuevaSubcategoria':
        id_category = context.user_data['IdCategory']
        user_data = context.user_data
        category = 'idNewCategory'
        user_data[category] = id_category
        query.edit_message_text('''Ahora por favor escribe "/subcategoria" seguido del nombre de la subcategoría a agregar.
         \nPor favor usa una palabra que sea auto-explicativa, por ejemplo:
                                \n/subcategoria Públicas.''')
        
    if f'{query.data}' == 'newSubcategory':
        id_category = context.user_data['IdCategory']
        user_data = context.user_data
        category = 'idNewCategory'
        user_data[category] = id_category
        query.edit_message_text('''Now please type "/subcategory" followed by the name of the subcategory you want to add.
            \nPlease, use one only,  self-explicative word, for example:
            \n/subcategory Publics''')
        
    for j in id_categories:
        if ((f'{query.data}' == j) and (search_var != 'Active')):
            user_data = context.user_data
            user_data['IdCategory'] = j
            subcategories = subcatgs_of_catg(j)
            #print (subcategories, type(subcategories))
            reply_keyboards = get_three(subcategories)
            keyboards = build_vert_keyboards(reply_keyboards)
            markup_to_send = InlineKeyboardMarkup(keyboards)
            if idiom == "es":
                query.edit_message_text('''¡Bien!, ahora por favor selecciona una de las siguientes subcategorías en la cual este lugar se encaja''', reply_markup=markup_to_send)
            else:
                query.edit_message_text('''Ok, now please select one of the following subcategories where this place fits''', reply_markup=markup_to_send)

        elif ((f'{query.data}' == j) and (search_var == 'Active')):
            user_data = context.user_data
            user_data['IdCategory'] = j
            subcategories = subcatgs_of_catg(j)
            #print (subcategories, type(subcategories))
            reply_keyboards = get_three(subcategories[:-1])
            keyboards = build_vert_keyboards(reply_keyboards)
            markup_to_send = InlineKeyboardMarkup(keyboards)
            if idiom == "es":
                query.edit_message_text('''Por favor selecciona la subcategoría en la cual quieres buscar \n(Ten en cuenta que si no obtienes respuesta es porque no tenemos datos registrados en la categoría que elegiste, en ese caso presiona aquí /buscar para recomenzar tu búsqueda en otra categoría, o aquí /Hacer si quieres realizar otra acción.)''', reply_markup=markup_to_send)
            else:
                query.edit_message_text('''Please select the subcategories where you want to search \n(Have into account that if you don't get any answer, it is because we don't have any data in the category you chose, in tha case, press here /search to restart your searching in a different category, or here /ToDo if you want to do another action. )''', reply_markup=markup_to_send)
        
        
    for l in id_subcategories:
        if ((f'{query.data}' == l) and (search_var != 'Active')):
            user_data = context.user_data
            user_data['SubCategoryId'] = l
            if idiom == "es":
                query.edit_message_text('''Ahora escribe "/mensaje" seguido de una corta descripción que le quieras dar al punto a registrar. Por ejemplo:
                    \n /mensaje Escuelas con cupos disponibles para sexto grado en 2022''')
            else:
                query.edit_message_text('''Write '/message' followed by a short message describing the place you are registering. Example:
                    \n /message Public Schools with the best sport facilities''')

        elif ((f'{query.data}' == l) and (search_var == 'Active')):
            user_data = context.user_data
            user_data['SubCategoryId'] = l
            data_points_ulr = 'https://kappasw.org/kappa/data/subcategory/' + f'{l}' 
            map_dat = get_json(data_points_ulr)
            map_code(map_dat, idiom)
            context.bot.sendDocument(update.effective_chat.id, document = open('Mapa_send.html', 'rb'))
            if idiom == "es":
                query.edit_message_text('''Los lugares que tenemos registrados para la categoría y subcategoría que escogiste se muestran en el siguiente mapa; después de su descarga no consumirás datos.''')
            else:
                query.edit_message_text('''The places we have registered in the category and subcategory you chose are presented below. You won't consume any data after the download.''')



def local_search(update: Update, context: CallbackContext):
    global search_var
    categories = jsons[1][0][:-1]
    reply_keyboards = get_three(categories)
    keyboards = build_vert_keyboards(reply_keyboards)
    markup_to_send = InlineKeyboardMarkup(keyboards)
    update.message.reply_text(''' Great! Now please select the category where you want to search.''', reply_markup=markup_to_send)
    search_var = 'Active'

def busqueda_local(update: Update, context: CallbackContext):
    global search_var
    categories = jsons[1][1][:-1]
    reply_keyboards = get_three(categories)
    keyboards = build_vert_keyboards(reply_keyboards)
    markup_to_send = InlineKeyboardMarkup(keyboards)
    update.message.reply_text('''¡Bien! Ahora por favor selecciona la categoría en la que quieres buscar.''', reply_markup=markup_to_send)
    search_var = 'Active'



def get_location(update: Update, context: CallbackContext):
    global search_var
    location = update.message.location
    lat = location.latitude
    lng = location.longitude
    user_data = context.user_data
    category = 'Location'
    user_data[category] = [lat, lng]

    if user_data['Location'] != []:
        pass
    else:
        if idiom == "es":
            update.message.reply_test("Algo salió mal, por favor envíame la localización nuevamente.")
        else:
            update.message.reply_text("Something went wrong, please send me the location again.")

    if idiom == "es":
        categories = jsons[1][1]
        reply_keyboards = get_three(categories)
        keyboards = build_vert_keyboards(reply_keyboards)
        markup_to_send = InlineKeyboardMarkup(keyboards)
        update.message.reply_text('''¡Bien! \nAhora por favor selecciona la categoría a la cual esta localización pertenece o agrega una nueva si ninguna de las disponibles te parece adecuada.''',
                                  reply_markup=markup_to_send)
        search_var = 'Non_active'
    else:
        categories = jsons[1][0]
        reply_keyboards = get_three(categories)
        keyboards = build_vert_keyboards(reply_keyboards)
        markup_to_send = InlineKeyboardMarkup(keyboards)
        update.message.reply_text(''' Great! \nNow please select in what of the following categories the place you want to 
        register fits or add a new category if none of the existing looks like the right one''', reply_markup=markup_to_send)
        search_var = 'Non_active'

def send_point(update: Update, context: CallbackContext):
    msg = update.message.text
    msg_lst = msg.split(" ")
    cmd = msg_lst[0]
    args = msg_lst[1:]
    coords = context.user_data['Location']
    lat = coords[0]
    lng = coords[1]
    subcategory_id = context.user_data['SubCategoryId']

    in_message = bad_language_filter(args)

    chat_id_send = update.message.chat_id
    user_id_verify_url = get_json("https://kappasw.org/kappa/telegramusers/" + f'{chat_id_send}')

    if ((cmd == "/message") or (cmd == "/mensaje")):
        if ((in_message[0] == 'Thank you') and (in_message[1] == 'Gracias')):
            json_new_point = json_skel_map(subcategory_id, " ".join(args), lat, lng)
            if user_id_verify_url.get('_id') != None:
                json_post("https://kappasw.org/kappa/data", json_new_point)
                print(json_new_point)
                update.message.reply_text('''Point updated! Thanks. \nTo perform another action press here /ToDo''')
            else:
                update.message.reply_text('''It seems you did not accept our Terms of Use and Privacy Policy. To register a point on the map, you must accept. To do so, please restart your interaction with the bot by pressing here /start''')
        elif ((in_message[0] != 'Thank you') or (in_message[1] != 'Gracias')):   
            update.message.reply_text('Inappropriate use of language detected, please remove any word that could be considered indecent or offensive.')

def enviar_punto(update: Update, context: CallbackContext):
    msg = update.message.text
    msg_lst = msg.split(" ")
    cmd = msg_lst[0]
    args = msg_lst[1:]
    coords = context.user_data['Location']
    lat = coords[0]
    lng = coords[1]
    subcategory_id = context.user_data['SubCategoryId']

    in_message = bad_language_filter(args)

    chat_id_send = update.message.chat_id
    user_id_verify_url = get_json("https://kappasw.org/kappa/telegramusers/" + f'{chat_id_send}')

    if ((cmd == "/message") or (cmd == "/mensaje")):
        if ((in_message[0] == 'Thank you') and (in_message[1] == 'Gracias')):
            json_new_point = json_skel_map(subcategory_id, " ".join(args), lat, lng)
            if user_id_verify_url.get('_id') != None:
                json_post("https://kappasw.org/kappa/data", json_new_point)
                print(json_new_point)
                update.message.reply_text('''¡Punto actualizado en el mapa! Gracias. \nPara realizar otra acción, presiona aquí /Hacer''')
            else:
                update.message.reply_text('''Parece que no has aceptado nuestros Términos de uso y Políticas de Privacidad. El registro de un punto en el mapa requiere que aceptes  nuestros términos y políticas, para esto, reinicia tu interacción con el bot presionando aqui /iniciar''')
        elif ((in_message[0] != 'Thank you') or (in_message[1] != 'Gracias')):
            update.message.reply_text('Uso inapropiado de lenguaje, por favor remueve cualquier palabra que pueda ser considerada indecente u ofensiva.')
    
        

#
## Exec
#

def main():
    updater = Updater(token='YOUR_TOKEN_HERE')
    
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("iniciar", start))
    dispatcher.add_handler(CommandHandler("Hacer", hacer))
    dispatcher.add_handler(CommandHandler("ToDo", to_do))
    dispatcher.add_handler(CommandHandler("mensaje", enviar_punto))
    dispatcher.add_handler(CommandHandler("message", send_point))
    dispatcher.add_handler(CallbackQueryHandler(interface))
    dispatcher.add_handler(MessageHandler(Filters.location, get_location))
    dispatcher.add_handler(CommandHandler("categoria", construir_categoria))
    dispatcher.add_handler(CommandHandler("category", build_category))
    dispatcher.add_handler(CommandHandler("subcategoria", construir_subcategoria))
    dispatcher.add_handler(CommandHandler("subcategory", build_subcategory))
    dispatcher.add_handler(CommandHandler("search", local_search))
    dispatcher.add_handler(CommandHandler("buscar", busqueda_local))

    updater.start_polling()


    
    global jsons
    jsons = jsons_first_time()
    loop_five_days = asyncio.new_event_loop()
    asyncio.set_event_loop(loop_five_days)
    loop_five_days.run_until_complete(loop_tasks())
    loop_five_days.close()

if __name__ == '__main__':
    main()
