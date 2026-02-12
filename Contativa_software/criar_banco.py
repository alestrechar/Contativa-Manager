import sqlite3
import os

# Rodar o arquivo uma vez para que crie o banco de dados
# Garante que o banco será criado na mesma pasta do script
caminho_banco = os.path.join(os.path.dirname(__file__), 'contativa.db')

def criar_tabelas():
    print(f"Criando banco de dados em: {caminho_banco}")
    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()

    # 1. Tabela Usuários
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nomeusr TEXT, nomeemp TEXT, cnpj TEXT, emailusr TEXT, senha TEXT,
        status INTEGER DEFAULT 1
    );
    """)

    # 2. Tabela Empresas Clientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS empcliente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cnpj TEXT, nome_empresa TEXT, instestadual TEXT, instmunicipal TEXT,
        capital TEXT, tributacao TEXT, cnae TEXT, cep TEXT, rua TEXT, numero TEXT,
        cidade TEXT, estado TEXT, nomesocio TEXT, cpfsocio TEXT, email TEXT,
        cepsocio TEXT, ruasocio TEXT, numerosocio TEXT, cidadesocio TEXT, estadosocio TEXT,
        status INTEGER DEFAULT 1
    );
    """)

    # 3. Tabela Documentos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_empresa INTEGER,
        nome_arquivo TEXT, tipo_documento TEXT, caminho_arquivo TEXT,
        data_upload TEXT, status INTEGER DEFAULT 1
    );
    """)

    # 4. Tabela Admin
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usr TEXT, pword TEXT
    );
    """)

    # Cria admin padrão se não existir
    cursor.execute("SELECT * FROM admin WHERE usr='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO admin (usr, pword) VALUES ('admin', 'admin')")
        print("Usuário Admin criado: admin / admin")

    conn.commit()
    conn.close()
    print("Sucesso! Todas as tabelas foram criadas.")

if __name__ == "__main__":
    criar_tabelas()
