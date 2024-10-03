import pandas as pd
import webbrowser  # Importar o módulo para abrir o navegador

# 1. Carregar a base de dados
def carregar_dados(caminho):
    return pd.read_csv(caminho, encoding='latin1', delimiter=';')

# 2. Função para listar candidatos por município e cargo
def listar_candidatos_por_municipio(df, nome_municipio, codigo_cargo):
    # Mapeamento dos códigos de entrada (1, 2, 3) para os códigos do CSV (11, 12, 13)
    mapa_cargo = {1: 11, 2: 12, 3: 13}

    try:
        codigo_cargo = int(codigo_cargo)
        if codigo_cargo in mapa_cargo:
            codigo_cargo = mapa_cargo[codigo_cargo]
        else:
            print('Código de cargo inválido. Escolha 1 para Prefeito, 2 para Vice-prefeito, ou 3 para Vereador.')
            return None
    except ValueError:
        print('Código inválido. Insira um valor numérico.')
        return None

    # Filtrar pelo nome do município
    municipio_selecionado = df[df['NM_UE'].str.contains(nome_municipio, case=False, na=False)]
    
    if municipio_selecionado.empty:
        print(f'Nenhum município encontrado com o nome "{nome_municipio}". (Verifique a acentuação no nome do município).')
        return None

    candidatos = municipio_selecionado[municipio_selecionado['CD_CARGO'] == codigo_cargo]
    if candidatos.empty:
        print(f'Nenhum candidato encontrado para o município "{nome_municipio}" e cargo fornecidos.')
    else:
        return candidatos[['NM_CANDIDATO', 'NM_URNA_CANDIDATO', 'NR_CANDIDATO', 'NR_PARTIDO']]

# 3. Função para exibir informações de um candidato específico
def exibir_informacoes_candidato(df, codigo_candidato, nome_municipio):
    # Filtrar pelo município
    municipio_selecionado = df[df['NM_UE'].str.contains(nome_municipio, case=False, na=False)]
    
    if municipio_selecionado.empty:
        print(f'Nenhum município encontrado com o nome "{nome_municipio}". (Verifique a acentuação no nome do município).')
        return None

    # Filtrar o candidato pela sua votação
    candidato = municipio_selecionado[municipio_selecionado['NR_CANDIDATO'].astype(str) == str(codigo_candidato)]
    
    if candidato.empty:
        print(f'Candidato com número de votação "{codigo_candidato}" não encontrado no município "{nome_municipio}".')
    else:
        return candidato[['NM_CANDIDATO', 'NM_URNA_CANDIDATO', 'NR_CANDIDATO', 'NR_PARTIDO']]

# 4. Menu interativo
def menu(df):
    while True:
        print("\nMenu:")
        print("1. Listar candidatos por município e cargo")
        print("2. Exibir informações de um candidato")
        print("3. Gerar página HTML com estatísticas")
        print("4. Sair")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            nome_municipio = input("Digite o nome do município: ")
            codigo_cargo = input("Digite o código do cargo (1 para prefeito, 2 para vice-prefeito e 3 para vereador): ")
            candidatos = listar_candidatos_por_municipio(df, nome_municipio, codigo_cargo)
            if candidatos is not None:
                print(candidatos.to_string(index=False))
        
        elif escolha == '2':
            nome_municipio = input("Digite o nome do município: ")  # Solicitar o município primeiro
            codigo_candidato = input("Digite o número de votação do candidato: ")  # Solicitar o número de votação
            informacoes = exibir_informacoes_candidato(df, codigo_candidato, nome_municipio)
            if informacoes is not None:
                print(informacoes.to_string(index=False))
                
        elif escolha == '3':
            arquivo_html = 'index.html'  # Substitua pelo caminho do seu arquivo HTML
            webbrowser.open(arquivo_html)  # Abrir o arquivo HTML no navegador
            print(f'A página HTML foi aberta: {arquivo_html}')
            
        elif escolha == '4':
            print("Saindo...")
            break
        
        else:
            print("Opção inválida! Tente novamente.")

# 5. Execução do programa
if __name__ == "__main__":
    caminho = 'Eleitorado/consulta_cand_2024_PB.csv'  # Substitua pelo caminho do seu arquivo
    df = carregar_dados(caminho)
    menu(df)
