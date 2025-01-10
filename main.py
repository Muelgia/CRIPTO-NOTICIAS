import requests, re
import bs4
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def pegarNoticias(driver, tag, classe, noticias : list):
    
    try:
        # pega o url atual da pagina
        urlAtual = driver.current_url
        print(urlAtual)
        # transforma o codigo fonte no html 
        paginaHtml = bs4.BeautifulSoup(driver.page_source, "html.parser")
        # pega o elemento que vai ser uma "lista"
        listaNoticias = paginaHtml.find_all(tag, class_=classe)
        # adiciona cada elemento da lista em outra lista, que é a principal
        for noticia in listaNoticias:
            print('ok')

            #adiciona o url da noticia no dicionario
            linkNoticia = noticia.get("href")
            #adiciona o titulo da noticia no dicionario
            noticia =  noticia.text

            noticias.append((noticia, linkNoticia))

    except Exception as e:
        print(e)
        print('Erro na função pegar noticías')

# entra até o side do google noticias com filtro de cripto a menos de um dia

pesquisa = str(input('Desejo dados das ultimas 24h sobre: \n>>> '))
# pesquisa = 'bitcoin btc'
url = f'https://www.google.com/search?q={pesquisa}&tbm=nws&tbs=qdr:d'

chrome_options = Options()
chrome_options.add_argument("--headless")  # Executar no modo headless

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get(url)

wait = WebDriverWait(driver, 3)

noticias = []

while True:

    pegarNoticias(driver=driver, tag='a', classe='WlydOe', noticias=noticias)

    print(noticias)

    try:
        
        avancaPagina = wait.until(EC.presence_of_element_located((By.ID, 'pnnext')))
        avancaPagina.click()
        continue

    except:
        print('Fim das páginas')
        break

# evita algumas detecções de bot
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# para cada noticia que foi adicionada na lista, entra no site e pega todos os <p>
for link in noticias:
    try:
        textoNoticia = ''    
        responseLink = requests.get(link[1], headers=headers)
        paginaLink = bs4.BeautifulSoup(responseLink.text, "html.parser")
        # pega o elemento que vai ser uma "lista"
        noticiaLink = paginaLink.find_all("p")

        for p in noticiaLink:
            textoNoticia += p.text + "\n"

        print(f'Noticia do site {link[1]} pega com sucesso!')
    except:
        print(f'Erro ao pegar noticia do site {link[1]}')
        pass


   




