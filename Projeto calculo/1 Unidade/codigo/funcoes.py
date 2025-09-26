import simpy
import numpy as np

# Entradas: salário, investimento, bônus, freelance
def entradas(env, salario_v, saldo,
             taxa_invest,
             bonus_v, bonus_tempo,
             freelance_v, freelance_intervalo):
    """
    Entradas financeiras:
    - Salário mensal fixo: é adicionado ao saldo a cada 30 dias.
    - Investimento com juros compostos contínuos: o saldo é atualizado diariamente com juros compostos.
    - Bônus único: adicionado ao saldo em um dia específico.
    - Freelance: valor recebido periodicamente (adicionado ao saldo a cada intervalo de dias).
    """

    # Salário mensal fixo
    if env.now % 30 == 0:
        saldo += salario_v

    # Aplicação de juros compostos contínuos: 
    # A fórmula usada é S(t) = S0 * exp(r * t), onde:
    # r é a taxa de juros anual (ajustada para taxa diária com r/365).
    # A função np.exp aplica a fórmula de juros compostos contínuos ao saldo diariamente.
    saldo *= np.exp(taxa_invest / 365)

    # Bônus em um dia específico
    if env.now == bonus_tempo and bonus_v > 0:
        saldo += bonus_v

    # Freelance periódico
    if freelance_intervalo > 0 and env.now % freelance_intervalo == 0:
        saldo += freelance_v

    return saldo


# Saídas: aluguel, transporte, alimentação, saúde, emergências
def saidas(env, aluguel_v, transporte_v, alimentacao_base,
           alimentacao_var, saude_v,
           emergencia_v, emergencia_prob,
           saldo):
    """
    Saídas financeiras:
    - Custos fixos: são deduzidos do saldo a cada 30 dias (aluguel, transporte, saúde).
    - Alimentação: modelada por uma função senoidal, onde o gasto varia ao longo do ano com base em um ciclo anual (sinusoidal).
    - Emergência: uma despesa aleatória que ocorre com base em uma probabilidade (chance de ocorrer a cada ciclo).
    """
    if env.now % 30 == 0:
        saldo -= aluguel_v
        saldo -= transporte_v
        saldo -= saude_v

        # Alimentação modelada por função senoidal (variação ao longo do tempo)
        # f(t) = base + var * sin(2πt/365)
        saldo -= alimentacao_base + alimentacao_var * np.sin(2 * np.pi * env.now / 365)

    # Emergência (processo aleatório)
    if np.random.rand() < emergencia_prob:
        saldo -= emergencia_v

    return saldo


def simular(meses, seed,
            salario_v, investimento_inicial, taxa_invest,
            bonus_v, bonus_tempo,
            freelance_v, freelance_intervalo,
            aluguel_v, transporte_v,
            alimentacao_base, alimentacao_var,
            saude_v,
            emergencia_v, emergencia_prob):
    """
    Simulação da projeção financeira ao longo do tempo usando SimPy:
    - A função simula a evolução do saldo financeiro diariamente (30 dias por mês) 
      considerando as entradas (salário, investimentos, bônus, freelance) e saídas 
      (aluguel, alimentação, saúde, emergências).
    - A simulação é executada por um processo contínuo dentro de um ambiente SimPy, 
      onde os fluxos financeiros são atualizados a cada "dia" da simulação.
    """
    np.random.seed(seed)
    env = simpy.Environment()
    historico = []
    saldo = investimento_inicial

    def processo(env, saldo):
        for dia in range(meses * 30):
            saldo = entradas(env, salario_v, saldo,
                             taxa_invest,
                             bonus_v, bonus_tempo,
                             freelance_v, freelance_intervalo)
            saldo = saidas(env, aluguel_v, transporte_v, alimentacao_base,
                           alimentacao_var, saude_v,
                           emergencia_v, emergencia_prob,
                           saldo)
            historico.append((dia + 1, saldo))
            yield env.timeout(1)
        return saldo

    env.process(processo(env, saldo))
    env.run(until=meses * 30)

    return historico, historico[-1][1]
