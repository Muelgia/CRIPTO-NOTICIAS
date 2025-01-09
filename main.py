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

# entra até o side do google noticias com filtro de cripto a menos de um dia
url = 'https://news.google.com/search?q=cripto%20when%3A1d&hl=pt-BR&gl=BR&ceid=BR%3Apt-419'

# pega o codigo fonte da pagina
requisicao = requests.get(url)

# transforma o codigo fonte no html 
paginaHtml = bs4.BeautifulSoup(requisicao.text, "html.parser")

listaNoticias = paginaHtml.find_all("a", class_='JtKRv')

print(len(listaNoticias))


for item in listaNoticias:
    
    # titulo da noticia
    tituloNoticia = item.text
    print(tituloNoticia)

    # link da noticia do google news
    linkNoticia = item.get("href")
    linkNoticia = linkNoticia[1:]
    linkNoticia = 'https://news.google.com' + linkNoticia 
    

    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Executar no modo headless
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
        })
        """
})

    try:
        # Acessar o site desejado
        driver.get(linkNoticia)
        sleep(20)

        print(driver.current_url)

    except: 
        continue
    
driver.quit()




