import time
import secrets #secure way to generate cryptographically strong random numbers and tokens
import string #set of useful constants, such as ascii_letters and digits
import os

def limpar_tela():
    # cls limpa se for windows, clear se não pq ai é linux
    os.system("cls" if os.name == "nt" else "clear")


# ================================
# BANCO (APP + BACKEND SIMPLES)
# ================================
class Banco:  ####### CRIADO A CLASSE BANCO
    def __init__(self): # se inicia e cria a estrutura os dados do cliente
        self.clientes = {
            "123": {"nome": "Cliente Exemplo", "saldo": 1500, "limite": 1000}
        }
        # cria presaque zerado
        self.presaque = {}

    #pre saque precisa do self, user id e valor setado como zero
    def gerar_pre_saque(self, user_id, valor=None):
        # gera um otp de 6 digitos
        otp = ''.join(secrets.choice(string.digits) for _ in range(6))
        # gera um token de 4 digitos
        qr = secrets.token_hex(4)

        # tras a estrutura básica do pre saque
        self.presaque[user_id] = {
            "valor": valor,
            "otp": otp,
            "qr": qr,
            "expira": time.time() + 300,  # 5 min
            "autenticado": False,
            "liberado": False
        }
        # dá as duas opções
        return otp, qr

    # a pessoa tem que dar um dos codigos corretamente dentro de 5 min
    def autenticar(self, user_id, metodo, codigo):
        pre = self.presaque.get(user_id)
        if not pre:
            return False, "Nenhum pré‑saque encontrado."

        if time.time() > pre["expira"]:
            return False, "Pré‑saque expirado."

        if metodo == "QR" and codigo == pre["qr"]:
            pre["autenticado"] = True
            return True, "Autenticado com sucesso via QR Code."

        if metodo == "OTP" and codigo == pre["otp"]:
            pre["autenticado"] = True
            return True, "Autenticado com sucesso via código OTP."

        return False, "Código inválido."

    # sacar o valor
    def liberar(self, user_id, valor):
        pre = self.presaque[user_id]
        cliente = self.clientes[user_id]

        # verifica se há saldo para ser sacado e dentro do limite diário
        if valor > cliente["saldo"]:
            return False, "Saldo insuficiente."
        if valor > cliente["limite"]:
            return False, "Limite diário excedido."

        cliente["saldo"] -= valor
        pre["liberado"] = True
        return True, "Saque autorizado."


# ================================
# ATM COM TELA GUIADA
# ================================
class ATM: #### classe ATM criada
    #tras o self e o banco
    def __init__(self, banco):
        self.banco = banco
        # quantidade de cada nota no ATM para saque
        self.cassetes = {200: 10, 100: 20, 50: 20, 20: 50, 10: 100}

    # tela inicial
    def tela(self, texto):
        limpar_tela()
        print("====================================")
        print("              ATM 24H               ")
        print("====================================")
        print(texto)
        print("====================================")
        time.sleep(0.5)

    # seta resultado como vazio e restante como o valor a ser sacado
    def contar_notas(self, valor):
        resultado = {}
        restante = valor

        # arruma as notas do ATM das maiores para os menores
        for nota, qtd in sorted(self.cassetes.items(), reverse=True):
            # se a nota for 200, vai fazer 454 //200, e dar duas notas
            # a não ser que tenha apenas 1 nota (qtd), ai pega 1 e vai pra proxima nota
            usar = min(restante // nota, qtd)
            if usar > 0:
                resultado[nota] = usar
                # vai diminuindo o valor, ex 454 pra 54
                restante -= usar * nota
        #retorna a quantidade de cada nota
        return resultado if restante == 0 else None

    # tras o self e o usuário
    def sacar(self, user_id):
        # pega as unformações de pré saque
        pre = self.banco.presaque.get(user_id)

        # 1 — Tela inicial
        self.tela("Bem‑vindo!\n\n1 - Saque sem cartão\n2 - Cancelar")
        opc = input("Selecione a opção desejada: ")

        if opc != "1":
            self.tela("Operação cancelada.")
            return

        # 2 — Escolha de método
        self.tela("Selecione o método de autenticação:\n\n1 - QR Code\n2 - Código OTP")
        opc_metodo = input("Opção: ")

        if opc_metodo == "1":
            metodo = "QR"
            codigo = input("Digite o código QR exibido no seu app: ")
        else:
            metodo = "OTP"
            codigo = input("Digite o código OTP exibido no seu app: ")

        # return True, "Autenticado com sucesso!"
        ok, msg = self.banco.autenticar(user_id, metodo, codigo)
        self.tela(msg)
        if not ok:
            input("\nPressione ENTER para voltar...")
            return

        # 3 — Valor
        valor = pre["valor"]
        if valor:
            self.tela(f"O valor solicitado no app foi: R$ {valor}\n1 - Confirmar\n2 - Cancelar")
            confirm = input("Opção: ")
            if confirm != "1":
                self.tela("Operação cancelada.")
                return
        else:
            # muda o valor que foi colocado no app
            self.tela("Digite o valor desejado para saque:")
            valor = int(input("Valor: R$ "))
            if valor % 10 != 0:
                # porque se não não tem nota pra ele
                self.tela("Valor deve ser múltiplo de 10.")
                return

        # 4 — Autorização
        # se ok, libera o dinheiro
        ok, msg = self.banco.liberar(user_id, valor)
        self.tela(msg)
        if not ok:
            input("\nPressione ENTER para voltar...")
            return

        # 5 — Contagem de notas
        cedulas = self.contar_notas(valor)
        if not cedulas:
            self.tela("Desculpe, este ATM não possui notas suficientes.")
            return

        texto = "Contando notas...\n\n"
        for n, q in cedulas.items():
            texto += f"{q} nota(s) de R$ {n}\n"

        self.tela(texto)
        time.sleep(1.5)

        # 6 — Entrega
        self.tela("Por favor, retire seu dinheiro no compartimento abaixo.")
        time.sleep(2)

        # 7 — Finalização
        self.tela("Operação concluída com sucesso!\nObrigado por utilizar nosso ATM.")
        input("\nPressione ENTER para finalizar...")


# ================================
# SIMULAÇÃO COMPLETA
# ================================
banco = Banco()
atm = ATM(banco)

# APP cria pré-saque
print("=== APP DO CLIENTE ===")
otp, qr = banco.gerar_pre_saque("123", valor=380)
print(f"Pré-saque criado!")
print(f"OTP: {otp}")
print(f"QR Token: {qr}")
input("\nPressione ENTER para ir ao ATM...")

atm.sacar("123")