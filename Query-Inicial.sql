-- SQLite
-- Criação da tabela "filmes"
CREATE TABLE filmes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    ano_lancamento INTEGER NOT NULL,
    genero TEXT NOT NULL,
    diretor TEXT NOT NULL,
    imdb_id TEXT NOT NULL
);

-- Criação da tabela "avaliacoes"
CREATE TABLE avaliacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_avaliador TEXT NOT NULL,
    nota INTEGER CHECK(nota >= 1 AND nota <= 10),
    comentario TEXT,
    filme_id INTEGER NOT NULL,
    FOREIGN KEY (filme_id) REFERENCES filmes (id) ON DELETE CASCADE
);