import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DE PARAMETROS E CRIAÇÃO DO DATAFRAME BASE (2005 - 2026)
# -------------------------------------------------------------------------
anos = np.arange(2005, 2027)
n_anos = len(anos)

# Dados Econômicos Reais Aproximados (Base de partida 2005)
pib_real_2005 = 2.17  # em trilhões de R$
pop_2005 = 186.0      # em milhões de habitantes

# Taxas de Crescimento Estimadas
crescimento_pib_real_medio = 0.021  # ~2.1% ao ano na média histórica real
crescimento_pop_medio = 0.007       # ~0.7% ao ano

# Construção das Séries Reais Históricas
pib_real = [pib_real_2005 * ((1 + crescimento_pib_real_medio) ** i) for i in range(n_anos)]
populacao = [pop_2005 * ((1 + crescimento_pop_medio) ** i) for i in range(n_anos)]

df = pd.DataFrame({
    'Ano': anos,
    'PIB_Real': pib_real,
    'Populacao': populacao
})

# -------------------------------------------------------------------------
# 2. MODELAGEM DA CRISE CRÔNICA: LETALIDADE DA CORRUPÇÃO VS COVID-19
# -------------------------------------------------------------------------
# A letalidade reflexa da corrupção cresce exponencialmente devido ao envelhecimento 
# do passivo de infraestrutura e à falta cumulativa de investimentos básicos.
taxa_letalidade_inicial = 45000  # Mortes reflexas estimadas em 2005 (Saneamento, Estradas, Segurança)
taxa_exp_corrupcao = 0.082       # Fator de crescimento composto anual do colapso estrutural

df['Mortes_Corrupcao_Acumulada'] = taxa_letalidade_inicial * ((1 + taxa_exp_corrupcao) ** (df['Ano'] - 2005))

# Inserindo os dados reais da Pandemia de Covid-19 (Crise Aguda) focados no período de pico (2020-2022)
# Fora desse intervalo, o impacto biológico agudo da Covid-19 é zero para fins deste comparativo.
df['Mortes_Covid'] = 0.0
df.loc[df['Ano'] == 2020, 'Mortes_Covid'] = 224000
df.loc[df['Ano'] == 2021, 'Mortes_Covid'] = 405000
df.loc[df['Ano'] == 2022, 'Mortes_Covid'] = 97000

# -------------------------------------------------------------------------
# 3. MODELAGEM DO MUNDO PERFEITO (CORRUPÇÃO ZERO E GESTÃO EFICIENTE)
# -------------------------------------------------------------------------
# Premissas:
# - Recuperação de 2.3% do PIB ao ano que seriam desviados.
# - Multiplicador de reinvestimento em infraestrutura/ciência = 1.6
# - Ganho de produtividade por Capital Humano qualificado após 10 anos (+1.5% extra ao ano)
taxa_recuperacao = 0.023
multiplicador_investimento = 1.6

pib_simulado = []
pib_atual = pib_real_2005

for idx, row in df.iterrows():
    ano_atual = row['Ano']
    # Crescimento base + injeção do dividendo da governança
    dividendo_governanca = pib_atual * taxa_recuperacao * multiplicador_investimento
    
    # Efeito cumulativo do Capital Humano maduro a partir de 2015
    efeito_educacao = 0.015 if ano_atual >= 2015 else 0.0
    
    taxa_crescimento_total = crescimento_pib_real_medio + efeito_educacao
    pib_atual = (pib_atual + dividendo_governanca) * (1 + taxa_crescimento_total)
    pib_simulado.append(pib_atual)

df['PIB_Simulado'] = pib_simulado

# Cálculo do PIB per Capita (Métrica de convergência para o Primeiro Mundo)
df['PIB_per_Capita_Real'] = (df['PIB_Real'] * 1e12) / (df['Populacao'] * 1e6)
df['PIB_per_Capita_Simulado'] = (df['PIB_Simulado'] * 1e12) / (df['Populacao'] * 1e6)

# Linha de corte de Primeiro Mundo (Adotando parâmetro de ~35k dólares convertidos/ajustados)
piso_primeiro_mundo = 110000 

# -------------------------------------------------------------------------
# 4. PLOTAGEM DOS GRÁFICOS PARA A APRESENTAÇÃO
# -------------------------------------------------------------------------
plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'default')
fig, axes = plt.subplots(3, 1, figsize=(12, 18), sharex=False)
fig.suptitle('Análise de Impacto Humanitário e Socioeconômico:\nCorrupção Sistêmica vs. Desenvolvimento Nacional', fontsize=16, fontweight='bold', color='#1a1a1a')

# --- GRÁFICO 1: Comparativo de Impacto Humanitário (Crise Aguda vs. Crise Crônica) ---
axes[0].plot(df['Ano'], df['Mortes_Corrupcao_Acumulada'], label='Letalidade da Corrupção (Modelo Exponencial Cumulativo)', color='#d9534f', linewidth=2.5, marker='o')
axes[0].bar(df['Ano'], df['Mortes_Covid'], label='Pandemia de Covid-19 (Dados Reais de Óbitos)', color='#0275d8', alpha=0.7, width=0.6)
axes[0].set_title('Gráfico 1: Trajetória de Óbitos - Choque Biológico vs. Degradação Institucional', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Número Anual de Vítimas/Óbitos', fontsize=10)
axes[0].set_xlim(2018, 2026)  # Janela focada no período do evento pandêmico para visualização clara
axes[0].legend(loc='upper left', frameon=True)

# --- GRÁFICO 2: A Simulação Econômica (Brasil Corrupção Zero) ---
axes[1].plot(df['Ano'], df['PIB_per_Capita_Simulado'], label='Cenário Simulada: Corrupção Zero & Gestão Responsável', color='#5cb85c', linewidth=3)
axes[1].plot(df['Ano'], df['PIB_per_Capita_Real'], label='Trajetória Real Histórica', color='#777777', linewidth=2, linestyle='--')
axes[1].axhline(y=piso_primeiro_mundo, color='#f0ad4e', linestyle=':', label='Linha de Convergência: Primeiro Mundo', linewidth=2)
axes[1].set_title('Gráfico 2: Evolução da Riqueza Custo de Oportunidade (PIB per Capita em R$)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('PIB per Capita (R$)', fontsize=10)
axes[1].set_xlim(2005, 2026)
axes[1].legend(loc='upper left', frameon=True)

# Encontrar o ano de cruzamento com o primeiro mundo
ano_convergencia = df[df['PIB_per_Capita_Simulado'] >= piso_primeiro_mundo]['Ano'].min()
if not pd.isna(ano_convergencia):
    axes[1].annotate(f'Alvo atingido em {ano_convergencia}\n(~{ano_convergencia - 2005} anos de gestão ideal)', 
                     xy=(ano_convergencia, piso_primeiro_mundo), 
                     xytext=(ano_convergencia - 5, piso_primeiro_mundo + 20000),
                     arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6))

# --- GRÁFICO 3: O Gráfico Combinado (Informação Unificada para o Slide Principal) ---
# Cruza o ganho de riqueza gerado pela boa gestão com a queda drástica na curva de mortes evitáveis
color = '#5cb85c'
axes[2].set_title('Gráfico 3: Matriz Unificada - O Ponto de Inflexão do Desenvolvimento', fontsize=12, fontweight='bold')
axes[2].set_xlabel('Anos de Linha Evolutiva', fontsize=10)
axes[2].set_ylabel('PIB per Capita Simulado (R$)', color=color, fontsize=10)
line1 = axes[2].plot(df['Ano'], df['PIB_per_Capita_Simulado'], color=color, linewidth=2.5, label='Aceleração Econômica (Eixo Esq.)')
axes[2].tick_params(axis='y', labelcolor=color)

ax3_2 = axes[2].twinx()  
color2 = '#d9534f'
ax3_2.set_ylabel('Vítimas da Corrupção (Simulado)', color=color2, fontsize=10)
line2 = ax3_2.plot(df['Ano'], df['Mortes_Corrupcao_Acumulada'], color=color2, linewidth=2, linestyle='-.', label='Curva de Risco Humanitário Real (Eixo Dir.)')
ax3_2.tick_params(axis='y', labelcolor=color2)

# Junta as legendas dos dois eixos distintos
lines = line1 + line2
labels = [l.get_label() for l in lines]
axes[2].legend(lines, labels, loc='upper left', frameon=True)
axes[2].set_xlim(2005, 2026)

# Ajustes finais de layout
plt.tight_layout()
plt.show()
