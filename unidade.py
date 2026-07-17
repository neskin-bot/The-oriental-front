import random

import config
import utils


def criar_unidade(lado_id):
    dados = config.DADOS_LADOS[lado_id]
    return {
        "lado_id": lado_id,
        "nome": dados["nome"],
        "vida_atual": dados["vida_maxima"],
        "vida_maxima": dados["vida_maxima"],
        "pontos": config.PONTOS_INICIAIS,
        "municao_rifle": config.MUNICAO_MAXIMA_RIFLE,
        "municao_smg": config.MUNICAO_MAXIMA_SMG,
        "municao_anti_tank": config.MUNICAO_MAXIMA_ANTI_TANK,
        "efeito_incendiario_restante": 0,
        "tanque_ativo": False,
        "tanque_recem_chamado": False,
        "tanque_vida": 0,
        "tanque_cooldown": 0,
        "em_cobertura": False,
        "fugiu": False,
    }


def nome_alvo_principal(unidade):
    dados = config.DADOS_LADOS[unidade["lado_id"]]
    if unidade["tanque_ativo"]:
        return dados["tanque_nome"]
    return dados["nome"]


def vida_atual_principal(unidade):
    return unidade["tanque_vida"] if unidade["tanque_ativo"] else unidade["vida_atual"]


def vida_maxima_principal(unidade):
    return config.TANQUE_VIDA if unidade["tanque_ativo"] else unidade["vida_maxima"]


def unidade_derrotada(unidade):
    if unidade["tanque_ativo"]:
        return False
    return unidade["vida_atual"] <= 0


def pode_pagar(unidade, acao):
    return unidade["pontos"] >= config.CUSTOS_ACAO[acao]


def pagar(unidade, acao):
    unidade["pontos"] -= config.CUSTOS_ACAO[acao]


def ganhar_pontos_turno(unidade):
    unidade["pontos"] += config.GANHO_PONTOS_TURNO


def aplicar_dano(unidade, dano, pular_reducao_blindagem=False):
    """Aplica dano a uma unidade.

    pular_reducao_blindagem=True é usado pelas armas feitas pra furar blindagem
    (tiro perfurante do tanque, tiro explosivo do tanque e a arma antitanque de
    infantaria) — essas já calculam o dano certo sozinhas. Qualquer outra arma
    (rifle, submetralhadora, suporte aéreo, metralhadora do tanque) causa só
    uma fração do dano quando o alvo está com o tanque ativo, já que não tem
    poder de fogo real contra um blindado.
    """
    dados = config.DADOS_LADOS[unidade["lado_id"]]
    dano_efetivo = dano

    if unidade["tanque_ativo"] and not pular_reducao_blindagem:
        dano_reduzido = max(0, round(dano_efetivo * config.FATOR_DANO_ARMA_NORMAL_VS_TANQUE))
        print(f"A blindagem do {dados['tanque_nome']} absorve quase todo o impacto "
              f"(dano reduzido de {dano_efetivo} para {dano_reduzido}).")
        dano_efetivo = dano_reduzido

    dano_efetivo = consumir_cobertura_se_ativa(unidade, dano_efetivo)

    if unidade["tanque_ativo"]:
        unidade["tanque_vida"] = max(0, unidade["tanque_vida"] - dano_efetivo)
        if unidade["tanque_vida"] == 0:
            print(f"O {dados['tanque_nome']} foi destruído! O {dados['nome']} volta a estar exposto.")
            utils.espera(1.5)
            unidade["tanque_ativo"] = False
    else:
        unidade["vida_atual"] = max(0, unidade["vida_atual"] - dano_efetivo)

    return dano_efetivo


def ativar_cobertura(unidade):
    unidade["em_cobertura"] = True


def consumir_cobertura_se_ativa(unidade, dano):
    """Se a unidade buscou cobertura, essa proteção vale pro próximo dano que
    ela receber (e só esse) — depois disso a cobertura se esgota, tenha
    funcionado ou não."""
    if not unidade["em_cobertura"]:
        return dano

    unidade["em_cobertura"] = False

    if random.randint(1, 100) <= config.PROBABILIDADE_COBERTURA_FALHA:
        print(f"{unidade['nome']} estava em cobertura, mas o ataque encontrou uma brecha!")
        return dano

    dano_reduzido = max(0, round(dano * (1 - config.FATOR_REDUCAO_COBERTURA)))
    print(f"A cobertura de {unidade['nome']} funcionou! Dano reduzido de {dano} para {dano_reduzido}.")
    return dano_reduzido


def aplicar_cura(unidade, cura):
    if unidade["tanque_ativo"]:
        unidade["tanque_vida"] = min(config.TANQUE_VIDA, unidade["tanque_vida"] + cura)
    else:
        unidade["vida_atual"] = min(unidade["vida_maxima"], unidade["vida_atual"] + cura)


def chance_buff_defesa(unidade):
    dados = config.DADOS_LADOS[unidade["lado_id"]]
    return random.randint(1, 100) <= dados["buff_defesa"] * 100


def dano_com_buff(unidade_defensora, dano):
    if chance_buff_defesa(unidade_defensora):
        print("A trincheira soviética resistiu! O dano foi reduzido pela metade.")
        return dano // 2
    return dano


def tem_municao(unidade, arma):
    if arma == "rifle":
        return unidade["municao_rifle"] >= config.MUNICAO_GASTA_RIFLE
    if arma == "smg":
        return unidade["municao_smg"] >= config.MUNICAO_GASTA_SMG
    if arma == "anti_tank":
        return unidade["municao_anti_tank"] >= config.MUNICAO_GASTA_ANTI_TANK
    return True


def usos_restantes(unidade, arma):
    if arma == "rifle":
        return unidade["municao_rifle"] // config.MUNICAO_GASTA_RIFLE
    if arma == "smg":
        return unidade["municao_smg"] // config.MUNICAO_GASTA_SMG
    if arma == "anti_tank":
        return unidade["municao_anti_tank"] // config.MUNICAO_GASTA_ANTI_TANK
    return 0


def usos_maximos(arma):
    if arma == "rifle":
        return config.MUNICAO_MAXIMA_RIFLE // config.MUNICAO_GASTA_RIFLE
    if arma == "smg":
        return config.MUNICAO_MAXIMA_SMG // config.MUNICAO_GASTA_SMG
    if arma == "anti_tank":
        return config.MUNICAO_MAXIMA_ANTI_TANK // config.MUNICAO_GASTA_ANTI_TANK
    return 0


def consumir_municao(unidade, arma):
    if arma == "rifle":
        unidade["municao_rifle"] -= config.MUNICAO_GASTA_RIFLE
    elif arma == "smg":
        unidade["municao_smg"] -= config.MUNICAO_GASTA_SMG
    elif arma == "anti_tank":
        unidade["municao_anti_tank"] -= config.MUNICAO_GASTA_ANTI_TANK


def recarregar_municao(unidade, arma):
    if arma == "rifle":
        unidade["municao_rifle"] = config.MUNICAO_MAXIMA_RIFLE
    elif arma == "smg":
        unidade["municao_smg"] = config.MUNICAO_MAXIMA_SMG
    elif arma == "anti_tank":
        unidade["municao_anti_tank"] = config.MUNICAO_MAXIMA_ANTI_TANK
        