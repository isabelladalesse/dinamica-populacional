import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

st.title("Simulador de Dinâmica Populacional de Aguapés, Sapos-cururu e Escorpiões Amarelos")

# Variáveis
A, G, S, E = sp.symbols('A G S E')
vars = (A, G, S, E)

# Parâmetros
na, ne, mu_s, delta, alpha, beta, theta = sp.symbols('na ne mu_s delta alpha beta theta')
ka, kg, ks, ke, ng = sp.symbols('ka kg ks ke ng')

param_values = {
na: 2.73e-3,
ne: 3.26e-3,
mu_s: 1.97e-5,
delta: 7.57e-7,
alpha: 1.07,
beta: 2.18e-3,
theta: 0.18}

param_dim_values = {
ka: 14,
kg: 144,
ke: 0.17,
ng: 6600
}

# Sistema
dA = na*A*(1-A)
dG = S*(1-G*(1+(A**2/alpha**2)))-delta*G
dS = delta*G-mu_s*S
dE = E*ne*(1-E)-E*S*beta*(1+(E**2/theta**2))

dA_num = dA.subs(param_values)
dG_num = dG.subs(param_values)
dS_num = dS.subs(param_values)
dE_num = dE.subs(param_values)

f_num = sp.lambdify(vars, [dA_num, dG_num, dS_num, dE_num], 'numpy')

def sistema(t, y):
    A, G, S, E = y
    if any(abs(val) > 1e6 for val in y):
        print(f"Explodiu em t={t}: {y}")

    return f_num(A, G, S, E)


st.subheader("Insira a densidade de seres presentes no ecossistema:")

y0_dim = {
    'A': st.number_input("Aguapés/m²: ", value=10.0),
    'G': st.number_input("Girinos/m²: ", value=50.0),
    'S': st.number_input("Sapos/m²: ", value=5.0),
    'E': st.number_input("Escorpiões/m²: ", value=0.4)
}

# Condições iniciais adimensionais
map_k = {
    'A': ka,
    'G': kg,
    'S': kg,
    'E': ke
}

y0 = [
    y0_dim[nome] / param_dim_values[map_k[nome]]
    for nome in ['A', 'G', 'S', 'E']
]

if st.button("Rodar simulação"):
    t_span = (0, 500000)
    t_eval = np.linspace(0, 500000, 1000)
    sol = solve_ivp(sistema, t_span, y0, t_eval=t_eval, method='LSODA')

    # Gráfico
    plt.figure(figsize=(10,6))

    labels = ['A(t)', 'G(t)', 'S(t)', 'E(t)']
    for i in range(4):
        plt.plot(sol.t, sol.y[i], label=labels[i])

    plt.xlabel('Tempo (adimensional)')
    plt.ylabel('Populações (adimensionais)')
    plt.title('Dinâmica das populações')
    plt.legend()
    plt.grid()
    st.pyplot(plt)

    # Detecção de estabilização
    tol = 1e-5
    window = 20
    nomes = ['A', 'G', 'S', 'E']

    valores_estab = {}
    tempos_estab = {}

    for i, nome in enumerate(nomes):
        pop = sol.y[i]
        t = sol.t

        t_estab = None
        pop_estab = None

        for j in range(window, len(pop)):
            if np.std(pop[j-window:j]) < tol:
                t_estab = t[j]
                pop_estab = np.mean(pop[j-window:j])
                break

        # se NÃO encontrou estabilização
        if t_estab is None:
            t_estab = t[-1]
            pop_estab = pop[-1]

        # salva resultados
        valores_estab[nome] = pop_estab
        tempos_estab[nome] = t_estab

    # Conversão de resultados para dimensional
    valores_dim = {}
    tempos_dim = {}

    for nome in nomes:

        # Pega valor adimensional
        pop_adm = valores_estab[nome]
        t_adm = tempos_estab[nome]

        # Converte a população
        if nome == 'A':
            pop_dim = param_dim_values[ka] * pop_adm
        elif nome == 'G':
            pop_dim = param_dim_values[kg] * pop_adm
        elif nome == 'S':
            pop_dim = param_dim_values[kg] * pop_adm
        elif nome == 'E':
            pop_dim = param_dim_values[ke] * pop_adm

        # Converte o tempo
        t_real = t_adm / param_dim_values[ng]

        # salva
        valores_dim[nome] = pop_dim
        tempos_dim[nome] = t_real

    nomes = ['A', 'G', 'S', 'E']

    unidades = {
        'A': 'aguapés/m²',
        'G': 'indivíduos/m²',
        'S': 'indivíduos/m²',
        'E': 'indivíduos/m²'
    }

    descricao = {
        'A': 'aguapés',
        'G': 'girinos',
        'S': 'sapos',
        'E': 'escorpiões'
    }

    st.subheader("Interpretação da Dinâmica Populacional")

    for nome in nomes:
        inicial = y0_dim[nome]
        final = valores_dim[nome]
        tempo = tempos_dim[nome]

        if final > inicial:
            tendencia = "cresceu"
        elif final < inicial:
            tendencia = "decaiu"
        else:
            tendencia = "permaneceu constante"

        st.write(f"A população de {descricao[nome]} {tendencia} de "
            f"{inicial:.2f} para {final:.2f} {unidades[nome]}, "
            f"atingindo estabilização após aproximadamente {tempo:.2f} ano(s).\n")

    # Análise global
    tempos_lista = list(tempos_dim.values())
    tempo_total = max(tempos_lista)

    st.write(f"De forma geral, o tempo necessário para a estabilização completa do sistema "
        f"é {tempo_total:.2f} ano(s), "
        "correspondendo à população que estabiliza mais lentamente.")
