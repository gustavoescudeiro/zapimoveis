import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re

headers = {'User-Agent': 'Mozilla/5.0'}
url = f'https://www.zapimoveis.com.br/venda/imoveis/sp+sao-paulo/?onde=,S%C3%A3o%20Paulo,S%C3%A3o%20Paulo,,,,,city,BR%3ESao%20Paulo%3ENULL%3ESao%20Paulo,-22.909938,-47.062633&pagina={5}&tipo=Im%C3%B3vel%20usado&transacao=Venda'
r = requests.get(url, headers=headers).text
soup = BeautifulSoup(r, 'html.parser')
imoveis = soup.find_all('div', class_=['box--display-flex'])

list_imoveis = []
for i in imoveis:
    dict_infos = {}
    preco = i.find('div', class_=['simple-card__prices'])
    try:
        preco = preco.find('p', class_=['simple-card__price']).get_text()
        print(preco)
        dict_infos['preco'] = preco.rstrip().replace(" ", "")
    except:
        print(None)

    endereco = i.find('div', class_=['simple-card__actions'])
    try:
        endereco = i.find('p', class_=['color-dark text-regular simple-card__address']).get_text()
        print(endereco)
        dict_infos['endereco'] = endereco.rstrip().replace(" ", "")
    except:
        print(None)
    metragem = i.find('div', class_=['simple-card__actions'])
    try:
        metragem = i.find('li', class_=['feature__item text-small js-areas']).get_text()
        print(metragem)
        dict_infos['metragem'] = metragem.rstrip().replace(" ", "")
    except:
        print(None)
    quartos = i.find('div', class_=['simple-card__actions'])
    try:
        quartos = i.find('li', class_=['feature__item text-small js-bedrooms']).get_text()
        print(quartos)
        dict_infos['quartos'] = quartos.rstrip().replace(" ", "")
    except:
        print(None)

    vagas = i.find('div', class_=['simple-card__actions'])
    try:
        vagas = i.find('li', class_=['feature__item text-small js-parking-spaces']).get_text()
        print(vagas)
        dict_infos['vagas'] = vagas.rstrip().replace(" ", "")
    except:
        print(None)

    banheiros = i.find('div', class_=['simple-card__actions'])
    try:
        banheiros = i.find('li', class_=['feature__item text-small js-bathrooms']).get_text()
        print(banheiros)
        dict_infos['banheiros'] = banheiros.rstrip().replace(" ", "")
    except:
        print(None)

    try:
        infos = i.find('div', class_=['simple-card__prices'])
        print(infos.find_all('li', class_=['text-regular']))
        tipo = infos.find_all('li', class_=['text-regular'])


        lista_tipo = []
        lista_preco = []
        for k in tipo:
            text = k.get_text()
            lista_tipo.append(text.split("R$")[0].replace(' ', '').rstrip().replace(" ", ""))
            lista_preco.append(text.split("R$")[1].rstrip().replace(" ", ""))

        df_infos_adicionais = pd.DataFrame(list(zip(lista_tipo, lista_preco)),
                          columns=['variavel', 'valor'])
        new_dict = dict(df_infos_adicionais.values)
        dict_infos.update(new_dict)
    except:
        print(None)

    df_imovel = pd.DataFrame([dict_infos])
    list_imoveis.append(df_imovel)







dataframezao = pd.concat(list_imoveis, axis = 0)
print('a')