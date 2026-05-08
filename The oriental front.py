import random
import time
#criar um algorítimo que
# apresenta o nome do jogo
# sauda o jogador
# informa oque o jogo fará
# lista os personagens (nome, quantidade de vida, armamentos e suportes)
# lista 2 personagens que o jogador podera escolher, cada um com as suas caracteristicas
# informa quem vai atacar primeiro
# informa qual ataque ele vai usar
# informa o quanto de vida que ele tirou
# informa que o segundo personagem vai atacar 
# informa qual ataque ele vai usar
# informa o quanto de vida que ele tirou
# lista os personagens (nome e quantidade de vida atualizado)
# fala qual deles ganhou (quem ao final da partida tiver mais vida)
# tematica da segunda guerra mundial com o foco no front oriental
# sistema de ataque e de vida funcionais
# ✠ Lado Alemão (6ª Divisão de Infantaria):
# hp 100
# armamento: Kar98k
# suporte: Stuka
# ☭ Lado Soviético (13ª Divisão de Fuzileiros de Guarda):
# hp 120
# armamento: Mosin Nagant
# suporte IL-2
# os suportes só estarão disponiveis após 5 turnos
# o ataque do armamento alemão pode variar de 15 a 20 de dano
# o ataque do armamento soviético pode variar de 12 a 17 de dano
# o lado soviético tem um buff de 25% de chance de segurar metade do dano recebido a cada ataque alemão
#se o usuario escolheu o lado alemão, ele pode escolher entre atacar com o kar98k ou chamar o stuka
#se o usuario escolheu o lado soviético, ele ira esperar o ataque alemão, após o ataque, ele pode escolher entre atacar com o Mosin Nagant ou chamar o IL-2
#o sistema de dano e de vida deve ser funcional, ou seja, o dano deve ser subtraido da vida do personagem e a vida deve ser atualizada a após cada ataque
#o jogo deve continuar até que um dos personagens tenha a vida igual ou menor a 0, ou seja, até que um dos personagens morra
# o jogo deve informar o vencedor, ou seja, o personagem que tiver a vida maior que 0 ao final da partida    


print("|----------------------------------------|")
print("|        ✠ The oriental front ☭          |")
print("|----------------------------------------|")
time.sleep(2)
print()
print("Bem vindo ao The oriental front")
time.sleep(2)
print("Neste jogo, assuma o lado alemão ou soviético no front oriental")
time.sleep(3)
print()
# o usuaria irá escolher entre o lado alemão ou o lado soviético
print("Escolha o seu lado")
print("1 - Lado Alemão")
print("2 - Lado Soviético")
print()

 #valores iniciais
hp_alemao = 100
hp_sovietico = 120
turno = 1
    
lado = int(input("Digite a sua escolha: "))
match lado:
    case 1:
        print("Você escolheu o lado alemão")
        print()
        print("Seu pelotão é a 6ª divisão de infantaria e possui 100 de vida")
        print("Seu armamento é o rifle Kar98k")
        print("Seu suporte é o avião de ataque Stuka")
        print()
    case 2:
        print("Você escolheu o lado soviético")
        print()
        print("Seu pelotão é a 13ª divisão de fuzileiros da guarda e possui 120 de vida")
        print("Seu armamento é o rifle Mosin Nagant")
        print("Seu suporte é o avião de ataque IL-2")
        print("O lado soviético tem um buff de 25% de chance de segurar metade do dano inimigo")
        print()
time.sleep(10)

print("A Batalha vai começar!")
time.sleep(2)
print()
print("O pacto Molotov-Ribbentrop foi quebrado!")
time.sleep(3)
print("A operação Barbarossa começou")
time.sleep(2)
print()
print("A tropa alemã avança para a linha de frente para o primeiro ataque")
if lado == 2:
    print("O pelotão alemão se posiciona na linha de frente e. . .")

time.sleep(2)
print()
if lado == 1:
    print("1- Atacar com rifle Kar98k")
    if turno >= 5:
        print("2- Chamar o suporte aéreo Stuka")
        escolha_ataque = int(input("Digite a sua escolha: "))
else: #se o jogador for soviético, o alemão é o BOT
    if turno >= 5:
        escolha_ataque = random.randint(1, 2)
    else:
        escolha_ataque = 1
# calculo do dano baseado na escolha
if escolha_ataque == 1:
    dano = random.randint(15, 20)
    if dano > 18 and escolha_ataque == 1:
        print("Tiro crítico")
        print("Os tiros da tropa alemã causou dano severo de", dano, "de dano")
    if random.randint(1, 100) <= 25 and escolha_ataque == 1 and lado == 2:
        print("O lado soviético se protegeu! O dano foi reduzido pela metade")
        dano = dano // 2
    hp_sovietico -= dano
    print(f"Vida atual do pelotão soviético: {hp_sovietico}")







