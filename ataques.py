import random

import config
import utils
import unidade


def ataque_rifle(atacante, defensor):
    dados = config.DADOS_LADOS[atacante["lado_id"]]
    dano = random.randint(1, 20) if atacante["lado_id"] == 1 else random.randint(1, 17)
    print(f"A infantaria dispara o {dados['rifle_nome']}!")
    utils.espera(2)
    dano = unidade.dano_com_buff(defensor, dano)

    if dano > 18:
        print(f"Tiro crítico! Causou {dano} de dano severo.")
    elif dano < 5:
        print(f"Erro de mira! O disparo só causou {dano} de dano por estilhaços.")
    else:
        print(f"O disparo acertou o alvo, causando {dano} de dano.")

    unidade.aplicar_dano(defensor, dano)
    unidade.consumir_municao(atacante, "rifle")
    usos = unidade.usos_restantes(atacante, "rifle")
    print(f"Ainda dá pra atirar mais {usos} vez(es) com o rifle antes de precisar de munição.")
    utils.espera(1.8)


def ataque_submetralhadora(atacante, defensor):
    dados = config.DADOS_LADOS[atacante["lado_id"]]
    faixa = (1, 7) if atacante["lado_id"] == 1 else (1, 5)
    print(f"Rajada de {dados['submetralhadora_nome']}!")
    dano_total = 0
    for tiro in range(1, 5):
        dano_tiro = random.randint(*faixa)
        dano_total += dano_tiro
        print(f"  Tiro {tiro}: {dano_tiro} de dano")
        utils.espera(0.6)
    dano_total = unidade.dano_com_buff(defensor, dano_total)
    print(f"A rajada causou {dano_total} de dano no total.")
    unidade.aplicar_dano(defensor, dano_total)
    unidade.consumir_municao(atacante, "smg")
    usos = unidade.usos_restantes(atacante, "smg")
    print(f"Ainda dá pra atirar mais {usos} vez(es) com a submetralhadora antes de precisar de munição.")
    utils.espera(1.8)


def usar_suporte_aereo(atacante, defensor):
    dados = config.DADOS_LADOS[atacante["lado_id"]]
    dano = random.randint(*config.DANO_SUPORTE_AEREO)
    print(f"O {dados['suporte_nome']} sobrevoa o campo de batalha!")
    utils.espera(2)
    dano = unidade.dano_com_buff(defensor, dano)
    print(f"O ataque aéreo causa {dano} de dano imediato.")
    utils.espera(1.5)
    unidade.aplicar_dano(defensor, dano)
    defensor["efeito_incendiario_restante"] = config.DURACAO_INCENDIARIO
    print("Incêndios se espalham na posição inimiga — dano contínuo nas próximas rodadas.")
    utils.espera(1.5)
