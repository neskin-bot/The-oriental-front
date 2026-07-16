import utils
import unidade
import interface
import batalha


def main():
    interface.introducao()
    lado = interface.escolher_lado()
    interface.apresentar_lado(lado)

    lado_oponente = 2 if lado == 1 else 1
    jogador = unidade.criar_unidade(lado)
    inimigo = unidade.criar_unidade(lado_oponente)

    print("A batalha vai começar!")
    utils.espera(1)
    interface.exibir_status(jogador, inimigo)

    motivo = batalha.rodar_batalha(jogador, inimigo)
    interface.anunciar_resultado(jogador, inimigo, motivo)


if __name__ == "__main__":
    main()
