import csv
import json
import time
from datetime import datetime
import re

class Assistente:
    def __init__(self, nome, base_conhecimento):
        self.nome = nome
        self.base = base_conhecimento


        try:
            with open("data/historico.json", "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            if isinstance(dados, list) and all(
                    isinstance(item, dict) for item in dados
            ):
                self.historico = dados
            else:
                print("Aviso: formato do histórico inválido.")
                self.historico = []

        except FileNotFoundError:
            self.historico = []

        except json.JSONDecodeError:
            print("Aviso: arquivo de histórico corrompido.")
            self.historico = []

        except OSError:
            print("Aviso: não foi possível ler o histórico.")
            self.historico = []
        try:
            with open("data/avaliacao.json", "r", encoding="utf-8") as arquivo:
                avaliacao = json.load(arquivo)
                self.nota_facilidade = avaliacao.get("nota_facilidade")

        except (FileNotFoundError, json.JSONDecodeError):
            self.nota_facilidade = None

    def perguntar(self):
        inicio = time.time()
        pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()

        if pergunta == "0":
            return

        if not pergunta:
            print("Digite uma pergunta válida.")
            return

        numeros = re.sub(r"\D", "", pergunta)

        if "@" in pergunta or len(numeros) >= 8:
            print("Atenção: não digite CPF, telefone ou e-mail.")
            print("Reescreva sua pergunta sem dados pessoais.")
            return

        resultados = self.base.buscar(pergunta)

        if not resultados:
            print("\nNão encontrei uma orientação para essa dúvida.")
            print("Tente utilizar outras palavras ou consultar as categorias.")

            tempo = round(time.time() - inicio, 1)

            self.registrar(
                pergunta, None, False, False, 1, tempo
            )
            return

        pontos, orientacao = resultados[0]

        if pontos >= 6:
            confianca = "ALTA"
        else:
            confianca = "MÉDIA"

        print(f"\nConfiança da resposta: {confianca} ({pontos} pontos)")

        orientacao.exibir()

        if len(resultados) > 1:
            print("\nOutras orientações relacionadas:")

            for pontos, alternativa in resultados[1:3]:
                print(f"- {alternativa.titulo} ({pontos} pontos)")

        tentativas = 1
        ajudou = input(
            "\nEssa orientação respondeu sua dúvida? (s/n): "
        ).lower().strip()

        while ajudou not in ["s", "n"]:
            tentativas += 1
            ajudou = input("Digite apenas s ou n: ").lower().strip()

        tempo = round(time.time() - inicio, 1)

        self.registrar(
            pergunta,
            orientacao.id,
            True,
            ajudou == "s",
            tentativas,
            tempo
        )

        print(f"\nAtendimento concluído em {tempo} segundos.")

    def registrar(self, pergunta, orientacao_id, encontrou, ajudou, tentativas, segundos):
        registro = {
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "origem": "terminal",
            "pergunta": pergunta,
            "orientacao_id": orientacao_id,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "segundos": segundos
        }

        self.historico.append(registro)

        try:
            with open("data/historico.json", "w", encoding="utf-8") as arquivo:
                json.dump(self.historico, arquivo, ensure_ascii=False, indent=4)

            print("Atendimento registrado no histórico.")

        except OSError:
            print("Não foi possível salvar o histórico.")

    def navegar(self):
        categorias = self.base.categorias()

        if not categorias:
            print("Nenhuma categoria disponível.")
            return

        while True:
            print("\n===== CATEGORIAS =====")

            for i, categoria in enumerate(categorias, start=1):
                print(f"{i} - {categoria}")

            print("0 - Voltar")

            opcao = input("\nEscolha uma categoria: ").strip()

            if opcao == "0":
                return

            if not opcao.isdigit() or not (1 <= int(opcao) <= len(categorias)):
                print("Opção inválida. Tente novamente.")
                continue

            categoria_escolhida = categorias[int(opcao) - 1]
            orientacoes = self.base.por_categoria(categoria_escolhida)

            while True:
                print(f"\n===== {categoria_escolhida} =====")

                for i, orientacao in enumerate(orientacoes, start=1):
                    print(f"{i} - {orientacao.titulo}")

                print("0 - Voltar")

                escolha = input("\nEscolha uma orientação: ").strip()

                if escolha == "0":
                    break

                if not escolha.isdigit() or not (1 <= int(escolha) <= len(orientacoes)):
                    print("Opção inválida. Tente novamente.")
                    continue

                orientacao_escolhida = orientacoes[int(escolha) - 1]
                orientacao_escolhida.exibir()

    def indicadores(self):
        total = len(self.historico)

        if total == 0:
            print("\nNenhum atendimento registrado.")
            return

        encontrados = sum(
            1 for registro in self.historico
            if registro["encontrou"]
        )

        ajudaram = sum(
            1 for registro in self.historico
            if registro["ajudou"] is True
        )

        tempo_total = sum(
            registro["segundos"] for registro in self.historico
        )

        tentativas_total = sum(
            registro["tentativas"] for registro in self.historico
        )

        nao_resolvidas = sum(
            1 for registro in self.historico
            if registro["ajudou"] is False
        )

        percentual_encontradas = (encontrados / total) * 100

        if encontrados > 0:
            percentual_ajudaram = (ajudaram / encontrados) * 100
        else:
            percentual_ajudaram = 0

        tempo_medio = tempo_total / total
        media_tentativas = tentativas_total / total

        print("\n===== INDICADORES =====")
        print(f"Total de atendimentos: {total}")
        print(f"Perguntas encontradas: {percentual_encontradas:.1f}%")
        print(f"Orientações que ajudaram: {percentual_ajudaram:.1f}%")
        print(f"Tempo médio: {tempo_medio:.1f} segundos")
        print(f"Média de tentativas: {media_tentativas:.1f}")
        print(f"Perguntas não resolvidas: {nao_resolvidas}")

        if self.nota_facilidade is not None:
            print(f"Nota de facilidade: {self.nota_facilidade}/5")
        else:
            print("Nota de facilidade: ainda não avaliada.")

    def exportar_csv(self):
        if not self.historico:
            print("\nNão existem atendimentos para exportar.")
            return

        try:
            with open("data/atendimentos.csv", "w", newline="", encoding="utf-8-sig") as arquivo:
                campos = [
                    "data",
                    "origem",
                    "pergunta",
                    "orientacao_id",
                    "encontrou",
                    "ajudou",
                    "tentativas",
                    "segundos"
                ]

                escritor = csv.DictWriter(
                    arquivo,
                    fieldnames=campos
                )

                escritor.writeheader()
                escritor.writerows(self.historico)

            print("\nHistórico exportado para data/atendimentos.csv!")

        except OSError:
            print("Não foi possível exportar o arquivo CSV.")

    def avaliar_facilidade(self):
        while True:
            nota = input("\nDe 1 a 5, como foi a facilidade de uso? ").strip()

            if nota.isdigit() and 1 <= int(nota) <= 5:
                self.nota_facilidade = int(nota)

                try:
                    with open("data/avaliacao.json", "w", encoding="utf-8") as arquivo:
                        json.dump(
                            {"nota_facilidade": self.nota_facilidade},
                            arquivo,
                            ensure_ascii=False,
                            indent=4
                        )

                    print("Avaliação salva com sucesso!")

                except OSError:
                    print("Não foi possível salvar a avaliação.")

                return

            print("Digite uma nota válida entre 1 e 5.")