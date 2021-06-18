import nasty_es
import nasty_en

def bad_language_filter(user_text):
    usertext = user_text[0].casefold()
    for i in nasty_en.nasty_words_en:
        if i.casefold() in user_text:
            message_en = "Inappropriate use of language detected, please remove any word that could be considered indecent or offensive."
            break
        else:
            message_en = 'Thank you'

    for i in nasty_es.nasty_words_es:
        if i.casefold() in user_text:
            message_es = "Uso inapropiado de lenguaje, por favor remueve cualquier palabra que pueda ser considerada indecente u ofensiva."
            break
        else:
            message_es = 'Gracias'
    return message_en, message_es
