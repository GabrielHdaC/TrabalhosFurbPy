# ========================================================
# BIBLIOTECAS QUE VAMOS USAR
# ========================================================
# pandas -> para criar e manipular tabelas de dados
# matplotlib -> para gerar gráficos
# matplotlib_venn -> para criar os diagramas de Venn
# unicodedata -> para tratar acentos e maiúsculas/minúsculas
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3
import matplotlib
import unicodedata

# Essa linha faz os gráficos abrirem em uma janela separada
matplotlib.use('TkAgg')

# ========================================================
# 1. BASE DE DADOS
# ========================================================
# Aqui criamos uma "tabela" com os estados e quais indústrias
# existem em cada um (Automobilística, Têxtil e Petroquímica).
dados = {
    'Estado': [
        'São Paulo', 'Minas Gerais', 'Rio de Janeiro', 'Rio Grande do Sul',
        'Paraná', 'Santa Catarina', 'Bahia', 'Pernambuco', 'Ceará', 'Amazonas'
    ],
    'Automobilistica': ['Sim', 'Sim', 'Não', 'Sim', 'Sim', 'Não', 'Sim', 'Sim', 'Não', 'Não'],
    'Textil': ['Sim'] * 10,  # todos os estados têm indústria têxtil
    'Petroquimica': ['Sim', 'Não', 'Sim', 'Sim', 'Não', 'Não', 'Sim', 'Não', 'Não', 'Sim']
}

# Converte o dicionário para uma tabela (DataFrame do pandas)
df = pd.DataFrame(dados)

print("📊 DADOS DOS ESTADOS E INDÚSTRIAS:")
print(df.to_string(index=False))  # mostra a tabela de forma bonita no terminal

# ========================================================
# 2. CRIAÇÃO DOS CONJUNTOS
# ========================================================
# Cada indústria vai virar um conjunto (set), ou seja,
# um agrupamento de estados que têm aquela indústria.
A = set(df[df['Automobilistica'] == 'Sim']['Estado'])  # Automobilística
B = set(df[df['Textil'] == 'Sim']['Estado'])           # Têxtil
C = set(df[df['Petroquimica'] == 'Sim']['Estado'])     # Petroquímica
U = set(df['Estado'])                                  # Universo = todos os estados

# Para deixar os diagramas mais limpos, vamos usar siglas
ufs = {
    'São Paulo': 'SP', 'Minas Gerais': 'MG', 'Rio de Janeiro': 'RJ',
    'Rio Grande do Sul': 'RS', 'Paraná': 'PR', 'Santa Catarina': 'SC',
    'Bahia': 'BA', 'Pernambuco': 'PE', 'Ceará': 'CE', 'Amazonas': 'AM'
}

# ========================================================
# 3. FUNÇÃO PARA NORMALIZAR TEXTO
# ========================================================
# Essa função serve para não dar erro quando o usuário digitar
# sem acento ou em minúsculo. Exemplo: "sao paulo" = "São Paulo".
def _normaliza(txt: str) -> str:
    s = unicodedata.normalize('NFKD', txt)
    s = ''.join(c for c in s if not unicodedata.combining(c))  # tira acentos
    s = ' '.join(s.lower().split())  # deixa minúsculo e remove espaços extras
    return s

# ========================================================
# 4. FUNÇÃO DE PERGUNTA (O QUIZ)
# ========================================================
# Essa função faz uma pergunta, pede a resposta do usuário,
# e só avança quando ele acertar.
def pergunta(titulo, enunciado, resposta_correta, explicacao):
    print(f"\n🔶 {titulo}")
    print(enunciado)

    if isinstance(resposta_correta, set):  # quando a resposta é um conjunto de estados
        gabarito = {_normaliza(x) for x in resposta_correta}
        while True:
            raw = input("Sua resposta (separe por vírgulas): ").strip()
            tokens = [t for t in raw.replace(';', ',').split(',') if t.strip()]
            resposta_usuario = {_normaliza(t) for t in tokens}
            if resposta_usuario == gabarito:
                print("✅ Correto!")
                print(explicacao)
                break
            else:
                print("❌ Incorreto! Tente novamente...")
    else:  # quando a resposta é "sim" ou "não"
        gabarito = _normaliza(str(resposta_correta))
        while True:
            raw = input("Sua resposta: ").strip()
            if _normaliza(raw) == gabarito:
                print("✅ Correto!")
                print(explicacao)
                break
            else:
                print("❌ Incorreto! Tente novamente...")

# ========================================================
# 5. FUNÇÕES PARA DESENHAR DIAGRAMAS
# ========================================================
def diagrama_venn2(conj1, conj2, nome1, nome2, titulo):
    """Mostra um diagrama de Venn de 2 conjuntos, com as siglas dos estados"""
    plt.figure(figsize=(8, 6))
    only1, only2, both = conj1 - conj2, conj2 - conj1, conj1 & conj2
    venn = venn2(subsets=(len(only1), len(only2), len(both)),
                 set_labels=(nome1, nome2))

    # Substitui os números pelas siglas (UFs)
    if venn.get_label_by_id('10'):
        venn.get_label_by_id('10').set_text('\n'.join(sorted([ufs[e] for e in only1])))
    if venn.get_label_by_id('01'):
        venn.get_label_by_id('01').set_text('\n'.join(sorted([ufs[e] for e in only2])))
    if venn.get_label_by_id('11'):
        venn.get_label_by_id('11').set_text('\n'.join(sorted([ufs[e] for e in both])))

    plt.title(titulo, fontsize=14)
    plt.show()

def diagrama_final():
    """Mostra o diagrama de Venn com os 3 conjuntos (A, B e C)"""
    plt.figure(figsize=(12, 8))
    venn = venn3([A, B, C],
                 set_labels=('Automobilística (A)', 'Têxtil (B)', 'Petroquímica (C)'))

    # Preenche cada parte com as siglas
    if venn.get_label_by_id('100'):
        venn.get_label_by_id('100').set_text('\n'.join(sorted([ufs[e] for e in A - B - C])))
    if venn.get_label_by_id('010'):
        venn.get_label_by_id('010').set_text('\n'.join(sorted([ufs[e] for e in B - A - C])))
    if venn.get_label_by_id('001'):
        venn.get_label_by_id('001').set_text('\n'.join(sorted([ufs[e] for e in C - A - B])))
    if venn.get_label_by_id('110'):
        venn.get_label_by_id('110').set_text('\n'.join(sorted([ufs[e] for e in (A & B) - C])))
    if venn.get_label_by_id('101'):
        venn.get_label_by_id('101').set_text('\n'.join(sorted([ufs[e] for e in (A & C) - B])))
    if venn.get_label_by_id('011'):
        venn.get_label_by_id('011').set_text('\n'.join(sorted([ufs[e] for e in (B & C) - A])))
    if venn.get_label_by_id('111'):
        venn.get_label_by_id('111').set_text('\n'.join(sorted([ufs[e] for e in A & B & C])))

    plt.title("Diagrama de Venn Final - Estados por Indústrias", fontsize=14)
    plt.show()

# ========================================================
# 6. PERGUNTAS DO TRABALHO
# ========================================================
# Agora vem as perguntas exigidas no enunciado.
# O programa só avança se o usuário acertar cada uma.

# 1. União
pergunta(
    "Pergunta 1 - União",
    "Quais estados pertencem a A ∪ C (Automobilística OU Petroquímica)?",
    A | C,
    f"A ∪ C = {A | C}"
)
diagrama_venn2(A, C, "Automobilística", "Petroquímica", "União A ∪ C")

# 2. Interseção
pergunta(
    "Pergunta 2 - Interseção",
    "Quais estados pertencem a A ∩ B (Automobilística E Têxtil)?",
    A & B,
    f"A ∩ B = {A & B}"
)
diagrama_venn2(A, B, "Automobilística", "Têxtil", "Interseção A ∩ B")

# 3. Diferença
pergunta(
    "Pergunta 3 - Diferença",
    "Quais estados pertencem a B - C (Têxtil mas NÃO Petroquímica)?",
    B - C,
    f"B - C = {B - C}"
)
diagrama_venn2(B, C, "Têxtil", "Petroquímica", "Diferença B - C")

# 4. Complementar
pergunta(
    "Pergunta 4 - Complementar",
    "Quais estados pertencem ao complementar de A (A')?",
    U - A,
    f"A' = {U - A}"
)

# 5. Subconjunto
sul = {"Rio Grande do Sul", "Paraná", "Santa Catarina"}
pergunta(
    "Pergunta 5 - Subconjunto",
    "O conjunto dos estados do Sul que têm Têxtil é subconjunto de B?",
    sul & B,
    f"Sul ∩ B = {sul & B} ⊆ B"
)

# 6. Pertinência
pergunta(
    "Pergunta 6 - Pertinência",
    "O estado 'São Paulo' pertence ao conjunto C (Petroquímica)? (sim/não)",
    "sim" if "São Paulo" in C else "não",
    f"São Paulo {'∈' if 'São Paulo' in C else '∉'} C"
)

# ========================================================
# 7. DIAGRAMA FINAL
# ========================================================
# Por último, mostramos o diagrama de Venn com os 3 conjuntos juntos.
diagrama_final()
