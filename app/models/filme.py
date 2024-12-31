from app import db

class Filme(db.Model):
    __tablename__ = 'filmes'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255))
    ano_lancamento = db.Column(db.Integer)
    genero = db.Column(db.String(100))
    diretor = db.Column(db.String(255))
    imdb_id = db.Column(db.String(100))

    avaliacoes = db.relationship('Avaliacao', back_populates='filme', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "ano_lancamento": self.ano_lancamento,
            "genero": self.genero,
            "diretor": self.diretor,
            "imdb_id": self.imdb_id,
            "avaliacoes": [avaliacao.to_dict() for avaliacao in self.avaliacoes]
        }

class Avaliacao(db.Model):
    __tablename__ = 'avaliacoes'
    id = db.Column(db.Integer, primary_key=True)
    nome_avaliador = db.Column(db.String(100), nullable=False)
    nota = db.Column(db.Integer)
    comentario = db.Column(db.Text, nullable=True)
    filme_id = db.Column(db.Integer, db.ForeignKey('filmes.id'), nullable=False)

    filme = db.relationship('Filme', back_populates='avaliacoes')

    def to_dict(self):
        return {
            "id": self.id,
            "nome_avaliador": self.nome_avaliador,
            "nota": self.nota,
            "comentario": self.comentario,
            "filme_id": self.filme_id
        }
