import config
import utils
import unidade


def aplica_efeito_incendiario(unidade_atual):
    if unidade_atual["efeito_incendiario_restante"] > 0 and not unidade.unidade_derrotada(unidade_atual):
        unidade.aplicar_dano(unidade_atual, config.DANO_INCENDIARIO_POR_RODADA)
        unidade_atual["efeito_incendiario_restante"] -= 1
        print(f"Bombas incendiárias continuam queimando o {unidade.nome_alvo_principal(unidade_atual)}! "
              f"Perdeu {config.DANO_INCENDIARIO_POR_RODADA} de vida.")
        utils.espera(1.3)
