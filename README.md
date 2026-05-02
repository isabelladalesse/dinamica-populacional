# Simulador de Dinâmica Populacional de Aguapés, Sapos-cururu e Escorpiões-amarelos

Este projeto consiste em um **simulador interativo de dinâmica populacional** desenvolvido em Python, utilizando um sistema de **equações diferenciais ordinárias (EDOs)** para modelar a interação entre quatro populações:

* Aguapés (A)
* Girinos (G)
* Sapos (S)
* Escorpiões (E)

A aplicação permite, a partir de uma condição incial de densidades populacionais, visualizar a evolução temporal das populações e interpretar automaticamente os resultados. Projeto desenvolvido para estudo de **modelagem matemática e biomatemática**, com foco em dinâmica populacional.

---

## Modelo Matemático

Em iniciação científica, modelei a interação entre as espécies supracitadas, obtendo:

$$
\begin{cases}
        \dfrac{dA}{dt} = n_aA\left(1-\dfrac{A}{k_a}\right)\\
        \dfrac{dG}{dt}=  n_{g} S\left(1-\dfrac{G}{\gamma(A)}\right) - \delta G\\
        \dfrac{dS}{dt}=\delta G - \mu_s S\\
        \dfrac{dE}{dt}=n_eE\left(1-\dfrac{E}{k_e}\right)-\lambda(E).
    \end{cases}
$$

Os valores dos parâmetros foram obtidos após uma cuidadosa revisão de literatura.

---

## Interface

A aplicação foi construída com **Streamlit**, permitindo:

* Inserção de parâmetros e condições iniciais
* Execução da simulação com um clique
* Visualização gráfica das populações
* Interpretação automática dos resultados

---

## Tecnologias utilizadas

* Python
* Streamlit
* NumPy
* SciPy
* Matplotlib
* SymPy (para manipulação simbólica)

---

## Como acessar o simulador

Esse projeto possui acesso livre através do Streamlit Cloud, pelo link: https://dinamica-populacional-blhbxzdb6jta29jxgv3myw.streamlit.app/.

---
