
class Orientacao:
    def __init__(self, dados):
        self.id = dados["id"]
        self.categoria = dados["categoria"]
        self.titulo = dados["titulo"]
        self.palavras_chave = dados["palavras_chave"]
        self.resposta = dados["resposta"]
        self.documentos = dados["documentos"]
        self.onde = dados["onde"]
        self.fonte = dados["fonte"]
        self.verificado_em = dados["verificado_em"]

    def exibir(self):
        print("\n" + self.titulo)
        print("-" * 40)
        print(self.resposta)

        print("\nDocumentos necessários:")
        for documento in self.documentos:
            print(f"- {documento}")

        print(f"\nOnde resolver: {self.onde}")
        print(f"Fonte: {self.fonte}")
        print(f"Verificado em: {self.verificado_em}")
        print("\nEste assistente não é um canal oficial.")
