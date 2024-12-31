# Desafio técnico

## Execução

### Dependências

Para rodar a aplicação, crie um ambiente com os arquivos e instale os pacotes necessários que estão listados no arquivo requirements.txt

Você pode instalar as dependências executando:

##### Instalar dependências
	pip install -r requirements.txt

Isso instalará o Flask (para o framework web) e o Flask-SQLAlchemy (para integração com banco de dados SQLite)

### Configuração do banco de dados

- Crie o banco de dados filmes_avaliacoes.db usando um cliente SQLite. 

- Em seguida, execute o script Query-Inicial.sql no terminal ou em um cliente SQLite para criar as tabelas.
![teste_tecnico_1](https://github.com/user-attachments/assets/e48b21d5-5e0e-4aee-8baf-0f9dc3fc6bc4)

Isso irá configurar o banco de dados e as tabelas necessárias.

### Executando servidor

Após garantir que o banco de dados foi configurado, execute o comando abaixo para iniciar o servidor Flask:

##### Ininiciar aplicação
	python run.py

O servidor Flask será iniciado, e você poderá acessar a aplicação no seu navegador em http://127.0.0.1:5000 ou http://localhost:5000

Esse processo iniciará o servidor da aplicação e a partir daí você pode começar a interagir com os endpoints definidos.

Link para um vídeo contendo [endpoints iniciais](https://youtu.be/FxoiXFFHzlI)

## Comentários sobre o projeto

### Decisões Técnicas

- Banco de Dados: Utilizou-se SQLite para simplicidade e facilidade de configuração durante o desenvolvimento, para algo com escalabilidade em grandes produções não seria recomendado seu uso. 
A estrutura do banco foi composta por duas tabelas principais: filmes e avaliacoes, com um relacionamento de um-para-muitos entre filmes e avaliações.

- Para o frontend foi utilizado Bootstrap, AJAX e JS. Com estes componentes, pode ser usado suas ferramentas para criar um layout responsivo e estilizado, 
o uso de requisições assíncronas sem recarregar a página conectando frontend com o backend, facilitando a interação com a API e atualização dinâmica.

### Melhorias Futuras

- Migração para Banco Robusto: Considerar o uso de PostgreSQL ou MySQL para melhorar o desempenho e escalabilidade.
- Otimização de Consultas: Implementação de índices e otimização de queries à medida que o sistema cresce.
- Endireitar funcionalidades que estão faltando ajustes mais aprofundados
- Melhorar no frontend, deixando mais harmônico para o usuário




