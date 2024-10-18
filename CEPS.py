import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Tabela de fatores para diferentes tamanhos de amostras (n)
tabela_fatores = {
    2: {'A2': 1.88, 'A3': 2.659, 'B3': 0, 'B4': 3.267, 'D3': 0, 'D4': 3.267},
    3: {'A2': 1.023, 'A3': 1.954, 'B3': 0, 'B4': 2.568, 'D3': 0, 'D4': 2.574},
    4: {'A2': 0.729, 'A3': 1.628, 'B3': 0, 'B4': 2.266, 'D3': 0, 'D4': 2.282},
    5: {'A2': 0.577, 'A3': 1.427, 'B3': 0, 'B4': 2.089, 'D3': 0, 'D4': 2.114},
    6: {'A2': 0.483, 'A3': 1.287, 'B3': 0.03, 'B4': 1.97, 'D3': 0, 'D4': 2.004},
    7: {'A2': 0.419, 'A3': 1.182, 'B3': 0.118, 'B4': 1.882, 'D3': 0.076, 'D4': 1.924},
    8: {'A2': 0.373, 'A3': 1.099, 'B3': 0.185, 'B4': 1.815, 'D3': 0.136, 'D4': 1.864},
    9: {'A2': 0.337, 'A3': 1.032, 'B3': 0.239, 'B4': 1.761, 'D3': 0.184, 'D4': 1.816},
    10: {'A2': 0.308, 'A3': 0.975, 'B3': 0.284, 'B4': 1.716, 'D3': 0.223, 'D4': 1.777},
    11: {'A2': 0.285, 'A3': 0.927, 'B3': 0.321, 'B4': 1.679, 'D3': 0.256, 'D4': 1.744},
    12: {'A2': 0.266, 'A3': 0.886, 'B3': 0.354, 'B4': 1.646, 'D3': 0.283, 'D4': 1.717},
    13: {'A2': 0.249, 'A3': 0.85, 'B3': 0.382, 'B4': 1.618, 'D3': 0.307, 'D4': 1.693},
    14: {'A2': 0.235, 'A3': 0.817, 'B3': 0.406, 'B4': 1.594, 'D3': 0.328, 'D4': 1.672},
    15: {'A2': 0.223, 'A3': 0.789, 'B3': 0.428, 'B4': 1.572, 'D3': 0.347, 'D4': 1.653},
    16: {'A2': 0.212, 'A3': 0.763, 'B3': 0.448, 'B4': 1.552, 'D3': 0.363, 'D4': 1.637},
    17: {'A2': 0.203, 'A3': 0.739, 'B3': 0.466, 'B4': 1.534, 'D3': 0.378, 'D4': 1.622},
    18: {'A2': 0.194, 'A3': 0.718, 'B3': 0.482, 'B4': 1.518, 'D3': 0.391, 'D4': 1.608},
    19: {'A2': 0.187, 'A3': 0.698, 'B3': 0.497, 'B4': 1.503, 'D3': 0.403, 'D4': 1.597},
    20: {'A2': 0.18, 'A3': 0.68, 'B3': 0.51, 'B4': 1.49, 'D3': 0.415, 'D4': 1.585},
    21: {'A2': 0.173, 'A3': 0.663, 'B3': 0.523, 'B4': 1.477, 'D3': 0.425, 'D4': 1.575},
    22: {'A2': 0.167, 'A3': 0.647, 'B3': 0.534, 'B4': 1.466, 'D3': 0.434, 'D4': 1.566},
    23: {'A2': 0.162, 'A3': 0.633, 'B3': 0.545, 'B4': 1.455, 'D3': 0.443, 'D4': 1.557},
    24: {'A2': 0.157, 'A3': 0.619, 'B3': 0.555, 'B4': 1.445, 'D3': 0.451, 'D4': 1.548},
    25: {'A2': 0.153, 'A3': 0.606, 'B3': 0.565, 'B4': 1.435, 'D3': 0.459, 'D4': 1.541},
}


# Função para selecionar os fatores com base no tamanho da amostra
def get_factors(n):
    return tabela_fatores.get(n, {'A2': 0, 'A3': 0, 'B3': 0, 'B4': 0, 'D3': 0, 'D4': 0})

# Configuração do aplicativo Streamlit
st.title("Gráficos de Controle")

# Upload de arquivo Excel
uploaded_file = st.file_uploader("Escolha um arquivo Excel", type="xlsx")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
     # Criando um container com borda
    container = st.container(border=True)
    
    # Colocando as opções e gráficos dentro do container
    with container:
        
        # Opções para seleção
        option = st.selectbox("Escolha uma opção de gráfico:", 
                            ["Média Vs Amplitude", "Média Vs Desvio Padrão", "Média Vs CUSUM"])
        
        
        if option == "Média Vs Amplitude":
            def calcular_media_r(df):
                        
                st.subheader("Gráfico de Controle - Média")
                n = df.shape[1]
                fatores = get_factors(n)
                A2 = fatores['A2']

                medias_linhas = df.mean(axis=1)
                amplitude_linhas = df.max(axis=1) - df.min(axis=1)

                media_global = medias_linhas.mean()
                amplitude_media = amplitude_linhas.mean()

                lsc_xr = media_global + A2 * amplitude_media
                lic_xr = media_global - A2 * amplitude_media
                # Calculando as métricas
                acima_lsc = sum(medias_linhas > lsc_xr)
                abaixo_lic = sum(medias_linhas < lic_xr)

                # Criando os cartões acima do gráfico
                coluna_esquerda, coluna_direita = st.columns([1, 1])
                coluna_esquerda.metric("Amostras acima do LSC", f'{acima_lsc}')
                coluna_direita.metric("Amostras abaixo do LIC", f'{abaixo_lic}')

                # Criando o gráfico com Plotly
                fig = go.Figure()

                # Adicionando a linha de média das amostras
                fig.add_trace(go.Scatter(
                    y=medias_linhas,
                    mode='lines+markers',
                    name='Média das Amostras',
                    line=dict(color='blue')
                ))

                # Adicionando as linhas de controle
                fig.add_hline(y=media_global, line_dash="dash", line_color="green")
                fig.add_hline(y=lsc_xr, line_dash="dash", line_color="red")
                fig.add_hline(y=lic_xr, line_dash="dash", line_color="red")
                # Adicionando anotações à esquerda
               
                fig.add_annotation(x=0, y=lsc_xr, text=f"{lsc_xr:.2f}", 
                                showarrow=False, xanchor='left', align='left', 
                                xref='paper', yref='y', xshift=10)
                fig.add_annotation(x=0, y=lic_xr, text=f"{lic_xr:.2f}", 
                                showarrow=False, xanchor='left', align='left', 
                                xref='paper', yref='y', xshift=10)

                # Configurando o layout
                fig.update_layout(
                    xaxis_title='Amostra',
                    yaxis_title='Média',
                    height=600)

                # Mostrar o gráfico no Streamlit
                st.plotly_chart(fig, use_container_width=True)
                                                

            # Chamada da função
            calcular_media_r(df)

            # Função para calcular e plotar o gráfico de controle da amplitude (R)
            def calcular_amplitude(df):
                st.subheader("Gráfico de Controle - Amplitude")
                n = df.shape[1]
                fatores = get_factors(n)
                D3 = fatores['D3']
                D4 = fatores['D4']

                amplitudes = df.max(axis=1) - df.min(axis=1)
                amplitude_media = amplitudes.mean()

                lsc_r = D4 * amplitude_media
                lic_r = D3 * amplitude_media
                
                # Calculando as métricas
                acima_lsc = sum(amplitudes > lsc_r)
                abaixo_lic = sum(amplitudes < lic_r)

                # Criando os cartões acima do gráfico
                coluna_esquerda, coluna_direita = st.columns([1, 1])
                coluna_esquerda.metric("Amostras acima do LSC", f'{acima_lsc}')
                coluna_direita.metric("Amostras abaixo do LIC", f'{abaixo_lic}')

                # Criando o gráfico com Plotly
                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    y=amplitudes,
                    mode='lines+markers',
                    name='Amplitude das Amostras',
                    line=dict(color='blue')
                ))

                fig.add_hline(y=amplitude_media, line_dash="dash", line_color="green")
                fig.add_hline(y=lsc_r, line_dash="dash", line_color="red")
                fig.add_hline(y=lic_r, line_dash="dash", line_color="red")

               
                fig.add_annotation(x=0, y=lsc_r, text=f"{lsc_r:.2f}", 
                                   showarrow=False, xanchor='left', align='left', 
                                   xref='paper', yref='y', xshift=10)
                fig.add_annotation(x=0, y=lic_r, text=f"{lic_r:.2f}", 
                                   showarrow=False, xanchor='left', align='left', 
                                   xref='paper', yref='y', xshift=10)

                fig.update_layout(
                    xaxis_title='Amostra',
                    yaxis_title='Amplitude',
                    height=600
                )

                st.plotly_chart(fig, use_container_width=True)

            calcular_amplitude(df)    

        elif option == "Média Vs Desvio Padrão":
            def calcular_media_s(df):
                        
                st.subheader("Gráfico de Controle - Média")
                n = df.shape[1]
                fatores = get_factors(n)
                A3 = fatores['A3']

                medias_linhas = df.mean(axis=1)
                amplitude_linhas = df.max(axis=1) - df.min(axis=1)

                media_global = medias_linhas.mean()
                amplitude_media = amplitude_linhas.mean()

                lsc_xr = media_global + A3 * amplitude_media
                lic_xr = media_global - A3 * amplitude_media
                medias_linhas = df.mean(axis=1)
                amplitude_linhas = df.max(axis=1) - df.min(axis=1)

                media_global = medias_linhas.mean()
                amplitude_media = amplitude_linhas.mean()

                lsc_xr = media_global + A3 * amplitude_media
                lic_xr = media_global - A3 * amplitude_media
                # Calculando as métricas
                acima_lsc = sum(medias_linhas > lsc_xr)
                abaixo_lic = sum(medias_linhas < lic_xr)

                # Criando os cartões acima do gráfico
                coluna_esquerda, coluna_direita = st.columns([1, 1])
                coluna_esquerda.metric("Amostras acima do LSC", f'{acima_lsc}')
                coluna_direita.metric("Amostras abaixo do LIC", f'{abaixo_lic}')


                # Criando o gráfico com Plotly
                fig = go.Figure()

                # Adicionando a linha de média das amostras
                fig.add_trace(go.Scatter(
                    y=medias_linhas,
                    mode='lines+markers',
                    name='Média das Amostras',
                    line=dict(color='blue')
                ))

                # Adicionando as linhas de controle
                fig.add_hline(y=media_global, line_dash="dash", line_color="green")
                fig.add_hline(y=lsc_xr, line_dash="dash", line_color="red")
                fig.add_hline(y=lic_xr, line_dash="dash", line_color="red")
                # Adicionando anotações à esquerda
                
                fig.add_annotation(x=0, y=lsc_xr, text=f"{lsc_xr:.2f}", 
                                showarrow=False, xanchor='left', align='left', 
                                xref='paper', yref='y', xshift=10)
                fig.add_annotation(x=0, y=lic_xr, text=f"{lic_xr:.2f}", 
                                showarrow=False, xanchor='left', align='left', 
                                xref='paper', yref='y', xshift=10)

                # Configurando o layout
                fig.update_layout(
                    xaxis_title='Amostra',
                    yaxis_title='Média',
                    height=600)

                # Mostrar o gráfico no Streamlit
                st.plotly_chart(fig, use_container_width=True)
            
            calcular_media_s(df)

            # Função para calcular e plotar o gráfico de controle do desvio padrão
            def calcular_desvio_padrao(df):
                st.subheader("Gráfico de Controle - Desvio padrão")
                n = df.shape[1]
                fatores = get_factors(n)
                B3 = fatores['B3']
                B4 = fatores['B4']

                desvios = df.std(axis=1)
                media_dos_desvios = desvios.mean()

                lsc = B4 * media_dos_desvios
                lc = media_dos_desvios
                lic = B3 * media_dos_desvios
                
                # Calculando as métricas
                acima_lsc = sum(desvios > lsc)
                abaixo_lic = sum(desvios < lic)

                # Criando os cartões acima do gráfico
                coluna_esquerda, coluna_direita = st.columns([1, 1])
                coluna_esquerda.metric("Amostras acima do LSC", f'{acima_lsc}')
                coluna_direita.metric("Amostras abaixo do LIC", f'{abaixo_lic}')

                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    y=desvios,
                    mode='lines+markers',
                    name='Desvio Padrão das Amostras',
                    line=dict(color='blue')
                ))

                fig.add_hline(y=lc, line_dash="dash", line_color="green")
                fig.add_hline(y=lsc, line_dash="dash", line_color="red")
                fig.add_hline(y=lic, line_dash="dash", line_color="red")

                fig.add_annotation(x=0, y=lsc, text=f"{lsc:.2f}", 
                                showarrow=False, xanchor='left', align='left', 
                                xref='paper', yref='y', xshift=10)
                fig.add_annotation(x=0, y=lic, text=f" {lic:.2f}", 
                                showarrow=False, xanchor='left', align='left', 
                                xref='paper', yref='y', xshift=10)

                fig.update_layout(
                    title='Gráfico de Controle - Desvio Padrão',
                    xaxis_title='Amostra',
                    yaxis_title='Desvio Padrão',
                    height=600
                )

                st.plotly_chart(fig, use_container_width=True)

            calcular_desvio_padrao(df)

        elif option == "Média Vs CUSUM":        
            # Função para calcular e plotar o gráfico de CUSUM
            def calcular_media_r(df):
                        
                st.subheader("Gráfico de Controle - Média")
                n = df.shape[1]
                fatores = get_factors(n)
                A2 = fatores['A2']

                medias_linhas = df.mean(axis=1)
                amplitude_linhas = df.max(axis=1) - df.min(axis=1)

                media_global = medias_linhas.mean()
                amplitude_media = amplitude_linhas.mean()

                lsc_xr = media_global + A2 * amplitude_media
                lic_xr = media_global - A2 * amplitude_media
                medias_linhas = df.mean(axis=1)
                amplitude_linhas = df.max(axis=1) - df.min(axis=1)

                media_global = medias_linhas.mean()
                amplitude_media = amplitude_linhas.mean()

                lsc_xr = media_global + A2 * amplitude_media
                lic_xr = media_global - A2 * amplitude_media
                # Calculando as métricas
                acima_lsc = sum(medias_linhas > lsc_xr)
                abaixo_lic = sum(medias_linhas < lic_xr)
                coluna_esquerda, coluna_direita = st.columns([1, 1])
                coluna_esquerda.metric("Amostras acima do LSC", f'{acima_lsc}')
                coluna_direita.metric("Amostras abaixo do LIC", f'{abaixo_lic}')



                # Criando o gráfico com Plotly
                fig = go.Figure()

                # Adicionando a linha de média das amostras
                fig.add_trace(go.Scatter(
                    y=medias_linhas,
                    mode='lines+markers',
                    name='Média das Amostras',
                    line=dict(color='blue')
                ))

                # Adicionando as linhas de controle
                fig.add_hline(y=media_global, line_dash="dash", line_color="green")
                fig.add_hline(y=lsc_xr, line_dash="dash", line_color="red")
                fig.add_hline(y=lic_xr, line_dash="dash", line_color="red")
                # Adicionando anotações à esquerda
                
                fig.add_annotation(x=0, y=lsc_xr, text=f"{lsc_xr:.2f}", 
                                showarrow=False, xanchor='left', align='left', 
                                xref='paper', yref='y', xshift=10)
                fig.add_annotation(x=0, y=lic_xr, text=f"{lic_xr:.2f}", 
                                showarrow=False, xanchor='left', align='left', 
                                xref='paper', yref='y', xshift=10)

                # Configurando o layout
                fig.update_layout(
                    xaxis_title='Amostra',
                    yaxis_title='Média',
                    height=600)

                # Mostrar o gráfico no Streamlit
                st.plotly_chart(fig, use_container_width=True)

                

            # Chamada da função
            calcular_media_r(df)
        
            def calcular_cusum(df):
                st.subheader("Gráfico de Controle - CUSUM")
                n = df.shape[1]
                fatores = get_factors(n)
                A2 = fatores['A2']

                medias_linhas = df.mean(axis=1)
                media_global = medias_linhas.mean()
                amplitude_linhas = df.max(axis=1) - df.min(axis=1)
                amplitude_media = amplitude_linhas.mean()
                lsc_xr = media_global + A2 * amplitude_media
                dados = df.mean(axis=1).values  # Calcula a média das linhas e converte em array

                # Parâmetros
                mu0 = media_global         # Valor alvo
                K = (lsc_xr-mu0)/2   # Metade da magnitude da mudança

                # Inicializando os acumuladores CUSUM
                C_plus = np.zeros(len(dados))  # CUSUM superior
                C_minus = np.zeros(len(dados))  # CUSUM inferior

                # Cálculo dos acumuladores CUSUM
                for i in range(len(dados)):
                    xi = dados[i]
                    
                    # Cálculo de (mu0 - xi) - K
                    u_minus_xi_minus_K = (mu0 - xi) - K

                    # Cálculo do CUSUM inferior
                    if i == 0:
                        C_minus[i] = u_minus_xi_minus_K  # Para o primeiro período
                    else:
                        # Corrigindo a acumulação de C-
                        C_minus[i] = (mu0 - dados[i - 1]) - K + C_minus[i - 1]

                    # Aplicando max para garantir que não seja negativo
                    C_minus[i] = max(0, C_minus[i])

                    # Cálculo do CUSUM superior
                    xi_minus_uK = xi - (mu0 + K)
                    if i == 0:
                        C_plus[i] = max(0, xi_minus_uK)  # Para o primeiro valor
                    else:
                        C_plus[i] = max(0, xi_minus_uK + C_plus[i - 1])  # Acumulação do C+

                    # Debug: Print dos resultados
                    print(f"Período {i + 1}: X-BARRA = {xi:.3f}, (mu0 - xi) - K = {u_minus_xi_minus_K:.3f}, "
                        f"C- = {C_minus[i]:.3f}, C+ = {C_plus[i]:.3f}")

                # Calculando as métricas
                pontos_acima_zero_cplus = sum(C_plus > 0)
                pontos_acima_zero_cminus = sum(C_minus > 0)

                # Criando os cartões acima do gráfico
                coluna_esquerda, coluna_direita = st.columns([1, 1])
                coluna_esquerda.metric("Pontos C+ > 0", f'{pontos_acima_zero_cplus}')
                coluna_direita.metric("Pontos C- > 0", f'{pontos_acima_zero_cminus}')

                # Plotando o gráfico CUSUM com Plotly
                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    y=C_plus,
                    mode='lines+markers',
                    name='CUSUM Superior (C⁺)',
                    line=dict(color='blue')
                ))

                fig.add_trace(go.Scatter(
                    y=C_minus,
                    mode='lines+markers',
                    name='CUSUM Inferior (C⁻)',
                    line=dict(color='red')
                ))

                fig.update_layout(
                    title='Gráfico CUSUM',
                    xaxis_title='Período',
                    yaxis_title='CUSUM',
                    legend=dict(x=0, y=1, xanchor='left', yanchor='top'),
                    height=600,
                    yaxis=dict(range=[-5, 10])  # Definindo limites do eixo y
                )

                # Mostrar o gráfico no Streamlit
                st.plotly_chart(fig, use_container_width=True)
        
            calcular_cusum(df)    

# Fim do bloco if uploaded_file is not None