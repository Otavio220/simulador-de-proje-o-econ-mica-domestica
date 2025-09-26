import pygame
import sys
import matplotlib.pyplot as plt
from funcoes import simular

# Tamanho da tela definida em largura e altura
LARGURA, ALTURA = 1000, 700

# Definição de cores para a interface gráfica
AMARELO = (255, 215, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 200, 0)
VERMELHO = (200, 0, 0)

# Inicialização da fonte, que será definida mais tarde
fonte = None

# Definição dos campos que serão utilizados no formulário de entrada
CAMPOS = [
    "Meses", "Semente",
    "Salário mensal", "Investimento inicial", "Taxa de rendimento anual",
    "Bônus único", "Dia do bônus",
    "Freelance valor", "Freelance intervalo",
    "Aluguel", "Transporte",
    "Alimentação base", "Alimentação variação",
    "Saúde", "Emergência valor", "Emergência probabilidade"
]

# Dicionário contendo os rótulos para as perguntas no formulário
ROTULOS = {
    "Meses": "Por quantos meses você quer simular?",
    "Semente": "Número aleatório para repetir a simulação",
    "Salário mensal": "Qual é o seu salário por mês? (R$)",
    "Investimento inicial": "Quanto você tem investido no início? (R$)",
    "Taxa de rendimento anual": "Qual a taxa de rendimento anual do investimento? (ex: 0.05 = 5%)",
    "Bônus único": "Recebeu algum bônus extra? Informe o valor (R$)",
    "Dia do bônus": "Em qual dia esse bônus será recebido?",
    "Freelance valor": "Quanto você ganha por cada trabalho extra (freelance)? (R$)",
    "Freelance intervalo": "A cada quantos dias você faz um freelance?",
    "Aluguel": "Quanto você gasta por mês com aluguel? (R$)",
    "Transporte": "Quanto você gasta por mês com transporte? (R$)",
    "Alimentação base": "Gasto médio por mês com alimentação (R$)",
    "Alimentação variação": "Gasto extra em meses especiais (R$)",
    "Saúde": "Gasto mensal com saúde (R$)",
    "Emergência valor": "Se ocorrer uma emergência, quanto custa? (R$)",
    "Emergência probabilidade": "Qual a chance de ter uma emergência no mês? (0 a 1)"
}

# Função para criar o formulário e obter as respostas dos usuários
def tela_formulario(tela, fundo):
    # Inicializa o dicionário de respostas com valores vazios
    respostas = {campo: "" for campo in CAMPOS}
    selecionado = 0  # Inicia na primeira pergunta
    rodando = True

    # Botão de confirmação no canto inferior direito
    botao_rect = pygame.Rect(LARGURA - 160, ALTURA - 60, 140, 40)

    while rodando:
        tela.blit(fundo, (0, 0))  # Exibe o fundo da tela

        # Exibe o título do formulário
        titulo = fonte.render("PROJEÇÃO FINANCEIRA", True, AMARELO)
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 20))

        # Exibe o subtítulo
        subtitulo = fonte.render("Digite os dados solicitados abaixo:", True, BRANCO)
        tela.blit(subtitulo, (LARGURA // 2 - subtitulo.get_width() // 2, 60))

        # Exibe as perguntas e as respostas preenchidas
        for i, campo in enumerate(CAMPOS):
            cor = AMARELO if i == selecionado else BRANCO
            texto = f"{ROTULOS[campo]}: {respostas[campo]}"
            txt_surface = fonte.render(texto, True, cor)
            tela.blit(txt_surface, (100, 120 + i * 35))

        # Exibe o botão "CONFIRMAR"
        pygame.draw.rect(tela, AMARELO, botao_rect, border_radius=8)
        fonte_botao = pygame.font.SysFont("Segoe UI", 18, bold=True)
        texto_botao = fonte_botao.render("CONFIRMAR", True, (10, 10, 30))
        tela.blit(
            texto_botao,
            (botao_rect.centerx - texto_botao.get_width() // 2,
             botao_rect.centery - texto_botao.get_height() // 2)
        )

        pygame.display.flip()  # Atualiza a tela

        # Loop de eventos, onde o usuário interage com o formulário
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()  # Fecha a janela
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()  # Fecha a janela ao pressionar ESC
                    sys.exit()
                elif e.key == pygame.K_RETURN:
                    if selecionado == len(CAMPOS) - 1:
                        rodando = False  # Finaliza o formulário ao pressionar ENTER
                    else:
                        selecionado += 1  # Avança para a próxima pergunta
                elif e.key == pygame.K_BACKSPACE:
                    respostas[CAMPOS[selecionado]] = respostas[CAMPOS[selecionado]][:-1]  # Apaga o último caractere
                elif e.key == pygame.K_UP:
                    selecionado = max(0, selecionado - 1)  # Move para a pergunta anterior
                elif e.key == pygame.K_DOWN:
                    selecionado = min(len(CAMPOS) - 1, selecionado + 1)  # Move para a próxima pergunta
                else:
                    respostas[CAMPOS[selecionado]] += e.unicode  # Adiciona o caractere digitado

            if e.type == pygame.MOUSEBUTTONDOWN and botao_rect.collidepoint(e.pos):
                rodando = False  # Fecha o formulário ao clicar no botão confirmar

    return respostas  # Retorna as respostas preenchidas

# Função para exibir o gráfico dos resultados da simulação
def mostrar_grafico(historico):
    # Separa os tempos e saldos para a plotagem
    tempos = [t for t, _ in historico]
    saldos = [s for _, s in historico]

    # Cria o gráfico de evolução do saldo
    plt.figure(figsize=(10, 6))
    plt.plot(tempos, saldos, marker="o", color="blue", linewidth=2)
    plt.title("Evolução do Saldo - Projeção Financeira")
    plt.xlabel("Dias")
    plt.ylabel("Saldo (R$)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()  # Exibe o gráfico

# Função para exibir os resultados da simulação, incluindo o saldo final
def tela_saidas(tela, fundo, historico, saldo_final):
    saldos = [s for _, s in historico]  # Extrai os saldos da simulação
    saldo_min = min(saldos)  # Saldo mínimo
    saldo_max = max(saldos)  # Saldo máximo

    rodando = True
    while rodando:
        tela.blit(fundo, (0, 0))  # Exibe o fundo da tela

        # Exibe o título dos resultados
        titulo = fonte.render("Resultados da Simulação", True, AMARELO)
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 50))

        # Define a cor do saldo final (verde para positivo, vermelho para negativo)
        cor_saldo = VERDE if saldo_final >= 0 else VERMELHO
        saidas = [
            (f"Saldo final: R$ {saldo_final:.2f}", cor_saldo),
            (f"Saldo mínimo: R$ {saldo_min:.2f}", BRANCO),
            (f"Saldo máximo: R$ {saldo_max:.2f}", BRANCO),
            (f"Dias simulados: {historico[-1][0]} dias", BRANCO)
        ]

        # Exibe as informações de saldo e dias simulados
        for i, (texto, cor) in enumerate(saidas):
            txt_surface = fonte.render(texto, True, cor)
            tela.blit(txt_surface, (100, 150 + i * 50))

        # Instrução para o usuário
        instrucao = fonte.render("Pressione G para ver o gráfico | ESC para sair", True, AMARELO)
        tela.blit(instrucao, (LARGURA // 2 - instrucao.get_width() // 2, ALTURA - 80))

        pygame.display.flip()  # Atualiza a tela

        # Loop de eventos para a interação do usuário
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                rodando = False  # Fecha a tela
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    rodando = False  # Fecha a tela ao pressionar ESC
                if e.key == pygame.K_g:
                    mostrar_grafico(historico)  # Exibe o gráfico ao pressionar G

# Função principal do programa
def main():
    global fonte

    pygame.init()  # Inicializa o Pygame
    tela = pygame.display.set_mode((LARGURA, ALTURA))  # Cria a janela da aplicação
    pygame.display.set_caption("Projeção Financeira")  # Título da janela
    fonte = pygame.font.SysFont("Segoe UI", 26, bold=True)  # Define a fonte

    # Carrega o fundo da tela
    fundo = pygame.image.load("fundo.png")
    fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))  # Ajusta o tamanho do fundo

    # Coleta as respostas do usuário através do formulário
    respostas = tela_formulario(tela, fundo)
    pygame.quit()

    try:
        # Converte as respostas para os valores necessários e realiza a simulação
        historico, saldo_final = simular(
            meses=int(respostas["Meses"]),
            seed=int(respostas["Semente"]),
            salario_v=float(respostas["Salário mensal"]),
            investimento_inicial=float(respostas["Investimento inicial"]),
            taxa_invest=float(respostas["Taxa de rendimento anual"]),
            bonus_v=float(respostas["Bônus único"]),
            bonus_tempo=int(respostas["Dia do bônus"]),
            freelance_v=float(respostas["Freelance valor"]),
            freelance_intervalo=int(respostas["Freelance intervalo"]),
            aluguel_v=float(respostas["Aluguel"]),
            transporte_v=float(respostas["Transporte"]),
            alimentacao_base=float(respostas["Alimentação base"]),
            alimentacao_var=float(respostas["Alimentação variação"]),
            saude_v=float(respostas["Saúde"]),
            emergencia_v=float(respostas["Emergência valor"]),
            emergencia_prob=float(respostas["Emergência probabilidade"])
        )
    except ValueError as e:
        print("❌ Erro: verifique se todos os campos foram preenchidos corretamente.")
        print("Detalhes:", e)
        return

    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))  # Reabre a janela para os resultados
    pygame.display.set_caption("Resultados da Simulação")  # Título da janela
    fonte = pygame.font.SysFont("Segoe UI", 28, bold=True)  # Define a fonte para os resultados

    fundo = pygame.image.load("fundo.png")
    fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))  # Ajusta o fundo

    # Exibe os resultados finais
    tela_saidas(tela, fundo, historico, saldo_final)
    pygame.quit()
    sys.exit()

# Garantia de que a função main() será chamada apenas ao executar o script diretamente
if __name__ == "__main__":
    main()
