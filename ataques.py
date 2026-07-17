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

def ataque_anti_tank(atacante, defensor):
    """Arma antitanque de infantaria (Panzerfaust / PTRS-41).
    Dano cheio (20-30) só contra um tanque ativo; 10% de chance de crítico
    (40 de dano fixo + incêndio no tanque por algumas rodadas). Contra
    infantaria, o dano é baixo (5-10) e não incendeia nada."""
    dados = config.DADOS_LADOS[atacante["lado_id"]]
    if defensor["tanque_ativo"]:
        dano = random.randint(20, 30)
        if random.random() < 0.1:
            dano = 40
            defensor["efeito_incendiario_restante"] = config.DURACAO_INCENDIARIO_ANTITANQUE
            print(f"O {dados['arma_anti_tank_nome']} acerta o tanque inimigo com um tiro crítico! "
                  f"Causando {dano} de dano e incendiando o tanque!")
        else:
            print(f"O {dados['arma_anti_tank_nome']} acerta o tanque inimigo, causando {dano} de dano.")
    else:
        dano = random.randint(5, 10)
        print(f"O {dados['arma_anti_tank_nome']} atira no inimigo, mas não é eficaz contra unidades "
              f"não blindadas. Causando apenas {dano} de dano.")

    utils.espera(2)
    dano = unidade.dano_com_buff(defensor, dano)
    unidade.aplicar_dano(defensor, dano, pular_reducao_blindagem=True)
    unidade.consumir_municao(atacante, "anti_tank")
    usos = unidade.usos_restantes(atacante, "anti_tank")
    print(f"Ainda dá pra atirar mais {usos} vez(es) com a arma antitanque antes de precisar de munição.")
    utils.espera(1.8)

def usar_suporte_aereo(atacante, defensor):
    dados = config.DADOS_LADOS[atacante["lado_id"]]
    if defensor["tanque_ativo"]:
        dano = random.randint(*config.DANO_SUPORTE_AEREO_VS_TANQUE)
    else:
        dano = random.randint(*config.DANO_SUPORTE_AEREO)
    print(f"O {dados['suporte_nome']} sobrevoa o campo de batalha!")
    utils.espera(2)
    dano = unidade.dano_com_buff(defensor, dano)
    print(f"O ataque aéreo causa {dano} de dano imediato.")
    utils.espera(1.5)
    unidade.aplicar_dano(defensor, dano, pular_reducao_blindagem=True)
    defensor["efeito_incendiario_restante"] = config.DURACAO_INCENDIARIO
    print("Incêndios se espalham na posição inimiga — dano contínuo nas próximas rodadas.")
    utils.espera(1.5)
    