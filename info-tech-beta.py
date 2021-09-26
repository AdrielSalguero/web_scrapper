import requests
import lxml.html as html
import os
import datetime



#CONSTANTES
HOME_URL= 'https://www.infotechnology.com/'
XPATH_LINKS_TO_ARTICLE= '//h2 [@class = "title"]/a/@href'
XPATH_CATHEGORIES= '//div [@class = "ts"]/div [@class = "kicker"]/text()'
XPATH_TITLE= '//article [@class = "main-article news-group"]/h1/text()'
XPATH_SUMMARY= '//article [@class = "main-article news-group"]/h2/text()'


def parse_notice(link,today):

    try:
        response = requests.get(link)

        if response.status_code == 200:

            #traigo el html que voy a trabajar
            notice= response.content.decode('utf-8')

            #para poder usar XPATH  
            parsed = html.fromstring(notice)

            try:

                title= parsed.xpath(XPATH_TITLE)[0]
                title=title.replace('\"', '')
                cathegorie= parsed.xpath(XPATH_CATHEGORIES)[0]
                summary= parsed.xpath(XPATH_SUMMARY)[0]    

            except IndexError:

                return

            # with manejador contextual, si el archivo se cierra inesperado no se corrompe
            with open(f'{today}/{title}.txt','w',encoding= 'utf-8') as f:

                f.write(title)
                f.write('\n \n')
                f.write(summary)
                

        else:

            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:

        print(ve)




def parse_home():
    # se utiliza para extraer los links de noticias
    try:

        response= requests.get(HOME_URL)
        if response.status_code == 200:

            home= response.content.decode('utf-8')
            #toma el contenido de html que ya tengo en home y
            #Lo transforma en un documento especial que manipulo con XPATH
            parse= html.fromstring(home)

            #obtengo uan lista de tdoso los resultado de aplicar ese xpath
            links_to_notices= parse.xpath(XPATH_LINKS_TO_ARTICLE)
            #print(links_to_notices)

            today = datetime.date.today().strftime('%d-%m-%Y')
            #si no existe esa ruta hace este, el isdir trae un bool
            if  not os.path.isdir(f'info-technology {today}'):

                os.mkdir(f'info-technology {today}')
            
            for link in links_to_notices:

                parse_notice(link,today)


            

        else:
            #Lanzo el error del codigo que estoy teniendod
            raise ValueError(f'Erorr: {response}')



    except ValueError as ve:
         
         print(ve)   
        



def run():

    parse_home()


if __name__ == "__main__":

    run()