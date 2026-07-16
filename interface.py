import config
import utils
import unidade


def exibir_status(jogador, inimigo):
    print("\n=== STATUS ===")
    for u in (jogador, inimigo):
        alvo = unidade.nome_alvo_principal(u)
        vida_atual = unidade.vida_atual_principal(u)
        vida_max = unidade.vida_maxima_principal(u)
        print(f"\n{u['nome']} ({alvo})")
        print(f"  Vida: {vida_atual}/{vida_max}")
        if not u["tanque_ativo"]:
            usos_rifle = unidade.usos_restantes(u, "rifle")
            usos_smg = unidade.usos_restantes(u, "smg")
            print(f"  Rifle: dá pra atirar mais {usos_rifle} vez(es) antes de precisar de munição.")
            print(f"  Submetralhadora: dá pra atirar mais {usos_smg} vez(es) antes de precisar de munição.")
        print(f"  Pontos: {u['pontos']}")
    print("\n==============\n")
    utils.espera(2.5)


def introducao():
    print("Selecione o modo de exibição:")
    print("1 - Modo imersivo (com pausas e efeitos)")
    print("2 - Modo rápido (texto instantâneo)")
    modo = utils.menu_seguro("Escolha: ", [1, 2])
    utils.definir_modo_rapido(modo == 2)

    utils.digitar("Qualquer pessoa que já tenha olhado nos olhos vidrados de um soldado")
    utils.digitar("morrendo no campo de batalha pensará muito antes de iniciar uma guerra.")
    utils.digitar("- Otto von Bismarck.")
    utils.espera(2)
    print("✠-----------------------------------------------✠")
    print("╔╦╗┬ ┬┌─┐  ┌─┐┬─┐┬┌─┐┌┐┌┌┬┐┌─┐┬    ┌─┐┬─┐┌─┐┌┐┌┌┬┐")
    print(" ║ ├─┤├┤   │ │├┬┘│├┤ │││ │ ├─┤│    ├┤ ├┬┘│ ││││ │")
    print(" ╩ ┴ ┴└─┘  └─┘┴└─┴└─┘┘└┘ ┴ ┴ ┴┴─┘  └  ┴└─└─┘┘└┘ ┴")
    print("☭-----------------------------------------------☭")
    utils.espera(2)
    utils.digitar("Bem vindo ao The Oriental Front.")
    utils.digitar("Assuma o lado alemão ou soviético no front oriental,")
    utils.digitar("em uma batalha por turnos com economia de recursos.")
    utils.espera(1)


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
    print(f"{'':<18}{config.DADOS_LADOS[1]['nome']:<28}{config.DADOS_LADOS[2]['nome']:<28}")
    print("-" * 78)
    for rotulo, chave in linhas:
        print(f"{rotulo:<18}{str(config.DADOS_LADOS[1][chave]):<28}{str(config.DADOS_LADOS[2][chave]):<28}")

    buff_texto = str(int(config.DADOS_LADOS[2]['buff_defesa'] * 100)) + "% de reduzir dano recebido pela metade"
    print(f"{'Buff especial':<18}{'Nenhum':<28}{buff_texto:<28}")
    print("=" * 78)

    usos_rifle = unidade.usos_maximos("rifle")
    usos_smg = unidade.usos_maximos("smg")
    print("\nSistema de munição (igual para os dois lados):")
    print(f"  Rifle: {usos_rifle} usos por carga — recarga custa {config.CUSTOS_ACAO['suprimento_municao_rifle']} pontos.")
    print(f"  Submetralhadora: {usos_smg} usos por carga — recarga custa {config.CUSTOS_ACAO['suprimento_municao_smg']} pontos.")
    print()


def escolher_lado():
    print()
    utils.digitar("Escolha o seu lado nesta guerra")
    exibir_comparativo_lados()
    print("1 - Lado Alemão")
    print("2 - Lado Soviético")
    return utils.menu_seguro("Digite o número correspondente à sua escolha: ", [1, 2])


def apresentar_lado(lado_id):
    dados = config.DADOS_LADOS[lado_id]
    print(f"\nVocê escolheu o {dados['nome']}.")
    print(f"Vida inicial: {dados['vida_maxima']}")
    print(f"Armamento: {dados['rifle_nome']} e {dados['submetralhadora_nome']}")
    print(f"Munição inicial: {unidade.usos_maximos('rifle')} usos de rifle,"
          f" {unidade.usos_maximos('smg')} usos de submetralhadora")
    print(f"Suporte aéreo: {dados['suporte_nome']}")
    print(f"Suprimento: {dados['caminhao_nome']} (médico, munição de rifle ou munição de SMG)")
    print(f"Blindado: {dados['tanque_nome']}")
    if dados["buff_defesa"] > 0:
        print(f"Buff: {int(dados['buff_defesa'] * 100)}% de chance de reduzir qualquer dano recebido pela metade.")
    print()
    utils.espera(5)


def anunciar_resultado(jogador, inimigo, motivo):
    print("\n--- FIM DA BATALHA ---")
    utils.espera(1)

    if motivo == "fuga":
        if jogador["fugiu"]:
            print(f"{jogador['nome']} fugiu do campo de batalha. VITÓRIA DO {inimigo['nome'].upper()}!")
        else:
            print(f"{inimigo['nome']} fugiu do campo de batalha. VITÓRIA DO {jogador['nome'].upper()}!")
        return

    if unidade.unidade_derrotada(jogador):
        print(f"VITÓRIA DO {inimigo['nome'].upper()}!")
    else:
        print(f"VITÓRIA DO {jogador['nome'].upper()}!")
