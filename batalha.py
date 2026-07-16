import utils
import unidade
import efeitos
import tanque as modulo_tanque
import turnos
import interface


def rodar_batalha(jogador, inimigo):
    turno = 1
    alemao = jogador if jogador["lado_id"] == 1 else inimigo
    sovietico = inimigo if jogador["lado_id"] == 1 else jogador

    while True:

        print("\n" + "=" * 50)
        print(f"| --- Turno {turno} --- |")
        utils.espera(1)
        if turno > 1:
         unidade.ganhar_pontos_turno(jogador)
         unidade.ganhar_pontos_turno(inimigo)

        for u, oponente in ((alemao, sovietico), (sovietico, alemao)):
            modulo_tanque.processa_chegada_e_cooldown_tanque(u)
            eh_humano = u is jogador
            if eh_humano:
                turnos.turno_humano(u, oponente, turno)
            else:
                turnos.turno_bot(u, oponente, turno)

            if u["fugiu"] or oponente["fugiu"]:
                break
            if unidade.unidade_derrotada(oponente):
                break

        efeitos.aplica_efeito_incendiario(alemao)
        efeitos.aplica_efeito_incendiario(sovietico)

        interface.exibir_status(jogador, inimigo)

        if jogador["fugiu"] or inimigo["fugiu"]:
            return "fuga"
        if unidade.unidade_derrotada(jogador) or unidade.unidade_derrotada(inimigo):
            return "combate"

        turno += 1
