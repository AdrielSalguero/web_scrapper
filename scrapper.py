import requests
import lxml.html as html
import os #sirve para crear carpetas con el dia de la fecha
import datetime # sirve para traer la fecha de hoy



HOME_URL ='https://www.larepublica.co/'
XPATH_LINK_TO_ARTICLE= '//text-fill/a[@class="economiaSect" or @class="empresasSect" or @class="ocioSect" or @class="globoeconomiaSect" or @class="analistas-opinionSect"]/@href'
XPATH_TITLE= '//div[@class="mb-auto"]/text-fill/span/text()'
XPATH_SUMMARY= '//div[@class="lead"]/p/text()'
XPATH_BODY= '//div[@class="html-content"]/p[not(@class)]/text()'


def parse_notice(link,today):
    
    try:
        response= requests.get(link)
        
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed= html.fromstring(notice)
            
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                
                #saco las posibles comillas de las cadenas del titutlo
                title = title.replace('\"','')
                #[0] es para traer siempre el primer valor que es el que buscamos
                summary= parsed.xpath(XPATH_SUMMARY)[0]
                 
                body= parsed.xpath(XPATH_BODY)
                

            except IndexError:
                return

            #with manejador contextual, si se cierra por alguna circunstacia,
            #este pad me mantiene todo de manera segura
            
            #fx open me permite abrir archivos
            #open(nombre de archivo o ruta, tipo wrm, codificacion siemrpe utf 8)
            with open(f'{today}/{title}.txt', 'w', encoding= 'utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            #raise para lanzar errores
            raise ValueError(f'Error: {response.status_code}')
    
    except ValueError as ve:
        print(ve)


def parse_home():
    #salvamos los errores que van a ocurrir
    try:
        #traigo la pagina que yo quiero, en este caso la republica
        response= requests.get(HOME_URL)
        #print(response) 200 then we are going well
        #if status_code(look status code in lesson 1 PLATZI 200 ----> ok)
        if response.status_code == 200:
            #solo traigo los links, response.content= devuelve el html
            #decode es un metodo que ayuda a trasnformar caracteres especiales en algo para python
            home= response.content.decode('utf-8')
            #tomamos el html y lo llevamos a un doc especial para hacer xpath
            parsed= html.fromstring(home)
            links_to_notices= parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_to_notices)

            #datetime para fechas, datye para traer fechas,today
            #strftime convierte en cadena de caracteres
            today=datetime.date.today().strftime('%d-%m-%Y')
           #os.paths.isdir trae true or false dependiendo si en la arpeta que estoy existe o no
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_notices:
                parse_notice(link,today)
                

        else:
            #raise= para elevar un error
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:
        print(ve)
        

def run():
    parse_home()


if __name__ == '__main__':
    run()