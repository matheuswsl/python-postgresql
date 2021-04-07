Controle_funcionario
*****

Introdução
==========

Este programa é um exemplo simples de integração entre python e 
postgresql através do módulo psycopg2.

Os campos disponíveis para preenchimento são:

- id --> Auto-incrementado
- Nome --> Text
- Cargo --> Text
- Salário --> Text 

Funcionalidades
===============

- Adicionar Cadastros
- Atualizar Cadastros
- Remover Cadastros
- Selecionar Cadastros

Observação
==========

É necessário a atualização das informações de conexão com o postgres.
Para isso, deve-se fazer as alterações necessárias na variável 
"info_conexao" dentro da função "main()".

