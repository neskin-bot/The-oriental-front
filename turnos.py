import random

import config
import utils
import unidade
import ataques
import suprimentos
import tanque as modulo_tanque


def montar_opcoes_disponiveis(unidade_atual):
    opcoes = []
    n = 1

    if unidade_atual["tanque_ativo"]:
        if modulo_tanque.tanque_pode_atacar(unidade_atual):
            for chave, texto in [
                ("tanque_metralhadora", "Rajada de metralhadora do tanque"),
                ("tanque_perfurante", "Tiro perfurante (eficaz contra tanques)"),
                ("tanque_explosivo", "Tiro explosivo (eficaz contra infantaria)"),
            ]:
                opcoes.append((n, chave, f"{texto} — custo {config.CUSTOS_ACAO[chave]}"))
                n += 1
        else:
            opcoes.append((None, None, "O tanque está em cooldown / se posicionando nesta rodada."))
    else:
        if unidade.tem_municao(unidade_atual, "rifle"):
            usos = unidade.usos_restantes(unidade_atual, "rifle")
            texto = f"Atacar com rifle (restam {usos} uso(s)) — custo {config.CUSTOS_ACAO['rifle']}"
            opcoes.append((n, "rifle", texto))
            n += 1
        else:
            opcoes.append((None, None, "Rifle sem munição — chame o caminhão de suprimento."))

        if unidade.tem_municao(unidade_atual, "smg"):
            usos = unidade.usos_restantes(unidade_atual, "smg")
            texto = f"Atacar com submetralhadora (restam {usos} uso(s)) — custo {config.CUSTOS_ACAO['submetralhadora']}"
            opcoes.append((n, "submetralhadora", texto))
            n += 1
        else:
            opcoes.append((None, None, "Submetralhadora sem munição — chame o caminhão de suprimento."))

        opcoes.append((n, "suporte_aereo", f"Suporte aéreo — custo {config.CUSTOS_ACAO['suporte_aereo']}"))
        n += 1
        opcoes.append((n, "chamar_tanque", f"Chamar tanque — custo {config.CUSTOS_ACAO['chamar_tanque']}"))
        n += 1

    opcoes.append((n, "caminhao_suprimento", "Chamar caminhão de suprimento"))
    n += 1
    opcoes.append((n, "pular_vez", "Pular a vez (ganha pontos extras se reagrupando)"))
    n += 1
    opcoes.append((n, "fugir", "Fugir da batalha"))

    return opcoes


def escolher_tipo_suprimento():
    print("\nQual caminhão você quer chamar?")
    print(f"[1] Caminhão médico — regenera {config.CURA_SUPRIMENTO} de vida"
          f" — custo {config.CUSTOS_ACAO['suprimento_medico']}")
    print(f"[2] Caminhão de munição de rifle — recarrega o rifle"
          f" — custo {config.CUSTOS_ACAO['suprimento_municao_rifle']}")
    print(f"[3] Caminhão de munição de submetralhadora — recarrega a SMG"
          f" — custo {config.CUSTOS_ACAO['suprimento_municao_smg']}")
    escolha = utils.menu_seguro("Escolha o caminhão: ", [1, 2, 3])
    return {
        1: "suprimento_medico",
        2: "suprimento_municao_rifle",
        3: "suprimento_municao_smg",
    }[escolha]


def turno_humano(unidade_atual, oponente, turno):
    vida_atual = unidade.vida_atual_principal(unidade_atual)
    vida_max = unidade.vida_maxima_principal(unidade_atual)
    print(f"\n{unidade_atual['nome']} — vida: {vida_atual}/{vida_max}")
    print(f"{unidade_atual['nome']} — pontos disponíveis: {unidade_atual['pontos']}")
    opcoes = montar_opcoes_disponiveis(unidade_atual)
    for numero, chave, texto in opcoes:
        if numero is not None:
            print(f"[{numero}] {texto}")
        else:
            print(f"      {texto}")

    validas = [numero for numero, chave, _ in opcoes if numero is not None]
    escolha = utils.menu_seguro("Escolha sua ação: ", validas)
    chave_escolhida = next(chave for numero, chave, _ in opcoes if numero == escolha)

    if chave_escolhida == "caminhao_suprimento":
        chave_escolhida = escolher_tipo_suprimento()

    executar_acao(chave_escolhida, unidade_atual, oponente)


def escolher_acao_bot(unidade_atual, oponente, turno):
    if unidade_atual["tanque_ativo"]:
        if not modulo_tanque.tanque_pode_atacar(unidade_atual):
            if (unidade.vida_atual_principal(unidade_atual) < unidade_atual["vida_maxima"] * 0.4
                    and unidade.pode_pagar(unidade_atual, "suprimento_medico")):
                return "suprimento_medico"
            return "pular_vez"

        if oponente["tanque_ativo"]:
            return "tanque_perfurante"
        return "tanque_explosivo" if random.random() < 0.7 else "tanque_metralhadora"

    vida_pct = unidade_atual["vida_atual"] / unidade_atual["vida_maxima"]
    if vida_pct < 0.3 and unidade.pode_pagar(unidade_atual, "suprimento_medico") and random.randint(1, 100) <= 60:
        return "suprimento_medico"

    if (not oponente["tanque_ativo"] and turno >= 3 and unidade.pode_pagar(unidade_atual, "chamar_tanque")
            and random.randint(1, 100) <= 25):
        return "chamar_tanque"

    if turno >= 4 and unidade.pode_pagar(unidade_atual, "suporte_aereo") and random.randint(1, 100) <= 30:
        return "suporte_aereo"

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

    return "pular_vez"


def turno_bot(unidade_atual, oponente, turno):
    acao = escolher_acao_bot(unidade_atual, oponente, turno)
    print(f"\n{unidade_atual['nome']} decide sua ação...")
    utils.espera(1)
    executar_acao(acao, unidade_atual, oponente)


def executar_acao(chave_acao, unidade_atual, oponente):
    if chave_acao == "pular_vez":
        unidade_atual["pontos"] += config.BONUS_PULAR_VEZ
        print(f"{unidade_atual['nome']} se reagrupa e ganha {config.BONUS_PULAR_VEZ} pontos extras.")
        utils.espera(1.3)
        return

    if chave_acao == "fugir":
        unidade_atual["fugiu"] = True
        print(f"{unidade_atual['nome']} recua e abandona o campo de batalha!")
        utils.espera(1.5)
        return

    if chave_acao == "rifle" and not unidade.tem_municao(unidade_atual, "rifle"):
        print(f"{unidade_atual['nome']} está sem munição de rifle!")
        utils.espera(1.2)
        return

    if chave_acao == "submetralhadora" and not unidade.tem_municao(unidade_atual, "smg"):
        print(f"{unidade_atual['nome']} está sem munição de submetralhadora!")
        utils.espera(1.2)
        return

    if not unidade.pode_pagar(unidade_atual, chave_acao):
        print(f"{unidade_atual['nome']} não tem pontos suficientes para essa ação!")
        utils.espera(1.2)
        return

    unidade.pagar(unidade_atual, chave_acao)

    if chave_acao == "rifle":
        ataques.ataque_rifle(unidade_atual, oponente)
    elif chave_acao == "submetralhadora":
        ataques.ataque_submetralhadora(unidade_atual, oponente)
    elif chave_acao == "suporte_aereo":
        ataques.usar_suporte_aereo(unidade_atual, oponente)
    elif chave_acao == "suprimento_medico":
        suprimentos.usar_suprimento_medico(unidade_atual)
    elif chave_acao == "suprimento_municao_rifle":
        suprimentos.usar_suprimento_municao_rifle(unidade_atual)
    elif chave_acao == "suprimento_municao_smg":
        suprimentos.usar_suprimento_municao_smg(unidade_atual)
    elif chave_acao == "chamar_tanque":
        modulo_tanque.chamar_tanque(unidade_atual)
    elif chave_acao == "tanque_metralhadora":
        modulo_tanque.ataque_tanque_metralhadora(unidade_atual, oponente)
    elif chave_acao == "tanque_perfurante":
        modulo_tanque.ataque_tanque_perfurante(unidade_atual, oponente)
    elif chave_acao == "tanque_explosivo":
        modulo_tanque.ataque_tanque_explosivo(unidade_atual, oponente)
