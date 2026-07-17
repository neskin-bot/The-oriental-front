import config
import utils
import unidade


def usar_suprimento_medico(alvo):
    dados = config.DADOS_LADOS[alvo["lado_id"]]
    print(f"O {dados['caminhao_nome']} chega com suprimentos médicos!")
    utils.espera(1.2)
    unidade.aplicar_cura(alvo, config.CURA_SUPRIMENTO)
    print(f"{unidade.nome_alvo_principal(alvo)} recuperou {config.CURA_SUPRIMENTO} de vida.")
    utils.espera(1.5)


def usar_suprimento_municao_rifle(alvo):
    dados = config.DADOS_LADOS[alvo["lado_id"]]
    print(f"O {dados['caminhao_nome']} chega com munição de {dados['rifle_nome']}!")
    utils.espera(1.2)
    unidade.recarregar_municao(alvo, "rifle")
    usos = unidade.usos_restantes(alvo, "rifle")
    print(f"Munição de rifle recarregada! Dá pra atirar mais {usos} vez(es) agora.")
    utils.espera(1.5)


def usar_suprimento_municao_smg(alvo):
    dados = config.DADOS_LADOS[alvo["lado_id"]]
    print(f"O {dados['caminhao_nome']} chega com munição de {dados['submetralhadora_nome']}!")
    utils.espera(1.2)
    unidade.recarregar_municao(alvo, "smg")
    usos = unidade.usos_restantes(alvo, "smg")
    print(f"Munição de submetralhadora recarregada! Dá pra atirar mais {usos} vez(es) agora.")
    utils.espera(1.5)


def usar_suprimento_municao_anti_tank(alvo):
    dados = config.DADOS_LADOS[alvo["lado_id"]]
    nome_arma = dados["arma_anti_tank_nome"]
    print(f"O {dados['caminhao_nome']} chega com munição de {nome_arma}!")
    utils.espera(1.2)
    unidade.recarregar_municao(alvo, "anti_tank")
    usos = unidade.usos_restantes(alvo, "anti_tank")
    print(f"Munição de {nome_arma} recarregada! Dá pra atirar mais {usos} vez(es) agora.")
    utils.espera(1.5)