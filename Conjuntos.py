import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3
import matplotlib
import sys

# Configuração para funcionar tanto no Colab quanto no VS Code
if 'google.colab' in sys.modules or 'ipykernel' in sys.modules:
    pass  # Colab/Jupyter já sabem exibir gráficos
else:
    matplotlib.use('TkAgg')  # No VS Code abre janelas separadas

# ----------------------------
# Carregando os dados
# ----------------------------
# Aqui temos a tabela de estados com as três indústrias: Automobilística, Têxtil e Petroquímica
dados = {
    'Estado': [
        'São Paulo', 'Minas Gerais', 'Rio de Janeiro', 'Rio Grande do Sul',
        'Paraná', 'Santa Catarina', 'Bahia', 'Pernambuco', 'Ceará', 'Amazonas'
    ],
    'Automobilistica': ['Sim', 'Sim', 'Não', 'Sim', 'Sim', 'Não', 'Sim', 'Sim', 'Não', 'Não'],
    'Textil': ['Sim'] * 10,
    'Petroquimica': ['Sim', 'Não', 'Sim', 'Sim', 'Não', 'Não', 'Sim', 'Não', 'Não', 'Sim']
}

df = pd.DataFrame(dados)

print("\n📊 BASE DE DADOS - ESTADOS E INDÚSTRIAS:")
print(df.to_string(index=False))

# ----------------------------
# Criando os conjuntos
# ----------------------------
# A partir da tabela, cada indústria se torna um conjunto (set).
A = set(df[df['Automobilistica'] == 'Sim']['Estado'])
B = set(df[df['Textil'] == 'Sim']['Estado'])
C = set(df[df['Petroquimica'] == 'Sim']['Estado'])
U = set(df['Estado'])  # Universo de todos os estados

# Siglas para deixar os diagramas mais limpos
ufs = {
    'São Paulo': 'SP', 'Minas Gerais': 'MG', 'Rio de Janeiro': 'RJ',
    'Rio Grande do Sul': 'RS', 'Paraná': 'PR', 'Santa Catarina': 'SC',
    'Bahia': 'BA', 'Pernambuco': 'PE', 'Ceará': 'CE', 'Amazonas': 'AM'
}

# ----------------------------
# Função para perguntas
# ----------------------------
# Essa função faz a pergunta, compara a resposta do usuário e mostra se está correta.
def pergunta(titulo, pergunta_texto, resposta_correta, explicacao):
    print("\n" + "="*60)
    print(f"🔶 {titulo}")
    print(pergunta_texto)
    resposta = input("Sua resposta: ").strip()

    if isinstance(resposta_correta, set):
        resposta_usuario = {estado.strip().title() for estado in resposta.replace(';', ',').split(',')}
        if resposta_usuario == resposta_correta:
            print("✅ CORRETO!")
            print(explicacao)
        else:
            print("❌ INCORRETO!")
            print(f"Resposta correta: {explicacao}")
    else:
        if resposta.lower() == str(resposta_correta).lower():
            print("✅ CORRETO!")
            print(explicacao)
        else:
            print("❌ INCORRETO!")
            print(f"Resposta correta: {explicacao}")

# ----------------------------
# Funções de diagramas
# ----------------------------
# Cria diagramas de Venn para dois conjuntos, destacando a operação escolhida.
def diagrama_venn2(conj1, conj2, nome1, nome2, titulo, destacar='união'):
    plt.figure(figsize=(12, 8))
    only1, only2, both = conj1 - conj2, conj2 - conj1, conj1 & conj2
    venn = venn2(subsets=(len(only1), len(only2), len(both)),
                 set_labels=(nome1, nome2))

    # Definindo cores conforme a operação
    if destacar == 'união':
        if venn.get_patch_by_id('10'): venn.get_patch_by_id('10').set_color('#FFD700')
        if venn.get_patch_by_id('01'): venn.get_patch_by_id('01').set_color('#87CEEB')
        if venn.get_patch_by_id('11'): venn.get_patch_by_id('11').set_color('#98FB98')
    elif destacar == 'interseção':
        if venn.get_patch_by_id('10'): venn.get_patch_by_id('10').set_color('#DDDDDD')
        if venn.get_patch_by_id('01'): venn.get_patch_by_id('01').set_color('#DDDDDD')
        if venn.get_patch_by_id('11'): venn.get_patch_by_id('11').set_color('#FF0000FF')
    elif destacar == 'diferença':
        if venn.get_patch_by_id('10'): venn.get_patch_by_id('10').set_color('#FF8C00')
        if venn.get_patch_by_id('01'): venn.get_patch_by_id('01').set_color('#DDDDDD')
        if venn.get_patch_by_id('11'): venn.get_patch_by_id('11').set_color('#DDDDDD')

    # Labels com siglas
    if venn.get_label_by_id('10'):
        venn.get_label_by_id('10').set_text('\n'.join(sorted([ufs[e] for e in only1])))
    if venn.get_label_by_id('01'):
        venn.get_label_by_id('01').set_text('\n'.join(sorted([ufs[e] for e in only2])))
    if venn.get_label_by_id('11'):
        venn.get_label_by_id('11').set_text('\n'.join(sorted([ufs[e] for e in both])))

    plt.title(titulo, fontsize=16, fontweight='bold', pad=20)
    plt.show()

# Diagrama com os três conjuntos (A, B e C)
def diagrama_final():
    plt.figure(figsize=(14, 10))
    venn = venn3(
        subsets=(len(A - B - C), len(B - A - C), len((A & B) - C),
                 len(C - A - B), len((A & C) - B), len((B & C) - A), len(A & B & C)),
        set_labels=('Automobilística (A)', 'Têxtil (B)', 'Petroquímica (C)')
    )
    plt.title('DIAGRAMA FINAL - DISTRIBUIÇÃO DAS INDÚSTRIAS POR ESTADO',
              fontsize=16, fontweight='bold', pad=30)
    plt.show()
