LIMPAR_TELA_ENTRE_TURNOS = True

DADOS_LADOS = {
    1: {
        "nome": "Pelotão Alemão",
        "vida_maxima": 100,
        "rifle_nome": "Rifle Kar98k",
        "submetralhadora_nome": "Submetralhadora MP-40",
        "suporte_nome": "Stuka JU-87",
        "caminhao_nome": "Caminhão Opel Blitz",
        "tanque_nome": "Panzer IV",
        "arma_anti_tank_nome": "Panzerfaust",
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
        "arma_anti_tank_nome": "PTRS-41",
        "buff_defesa": 0.25,
    },
}

CUSTOS_ACAO = {
    "rifle": 5,
    "submetralhadora": 10,
    "suprimento_medico": 25,
    "suprimento_municao_rifle": 10,
    "suprimento_municao_smg": 30,
    "anti_tank": 30,
    "suprimento_municao_anti_tank": 40,
    "chamar_tanque": 50,
    "sair_tanque": 0,
    "cobertura": 0,
    "tanque_metralhadora": 8,
    "tanque_perfurante": 12,
    "tanque_explosivo": 12,
    "suporte_aereo": 40,
    "pular_vez": 0,
    "fugir": 0,
}

GANHO_PONTOS_TURNO = 10
BONUS_PULAR_VEZ = 10
PONTOS_INICIAIS = 30

CURA_SUPRIMENTO = 30

MUNICAO_MAXIMA_RIFLE = 25
MUNICAO_GASTA_RIFLE = 5

MUNICAO_MAXIMA_SMG = 16
MUNICAO_GASTA_SMG = 4


MUNICAO_MAXIMA_ANTI_TANK = 2
MUNICAO_GASTA_ANTI_TANK = 1

TANQUE_VIDA = 80
TANQUE_COOLDOWN_RODADAS = 1

DANO_SUPORTE_AEREO = (30, 50)
DANO_SUPORTE_AEREO_VS_TANQUE = (20, 35)
DURACAO_INCENDIARIO = 5
DANO_INCENDIARIO_POR_RODADA = 3


DURACAO_INCENDIARIO_ANTITANQUE = 3


FATOR_DANO_ARMA_NORMAL_VS_TANQUE = 0.10


PROBABILIDADE_COBERTURA_FALHA = 25   
FATOR_REDUCAO_COBERTURA = 0.5