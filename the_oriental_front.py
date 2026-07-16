import random
import time
import sys
import os

pular_dialogo = False

# Se der problema pra limpar a tela no seu terminal/IDE, é só trocar pra False.
LIMPAR_TELA_ENTRE_TURNOS = True

# =================================================================
# CONFIGURAÇÃO DO JOGO (dados centralizados em dicionários)
# =================================================================

DADOS_LADOS = {
    1: {
        "nome": "Pelotão Alemão",
        "vida_maxima": 100,
        "rifle_nome": "Rifle Kar98k",
        "submetralhadora_nome": "Submetralhadora MP-40",
        "suporte_nome": "Stuka JU-87",
        "caminhao_nome": "Caminhão Opel Blitz",
        "tanque_nome": "Panzer IV",
        "buff_defesa": 0,
    },
    2: {
        "nome": "Pelotão Soviético",
        "vida_maxima": 120,
        "rifle_nome": "Rifle Mosin Nagant",
        "submetralhadora_nome": "Submetralhadora PPSh-41",
        "suporte_nome": "IL-2 Shturmovik",
        "caminhao_nome": "Caminhão ZIS-5",
        "tanque_nome": "Tanque T-34",
        "buff_defesa": 0.25,  # 25% de chance de reduzir qualquer dano recebido pela metade
    },
}

# custo em pontos de economia de cada ação
CUSTOS_ACAO = {
    "rifle": 5,
    "submetralhadora": 10,
    "suprimento": 20,
    "chamar_tanque": 50,
    "tanque_metralhadora": 8,
    "tanque_perfurante": 12,
    "tanque_explosivo": 12,
    "suporte_aereo": 40,
    "pular_vez": 0,
    "fugir": 0,
}

GANHO_PONTOS_TURNO = 15      # pontos ganhos por rodada (recursos/suprimentos chegando)
BONUS_PULAR_VEZ = 10          # pontos extras por optar por se reagrupar em vez de atacar
PONTOS_INICIAIS = 30

CURA_SUPRIMENTO = 30

TANQUE_VIDA = 80
TANQUE_COOLDOWN_RODADAS = 1

DANO_SUPORTE_AEREO = (30, 50)
DURACAO_INCENDIARIO = 5
DANO_INCENDIARIO_POR_RODADA = 3


# =================================================================
# UTILITÁRIOS DE TEXTO / ENTRADA
# =================================================================

def menu_seguro(pergunta, opcoes_validas):
    while True:
        try:
            escolha = int(input(pergunta))
            if escolha in opcoes_validas:
                return escolha
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
    print()


# =================================================================
# CRIAÇÃO E ESTADO DAS UNIDADES
# =================================================================

def criar_unidade(lado_id):
    dados = DADOS_LADOS[lado_id]
    return {
        "lado_id": lado_id,
        "nome": dados["nome"],
        "vida_atual": dados["vida_maxima"],
        "vida_maxima": dados["vida_maxima"],
        "pontos": PONTOS_INICIAIS,
        "efeito_incendiario_restante": 0,
        "tanque_ativo": False,
        "tanque_recem_chamado": False,   # True na rodada em que o tanque ainda está chegando
        "tanque_vida": 0,
        "tanque_cooldown": 0,
        "fugiu": False,
    }


def nome_alvo_principal(unidade):
    dados = DADOS_LADOS[unidade["lado_id"]]
    if unidade["tanque_ativo"]:
        return dados["tanque_nome"]
    return dados["nome"]


def vida_atual_principal(unidade):
    return unidade["tanque_vida"] if unidade["tanque_ativo"] else unidade["vida_atual"]


def vida_maxima_principal(unidade):
    return TANQUE_VIDA if unidade["tanque_ativo"] else unidade["vida_maxima"]


def unidade_derrotada(unidade):
    if unidade["tanque_ativo"]:
        return False  # o tanque pode morrer sem tirar o pelotão da batalha
    return unidade["vida_atual"] <= 0


# =================================================================
# ECONOMIA
# =================================================================

def pode_pagar(unidade, acao):
    return unidade["pontos"] >= CUSTOS_ACAO[acao]


def pagar(unidade, acao):
    unidade["pontos"] -= CUSTOS_ACAO[acao]


def ganhar_pontos_turno(unidade):
    unidade["pontos"] += GANHO_PONTOS_TURNO


# =================================================================
# APLICAÇÃO DE DANO / CURA (respeitando a regra do tanque)
# =================================================================

def aplicar_dano(unidade, dano):
    """O tanque, quando ativo, absorve todo o dano no lugar do pelotão."""
    dados = DADOS_LADOS[unidade["lado_id"]]
    if unidade["tanque_ativo"]:
        unidade["tanque_vida"] = max(0, unidade["tanque_vida"] - dano)
        if unidade["tanque_vida"] == 0:
            print(f"O {dados['tanque_nome']} foi destruído! O {dados['nome']} volta a estar exposto.")
            espera(1.5)
            unidade["tanque_ativo"] = False
    else:
        unidade["vida_atual"] = max(0, unidade["vida_atual"] - dano)


def aplicar_cura(unidade, cura):
    if unidade["tanque_ativo"]:
        unidade["tanque_vida"] = min(TANQUE_VIDA, unidade["tanque_vida"] + cura)
    else:
        unidade["vida_atual"] = min(unidade["vida_maxima"], unidade["vida_atual"] + cura)


def chance_buff_defesa(unidade):
    dados = DADOS_LADOS[unidade["lado_id"]]
    return random.randint(1, 100) <= dados["buff_defesa"] * 100


def dano_com_buff(unidade_defensora, dano):
    if chance_buff_defesa(unidade_defensora):
        print("A trincheira soviética resistiu! O dano foi reduzido pela metade.")
        return dano // 2
    return dano


# =================================================================
# ATAQUES DE INFANTARIA
# =================================================================

def ataque_rifle(atacante, defensor):
    dados = DADOS_LADOS[atacante["lado_id"]]
    dano = random.randint(1, 20) if atacante["lado_id"] == 1 else random.randint(1, 17)
    print(f"A infantaria dispara o {dados['rifle_nome']}!")
    espera(2)
    dano = dano_com_buff(defensor, dano)

    if dano > 18:
        print(f"Tiro crítico! Causou {dano} de dano severo.")
    elif dano < 5:
        print(f"Erro de mira! O disparo só causou {dano} de dano por estilhaços.")
    else:
        print(f"O disparo acertou o alvo, causando {dano} de dano.")

    aplicar_dano(defensor, dano)
    espera(1.8)


def ataque_submetralhadora(atacante, defensor):
    dados = DADOS_LADOS[atacante["lado_id"]]
    faixa = (1, 7) if atacante["lado_id"] == 1 else (1, 5)
    print(f"Rajada de {dados['submetralhadora_nome']}!")
    dano_total = 0
    for tiro in range(1, 5):
        dano_tiro = random.randint(*faixa)
        dano_total += dano_tiro
        print(f"  Tiro {tiro}: {dano_tiro} de dano")
        espera(0.6)
    dano_total = dano_com_buff(defensor, dano_total)
    print(f"A rajada causou {dano_total} de dano no total.")
    aplicar_dano(defensor, dano_total)
    espera(1.8)


def usar_suprimento(unidade):
    dados = DADOS_LADOS[unidade["lado_id"]]
    print(f"O {dados['caminhao_nome']} chega com suprimentos!")
    espera(1.2)
    aplicar_cura(unidade, CURA_SUPRIMENTO)
    print(f"{nome_alvo_principal(unidade)} recuperou {CURA_SUPRIMENTO} de vida.")
    espera(1.5)


def usar_suporte_aereo(atacante, defensor):
    dados = DADOS_LADOS[atacante["lado_id"]]
    dano = random.randint(*DANO_SUPORTE_AEREO)
    print(f"O {dados['suporte_nome']} sobrevoa o campo de batalha!")
    espera(2)
    dano = dano_com_buff(defensor, dano)
    print(f"O ataque aéreo causa {dano} de dano imediato.")
    espera(1.5)
    aplicar_dano(defensor, dano)
    defensor["efeito_incendiario_restante"] = DURACAO_INCENDIARIO
    print("Incêndios se espalham na posição inimiga — dano contínuo nas próximas rodadas.")
    espera(1.5)


# =================================================================
# TANQUE
# =================================================================

def chamar_tanque(unidade):
    dados = DADOS_LADOS[unidade["lado_id"]]
    unidade["tanque_ativo"] = True
    unidade["tanque_vida"] = TANQUE_VIDA
    unidade["tanque_recem_chamado"] = True
    unidade["tanque_cooldown"] = 0
    print(f"O {dados['tanque_nome']} avança e assume a linha de frente!")
    espera(1.2)
    print("Ele ainda está se posicionando — só poderá atacar na próxima rodada.")
    espera(1.5)


def ataque_tanque_metralhadora(atacante, defensor):
    dados = DADOS_LADOS[atacante["lado_id"]]
    print(f"O {dados['tanque_nome']} abre fogo com a metralhadora coaxial!")
    dano_total = 0
    for tiro in range(1, 6):
        dano_tiro = random.randint(4, 10)
        dano_total += dano_tiro
        print(f"  Tiro {tiro}: {dano_tiro} de dano")
        espera(0.5)
    dano_total = dano_com_buff(defensor, dano_total)
    print(f"A rajada do tanque causou {dano_total} de dano no total.")
    aplicar_dano(defensor, dano_total)
    atacante["tanque_cooldown"] = TANQUE_COOLDOWN_RODADAS
    espera(1.8)


def ataque_tanque_perfurante(atacante, defensor):
    dados = DADOS_LADOS[atacante["lado_id"]]
    print(f"O {dados['tanque_nome']} dispara um tiro perfurante!")
    espera(1)
    if defensor["tanque_ativo"]:
        dano = random.randint(25, 45)
        print(f"O projétil perfura o blindado inimigo, causando {dano} de dano!")
    else:
        dano = random.randint(2, 6)
        print("Sem um tanque inimigo pra perfurar, o disparo causa só um dano residual.")
    dano = dano_com_buff(defensor, dano)
    aplicar_dano(defensor, dano)
    atacante["tanque_cooldown"] = TANQUE_COOLDOWN_RODADAS
    espera(1.8)


def ataque_tanque_explosivo(atacante, defensor):
    dados = DADOS_LADOS[atacante["lado_id"]]
    print(f"O {dados['tanque_nome']} dispara um projétil explosivo!")
    espera(1)
    if not defensor["tanque_ativo"]:
        dano = random.randint(20, 35)
        print(f"A explosão devasta a infantaria inimiga, causando {dano} de dano!")
    else:
        dano = random.randint(2, 6)
        print("Contra um blindado, a explosão causa só um dano residual.")
    dano = dano_com_buff(defensor, dano)
    aplicar_dano(defensor, dano)
    atacante["tanque_cooldown"] = TANQUE_COOLDOWN_RODADAS
    espera(1.8)


def processa_chegada_e_cooldown_tanque(unidade):
    """Chamado no início do turno da unidade: resolve a chegada do tanque
    (ele não ataca na rodada em que foi chamado) e reduz o cooldown."""
    if unidade["tanque_recem_chamado"]:
        unidade["tanque_recem_chamado"] = False
        return
    if unidade["tanque_cooldown"] > 0:
        unidade["tanque_cooldown"] -= 1


def tanque_pode_atacar(unidade):
    return unidade["tanque_ativo"] and not unidade["tanque_recem_chamado"] and unidade["tanque_cooldown"] == 0


# =================================================================
# EFEITO PERSISTENTE (bombas incendiárias)
# =================================================================

def aplica_efeito_incendiario(unidade):
    if unidade["efeito_incendiario_restante"] > 0 and not unidade_derrotada(unidade):
        aplicar_dano(unidade, DANO_INCENDIARIO_POR_RODADA)
        unidade["efeito_incendiario_restante"] -= 1
        print(f"Bombas incendiárias continuam queimando o {nome_alvo_principal(unidade)}! "
              f"Perdeu {DANO_INCENDIARIO_POR_RODADA} de vida.")
        espera(1.3)


# =================================================================
# TURNO CONTROLADO PELO JOGADOR (menu)
# =================================================================

def montar_opcoes_disponiveis(unidade):
    """Retorna uma lista de (numero, chave_acao, texto) com as ações
    que a unidade pode de fato executar agora."""
    opcoes = []
    n = 1

    if unidade["tanque_ativo"]:
        if tanque_pode_atacar(unidade):
            for chave, texto in [
                ("tanque_metralhadora", "Rajada de metralhadora do tanque"),
                ("tanque_perfurante", "Tiro perfurante (eficaz contra tanques)"),
                ("tanque_explosivo", "Tiro explosivo (eficaz contra infantaria)"),
            ]:
                opcoes.append((n, chave, f"{texto} — custo {CUSTOS_ACAO[chave]}"))
                n += 1
        else:
            opcoes.append((None, None, "O tanque está em cooldown / se posicionando nesta rodada."))
    else:
        opcoes.append((n, "rifle", f"Atacar com rifle — custo {CUSTOS_ACAO['rifle']}"))
        n += 1
        opcoes.append((n, "submetralhadora", f"Atacar com submetralhadora — custo {CUSTOS_ACAO['submetralhadora']}"))
        n += 1
        opcoes.append((n, "suporte_aereo", f"Suporte aéreo — custo {CUSTOS_ACAO['suporte_aereo']}"))
        n += 1
        opcoes.append((n, "chamar_tanque", f"Chamar tanque — custo {CUSTOS_ACAO['chamar_tanque']}"))
        n += 1

    opcoes.append((n, "suprimento", f"Usar caminhão de suprimento — custo {CUSTOS_ACAO['suprimento']}"))
    n += 1
    opcoes.append((n, "pular_vez", "Pular a vez (ganha pontos extras se reagrupando)"))
    n += 1
    opcoes.append((n, "fugir", "Fugir da batalha"))

    return opcoes


def turno_humano(unidade, oponente, turno):
    print(f"\n{unidade['nome']} — pontos disponíveis: {unidade['pontos']}")
    opcoes = montar_opcoes_disponiveis(unidade)
    for numero, chave, texto in opcoes:
        if numero is not None:
            print(f"[{numero}] {texto}")
        else:
            print(f"      {texto}")

    validas = [numero for numero, chave, _ in opcoes if numero is not None]
    escolha = menu_seguro("Escolha sua ação: ", validas)
    chave_escolhida = next(chave for numero, chave, _ in opcoes if numero == escolha)

    executar_acao(chave_escolhida, unidade, oponente)


# =================================================================
# TURNO CONTROLADO PELA IA
# =================================================================

def escolher_acao_bot(unidade, oponente, turno):
    if unidade["tanque_ativo"]:
        if not tanque_pode_atacar(unidade):
            if vida_atual_principal(unidade) < unidade["vida_maxima"] * 0.4 and pode_pagar(unidade, "suprimento"):
                return "suprimento"
            return "pular_vez"

        if oponente["tanque_ativo"]:
            return "tanque_perfurante"
        return "tanque_explosivo" if random.random() < 0.7 else "tanque_metralhadora"

    vida_pct = unidade["vida_atual"] / unidade["vida_maxima"]
    if vida_pct < 0.3 and pode_pagar(unidade, "suprimento") and random.randint(1, 100) <= 60:
        return "suprimento"

    if (not oponente["tanque_ativo"] and turno >= 3 and pode_pagar(unidade, "chamar_tanque")
            and random.randint(1, 100) <= 25):
        return "chamar_tanque"

    if turno >= 4 and pode_pagar(unidade, "suporte_aereo") and random.randint(1, 100) <= 30:
        return "suporte_aereo"

    if pode_pagar(unidade, "submetralhadora") and random.randint(1, 100) <= 55:
        return "submetralhadora"

    if pode_pagar(unidade, "rifle"):
        return "rifle"

    return "pular_vez"


def turno_bot(unidade, oponente, turno):
    acao = escolher_acao_bot(unidade, oponente, turno)
    print(f"\n{unidade['nome']} decide sua ação...")
    espera(1)
    executar_acao(acao, unidade, oponente)


# =================================================================
# EXECUÇÃO DE AÇÃO (compartilhada entre humano e bot)
# =================================================================

def executar_acao(chave_acao, unidade, oponente):
    if chave_acao == "pular_vez":
        unidade["pontos"] += BONUS_PULAR_VEZ
        print(f"{unidade['nome']} se reagrupa e ganha {BONUS_PULAR_VEZ} pontos extras.")
        espera(1.3)
        return

    if chave_acao == "fugir":
        unidade["fugiu"] = True
        print(f"{unidade['nome']} recua e abandona o campo de batalha!")
        espera(1.5)
        return

    if not pode_pagar(unidade, chave_acao):
        print(f"{unidade['nome']} não tem pontos suficientes para essa ação!")
        espera(1.2)
        return

    pagar(unidade, chave_acao)

    if chave_acao == "rifle":
        ataque_rifle(unidade, oponente)
    elif chave_acao == "submetralhadora":
        ataque_submetralhadora(unidade, oponente)
    elif chave_acao == "suprimento":
        usar_suprimento(unidade)
    elif chave_acao == "suporte_aereo":
        usar_suporte_aereo(unidade, oponente)
    elif chave_acao == "chamar_tanque":
        chamar_tanque(unidade)
    elif chave_acao == "tanque_metralhadora":
        ataque_tanque_metralhadora(unidade, oponente)
    elif chave_acao == "tanque_perfurante":
        ataque_tanque_perfurante(unidade, oponente)
    elif chave_acao == "tanque_explosivo":
        ataque_tanque_explosivo(unidade, oponente)


# =================================================================
# STATUS
# =================================================================

def exibir_status(jogador, inimigo):
    print("\n=== STATUS ===")
    for u in (jogador, inimigo):
        alvo = nome_alvo_principal(u)
        print(f"{u['nome']} ({alvo}): {vida_atual_principal(u)}/{vida_maxima_principal(u)} de vida "
              f"| Pontos: {u['pontos']}")
    print("==============\n")
    espera(2.5)


# =================================================================
# INTRODUÇÃO E SELEÇÃO
# =================================================================

def introducao():
    print("Selecione o modo de exibição:")
    print("1 - Modo imersivo (com pausas e efeitos)")
    print("2 - Modo rápido (texto instantâneo)")
    modo = menu_seguro("Escolha: ", [1, 2])
    global pular_dialogo
    pular_dialogo = modo == 2

    digitar("Qualquer pessoa que já tenha olhado nos olhos vidrados de um soldado")
    digitar("morrendo no campo de batalha pensará muito antes de iniciar uma guerra.")
    digitar("- Otto von Bismarck.")
    espera(1)
    print("✠-----------------------------------------------✠")
    print("╔╦╗┬ ┬┌─┐  ┌─┐┬─┐┬┌─┐┌┐┌┌┬┐┌─┐┬    ┌─┐┬─┐┌─┐┌┐┌┌┬┐")
    print(" ║ ├─┤├┤   │ │├┬┘│├┤ │││ │ ├─┤│    ├┤ ├┬┘│ ││││ │")
    print(" ╩ ┴ ┴└─┘  └─┘┴└─┴└─┘┘└┘ ┴ ┴ ┴┴─┘  └  ┴└─└─┘┘└┘ ┴")
    print("☭-----------------------------------------------☭")
    digitar("Bem vindo ao The Oriental Front.")
    digitar("Assuma o lado alemão ou soviético no front oriental,")
    digitar("em uma batalha por turnos com economia de recursos.")
    espera(1)


def exibir_comparativo_lados():
    print("\n=========================== COMPARATIVO DE FORÇAS ===========================")
    linhas = [
        ("Vida inicial", "vida_maxima"),
        ("Rifle", "rifle_nome"),
        ("Submetralhadora", "submetralhadora_nome"),
        ("Suporte aéreo", "suporte_nome"),
        ("Suprimento", "caminhao_nome"),
        ("Blindado", "tanque_nome"),
    ]
    print(f"{'':<18}{DADOS_LADOS[1]['nome']:<28}{DADOS_LADOS[2]['nome']:<28}")
    print("-" * 78)
    for rotulo, chave in linhas:
        print(f"{rotulo:<18}{str(DADOS_LADOS[1][chave]):<28}{str(DADOS_LADOS[2][chave]):<28}")

    print(f"{'Buff especial':<18}{'Nenhum':<28}"
          f"{str(int(DADOS_LADOS[2]['buff_defesa'] * 100)) + '% de reduzir dano recebido pela metade':<28}")
    print("=" * 78 + "\n")


def escolher_lado():
    print()
    digitar("Escolha o seu lado nesta guerra")
    exibir_comparativo_lados()
    print("1 - Lado Alemão")
    print("2 - Lado Soviético")
    return menu_seguro("Digite o número correspondente à sua escolha: ", [1, 2])


def apresentar_lado(lado_id):
    dados = DADOS_LADOS[lado_id]
    print(f"\nVocê escolheu o {dados['nome']}.")
    print(f"Vida inicial: {dados['vida_maxima']}")
    print(f"Armamento: {dados['rifle_nome']} e {dados['submetralhadora_nome']}")
    print(f"Suporte aéreo: {dados['suporte_nome']}")
    print(f"Suprimento: {dados['caminhao_nome']}")
    print(f"Blindado: {dados['tanque_nome']}")
    if dados["buff_defesa"] > 0:
        print(f"Buff: {int(dados['buff_defesa'] * 100)}% de chance de reduzir qualquer dano recebido pela metade.")
    print()


# =================================================================
# LOOP PRINCIPAL DA BATALHA
# =================================================================

def rodar_batalha(jogador, inimigo):
    turno = 1
    alemao = jogador if jogador["lado_id"] == 1 else inimigo
    sovietico = inimigo if jogador["lado_id"] == 1 else jogador

    while True:
        print(f"\n| --- Turno {turno} --- |")
        espera(1)
        ganhar_pontos_turno(jogador)
        ganhar_pontos_turno(inimigo)

        for unidade, oponente in ((alemao, sovietico), (sovietico, alemao)):
            processa_chegada_e_cooldown_tanque(unidade)
            eh_humano = unidade is jogador
            if eh_humano:
                turno_humano(unidade, oponente, turno)
            else:
                turno_bot(unidade, oponente, turno)

            if unidade["fugiu"] or oponente["fugiu"]:
                break
            if unidade_derrotada(oponente):
                break

        aplica_efeito_incendiario(alemao)
        aplica_efeito_incendiario(sovietico)

        exibir_status(jogador, inimigo)

        if jogador["fugiu"] or inimigo["fugiu"]:
            return "fuga"
        if unidade_derrotada(jogador) or unidade_derrotada(inimigo):
            return "combate"

        turno += 1


def anunciar_resultado(jogador, inimigo, motivo):
    print("\n--- FIM DA BATALHA ---")
    espera(1)

    if motivo == "fuga":
        if jogador["fugiu"]:
            print(f"{jogador['nome']} fugiu do campo de batalha. VITÓRIA DO {inimigo['nome'].upper()}!")
        else:
            print(f"{inimigo['nome']} fugiu do campo de batalha. VITÓRIA DO {jogador['nome'].upper()}!")
        return

    if unidade_derrotada(jogador):
        print(f"VITÓRIA DO {inimigo['nome'].upper()}!")
    else:
        print(f"VITÓRIA DO {jogador['nome'].upper()}!")


# =================================================================
# PONTO DE ENTRADA
# =================================================================

def main():
    introducao()
    lado = escolher_lado()
    apresentar_lado(lado)

    lado_oponente = 2 if lado == 1 else 1
    jogador = criar_unidade(lado)
    inimigo = criar_unidade(lado_oponente)

    print("A batalha vai começar!")
    espera(1)
    exibir_status(jogador, inimigo)

    motivo = rodar_batalha(jogador, inimigo)
    anunciar_resultado(jogador, inimigo, motivo)


if __name__ == "__main__":
    main()
