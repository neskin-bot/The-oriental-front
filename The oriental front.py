import random
import time
import sys
def menu_seguro(pergunta, opcoes_validas):
    while True:
        try:
            escolha = int(input(pergunta))
            if escolha in opcoes_validas:
                return escolha
            else:
                print(f"Opção inválida! Escolha entre: {opcoes_validas}")
        except ValueError:
             print("Erro! Digite apenas o NÚMERO correspondente à sua escolha.")

def digitar(texto):
    for letra in texto:
        sys.stdout.write(letra)
        sys.stdout.flush()
        time.sleep(0.04)

digitar("Vasculhando arquivos de guerra. . . .")
print()
time.sleep(2)
digitar("Pasta encontrada: ✠  The oriental front ☭")
print()
time.sleep(2)
print("✠-----------------------------------------------✠")
print("╔╦╗┬ ┬┌─┐  ┌─┐┬─┐┬┌─┐┌┐┌┌┬┐┌─┐┬    ┌─┐┬─┐┌─┐┌┐┌┌┬┐")
print(" ║ ├─┤├┤   │ │├┬┘│├┤ │││ │ ├─┤│    ├┤ ├┬┘│ ││││ │")
print(" ╩ ┴ ┴└─┘  └─┘┴└─┴└─┘┘└┘ ┴ ┴ ┴┴─┘  └  ┴└─└─┘┘└┘ ┴")
print("☭-----------------------------------------------☭")
time.sleep(2)
print()
digitar("Bem vindo ao The oriental front.")
print()
print()
time.sleep(2)
digitar("Neste jogo, assuma o lado alemão ou soviético no front oriental")
print()
digitar("em um jogo de batalha por turnos.")
time.sleep(3)
print()
print()
print("Deseja ler o contexto histórico antes de começar?")
time.sleep(1)
print("1 - Sim, desejo ler o contexto histórico.")
time.sleep(1)
print("2 - Não, quero ir direto para a batalha.")
time.sleep(1)
print()
escolha_intro = menu_seguro("Digite o número correspondente à sua escolha: ", [1, 2])
if escolha_intro == 1:
    digitar(". . . .")
    print()
    time.sleep(2)
    digitar("O FRONT ORIENTAL")
    print()
    time.sleep(2)
    digitar("22 de Junho de 1941")
    print()
    print()
    time.sleep(2)
    digitar("Em 22 de junho de 1941, o silêncio da madrugada europeia foi rompido pelo rugido de")
    print()
    digitar("milhares e de canhões alemães. A operação Barbarossa havia começado. Do Mar Báltico até")
    print()
    digitar("o Mar Negro, colunas intermináveis de tanques cruzavam as fronteiras da União Soviética")
    print()
    digitar("enquanto aviões incendiavam cidades e campos. Era o início do Front Oriental da Segunda")
    print()
    digitar("Guerra Mundial, um conflito tão colossal que transformaria rios em linhas de sangue e cidades em")
    print()
    digitar("ruínas fumegantes.")
    print()
    print()
    time.sleep(2)
    input("\nPressione ENTER para continuar para a seleção de tropas...")

print()
# o usuaria irá escolher entre o lado alemão ou o lado soviético
digitar("Escolha o seu lado nesta guerra")
time.sleep(2)
print()
print()
print("1 - Lado Alemão")
print()
time.sleep(2)
print("2 - Lado Soviético")
print()

 #valores iniciais
hp_alemao = 100
hp_sovietico = 120
turno = 1
    
lado = menu_seguro("Digite o número correspondente a sua escolha: ", [1, 2])
match lado:
    case 1:
        print("Você escolheu o lado alemão.")
        time.sleep(2)
        print()
        print("Seu pelotão é a 6ª divisão de infantaria e possui 100 de vida")
        print("Seu armamento principal é o rifle Kar98k que o dano maximo é de 20")
        print("Seu suporte é o avião de ataque JU-87 Stuka que o dano maximo é de 45")
        print()
    case 2:
        print("Você escolheu o lado soviético.")
        time.sleep(2)
        print()
        print("Seu pelotão é a 13ª divisão de fuzileiros da guarda e possui 120 de vida")
        print("Seu armamento é o rifle Mosin Nagant que o dano maximo é de 17")
        print("Seu suporte é o avião de ataque IL-2 que o dano maximo é de 45")
        print("O lado soviético tem um buff de 25% de chance de segurar metade do dano inimigo")
        print()
time.sleep(10)


print("A Batalha vai começar!")
time.sleep(3)
print()
print("A tropa alemã avança para a linha de frente para o primeiro ataque")
time.sleep(3)

while hp_alemao > 0 and hp_sovietico > 0:
 print(f"\n| --- Turno {turno} --- |")
 if lado == 2:
     print("O pelotão alemão se posiciona na linha de frente. . .")
     print()
 time.sleep(3)
 print()
 if lado == 1:
     print("1- Atacar com rifle Kar98k")
     if turno >= 5:
         print("2- Chamar o suporte aéreo Stuka")
         
     escolha_ataque = int(input("Digite a sua escolha: "))
     if escolha_ataque == 2 and turno < 5:
         print("O suporte Stuka ainda não está disponível! Você perdeu o tempo de mira e usou o Kar98k por padrão.")
         escolha_ataque = 1

    
 else: #se o jogador for soviético, o alemão é o BOT
     if turno >= 5:
         escolha_ataque = random.randint(1, 2)
     else:
         escolha_ataque = 1
 # calculo do dano baseado na escolha
 if escolha_ataque == 1:
     dano = random.randint(1, 20)
     print("A infantaria alemã dispara seus rifles Kar98k!")
     print()
     time.sleep(4)
 else:
     dano = random.randint(30, 45)
     print("Se escuta um apito no céu! O Stuka mergulha sobre as linhas soviéticas!")
     time.sleep(3)
     print(f"O Stuka solta suas bombas sobre as tropas soviéticas causando {dano} de dano!")
     time.sleep(3)
 if dano > 18 and escolha_ataque == 1:
     print("Tiro crítico")
     time.sleep(1)
     print("Os tiros da tropa alemã causou dano severo de", dano, "de dano")
 if dano < 5:
    print("Erro fatal para as tropas alemãs!")
    print("Os tiros da tropa alemã erraram o alvo, causando apenas", dano, "de dano por estilhaços")
 if dano >= 5 and dano <= 18:
     print("Os tiros da tropa alemã acertaram o alvo, causando", dano, "de dano")
 if random.randint(1, 100) <= 25 and escolha_ataque == 1:
     print("A tropa soviética se protegeu! O dano foi reduzido pela metade")
     dano = dano // 2
 hp_sovietico -= dano
 print()
 print(f"A vida do pelotão soviético é de {hp_sovietico}")
 print()
 if hp_sovietico <= 0:
     break
 else:
     time.sleep(4)
     print("O pelotão soviético se prepara para contra-atacar. . .")
     time.sleep(3)
     print()
     if lado == 2:
            print("1- Atacar com rifle Mosin Nagant")
            if turno >= 5:
                print("2- Chamar o suporte aéreo IL-2")
                
            escolha_ataque = int(input("Digite a sua escolha: "))
            if escolha_ataque == 2 and turno < 5:
                print("O suporte IL-2 ainda não está disponível! Você perdeu o tempo de mira e usou o Mosin Nagant por padrão.")
                escolha_ataque = 1
     else:
         if turno >= 5:
             escolha_ataque = random.randint(1, 2)
         else:
             escolha_ataque = 1
 if escolha_ataque == 1:
         dano = random.randint(1,17)
         print("A infantaria soviética dispara seus rifles Mosin Nagant!")
         time.sleep(3)
         if dano < 5:
             print("Erro fatal para as tropas soviéticas!")
             print("Os tiros da tropa soviética erraram o alvo, causando apenas", dano, "de dano por estilhaços")
         elif dano > 15:
             print("Tiro crítico")
             time.sleep(2)
             print("Os tiros da tropa soviética causou dano severo de", dano, "de dano")
         elif dano >= 5 and dano <= 15:
             print("Os tiros da tropa soviética acertaram o alvo, causando", dano, "de dano") 
         hp_alemao -= dano
         print(f"A vida do pelotão alemão é de {hp_alemao}")
         time.sleep(4)
 else:
     dano = random.randint(30, 45)
     print("Se escura o rugido de motores no céu! O IL-2 se posiciona para atacar a tropa alemã!")
     time.sleep(3)
     print(f"O IL-2 atira com os seus canhões de 20mm em uma rajada de fogo na tropa alemã causando {dano} de dano!")
     time.sleep(5)
     hp_alemao -= dano
     print(f"A vida do pelotão alemão é de {hp_alemao}")
 turno += 1
print("\n--- FIM DA BATALHA ---")
time.sleep(3)
if hp_alemao > hp_sovietico:
    print("VITÓRIA ALEMÃ!")
    time.sleep(2)
    print("O pelotão alemão conseguiu romper as linhas de defesa soviéticas e conquistou a vitória!")
else:
    print("VITÓRIA SOVIÉTICA!")
    time.sleep(2)
    print("O pelotão soviético resistiu bravamente e derrotou as forças invasoras alemãs, garantindo a vitória soviética!")
     

