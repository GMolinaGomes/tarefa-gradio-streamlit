# Importações e constantes

import os
from datetime import datetime

import pandas as pd
import gradio as gr

ARQUIVO_CSV = "pacientes.csv"
COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]

# Função de cadastro

def cadastrar_paciente(nome, idade, convenio, prioridade, motivo):
    linha = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome,
        "idade": idade,
        "convenio": convenio,
        "prioridade": prioridade,
        "motivo": motivo,
    }
    novo = pd.DataFrame([linha], columns=COLUNAS)

    if os.path.exists(ARQUIVO_CSV):
        novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False)
    else:
        novo.to_csv(ARQUIVO_CSV, mode="w", header=True, index=False)

    return (
        "Paciente cadastrado com sucesso!",
        pd.read_csv(ARQUIVO_CSV).tail(5),
        "",    # nome
        None,  # idade
        None,  # convênio
        1,     # prioridade
        "",    # motivo
    )

with gr.Blocks() as demo:
    gr.Markdown("## Cadastro de Pacientes")

    nome = gr.Textbox(label="Nome do paciente")
    idade = gr.Number(label="Idade", precision=0)
    convenio = gr.Dropdown(
        ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"],
        label="Convênio",
    )
    prioridade = gr.Slider(1, 5, step=1, label="Prioridade do atendimento")
    motivo = gr.Textbox(label="Motivo da consulta / observações", lines=3)

    botao = gr.Button("Cadastrar")
    saida_msg = gr.Textbox(label="Status", interactive=False)
    tabela = gr.Dataframe(label="Últimos pacientes cadastrados")

    botao.click(
        cadastrar_paciente,
        [nome, idade, convenio, prioridade, motivo],
        [saida_msg, tabela, nome, idade, convenio, prioridade, motivo],
    )

demo.launch()
