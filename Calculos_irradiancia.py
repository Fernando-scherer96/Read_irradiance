import math
import pandas as pd #renomeado pandas como pd, para a chamada ficar mais simples
from Read_arquivo import ArquivoTxt
from Range_irradiance import categorizar_irradiancia

dados_irradiacao = ArquivoTxt(nome_arquivo='./Dados_irradiacao/dados_irradiancia_tamp_etc.csv')

# Use índices 13 e 14 para a 14ª e 15ª colunas, respectivamente
Hst = dados_irradiacao.extrair_colunas(indice_coluna=1)  #horario solar 
Tamb = dados_irradiacao.extrair_colunas(indice_coluna=3)  
Vento = dados_irradiacao.extrair_colunas(indice_coluna=4)  
G_inc = dados_irradiacao.extrair_colunas(indice_coluna=2)

# Corrigido para utilizar o objeto correto e índices ajustados se necessário
# crio um dataSeries para depois criar um dataFrame completo e utilizar os comandos do pandas
# Colo nomes nas colunas para poder trabalhar melhor
df_Tamb = pd.Series(Tamb, name= 'Tamb')
df_HST = pd.Series(Hst, name= 'HST')
df_vento = pd.Series(Vento, name= 'Vento')
df_Ginc = pd.Series(G_inc, name= 'G_inc')

#df_Gor = pd.Series(G_hor, name='G_hor')

#Definindo o data frame a partir dos data Series criados 
df = pd.DataFrame({
    'HST':df_HST, 
    'Tamb': df_Tamb, 
    'Vento':df_vento, 
    'G_inc': df_Ginc, 
})
print(df) #Exibindo os valores de data frame 

# Converter para tipo numérico se necessário
df['Tamb'] = pd.to_numeric(df['Tamb'], errors='coerce')
df['G_inc'] = pd.to_numeric(df['G_inc'], errors='coerce')

# Agora, tente executar as operações novamente
Kpv = -0.46
df['tpv'] = (0.943 * df['Tamb']) + (0.028 * df['G_inc']) + 4.3
df['G_corr'] = (1 + (Kpv / 100) * (df['tpv'] - 25)) * df['G_inc']

#dividindo por faixas de irradiancia 
df['categoria_irradiancia'] = df['G_corr'].apply(categorizar_irradiancia)
soma_por_categoria = df.groupby('categoria_irradiancia')['G_corr'].sum()
print(f'\nIrradiancia por faixa (W/m²): {soma_por_categoria}')
tempo_operacao_por_faixa_segundos_inc_corrigida = df['categoria_irradiancia'].value_counts()
print(f'\nTempo de operação por minutos: {tempo_operacao_por_faixa_segundos_inc_corrigida}')
#print(soma_por_categoria)

mult_soma_por_tempo = soma_por_categoria * tempo_operacao_por_faixa_segundos_inc_corrigida
soma_mult_soma_por_tempo = sum(mult_soma_por_tempo)
ponderacao = mult_soma_por_tempo / soma_mult_soma_por_tempo

# Definir a nova ordem
nova_ordem = ['Faixa F', 'Faixa E', 'Faixa D', 'Faixa C', 'Faixa B', 'Faixa A']

# Reindexar a série ponderacao com a nova ordem
ponderacao_ordenada = ponderacao.reindex(nova_ordem)
print(f'\nPonderação final:\n{ponderacao_ordenada*100}')
print(sum(ponderacao))