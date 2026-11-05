
import json
import re
import unicodedata

from orientacao import Orientacao


class BaseConhecimento:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.orientacoes = []
        self.carregar()

    def carregar(self):
        try:
            with open(self.caminho_arquivo, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            self.orientacoes = [
                Orientacao(item) for item in dados
            ]

            print("Base de conhecimento carregada!")

        except FileNotFoundError:
            print("Arquivo JSON não encontrado.")

        except json.JSONDecodeError:
            print("Erro: o arquivo JSON está inválido.")

    def categorias(self):
        categorias = set()

        for orientacao in self.orientacoes:
            categorias.add(orientacao.categoria)

        return sorted(categorias)

    def por_categoria(self, categoria):
        resultado = []

        for orientacao in self.orientacoes:
            if orientacao.categoria.lower() == categoria.lower():
                resultado.append(orientacao)

        return resultado

    def normalizar(self, texto):
        texto = texto.lower()

        texto = unicodedata.normalize("NFD", texto)
        texto = "".join(
            caractere for caractere in texto
            if unicodedata.category(caractere) != "Mn"
        )

        texto = re.sub(r"[^a-z0-9\s]", " ", texto)
        texto = " ".join(texto.split())

        return texto

    def pontuar(self, pergunta, orientacao):
        pergunta = self.normalizar(pergunta)
        titulo = self.normalizar(orientacao.titulo)

        pontos = 0

        for palavra in orientacao.palavras_chave:
            palavra = self.normalizar(palavra)

            if palavra in pergunta:
                pontos += 3

        palavras_pergunta = set(pergunta.split())
        palavras_titulo = set(titulo.split())

        for palavra in palavras_pergunta:
            if len(palavra) >= 4 and palavra in palavras_titulo:
                pontos += 1

        return pontos

    def buscar(self, pergunta):
        resultados = []

        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta, orientacao)

            if pontos >= 3:
                resultados.append((pontos, orientacao))

        resultados.sort(key=lambda item: item[0], reverse=True)

        return resultados
