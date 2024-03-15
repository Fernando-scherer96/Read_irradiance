import math
import pandas as pd #renomeado pandas como pd, para a chamada ficar mais simples
from Read_arquivo import ArquivoTxt
from Range_irradiance import categorizar_irradiancia

#import matplotlib.pyplot as plt -- CASO PRECISE PLOTAR GRÁFICOS

#criando uma classe para fazer a leitura dos dados de irradiação
dados_irradiacao_318 = ArquivoTxt(nome_arquivo='./Dados_irradiacao/20100318.txt')
dados_irradiacao_B77 = ArquivoTxt(nome_arquivo='./Dados_irradiacao/resultsB77.txt')

# Use índices 13 e 14 para a 14ª e 15ª colunas, respectivamente
Hst = dados_irradiacao_B77.extrair_colunas(indice_coluna=0)  #horario solar 
Tamb = dados_irradiacao_B77.extrair_colunas(indice_coluna=1)  
Vento = dados_irradiacao_B77.extrair_colunas(indice_coluna=2)  
G_hor = dados_irradiacao_318.extrair_colunas(indice_coluna=13)
G_inc = dados_irradiacao_318.extrair_colunas(indice_coluna=14)

# Corrigido para utilizar o objeto correto e índices ajustados se necessário
# crio um dataSeries para depois criar um dataFrame completo e utilizar os comandos do pandas
# Colo nomes nas colunas para poder trabalhar melhor
df_Tamb = pd.Series(Tamb, name= 'Tamb')
df_HST = pd.Series(Hst, name= 'HST')
df_vento = pd.Series(Vento, name= 'Vento')
df_Ginc = pd.Series(G_inc, name= 'G_inc')
df_Gor = pd.Series(G_hor, name='G_hor')

#Definindo o data frame a partir dos data Series criados 
df = pd.DataFrame({
    'HST':df_HST, 
    'Tamb': df_Tamb, 
    'Vento':df_vento, 
    'G_inc': df_Ginc, 
    'G_hor': df_Gor})
print(df) #Exibindo os valores de data frame 

#convertendo os valores de irradiancia que podem estar no typo str para float 
'''pd.to_numeric(): Esta é uma função do Pandas que tenta converter os valores passados para ela em números'''
'''
errors='coerce' é um parâmetro que diz à função como lidar com valores que não podem ser convertidos em números. 
Se você não incluir esse parâmetro, a função gerará um erro quando encontrar um valor que não pode ser convertido 
(como uma letra ou um símbolo). Com errors='coerce', esses valores problemáticos são substituídos por NaN (Not a Number), 
que é a maneira do Pandas representar valores ausentes ou indefinidos.'''
df['G_inc'] = pd.to_numeric(df['G_inc'], errors='coerce')
df['G_hor'] = pd.to_numeric(df['G_hor'], errors='coerce')

'''#criando uma nova coluna no nosso data frame para receber os valores das faixas 
df['Faixa_Irradiancia_Incidente'] = df['G_inc'].apply(categorizar_irradiancia) #essa função com as faixas de irradiancia estão separados em um modulo diferente
df['Faixa_Irradiancia_Horrizontal'] = df['G_hor'].apply(categorizar_irradiancia)
#A função apply no Pandas é usada para aplicar uma função ao longo de um eixo do DataFrame ou em valores de Series. 

tempo_operacao_por_faixa_segundos_inc = df['Faixa_Irradiancia_Incidente'].value_counts()
# Convertendo o tempo para horas e minutos para melhor interpretação
tempo_operacao_por_faixa_minutos_inc = tempo_operacao_por_faixa_segundos_inc / 60
tempo_operacao_por_faixa_horas_inc = tempo_operacao_por_faixa_segundos_inc / 3600

#Irradiação Horrizontal
tempo_operacao_por_faixa_segundos_hor = df['Faixa_Irradiancia_Horrizontal'].value_counts()
tempo_operacao_por_faixa_minutos_hor = tempo_operacao_por_faixa_segundos_hor / 60
tempo_operacao_por_faixa_horas_hor = tempo_operacao_por_faixa_segundos_hor / 3600


# Exibindo o tempo de operação por faixa em horas e minutos
print("Tempo de operação por faixa (em minutos):")
print(tempo_operacao_por_faixa_minutos_inc)
print("\nTempo de operação por faixa (em horas):")
print(f'{tempo_operacao_por_faixa_horas_inc}\n')

print('Para a irradiancia Horizontal')
print("Tempo de operação por faixa (em minutos):")
print(tempo_operacao_por_faixa_minutos_hor)
print("\nTempo de operação por faixa (em horas):")
print(f'{tempo_operacao_por_faixa_horas_hor}\n')'''

#Calculos para obter a irradiancia corrigida 
#objetivo reescrever o codigo dos codigos utilizando pandas 
# Criando um DataFrame a partir dos seus dados existentes
# Inicialização das variáveis

#Kfv é o coeficiente de perda de potência em função da temperatura
Kfv = -0.46 #Valor considerado do trabalho do henrique
df['Tamb'] = pd.to_numeric(df['Tamb'], errors='coerce')
df['Tfv'] = (0.943 * df['Tamb']) + (0.028 * df['G_inc']) + 4.3
df['G_corr'] = df['G_inc'] * (1 - Kfv * (df['Tfv'] - 25))

df['G_corr'] = pd.to_numeric(df['G_corr'], errors= 'coerce')

df['Faixa_irradiancia_Corrigida'] = df['G_corr'].apply(categorizar_irradiancia)
#calculo do tempo de operação por faixa
tempo_operacao_por_faixa_segundos_corr = df['Faixa_irradiancia_Corrigida'].value_counts()

G_corr_por_faixa = df.groupby('Faixa_irradiancia_Corrigida')['G_corr'].sum()
print(G_corr_por_faixa)

energia_por_faixa = G_corr_por_faixa * tempo_operacao_por_faixa_segundos_corr

energia_por_faixa_dict = energia_por_faixa.to_dict()

s = 0
for faixa, energia in energia_por_faixa_dict.items():
    #print(f"{faixa}: {energia} Wh") # ou Joules, já que 1 Ws = 1 J
    s =+ energia
#print(f'\n')

for faixa, energia in energia_por_faixa_dict.items():
    total = energia / s
    #print(f"{faixa}: {total}")




#print(f'\nPonderadores considerando a soma das irradiancias por faixa: {soma_G_corr_por_faixa_dividido_pelo_total*100}')

# Convertendo o tempo para horas e minutos para melhor interpretação
#tempo_operacao_por_faixa_minutos_corr = tempo_operacao_por_faixa_segundos_inc / 60
#tempo_operacao_por_faixa_horas_corr = tempo_operacao_por_faixa_segundos_inc / 3600

# Exibindo o tempo de operação por faixa em horas e minutos
'''print("Tempo de operação por faixa (em minutos):")
print(tempo_operacao_por_faixa_minutos_corr)
print("\nTempo de operação por faixa (em horas):")
print(f'{tempo_operacao_por_faixa_horas_corr}\n')'''
