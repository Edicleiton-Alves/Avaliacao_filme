import requests
from app import db
from flask import current_app as app
from app.models.filme import Filme, Avaliacao
from flask import Blueprint, request, jsonify, render_template

filmes_controller = Blueprint('filmes_controller', __name__)

@filmes_controller.route('/filmes/<int:id>', methods=['PUT'])
def atualizar_filme_com_post(id):
    filme = Filme.query.get(id)
    
    if not filme:
        return jsonify({"message": "Filme não encontrado!"}), 404
    
    dados_atualizados = request.get_json()
    if not dados_atualizados:
        return jsonify({"message": "Nenhum dado foi enviado para atualização!"}), 400
    
    try:
        if 'title' in dados_atualizados:
            filme.titulo = dados_atualizados['title'].strip() or filme.titulo
        if 'year' in dados_atualizados:
            filme.ano_lancamento = int(dados_atualizados['year'])
        if 'genre' in dados_atualizados:
            filme.genero = dados_atualizados['genre'].strip() or filme.genero
        if 'director' in dados_atualizados:
            filme.diretor = dados_atualizados['director'].strip() or filme.diretor
        if 'avaliacoes' in dados_atualizados:
            for avaliacao_dados in dados_atualizados['avaliacoes']:
                avaliacao = Avaliacao(
                    nome_avaliador=avaliacao_dados['nome_avaliador'],
                    nota=int(avaliacao_dados['nota']),
                    comentario=avaliacao_dados.get('comentario', ''),
                    filme_id=filme.id
                )
                db.session.add(avaliacao)
        
        db.session.commit()
        return jsonify({"message": "Filme atualizado com sucesso!", "filme": filme.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao atualizar o filme!", "error": str(e)}), 500

@filmes_controller.route('/filmes/<int:id>/avaliacoes', methods=['POST'])
def adicionar_avaliacao(id):
    filme = Filme.query.get(id)
    
    if not filme:
        return jsonify({"message": "Filme não encontrado!"}), 404
    
    dados_avaliacao = request.get_json()
    if not dados_avaliacao:
        return jsonify({"message": "Nenhuma avaliação foi enviada!"}), 400
    
    try:
        avaliacao = Avaliacao(
            nome_avaliador=dados_avaliacao['nome_avaliador'],
            nota=int(dados_avaliacao['nota']),
            comentario=dados_avaliacao.get('comentario', ''),
            filme_id=filme.id
        )
        db.session.add(avaliacao)
        db.session.commit()
        return jsonify({"message": "Avaliação adicionada com sucesso!", "avaliacao": avaliacao.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao adicionar a avaliação!", "error": str(e)}), 500

@filmes_controller.route('/adicionar_filmes_api', methods=['POST'])
def adicionar_filmes_api():
    api_key = app.config['API_KEY']
    filmes_ids = set()
    filmes_adicionados = []

    while len(filmes_ids) < 2:
        response = requests.get(f"http://www.omdbapi.com/?apikey={api_key}&s=movie&type=movie")
        if response.status_code != 200:
            return jsonify({"message": "Erro ao acessar a API de filmes!"}), 500

        filmes_info = response.json()
        if filmes_info.get("Response") == "False":
            return jsonify({"message": "Não foi possível encontrar filmes!"}), 404

        for filme_info in filmes_info.get('Search', []):
            imdb_id = filme_info['imdbID']
            if not Filme.query.filter_by(imdb_id=imdb_id).first():
                filmes_ids.add(imdb_id)

            if len(filmes_ids) >= 2:
                break

    for imdb_id in filmes_ids:
        response = requests.get(f"http://www.omdbapi.com/?apikey={api_key}&i={imdb_id}")
        if response.status_code != 200:
            return jsonify({"message": f"Erro ao acessar os detalhes do filme {imdb_id}!"}), 500

        filme_info = response.json()
        if filme_info.get("Response") == "False":
            continue

        # Adicionando filme
        filme = Filme(
            titulo=filme_info.get('Title', 'Desconhecido'),
            ano_lancamento=int(filme_info.get('Year', 0)),
            genero=filme_info.get('Genre', 'Desconhecido'),
            diretor=filme_info.get('Director', 'Desconhecido'),
            imdb_id=filme_info.get('imdbID')
        )
        db.session.add(filme)
        db.session.flush()  # Garante que o ID do filme está disponível antes de adicionar avaliações

        # Adicionando avaliações
        avaliacoes = filme_info.get('Ratings', [])
        for avaliacao_info in avaliacoes:
            nome_avaliador = avaliacao_info.get('Source', 'Desconhecido').strip()
            if not nome_avaliador or nome_avaliador.lower() == 'desconhecido':
                continue  # Ignorar avaliadores inválidos ou desconhecidos

            nota_raw = avaliacao_info.get('Value', '0')
            try:
                nota = float(nota_raw.split('/')[0])
            except ValueError:
                nota = 0

            if 1 <= nota <= 10:
                avaliacao = Avaliacao(
                    nome_avaliador=nome_avaliador,
                    nota=nota,
                    comentario='',
                    filme_id=filme.id
                )
                db.session.add(avaliacao)

        filmes_adicionados.append(filme.id)

    db.session.commit()
    return jsonify({"message": "Dois filmes adicionados com sucesso!", "filmes_adicionados": filmes_adicionados}), 201

@filmes_controller.route('/api/filmes', methods=['GET'])
def get_filmes():
    filmes = Filme.query.all()
    return jsonify({
        "total_filmes": len(filmes),
        "filmes": [filme.to_dict() for filme in filmes]
    })

@filmes_controller.route('/filmes/<int:id>', methods=['DELETE'])
def excluir_filme(id):
    filme = Filme.query.get(id)
    if not filme:
        return jsonify({"message": "Filme não encontrado!"}), 404

    db.session.delete(filme)
    db.session.commit()
    return jsonify({"message": "Filme excluído com sucesso!"}), 200

@filmes_controller.route('/filmes/<int:id>/avaliacoes', methods=['GET'])
def obter_avaliacoes(id):
    filme = Filme.query.get(id)
    
    if not filme:
        return jsonify({"message": "Filme não encontrado!"}), 404
    
    avaliacoes = Avaliacao.query.filter_by(filme_id=id).all()
    if not avaliacoes:
        return jsonify({"message": "Nenhuma avaliação encontrada para este filme."}), 404
    
    return jsonify({
        "filme": filme.titulo,
        "total_avaliacoes": len(avaliacoes),
        "avaliacoes": [avaliacao.to_dict() for avaliacao in avaliacoes]
    }), 200

@filmes_controller.route('/')
def index():
    filmes = Filme.query.all()
    return render_template('index.html', filmes=filmes)