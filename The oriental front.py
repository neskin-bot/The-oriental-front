import random
import time
import sys

pular_dialogo = False

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
            
def espera(segundos):
    if not pular_dialogo:
        time.sleep(segundos)

def digitar(texto):
    for letra in texto:
        sys.stdout.write(letra)
        sys.stdout.flush()
        time.sleep(0 if pular_dialogo else 0.04)

print("Selecione o modo de exibição:")
print("1- Modo Immersivo (Com pausas e efeitos)")
print("2- Modo Rapido (Texto instantâneo)")
modo = menu_seguro("Escolha: ", [1, 2])

if modo == 2:
    pular_dialogo = True

digitar("Qualquer pessoa que já tenha olhado nos olhos vidrados de um soldado")
print()
digitar("morrendo no campo de batalha pensará muito antes de iniciar uma guerra.")
espera(2)
print()
digitar("-Otto von Bismarck.")
print()
espera(2)
print("✠-----------------------------------------------✠")
print("╔╦╗┬ ┬┌─┐  ┌─┐┬─┐┬┌─┐┌┐┌┌┬┐┌─┐┬    ┌─┐┬─┐┌─┐┌┐┌┌┬┐")
print(" ║ ├─┤├┤   │ │├┬┘│├┤ │││ │ ├─┤│    ├┤ ├┬┘│ ││││ │")
print(" ╩ ┴ ┴└─┘  └─┘┴└─┴└─┘┘└┘ ┴ ┴ ┴┴─┘  └  ┴└─└─┘┘└┘ ┴")
print("☭-----------------------------------------------☭")
espera(2)
print()
digitar("Bem vindo ao The oriental front.")
print()
print()
espera(2)
digitar("Neste jogo, assuma o lado alemão ou soviético no front oriental")
print()
digitar("em um jogo de batalha por turnos.")
print()
espera(3)
print()
print("Deseja ler o contexto histórico antes de começar?")
espera(1)
print("1 - Sim, desejo ler o contexto histórico.")
espera(1)
print("2 - Não, quero ir direto para a batalha.")
espera(1)
print()
escolha_intro = menu_seguro("Digite o número correspondente à sua escolha: ", [1, 2])
if escolha_intro == 1:
    digitar(". . . .")
    print()
    espera(2)
    digitar("O FRONT ORIENTAL")
    print()
    espera(2)
    digitar("22 de Junho de 1941")
    print()
    print()
    espera(2)
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
    espera(2)
    input("\nPressione ENTER para continuar para a seleção de tropas...")

print()
# o usuaria irá escolher entre o lado alemão ou o lado soviético
digitar("Escolha o seu lado nesta guerra")
espera(2)
print()
print()
print("1 - Lado Alemão")
print()
espera(2)
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
        espera(2)
        print()
        print("Seu pelotão é a 6ª divisão de infantaria e possui 100 de vida")
        print("Seu armamento é o rifle Kar98k e a submetralhadora MP-40")
        print("Seu suporte é o avião de ataque JU-87 Stuka que o dano maximo é de 45")
        print()
    case 2:
        print("Você escolheu o lado soviético.")
        espera(2)
        print()
        print("Seu pelotão é a 13ª divisão de fuzileiros da guarda e possui 120 de vida")
        print("Seu armamento é o rifle Mosin Nagant e a submetralhadora PPSH-41")
        print("Seu suporte é o avião de ataque IL-2 que o dano maximo é de 45")
        print("O lado soviético tem um buff de 25% de chance de segurar metade do dano inimigo")
        print()
espera(10)


print("A Batalha vai começar!")
espera(3)
print()
print("A tropa alemã avança para a linha de frente para o primeiro ataque")
espera(3)

while hp_alemao > 0 and hp_sovietico > 0:
 print(f"\n| --- Turno {turno} --- |")
 if lado == 2:
     print("O pelotão alemão se posiciona na linha de frente. . .")
     print()
 espera(3)
 if lado == 1:
     print("1- Atacar com rifle Kar98k")
     print("2- Atacar usando submetralhadora MP-40")
     if turno >= 5:
         print("3- Chamar o suporte aéreo Stuka")
         
     escolha_ataque = menu_seguro("Digite a sua escolha: ", [1, 2, 3])
     print()
     if escolha_ataque == 3 and turno < 5:
         print("O suporte Stuka ainda não está disponível!")
         

    
 else: 
     if turno >= 5:
         escolha_ataque = random.randint(1, 3)
     else:
         escolha_ataque = random.randint(1, 2)

 if escolha_ataque == 1:
     dano = random.randint(1, 20)
     print("A infantaria alemã dispara seus rifles Kar98k!\n")
     espera(4)
     if random.randint(1, 100) <= 25 and escolha_ataque == 1:
         print("A tropa soviética se protegeu! O dano foi reduzido pela metade")
         dano = dano // 2

     if dano > 18 and escolha_ataque == 1:
         print("Tiro crítico")
         espera(1)
         print("Os tiros da tropa alemã causou dano severo de", dano, "de dano")
     elif dano < 5:
        print("Erro fatal para as tropas alemãs!")
        print("Os tiros da tropa alemã erraram o alvo, causando apenas", dano, "de dano por estilhaços")
     elif dano >= 5 and dano <= 18:
         print("Os tiros da tropa alemã acertaram o alvo, causando", dano, "de dano")
<<<<<<< HEAD
     hp_sovietico = max(0, hp_sovietico - dano)
=======
     hp_sovietico -= dano
>>>>>>> 52c75644c852d121327ba67dc8d84c1bb2893520
     print(f"A vida do pelotão soviético é de {hp_sovietico}")
     print()
       
 elif escolha_ataque == 2:
     print("\nA infantaria alemã avança atirando em rajada com as suas submetralhadoras MP-40!")

     dano_total = 0

<<<<<<< HEAD
     for tiro in range(1, 5):
=======
     for tiro in range(1, 7):
>>>>>>> 52c75644c852d121327ba67dc8d84c1bb2893520
        dano_tiro = random.randint(1, 7)
        dano_total += dano_tiro
        print(f"Tiro {tiro} acertou! Causou {dano_tiro} de dano")
        espera(1)

     print(f"\nA rajada do pelotão alemão causou {dano_total} de dano")

<<<<<<< HEAD
     hp_sovietico = max(0, hp_sovietico - dano_total)
=======
     hp_sovietico -= dano_total
>>>>>>> 52c75644c852d121327ba67dc8d84c1bb2893520

     print(f"A vida do pelotão soviético é de {hp_sovietico}")

 elif escolha_ataque == 3:
     dano = random.randint(35, 50)
     print("Se escuta um apito no céu! O Stuka mergulha sobre as linhas soviéticas!")
     espera(3)
     print(f"O Stuka solta suas bombas sobre as tropas soviéticas causando {dano} de dano!")
     espera(3)
<<<<<<< HEAD
     hp_sovietico = max(0, hp_sovietico - dano)
     print(f"A vida do pelotão soviético é de {hp_sovietico}")
=======
     hp_sovietico -= dano
     print(f"A vida do pelotão alemão é de {hp_alemao}")
>>>>>>> 52c75644c852d121327ba67dc8d84c1bb2893520
 if hp_sovietico <= 0:
     break
 print("O pelotão soviético se prepara para contra-atacar. . .")
 espera(3)
 print()
 if lado == 2:
        print("1- Atacar com rifle Mosin Nagant")
        print("2- Atacar com submetralhadora PPSH-41")
        if turno >= 5:
            print("3- Chamar o suporte aéreo IL-2")
            
        escolha_ataque = menu_seguro("Digite a sua escolha: ", [1, 2, 3])
        if escolha_ataque == 3 and turno < 5:
            print("O suporte IL-2 ainda não está disponível!")
 else:
     if turno >= 5:
         escolha_ataque = random.randint(1, 3)
     else:
         escolha_ataque = random.randint(1, 2)
 if escolha_ataque == 1:
     dano = random.randint(1,17)
     print("A infantaria soviética dispara seus rifles Mosin Nagant!")
     espera(3)
     if dano > 18:
         print("Tiro crítico")
         espera(2)
         print("Os tiros da tropa soviética causou dano severo de", dano, "de dano")
     elif dano < 5:
         print("Erro fatal para as tropas soviéticas!")
         print("Os tiros da tropa soviética erraram o alvo, causando apenas", dano, "de dano por estilhaços")
     else:
         print(f"Os tiros da tropa soviética acertam o alvo, causando {dano} de dano")
<<<<<<< HEAD
     hp_alemao = max(0, hp_alemao - dano)
=======
     hp_alemao -= dano
>>>>>>> 52c75644c852d121327ba67dc8d84c1bb2893520
     print(f"A vida do pelotão alemão é de {hp_alemao}")
     espera(4)
 elif escolha_ataque == 2:
     print("\nA infantaria soviética avança atirando em rajada com as suas submetralhadoras PPSH-41!")

     dano_total = 0

     for tiro in range(1, 5):
        dano_tiro = random.randint(1, 5)
        dano_total += dano_tiro
        print(f"Tiro {tiro} acertou! Causou {dano_tiro} de dano")
        espera(1)

     print(f"\nA rajada do pelotão soviético causou {dano_total} de dano")

<<<<<<< HEAD
     hp_alemao = max(0, hp_alemao - dano_total)
=======
     hp_alemao -= dano_total
>>>>>>> 52c75644c852d121327ba67dc8d84c1bb2893520

     print(f"A vida do pelotão alemão é de {hp_alemao}")

 elif escolha_ataque == 3:
     dano = random.randint(30, 45)
     print("Se escuta um rugido no céu! O IL-2 se posiciona para atacar a tropa alemã!")
     espera(3)
     print(f"O IL-2 atira uma rajada com os seus canhões de 20mm na tropa alemã, causando {dano} de dano!")
     espera(3)
<<<<<<< HEAD
     hp_alemao = max(0, hp_alemao - dano)
=======
     hp_alemao -= dano
>>>>>>> 52c75644c852d121327ba67dc8d84c1bb2893520
     print(f"A vida do pelotão alemão é de {hp_alemao}")
 if hp_alemao <= 0:
     break
 turno += 1
print("\n--- FIM DA BATALHA ---")
espera(3)
if hp_alemao > hp_sovietico:
    print("VITÓRIA ALEMÃ!")
    espera(2)
    print("O pelotão alemão conseguiu romper as linhas de defesa soviéticas e conquistou a vitória!")
else:
    print("VITÓRIA SOVIÉTICA!")
    espera(2)
    print("O pelotão soviético resistiu bravamente e derrotou as forças invasoras alemãs, garantindo a vitória soviética!")
     

