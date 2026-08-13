import random

import config
import unidade
import tanque as modulo_tanque


def escolher_pular_ou_cobertura(unidade_atual, oponente, permitir_pular_vez=True):
    """Quando o bot decide não gastar pontos nessa rodada, ele escolhe entre
    pular a vez (ganha pontos extras, melhor quando não há ameaça à vista) e
    buscar cobertura (sem bônus, mas reduz o próximo dano — melhor quando a
    vida já não está cheia ou o inimigo tem munição pra um golpe forte).
    permitir_pular_vez=False é usado quando o tanque está ativo, já que não
    faz sentido "reagrupar" com o bônus de pular a vez estando blindado."""
    if not permitir_pular_vez:
        return "cobertura"
    vida_pct = unidade.vida_atual_principal(unidade_atual) / unidade.vida_maxima_principal(unidade_atual)
    ameaca_grande = (
        oponente["tanque_ativo"]
        or unidade.pode_pagar(oponente, "suporte_aereo")
        or unidade.pode_pagar(oponente, "chamar_tanque")
    )
    if vida_pct < 0.6 or ameaca_grande:
        return "cobertura"
    return "pular_vez"


def escolher_acao_bot(unidade_atual, oponente, turno):
    if unidade_atual["tanque_ativo"]:
        if not modulo_tanque.tanque_pode_atacar(unidade_atual):
            if (unidade.vida_atual_principal(unidade_atual) < unidade_atual["vida_maxima"] * 0.4
                    and unidade.pode_pagar(unidade_atual, "suprimento_medico")):
                return "suprimento_medico"
            return escolher_pular_ou_cobertura(unidade_atual, oponente, permitir_pular_vez=False)

        if oponente["tanque_ativo"]:
            return "tanque_perfurante"
        return "tanque_explosivo" if random.random() < 0.7 else "tanque_metralhadora"

    vida_pct = unidade_atual["vida_atual"] / unidade_atual["vida_maxima"]
    if vida_pct < 0.3 and unidade.pode_pagar(unidade_atual, "suprimento_medico") and random.randint(1, 100) <= 60:
        return "suprimento_medico"

    # a partir daqui, cada "quero fazer algo grande" é separado de "tenho
    # pontos pra isso" — se o bot queria mas não pode pagar ainda, ele
    # economiza de propósito em vez de gastar os pontos em ataques pequenos.

    quer_chamar_tanque = not oponente["tanque_ativo"] and turno >= 3 and random.randint(1, 100) <= 25
    if quer_chamar_tanque:
        if unidade.pode_pagar(unidade_atual, "chamar_tanque"):
            return "chamar_tanque"
        return escolher_pular_ou_cobertura(unidade_atual, oponente)

    quer_suporte_aereo = turno >= 4 and random.randint(1, 100) <= 30
    if quer_suporte_aereo:
        if unidade.pode_pagar(unidade_atual, "suporte_aereo"):
            return "suporte_aereo"
        return escolher_pular_ou_cobertura(unidade_atual, oponente)

    if oponente["tanque_ativo"]:
        if unidade.pode_pagar(unidade_atual, "anti_tank") and unidade.tem_municao(unidade_atual, "anti_tank"):
            return "anti_tank"
        if unidade.pode_pagar(unidade_atual, "suprimento_municao_anti_tank"):
            return "suprimento_municao_anti_tank"
        # sem munição nem pontos pra recarregar — atirar com rifle/smg num
        # tanque não adianta quase nada, então prefere economizar a desperdiçar.
        return escolher_pular_ou_cobertura(unidade_atual, oponente)

    if unidade.pode_pagar(unidade_atual, "submetralhadora") and random.randint(1, 100) <= 55:
        if unidade.tem_municao(unidade_atual, "smg"):
            return "submetralhadora"
        if unidade.pode_pagar(unidade_atual, "suprimento_municao_smg"):
            return "suprimento_municao_smg"

    if unidade.pode_pagar(unidade_atual, "rifle"):
        if unidade.tem_municao(unidade_atual, "rifle"):
            return "rifle"
        if unidade.pode_pagar(unidade_atual, "suprimento_municao_rifle"):
            return "suprimento_municao_rifle"

    return escolher_pular_ou_cobertura(unidade_atual, oponente)
