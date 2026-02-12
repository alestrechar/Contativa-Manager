# Rodar o arquivo 'criar_banco.py' uma vez para que crie o banco de dados

from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3  # Mudamos de mysql.connector para sqlite3
import os
from werkzeug.utils import secure_filename
from datetime import datetime

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Função para conectar ao banco SQLite
def get_db_connection():
    # Isso garante que ele sempre ache o banco na pasta correta
    caminho_banco = os.path.join(os.path.dirname(__file__), 'contativa.db')
    conn = sqlite3.connect(caminho_banco)
    conn.row_factory = sqlite3.Row
    return conn

routes_bp = Blueprint('routes', __name__)
    
@routes_bp.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    mostrar_navbar=False
    mostrar_botao_sair=False
    if request.method == 'GET':
        return render_template("cadastro.html", mostrar_navbar=mostrar_navbar, mostrar_botao_sair=mostrar_botao_sair)
    else:
        conn = get_db_connection()
        cursor = conn.cursor()

        SQL_COMMAND = "INSERT INTO usuarios(nomeusr, nomeemp, cnpj, emailusr, senha) VALUES (?,?,?,?,?)"

        nomeusr = request.form['nomeusr']
        nomeemp = request.form['nomeemp']
        cnpj = request.form['cnpj']
        emailusr = request.form['emailusr']
        senhausr = request.form['senhausr']
        values = (nomeusr, nomeemp, cnpj, emailusr, senhausr)
        cursor.execute(SQL_COMMAND, values)
        conn.commit()
        conn.close()
        
        return redirect(url_for('routes.login'))

def verificar_login():
    if 'user' not in session:
        return redirect(url_for('routes.login'))

@routes_bp.route('/', methods=["GET", "POST"])
def login():
    mostrar_navbar = False
    mostrar_botao_sair = False

    if request.method == 'POST':
        cnpj = request.form['cnpj']
        nomeusr = request.form['nomeusr']
        senha = request.form['senha']

        # 1. Abre a conexão nova
        conn = get_db_connection()
        cursor = conn.cursor()

        # 2. SQL com ? no lugar de %s
        SQL_COMMAND = "SELECT * FROM usuarios WHERE cnpj=? AND nomeusr=? AND senha=? AND status=1"
        values = (cnpj, nomeusr, senha)
        
        cursor.execute(SQL_COMMAND, values)
        user = cursor.fetchone()
        
        # 3. Fecha a conexão (Importante no SQLite!)
        conn.close()

        if user:
            # 4. Converte para dicionário antes de salvar na sessão
            session['user'] = dict(user) 
            return redirect(url_for('routes.inicio'))
        else:
            print(f"Erro no Login: Usuario ou senha incorretos")
            mensagem = "Usuário, CPNJ ou Senha incorretos!"
            return render_template('login.html', mostrar_navbar=mostrar_navbar, mostrar_botao_sair=mostrar_botao_sair, mensagem=mensagem)

    return render_template('login.html', mostrar_navbar=mostrar_navbar, mostrar_botao_sair=mostrar_botao_sair)

@routes_bp.route('/redefinir_senha')
def redefinir_senha():
    mostrar_navbar=False
    mostrar_botao_sair=False
    return render_template('redefinir_senha.html', mostrar_navbar=mostrar_navbar, mostrar_botao_sair=mostrar_botao_sair)
    
@routes_bp.route('/codigo_senha')
def codigo_senha():
    mostrar_navbar=False
    mostrar_botao_sair=False
    return render_template('codigo_senha.html', mostrar_navbar=mostrar_navbar, mostrar_botao_sair=mostrar_botao_sair)

@routes_bp.route('/software_empresas', methods=["GET", "POST"])
def software_empresas():
    mostrar_navbar=True
    mostrar_botao_sair=True

    if 'user' not in session:
        return redirect(url_for('routes.login'))
    
    return render_template('inicio.html', mostrar_navbar=mostrar_navbar, mostrar_botao_sair=mostrar_botao_sair)

@routes_bp.route('/cadastro_empresa_cliente', methods=["GET", "POST"])
def cadastro_empresa_cliente():
    mostrar_navbar = True
    mostrar_botao_sair = True
    if 'user' not in session:
        return redirect(url_for('routes.login'))

    if request.method == 'POST':
        conn = get_db_connection() # Abre conexão
        cursor = conn.cursor()
        try:
            # Pega todos os dados do formulário
            cnpj = request.form.get('cnpj', '')
            nome_empresa = request.form.get('nome_empresa', '')
            instestadual = request.form.get('instestadual', '')
            instmunicipal = request.form.get('instmunicipal', '')
            capital = request.form.get('capital', '')
            tributacao = request.form.get('tributacao', '')
            cnae = request.form.get('cnae', '')
            cep = request.form.get('cep', '')  
            rua = request.form.get('rua', '')
            numero = request.form.get('numero', '')
            cidade = request.form.get('cidade', '')
            estado = request.form.get('estado', '')
            nomesocio = request.form.get('nomesocio', '')
            cpfsocio = request.form.get('cpfsocio', '')
            email = request.form.get('emailsocio', '')
            cepsocio = request.form.get('cepsocio1', '')  
            ruasocio = request.form.get('ruasocio', '')
            numerosocio = request.form.get('numerosocio', '')
            cidadesocio = request.form.get('cidadesocio', '')
            estadosocio = request.form.get('estadosocio', '')

            # SQL com ? (SQLite)
            SQL_COMMAND = """
                INSERT INTO empcliente (
                    cnpj, nome_empresa, instestadual, instmunicipal, capital, 
                    tributacao, cnae, cep, rua, numero, cidade, estado,
                    nomesocio, cpfsocio, email, cepsocio, ruasocio,
                    numerosocio, cidadesocio, estadosocio
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            """

            values = (
                cnpj, nome_empresa, instestadual, instmunicipal, capital,
                tributacao, cnae, cep, rua, numero, cidade,
                estado, nomesocio, cpfsocio, email, cepsocio,
                ruasocio, numerosocio, cidadesocio, estadosocio, 
            )

            cursor.execute(SQL_COMMAND, values)  
            conn.commit()
            return redirect(url_for('routes.empresas'))

        except Exception as e:
            conn.rollback()
            print(f"Erro: {e}")
            return redirect(url_for('routes.cadastro_empresa_cliente'))

        finally:
            conn.close() # Fecha conexão sempre!

    return render_template(
        "cadastro_empresa_cliente.html",
        mostrar_navbar=mostrar_navbar,
        mostrar_botao_sair=mostrar_botao_sair
    )

@routes_bp.route('/documentos', methods=['GET', 'POST'])
def documentos():
    if 'user' not in session:
        return redirect(url_for('routes.login'))
        
    mostrar_navbar = True
    mostrar_botao_sair = True
    mensagem = None
    
    # Busca empresas para o dropdown
    conn = get_db_connection()
    cursor = conn.cursor()
    SQL_COMMAND = "SELECT id, nome_empresa FROM empcliente WHERE status = 1"
    cursor.execute(SQL_COMMAND)
    empresas = cursor.fetchall()
    
    if request.method == 'POST':
        try:
            if 'arquivo' not in request.files:
                mensagem = "Nenhum arquivo selecionado"
                return redirect(request.url)
            
            file = request.files['arquivo']
            if file.filename == '':
                mensagem = "Nenhum arquivo selecionado"
                return redirect(request.url)
                
            id_empresa = request.form.get('empresa')
            tipo_documento = request.form.get('tipo')
            
            if file and allowed_file(file.filename):
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
            
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                
                # Inserção com SQLite
                SQL_COMMAND = """
                    INSERT INTO documentos 
                    (id_empresa, nome_arquivo, tipo_documento, caminho_arquivo, data_upload, status) 
                    VALUES (?, ?, ?, ?, ?, 1)
                """
                values = (
                    id_empresa, file.filename, tipo_documento,
                    filename, datetime.now()
                )
                
                cursor.execute(SQL_COMMAND, values)
                conn.commit()
                mensagem = "Documento enviado com sucesso!"
                
        except Exception as e:
            print(f"Erro no upload: {str(e)}")
            conn.rollback()
            mensagem = "Erro ao enviar documento"

    # Lista documentos
    SQL_COMMAND = """
        SELECT d.*, e.nome_empresa 
        FROM documentos d 
        JOIN empcliente e ON d.id_empresa = e.id 
        WHERE d.status = 1 
        ORDER BY d.data_upload DESC
    """
    cursor.execute(SQL_COMMAND)
    documentos_lista = cursor.fetchall() # Mudei o nome da variável para não confundir com a função
    conn.close()
    
    return render_template(
        'documentos.html',
        mostrar_navbar=mostrar_navbar,
        mostrar_botao_sair=mostrar_botao_sair,
        empresas=empresas,
        documentos=documentos_lista,
        mensagem=mensagem
    )

@routes_bp.route('/documentos/excluir/<int:id>')
def excluir_documento(id):
    if 'user' not in session:
        return redirect(url_for('routes.login'))
        
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        SQL_SELECT = "SELECT caminho_arquivo FROM documentos WHERE id = ?"
        cursor.execute(SQL_SELECT, (id,))
        resultado = cursor.fetchone()
        
        if resultado:
            caminho_arquivo = os.path.join(UPLOAD_FOLDER, resultado['caminho_arquivo']) # Acesso por chave string

            if os.path.exists(caminho_arquivo):
                try:
                    os.remove(caminho_arquivo)
                except:
                    pass # Se não conseguir deletar o arquivo, continua para inativar no banco

        SQL_UPDATE = "UPDATE documentos SET status = 0 WHERE id = ?"
        cursor.execute(SQL_UPDATE, (id,))
        conn.commit()
        
    except Exception as e:
        print(f"Erro ao excluir documento: {str(e)}")
        conn.rollback()
    finally:
        conn.close()
        
    return redirect(url_for('routes.documentos'))

@routes_bp.route('/inicio')
def inicio():

    if 'user' not in session:
        return redirect(url_for('routes.login'))
        
    mostrar_navbar = True
    mostrar_botao_sair = True
    

    user = session.get('user', {})
    nome_usuario = user.get('nomeusr', '')
    nome_empresa = user.get('nomeemp', '')
    
    return render_template(
        'inicio.html',
        mostrar_navbar=mostrar_navbar,
        mostrar_botao_sair=mostrar_botao_sair,
        nome_usuario=nome_usuario,
        nome_empresa=nome_empresa
    )

@routes_bp.route('/relatorios')
def relatorios():
    if 'user' not in session:
        return redirect(url_for('routes.login'))
        
    mostrar_navbar = True
    mostrar_botao_sair = True
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Como configuramos row_factory, podemos acessar ['chave']
        cursor.execute("SELECT COUNT(id) as total_usuarios FROM usuarios")
        res_usuarios = cursor.fetchone()
        total_usuarios = res_usuarios['total_usuarios'] if res_usuarios else 0
        
        cursor.execute("SELECT COUNT(id) as total_empresas FROM empcliente")
        res_empresas = cursor.fetchone()
        total_empresas = res_empresas['total_empresas'] if res_empresas else 0
        
        cursor.execute("SELECT COUNT(id) as total_documentos FROM documentos")
        res_docs = cursor.fetchone()
        total_documentos = res_docs['total_documentos'] if res_docs else 0
        
        estatisticas = {
            'total_usuarios': total_usuarios,
            'total_empresas': total_empresas,
            'total_documentos': total_documentos
        }
        
    except Exception as e:
        print(f"Erro ao buscar estatísticas: {str(e)}")
        estatisticas = {'total_usuarios': 0, 'total_empresas': 0, 'total_documentos': 0}
    finally:
        conn.close()
    
    return render_template(
        'relatorios.html',
        mostrar_navbar=mostrar_navbar,
        mostrar_botao_sair=mostrar_botao_sair,
        estatisticas=estatisticas
    )

@routes_bp.route('/impostos')
def impostos():
    mostrar_navbar=True
    mostrar_botao_sair=True
    if 'user' not in session:
        return redirect(url_for('routes.login'))
    return render_template('impostos.html', mostrar_navbar=mostrar_navbar, mostrar_botao_sair=mostrar_botao_sair)

@routes_bp.route('/empresas')
def empresas():
    if 'user' not in session:
        return redirect(url_for('routes.login'))
        
    mostrar_navbar = True
    mostrar_botao_sair = True
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        SQL_COMMAND = """
            SELECT id, cnpj, nome_empresa, instestadual, instmunicipal, 
                   capital, tributacao, cnae, cep, rua, numero, 
                   cidade, estado, nomesocio, cpfsocio, email,
                   cepsocio, ruasocio, numerosocio, cidadesocio, 
                   estadosocio, status
            FROM empcliente
        """
        cursor.execute(SQL_COMMAND)
        empresas = cursor.fetchall()
    except Exception as e:
        empresas = []
    finally:
        conn.close()
    
    return render_template(
        'empresas.html',
        mostrar_navbar=mostrar_navbar,
        mostrar_botao_sair=mostrar_botao_sair,
        empresas=empresas
    )

@routes_bp.route('/reativar_empresa/<int:id>')
def reativar_empresa(id):
    if 'user' not in session: return redirect(url_for('routes.login'))
    conn = get_db_connection()
    try:
        conn.execute("UPDATE empcliente SET status = 1 WHERE id = ?", (id,))
        conn.commit()
    except: pass
    finally: conn.close()
    return redirect(url_for('routes.empresas'))

@routes_bp.route('/editar_empresa/<int:id>', methods=['GET', 'POST'])
def editar_empresa(id):
    if 'user' not in session:
        return redirect(url_for('routes.login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        try:
            SQL_COMMAND = "SELECT * FROM empcliente WHERE id = ?" # Uso de ?
            cursor.execute(SQL_COMMAND, (id,))
            empresa = cursor.fetchone()
            
            if not empresa:
                return redirect(url_for('routes.empresas'))
                
            return render_template(
                'cadastro_empresa_cliente.html',
                empresa=empresa,
                modo_edicao=True
            )
        finally:
            conn.close()
            
    elif request.method == 'POST':
        try:
            SQL_COMMAND = """
                UPDATE empcliente SET
                    cnpj = ?, nome_empresa = ?, instestadual = ?, instmunicipal = ?,
                    capital = ?, tributacao = ?, cnae = ?, cep = ?,
                    rua = ?, numero = ?, cidade = ?, estado = ?,
                    nomesocio = ?, cpfsocio = ?, email = ?, cepsocio = ?,
                    ruasocio = ?, numerosocio = ?, cidadesocio = ?, estadosocio = ?
                WHERE id = ?
            """
            
            values = (
                request.form.get('cnpj'), request.form.get('nome_empresa'),
                request.form.get('instestadual'), request.form.get('instmunicipal'),
                request.form.get('capital'), request.form.get('tributacao'),
                request.form.get('cnae'), request.form.get('cep'),
                request.form.get('rua'), request.form.get('numero'),
                request.form.get('cidade'), request.form.get('estado'),
                request.form.get('nomesocio'), request.form.get('cpfsocio'),
                request.form.get('email'), request.form.get('cepsocio'),
                request.form.get('ruasocio'), request.form.get('numerosocio'),
                request.form.get('cidadesocio'), request.form.get('estadosocio'),
                id
            )
            
            cursor.execute(SQL_COMMAND, values)
            conn.commit()
            return redirect(url_for('routes.empresas'))
            
        except Exception as e:
            conn.rollback()
            return redirect(url_for('routes.empresas'))
        finally:
            conn.close()

@routes_bp.route('/inativar_empresa/<int:id>')
def inativar_empresa(id):
    if 'user' not in session: return redirect(url_for('routes.login'))
    conn = get_db_connection()
    try:
        conn.execute("UPDATE empcliente SET status = 0 WHERE id = ?", (id,))
        conn.commit()
    except: pass
    finally: conn.close()
    return redirect(url_for('routes.empresas'))

@routes_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.login'))

@routes_bp.route('/admin', methods=['GET','POST'])
def adm():
    if request.method == 'POST':
        usuario = request.form['user']
        senha = request.form['senha']

        conn = get_db_connection()
        cursor = conn.cursor()
        
        SQL_COMMAND = "SELECT * FROM admin WHERE usr=? AND pword=?"
        cursor.execute(SQL_COMMAND, (usuario, senha))
        admin = cursor.fetchone()
        conn.close()

        if admin:
            session['admin'] = dict(admin) # Converte para dict para a sessão
            return redirect(url_for('routes.admindex'))
        else:
            mensagem = "Usuário ou Senha incorretos!"
            return render_template('admin.html', mensagem=mensagem)
        
    return render_template('admin.html')

@routes_bp.route('/admindex')
def admindex():
    if 'admin' not in session:
        return redirect(url_for('routes.adm'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    SQL_COMMAND = "SELECT * FROM usuarios"
    cursor.execute(SQL_COMMAND)
    usuarios = cursor.fetchall()
    conn.close()
    
    return render_template('admindex.html', usuarios=usuarios)

@routes_bp.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    if 'admin' not in session:
        return redirect(url_for('routes.adm'))
        
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        SQL_COMMAND = "SELECT * FROM usuarios WHERE id = ?"
        cursor.execute(SQL_COMMAND, (id,))
        usuario = cursor.fetchone()
        conn.close()
        
        if not usuario:
            return redirect(url_for('routes.admindex'))
            
        return render_template('editar_usuario.html', usuario=usuario)
        
    elif request.method == 'POST':
        try:
            SQL_COMMAND = """
                UPDATE usuarios 
                SET nomeusr = ?, nomeemp = ?, cnpj = ?, emailusr = ?, senha = ?
                WHERE id = ?
            """
            
            values = (
                request.form['nomeusr'],
                request.form['nomeemp'],
                request.form['cnpj'],
                request.form['emailusr'],
                request.form['senha'],
                id
            )
            
            cursor.execute(SQL_COMMAND, values)
            conn.commit()
            return redirect(url_for('routes.admindex'))
            
        except Exception as e:
            conn.rollback()
            print(f"Erro ao atualizar usuário: {str(e)}")
            return redirect(url_for('routes.admindex'))
        finally:
            conn.close()

@routes_bp.route('/inativar_usuario/<int:id>')
def inativar_usuario(id):
    if 'admin' not in session: return redirect(url_for('routes.adm'))
    conn = get_db_connection()
    try:
        conn.execute("UPDATE usuarios SET status = 0 WHERE id = ?", (id,))
        conn.commit()
    except: pass
    finally: conn.close()
    return redirect(url_for('routes.admindex'))

@routes_bp.route('/reativar_usuario/<int:id>')
def reativar_usuario(id):
    if 'admin' not in session: return redirect(url_for('routes.adm'))
    conn = get_db_connection()
    try:
        conn.execute("UPDATE usuarios SET status = 1 WHERE id = ?", (id,))
        conn.commit()
    except: pass
    finally: conn.close()
    return redirect(url_for('routes.admindex'))
