# Languages

* [English](https://github.com/KappaSoftware/ktelegrambot#kappasoftwarebot)
* [Español](https://github.com/KappaSoftware/ktelegrambot#kappasoftwarebot-1)

# Kappa Software Telegram bot

The Kappa Software bot (**@kappa_software_bot**) is the communication interface between Telegram and the web application https://kappasw.org. The general functionalities of this tool in its first version released to the public are described here. Technical information on the implementation of this and other components of the Kappa project and some instructions for third-party contributions to the development of this tool can be found at https://github.com/KappaSoftware/KappaSoftware/blob/main/docs/servicios.md section "Telegram Bot Development".

The main functionality of **@kappa_software_bot** is registering the locations that will be shown on the map of the web application available at https://kappasw.org/map, which can be considered as the Kappa project’s heart. **@kappa_software_bot** lets the users register the location of their places and events of interest easily through the georeferencing functionality of their mobile phones. Registering a place in the Kappa database to be mapped on Kappa’s Website, does not require prior user registration, but it does require that the user accepts Kappa Software‘s Terms of Use and Privacy Policy available in https://kappasw.org/disclaimer.

To register a location, the user is guided through a series of sequential steps in the bot; there the user enters the necessary information for the location to be registered in the database and displayed on the map. This information contains the geographical location sent through the "Share location" function available in the Telegram interface for mobile devices, the category and subcategory where the mapped place or event fits, and a short description of the location that will appear as the Popup text when the point is created on the map. Additionally, the user can create a new category and/or subcategory in case none of the existing ones are suitable for the place it wants to register. The name of the chosen category should be a self-explanatory word, and it will serve for other users who look for places with similar characteristics. 

The instructions that guide the users during their interaction with **@kappa_software_bot**, and the categories initially proposed by the developers, are available in English and Spanish. The language of interaction can be chosen in the first interaction of each user with the bot, which is done through commands. Commands are specific words preceded by the symbol "/" that invoke the required functions. The most relevant function from the user's point of view, and the one that it will repeat in all its interactions with the bot, is the function linked to the /ToDo command, which shows the options of Search or Registering a new place. The functions linked to the registration of a place can be executed by any user, but the point will be updated on the map and registered in the Kappa database only if the user has accepted the Terms of Use and Privacy Policy of Kappa Software. In its first version, the final answer of option "search" is an html file containing a zoom-variable map where the locations available in the previously selected category and subcategory are marked; in this case, the only data consumption is the one of downloading the html file. Currently, **@kappa_software_bot** does not count with any simultaneous translation tool, so the categories and subcategories created by users after the release to the public of the first version of the ktelegrambot are presented only in the original language they were created. The same is true for the descriptive texts of the registered places.

**@kappa_software_bot** is an integral part of the Kappa project which has mainly a social focus. Thus, the project founders count on the good use and goodwill of users and developers who want to interact or contribute to the project in any way.

# Bot de Telegram de Kappa Software

El bot de Kappa Software (**@kappa_software_bot**) es la Interfaz de comunicación entre Telegram y la aplicación Web https://kappasw.org. En adelante, se describen las funcionalidades generales de esta herramienta en su primera versión liberada al público. Información técnica sobre la implementación de este y otros componentes del proyecto Kappa, así como algunas instrucciones para contribuciones de terceros al desarrollo de esta herramienta pueden consultarse en el enlace https://github.com/KappaSoftware/KappaSoftware/blob/main/docs/servicios.md, sección "Desarrollo del Bot de Telegram".

La funcionalidad principal de **@kappa_software_bot** es el registro de las ubicaciones que se muestran en el mapa de la aplicación Web disponible en https://kappasw.org/map, el cual constituye el corazón del proyecto Kappa. El uso del **@kappa_software_bot** facilita a los usuarios el registro de la localización de sus lugares y eventos de interés a través de la funcionalidad de georeferenciación de sus teléfonos móbiles. El registro de un punto en la base da datos de Kappa, para que este sea presentado en el mapa, no requiere un registro prévio de usuario, pero si que este acepte los Términos de Uso y Políticas de Privacidad de Kappa Software disponibles en https://kappasw.org/disclaimer. 

Para el registro de una ubicación, el usuario es guiado a través de una série de pasos secuenciales en el bot en los que este puede introducir los datos necesários para que la localización sea registrada y mostrada en el mapa. El primero de estos datos es la localización geográfica del lugar, la cual es enviada a través de la función "Compartir localización" disponible en la interfaz de Telegram para dispositivos móbiles. Después del registro de las coordenadas espaciales, el usuário puede escoger entre una de várias categorias en las cuales el sitio mapeado se encaja, o crear una nueva categoria en caso que ninguna de las ya existentes sea adecuada. El nombre de la cateoria escogida debe ser una palabra autoexplicativa, y servirá para que otros usuários que busquen lugares de caractersticas similares puedan acceder facilmente a la información del local mapeado. Después de escogida la categoría, el usuario debe también escoger o crear una subcategoria. Como paso final, el usuario debe suministrar una descripción corta del local que está registrando, la cual aparecerá como texto de Popup cuando el punto sea creado en el mapa. 


Las instrucciones que guian a los usuarios durante su interacción con **@kappa_software_bot**, y las categorías inicialmente propuestas por los desarrolladores, están disponibles en lengua inglesa y española. El lenguaje de interacción puede ser escogido en la primera interacción de cada usuario con el bot, la cual se hace a través de comandos, estos son palabras específicas precedidas del simbolo "/", las cuales que invocan las funciones requeridas. La función más relevante desde el punto de vista del usuario, y la que este irá a repetir en todas sus interacciones con el bot, es la función ligada al comando '/Hacer', la cual muestra las opciones de "Búsqueda" o "Registro de lugar". Las funciones siguientes que son ligadas al registro de un lugar pueden ser ejecutadas por cualquier usuário, pero el punto solo será actualizado en el mapa y registrado en la base de datos de Kappa si el usuario ha aceptado los Términos de Uso y Política de Privacidad de Kappa Software. En su primera version, la respuesta final de la opción "Búsqueda" es un archivo html que contiene un mapa de zoom variable, en el que se indican los puntos mapeados de la categoría y subcategoría previamente escogidas por el usuario. Esta opción no consume datos aparte la descarga del archivo html. En este momento **@kappa_software_bot** no cuenta con ninguna herramienta de traducción simultánea, por lo que las categorías y subcategorías creadas por los usuarios posteriormente a la liberación al público de la primera versión de **@kappa_software_bot** se presentan unicamente en la lengua original en que fueron creadas por los usuarios. Lo mismo es válido para los textos descriptivos de los lugares registrados.

**@kappa_software_bot**  es parte integral del proyecto Kappa el cuál es una inciativa con enfoque social. Así, los fundadores del proyecto confian en el buen uso y la buena voluntad de los usuários y desarrolladores que quieran de cualquier forma interactuar o contribuir con el proyecto. 

