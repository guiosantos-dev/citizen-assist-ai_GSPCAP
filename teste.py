
import json
from orientacao import Orientacao

with open("data/base_conhecimento.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

orientacao = Orientacao(dados[0])

orientacao.exibir()
