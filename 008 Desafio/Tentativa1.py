'''Desafio:
“Vamos desenvolver um jogo de adivinhação: o computador 'pensa' em um número secreto e o jogador deve adivinhar, recebendo dicas se o palpite é maior ou menor que o número secreto.”  
Decomposição do problema: 
(1) Gerar um número aleatório em uma faixa (por exemplo 1 a 50); 
(2) Inicializar uma variável tentativa do usuário; 
(3) Enquanto a tentativa estiver errada, dar feedback "maior" ou "menor" e pedir nova tentativa; 
(4) Se acertar, parabenizar e encerrar.desafio: '''

from random import randint

secret_Number = randint(1,50)

max = int(input("Insira o número máximo de tentativas:"))
##print(secret_Number)

tentativas = 1

while True:

    try:
        user_Guess = int(input("Send your guess: "))
    except:
        print("Entrada inválida")
        continue

    if user_Guess == secret_Number:
        print('''
    
    Congratualizations! You got it right!''')
        break

    elif user_Guess < secret_Number:
        print(f'''
    Tentativa: {tentativas}
    The secret number is greater than {user_Guess}''')
    
    elif user_Guess > secret_Number:
        print(f'''
    Tentativa: {tentativas}
    The secret number is less than {user_Guess}''')
