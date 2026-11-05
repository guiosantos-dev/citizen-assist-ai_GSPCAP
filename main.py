from base_conhecimento import BaseConhecimento
from assistente import Assistente


def main():
    base = BaseConhecimento("data/base_conhecimento.json")

    assistente = Assistente("Citizen Assist AI", base)

    while True:
        print("\n================================")
        print("       CITIZEN ASSIST AI")
        print("================================")
        print("1 - Fazer uma pergunta")
        print("2 - Navegar por categorias")
        print("3 - Consultar indicadores")
        print("4 - Exportar histórico para CSV")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            assistente.perguntar()

        elif opcao == "2":
            assistente.navegar()

        elif opcao == "3":
            assistente.indicadores()

        elif opcao == "4":
            assistente.exportar_csv()

        elif opcao == "0":
            assistente.avaliar_facilidade()

            print("\n===== RESULTADO FINAL =====")
            assistente.indicadores()
            assistente.exportar_csv()

            print("\nObrigado por utilizar o Citizen Assist AI!")
            break

        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    main()