#from flask import Flask, render_template,url_for,request,redirect
#import sqlite3


from flask import Flask,render_template,url_for,request,redirect
import pymysql  # Importar el conector PyMySQL


#def get_temporadas(Titulo):
#    conn = mysql.connect('src/database/series_retro.db')
#    query = """SELECT s.Titulo,s.imagen,s.Descripcion,s.Anio, s.Genero,t.NumeroTemporada, t.TemporadaID FROM Series s
#    LEFT JOIN Temporadas t ON t.SerieID = s.SerieID
#    WHERE s.Titulo = ?"""
#    temporadas = conn.execute(query, (Titulo,)).fetchall()
#    conn.close()
#    return temporadas
#
#
#def get_capitulos_por_temporada(TemporadaID):
#    conn = sqlite3.connect('src/database/series_retro.db')
#    query = """
#    SELECT s.Titulo, t.NumeroTemporada, c.NumeroCpitulo, c.EnlaceCapitulo, t.TemporadaID,c.CapituloID
#    FROM Series s
#    LEFT JOIN Temporadas t ON t.SerieID = s.SerieID
#    JOIN Capitulos c ON t.TemporadaID = c.TemporadaID
#    WHERE t.TemporadaID = ? 
#    ORDER BY t.NumeroTemporada ASC, c.NumeroCpitulo ASC
#    """
#    capitulos = conn.execute(query, (TemporadaID,)).fetchall()
#    conn.close()
#    return capitulos
#
#
#def get_capitulo(CapituloID):
#    conn = sqlite3.connect('src/database/series_retro.db')
#    query = """SELECT NumeroCpitulo,EnlaceCapitulo from Temporadas t
#    JOIN Capitulos c ON  t.TemporadaID=c.TemporadaID
#    WHERE c.CapituloID = ?
#    """
#    capitulo = conn.execute(query, (CapituloID,)).fetchall()
#    conn.close()
#    return capitulo
#
#
##def get_titulo(Titulo):
##    conn = sqlite3.connect('src/database/series_retro.db')
##    Titulo = f'%{Titulo}%'
##    sql_query = """SELECT Titulo,imagen FROM Series
##    WHERE REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
##    LOWER(Titulo), 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o'), 'ú', 'u') LIKE LOWER(?)
##    """
##    titulo = conn.execute(sql_query, (Titulo,)).fetchall()
##    conn.close()
##    return titulo
#
##def get_titulo(Titulo):
##    conn = mysql.connect('src/database/series_retro.db')
##    Titulo = f'%{Titulo}%'
##    sql_query = """SELECT Titulo,imagen FROM Series
##    WHERE REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
##    LOWER(Titulo), 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o'), 'ú', 'u') LIKE LOWER(?)
##    """
##    titulo = conn.execute(sql_query, (Titulo,)).fetchall()
##    conn.close()
##    return titulo
#
#
#def get_anios():
#    conn = sqlite3.connect('src/database/series_retro.db')
#    query = """SELECT DISTINCT Anio
#    FROM Series
#    ORDER BY Anio"""
#    anios = conn.execute(query).fetchall()
#    conn.close()
#    return anios
#
#
#def obtener_datos_anio(anio):
#    conn = sqlite3.connect('src/database/series_retro.db')
#    query = """SELECT Titulo,imagen FROM Series
#    WHERE Anio = ?"""
#    data = conn.execute(query, (anio,)).fetchall()
#    conn.close()
#    return data
#
#
#def obtener_datos(pagina, por_pagina):
#    conn = sqlite3.connect('src/database/series_retro.db')
#    query = """
#    SELECT * FROM Series LIMIT ? OFFSET ?
#    """
#    offset = (pagina - 1) * por_pagina
#    datos = conn.execute(query, (por_pagina, offset)).fetchall()
#    return datos
#
#
#def contar_datos():
#    conn = sqlite3.connect('src/database/series_retro.db')
#    cursor = conn.cursor()
#    cursor.execute('SELECT COUNT(*) FROM Series')
#    total = cursor.fetchone()[0]
#    conn.close()
#    return total
#
#
#
app = Flask(__name__)

# Configuración de la conexión a la base de datos
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = 'tatiana2006'
DB_NAME = 'series_retro'

def get_db_connection():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_NAME)
    return conn

def get_peliculas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM series')
    total_records = cursor.fetchone()[0]
    page = request.args.get('page', 1, type=int)
    per_page = 30  # Número de registros por página
    offset = (page - 1) * per_page
    limit = per_page
    cursor.execute('SELECT id, nombre, imagen FROM series LIMIT %s OFFSET %s', (limit, offset))
    movies = cursor.fetchall()

    total_pages = (total_records + per_page - 1) // per_page

    # Calcular las páginas a mostrar
    start_page = max(1, page - 2)
    end_page = min(total_pages, page + 2)

    if start_page > 3:
        start_page = max(1, start_page - 1)
    if end_page < total_pages - 2:
        end_page = min(total_pages, end_page + 1)

    pages_to_show = list(range(start_page, end_page + 1))

    cursor.close()
    conn.close()

    return page, movies, total_pages, pages_to_show





def buscador_titulo(titulo):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """SELECT id,nombre,imagen FROM series WHERE REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
    LOWER(nombre), 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o'), 'ú', 'u') LIKE LOWER(%s)"""
    cursor.execute(query, ('%' + titulo + '%',))
    movies = cursor.fetchall()
    cursor.close()
    conn.close()
    return movies


def get_temporadas(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """SELECT s.id,s.nombre,s.imagen,s.descripcion,s.anio, s.genero,t.numero_temporada,t.id FROM series s
    LEFT JOIN temporadas t ON t.serie_id = s.id
    WHERE s.id = %s"""
    cursor.execute(query, (id,))
    temporadas = cursor.fetchall()
    conn.close()
    return temporadas



def get_capitulos_por_temporada(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT s.nombre,s.imagen,s.descripcion,s.anio, s.genero, t.Numero_temporada, c.numero_capitulo, c.enlace, t.id,c.id
    FROM series s
    LEFT JOIN temporadas t ON t.serie_id = s.id
    JOIN capitulos c ON t.id = c.temporada_id
    WHERE t.id = %s 
    ORDER BY t.numero_temporada ASC, c.numero_capitulo ASC
    """
    cursor.execute(query, (id,))
    capitulos = cursor.fetchall()
    conn.close()
    return capitulos

def get_capitulo(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """SELECT s.nombre,s.imagen,s.descripcion,s.anio,s.genero,t.numero_temporada,c.numero_capitulo,c.enlace FROM series s
    JOIN temporadas t ON s.id=t.serie_id
    JOIN capitulos c ON c.temporada_id=t.id
    WHERE c.id = %s
    """
    cursor.execute(query, (id,))
    capitulo = cursor.fetchone()
    conn.close()
    return capitulo


#def get_pelicula(id):
#    conn = get_db_connection()
#    cursor = conn.cursor()
#    query =(""" SELECT s.id,s.nombre,s.imagen,s.descripcion,s.anio, s.genero,t.numero_temporada, t.id FROM series s
#    LEFT JOIN temporadas t ON t.serie_id = s.id
#    WHERE s.id = %s""")
#    cursor.execute(query, (id,))
#    pelicula = cursor.fetchone()
#    cursor.close()
#    conn.close()
#    return pelicula


#def get_titulo(nombre):
#    conn = get_db_connection()
#    cursor = conn.cursor()
#    Titulo = f'%{nombre}%'
#    sql_query = """SELECT nomnbre,imagen FROM series
#    WHERE REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
#    LOWER(Titulo), 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o'), 'ú', 'u') LIKE LOWER(%s)
#    """
#    titulo = cursor.execute(sql_query, (Titulo,)).fetchall()
#    conn.close()
#    return titulo
#

#def get_anios():
#    conn = get_db_connection()
#    cursor = conn.cursor()
#    query = """SELECT DISTINCT anio
#    FROM series
#    ORDER BY anio"""
#    anios = cursor.execute(query).fetchall()
#    conn.close()
#    return anios


#def obtener_datos(pagina, por_pagina):
#    conn = get_db_connection()
#    cursor = conn.cursor()
#    query = """
#    SELECT * FROM series LIMIT %s OFFSET %s
#    """
#    offset = (pagina - 1) * por_pagina
#    datos = cursor.execute(query, (por_pagina, offset)).fetchall()
#    return datos
#

#def contar_datos():
#    conn = get_db_connection()
#    cursor = conn.cursor()
#    cursor.execute('SELECT COUNT(*) FROM series_retro')
#    total = cursor.fetchone()[0]
#    conn.close()
#    return total

#@app.route('/', methods=['GET'])
#def index():
#    pagina = int(request.args.get('pagina', 1))
#    por_pagina = 10
#    datos = obtener_datos(pagina, por_pagina)
#    total = contar_datos()
#    total_paginas = (total + por_pagina - 1) // por_pagina  # Cálculo del total de páginas
#    return render_template('index.html', anios=get_anios(), datos=datos, pagina=pagina, total_paginas=total_paginas)
    
@app.route('/')
def home():
    page, movies, total_pages, pages_to_show = get_peliculas()
    return render_template('index.html', peliculas=movies, page=page, total_pages=total_pages, pages_to_show=pages_to_show)



@app.route('/buscador', methods=['GET', 'POST'])
def buscador():
    search_term = request.form.get('search_term', '')
    movies = buscador_titulo(search_term)
    return render_template('buscador.html', peliculas=movies, search_term=search_term)

@app.route('/serie/<id>')
def serie(id):
    serie = get_temporadas(id)
    return render_template('serie.html', serie=serie)

@app.route('/serie/temporada/<id>')
def temporada(id):
    capitulos = get_capitulos_por_temporada(id)
    return render_template('temporada.html', capitulos=capitulos)

@app.route('/serie/temporada/capitulo/<id>')
def capitulo(id):
    capitulo = get_capitulo(id)
    return render_template('capitulo.html', capitulo=capitulo)

#@app.route('/buscar_serie', methods=['GET', 'POST'])
#def buscadorSerie():
#    if request.method == 'POST':
#        search = request.form['query']
#        resultadoBusqueda = get_titulo(search)
#        return render_template('busqueda.html', miData = resultadoBusqueda, search=search)



#@app.route('/busqueda_anio', methods=['GET', 'POST'])
#def busqueda_anio():
#    
#    if request.method == 'POST':
#        anio = request.form['año']
#        resultado = obtener_datos_anio(anio)
#    return render_template('anios.html', miData=resultado)


#@app.errorhandler(404)
#def not_found(error):
#    return redirect(url_for('index'))
#
#@app.route('/serie/<id>')
#def serie(id):
#    temporadas = get_temporadas(id)
#    return render_template('serie.html', serie = temporadas)
#
#
#@app.route('/serie/<int:id>')
#def temporada(id):
#    capitulos = get_capitulos_por_temporada(id)
#    return render_template('temporada.html', capitulos=capitulos)

#@app.route('/serie/<int:id>')
#def capitulo(id):
#    capitulo = get_capitulo(id)
#    return render_template('capitulo.html', capitulo=capitulo)









#@app.route('/serie/<TemporadaID>')
#def temporada(TemporadaID):
#   get_capitulos_por_temporada(TemporadaID)
#   return 'hola'
    
#@app.route('/serie/temporadaID')
#def temporada(TemporadaID):
#    mi_conexion = sqlite3.connect("src/database/series_retro.db")
#    cur = mi_conexion.cursor()
#    cur.execute("""SELECT Titulo,NumeroTemporada, NumeroCpitulo, EnlaceCapitulo, t.TemporadaID FROM Series s
#                    LEFT JOIN Temporadas t ON t.SerieID = s.SerieID
#                    JOIN Capitulos c ON t.TemporadaID=c.TemporadaID
#                    WHERE t.TemporadaID = ? 
#                    ORDER BY t.NumeroTemporada ASC, c.NumeroCpitulo ASC""", (TemporadaID,))
#    data = cur.fetchall()
#    print(data)
#   
#    return render_template('temporada.html', capitulos=data)
#try:
#    mi_conexion = sqlite3.connect("src/database/series_retro.db")
#    cur = mi_conexion.cursor()
#    cur.execute('SELECT * FROM Series')
#    data = cur.fetchall()
#    for dato in data:
#        print(dato)
#
#except Exception as e:
#    print(e)

#@app.route('/')
#def index():
#    mi_conexion = sqlite3.connect("src/database/series_retro.db")
#    cur = mi_conexion.cursor()
#    cur.execute('SELECT SerieID,Titulo,imagen FROM Series')
#    data = cur.fetchall()
#    return render_template('index.html', series=data)
#
#
#
#@app.route('/<titulo>')
#def serie(titulo):
#    mi_conexion = sqlite3.connect('src/database/series_retro.db')
#    cur = mi_conexion.cursor()
#    cur.execute("""SELECT "Titulo",imagen,Descripcion,Anio,Genero,NumeroTemporada,t.TemporadaID FROM Series s
#                    LEFT JOIN Temporadas t ON t.SerieID = s.SerieID
#                    WHERE Titulo = ?""", (titulo,))
#    data = cur.fetchall()
#    
#    return render_template('vista_serie.html', serie=data)
#
#
#
#@app.route('/serie/<TemporadaID>')
#def temporada(TemporadaID):
#    mi_conexion = sqlite3.connect("src/database/series_retro.db")
#    cur = mi_conexion.cursor()
#    cur.execute("""SELECT Titulo,NumeroTemporada, NumeroCpitulo, EnlaceCapitulo, t.TemporadaID FROM Series s
#                    LEFT JOIN Temporadas t ON t.SerieID = s.SerieID
#                    JOIN Capitulos c ON t.TemporadaID=c.TemporadaID
#                    WHERE t.TemporadaID = ?
#                    ORDER BY t.NumeroTemporada ASC, c.NumeroCpitulo ASC""", (TemporadaID,))
#    data = cur.fetchall()
#    return render_template('vista_capitulos.html', capitulos=data)
#
#@app.route('/capitulo/<id>')
#def capitulo(id):
#    mi_conexion = sqlite3.connect('src/database/series_retro.db')
#    cur = mi_conexion.cursor()
#    cur.execute("""SELECT NumeroCpitulo,EnlaceCapitulo from Temporadas t
#                    JOIN Capitulos c ON  t.TemporadaID=c.TemporadaID
#                    WHERE c.TemporadaID={0}""".format(id))
#    data = cur.fetchall()
#    return render_template('capitulo.html', capitulo=data)
#
#
if __name__ == '__main__':
    app.run(debug=True)