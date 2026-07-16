import os
import sys
import time

import config

pular_dialogo = False


def definir_modo_rapido(ativo):
    global pular_dialogo
    pular_dialogo = ativo


def espera(segundos):
    if not pular_dialogo:
        time.sleep(segundos)


def digitar(texto):
    for letra in texto:
        sys.stdout.write(letra)
        sys.stdout.flush()
        time.sleep(0 if pular_dialogo else 0.04)
    print()


def menu_seguro(pergunta, opcoes_validas):
    while True:
        try:
            escolha = int(input(pergunta))
            if escolha in opcoes_validas:
                return escolha
            print(f"Opção inválida! Escolha entre: {opcoes_validas}")
        except ValueError:
            print("Erro! Digite apenas o NÚMERO correspondente à sua escolha.")


def limpar_tela():
    if config.LIMPAR_TELA_ENTRE_TURNOS:
        os.system("cls" if os.name == "nt" else "clear")
