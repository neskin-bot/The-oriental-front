import random

import config
import utils
import unidade


def chamar_tanque(unidade_atual):
    dados = config.DADOS_LADOS[unidade_atual["lado_id"]]
    unidade_atual["tanque_ativo"] = True
    unidade_atual["tanque_vida"] = config.TANQUE_VIDA
    unidade_atual["tanque_recem_chamado"] = True
    unidade_atual["tanque_cooldown"] = 0
    unidade_atual["tanque_bloqueado_por_cooldown"] = False
    print(f"O {dados['tanque_nome']} avança e assume a linha de frente!")
    utils.espera(1.2)
    print("Ele ainda está se posicionando — só poderá atacar na próxima rodada.")
    utils.espera(1.5)


def sair_do_tanque(unidade_atual):
    dados = config.DADOS_LADOS[unidade_atual["lado_id"]]
    print(f"A tripulação abandona o {dados['tanque_nome']} e volta a lutar como infantaria.")
    utils.espera(1.3)
    unidade_atual["tanque_ativo"] = False
    unidade_atual["tanque_vida"] = 0
    unidade_atual["tanque_recem_chamado"] = False
    unidade_atual["tanque_cooldown"] = 0
    unidade_atual["tanque_bloqueado_por_cooldown"] = False


def ataque_tanque_metralhadora(atacante, defensor):
    dados = config.DADOS_LADOS[atacante["lado_id"]]
    print(f"O {dados['tanque_nome']} abre fogo com a metralhadora coaxial!")
    dano_total = 0
    for tiro in range(1, 6):
        dano_tiro = random.randint(4, 10)
        dano_total += dano_tiro
        print(f"  Tiro {tiro}: {dano_tiro} de dano")
        utils.espera(0.5)
    dano_total = unidade.dano_com_buff(defensor, dano_total)
    print(f"A rajada do tanque causou {dano_total} de dano no total.")
    unidade.aplicar_dano(defensor, dano_total)
    atacante["tanque_cooldown"] = config.TANQUE_COOLDOWN_RODADAS
    utils.espera(1.8)


def ataque_tanque_perfurante(atacante, defensor):
    dados = config.DADOS_LADOS[atacante["lado_id"]]
    print(f"O {dados['tanque_nome']} dispara um tiro perfurante!")
    utils.espera(1)
    if defensor["tanque_ativo"]:
        dano = random.randint(25, 45)
        print(f"O projétil perfura o blindado inimigo, causando {dano} de dano!")
    else:
        dano = random.randint(2, 6)
        print("Sem um tanque inimigo pra perfurar, o disparo causa só um dano residual.")
    dano = unidade.dano_com_buff(defensor, dano)
    unidade.aplicar_dano(defensor, dano, pular_reducao_blindagem=True)
    atacante["tanque_cooldown"] = config.TANQUE_COOLDOWN_RODADAS
    utils.espera(1.8)


def ataque_tanque_explosivo(atacante, defensor):
    dados = config.DADOS_LADOS[atacante["lado_id"]]
    print(f"O {dados['tanque_nome']} dispara um projétil explosivo!")
    utils.espera(1)
    if not defensor["tanque_ativo"]:
        dano = random.randint(20, 35)
        print(f"A explosão devasta a infantaria inimiga, causando {dano} de dano!")
    else:
        dano = random.randint(2, 6)
        print("Contra um blindado, a explosão causa só um dano residual.")
    dano = unidade.dano_com_buff(defensor, dano)
    unidade.aplicar_dano(defensor, dano, pular_reducao_blindagem=True)
    atacante["tanque_cooldown"] = config.TANQUE_COOLDOWN_RODADAS
    utils.espera(1.8)


def processa_chegada_e_cooldown_tanque(unidade_atual):
    if unidade_atual["tanque_recem_chamado"]:
        unidade_atual["tanque_recem_chamado"] = False
        unidade_atual["tanque_bloqueado_por_cooldown"] = False
        return

    if unidade_atual["tanque_cooldown"] > 0:
        unidade_atual["tanque_bloqueado_por_cooldown"] = True
        unidade_atual["tanque_cooldown"] -= 1
    else:
        unidade_atual["tanque_bloqueado_por_cooldown"] = False


def tanque_pode_atacar(unidade_atual):
    return (unidade_atual["tanque_ativo"]
            and not unidade_atual["tanque_recem_chamado"]
            and not unidade_atual["tanque_bloqueado_por_cooldown"])