#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Exemplo de interface entre python e postgres"""

import psycopg2 as ps

class Conexao:
    
    def __init__(self, info_conexao):
        self.conexao = ps.connect(**info_conexao)
        self.cursor = self.conexao.cursor()
        cria_tabela(self.cursor)
        self.conexao.commit()
        
    def __new__(cls, info_conexao):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Conexao, cls).__new__(cls)
        return cls.instance
        
    def fechar_conexao(self):
        self.cursor.close()
        self.conexao.close()
        
class ControlaDatabase:        
    
    def __init__ (self, opcao, conexao, nome_tabela):
        self.conexao = conexao
        self.cursor = self.conexao.cursor
        self.opcao = opcao
        self.cursor.execute('SELECT * FROM Funcionarios limit 0')
        self.nome_colunas = [col[0] for col in self.cursor.description]
        self.nome_tabela = nome_tabela
        del(self.nome_colunas[0])
        self.comando = CriaComando(self.nome_tabela, self.nome_colunas)
    
    def inserir_cadastro(self):
        comando = self.comando
        self.cursor.execute(comando.inserir())
        self.conexao.conexao.commit()
        print('Cadastro Adicionado!!!')
        self.conexao.fechar_conexao()
        main()
    
    def alterar_cadastro(self, metodo):
        opcao_atualiza = Imprime().opcoes_atualiza_cadastro()
        comando = self.comando
        if opcao_atualiza == 1:
            valor_campo = input('Digite o id: ')
            opcao_campo_where='id'
        else:
            valor_campo = input('Digite o nome: ')
            valor_campo = "'%s'"%(valor_campo)
            opcao_campo_where='nome'
            
        if metodo == 'remover':
            comando = comando.remover(valor_campo, opcao_campo_where)
        else:
            comando = comando.atualizar(valor_campo, opcao_campo_where)
        try:
            self.cursor.execute(comando)
        except (SyntaxError, ps.errors.UndefinedColumn):
            print('\nValor para identificação do campo não é válido!!!')
        else:
            print('\nCadastro Atualizado!!!')
        self.conexao.conexao.commit()
        self.conexao.fechar_conexao()
        main()  
        
    def selecionar_cadastro(self):
        nome_colunas = ['id'] 
        nome_colunas.extend(self.nome_colunas)
        opcao_selecionar = Imprime().opcoes_selecionar_cadastro(nome_colunas)
        comando = self.comando
        if opcao_selecionar == 0:
            valor = (nome_colunas[opcao_selecionar-1], "%s"%(
                 input('\nDigite o valor do campo: ')))
        else:
            valor = (nome_colunas[opcao_selecionar-1], "'%s'"%(
                 input('\nDigite o valor do campo: ')))
        comando = comando.selecionar_cadastro(valor)
        try:
            self.cursor.execute(comando)
        except (SyntaxError, ps.errors.InvalidTextRepresentation):
            print('Valor para a identificação do campo não é válido!!!')
        else:
            fetch = self.cursor.fetchall()
            Imprime().apresenta_selecionados(fetch)
        self.conexao.conexao.commit()
        self.conexao.fechar_conexao()
        main()
        
    def sair(self):
        print('Até mais!')
        

class CriaComando:
    
    def __init__(self, nome_tabela, nome_colunas):
        self.nome_tabela = nome_tabela
        self.nome_colunas = nome_colunas
    
    def recupera_valores(self):
        valores = {}
        print('\nDigite os valores para cada coluna:')
        for titulo in self.nome_colunas:
            valores[titulo] = "'%s'"%(input(titulo.title() + ': '))
        return valores
        
    def inserir(self):
        valores = self.recupera_valores()
        comando = "INSERT INTO %s (" %(self.nome_tabela)
        for i in range(len(valores)-1):
            comando = comando + "%s, "
        comando = comando + "%s) VALUES ("
        comando = comando % tuple(valores.keys())
        for i in range(len(valores)-1):
            comando = comando + "%s, "
        comando = comando + '%s);'
        comando = comando %tuple(valores.values())
        return comando
    
    def atualizar(self, valor_campo, opcao_campo_where = ''):
        valores = self.recupera_valores()
        valores = [x+' = '+"%s"%(y) for x, y in valores.items()]
        valores = ', '.join(valores)
        comando = "UPDATE %s SET %s WHERE %s = %s;" %(self.nome_tabela,
                                                  valores,
                                                  opcao_campo_where,
                                                  valor_campo)
        return comando
    
    def remover(self, valor_campo, opcao_campo_where):
        comando = "DELETE FROM %s WHERE %s = %s;"%(self.nome_tabela,
                                                   opcao_campo_where,
                                                   valor_campo)
        return comando
    
    def selecionar_cadastro(self, valor):
        comando = "SELECT * FROM %s WHERE %s = %s;"%(self.nome_tabela,
                                                     valor[0],
                                                     valor[1])
        return comando
    
class Imprime:
        
    def inicio(self):
        opcao = input("""Escolha uma das opções abaixo:
                             (1) Inserir Cadastro
                             (2) Atualizar Cadastro
                             (3) Remover Cadastro
                             (4) Selecionar Cadastro
                             (5) Sair\nOpção: """)
        opcao = self.valida_opcao(opcao, 5)
        while not opcao:
            opcao = input("""Escolha uma das opções abaixo:
                             (1) Inserir Cadastro
                             (2) Atualizar Cadastro
                             (3) Remover Cadastro
                             (4) Selecionar Cadastro
                             (5) Sair\nOpção: """)
            opcao = self.valida_opcao(opcao, 5)
        return opcao
    
    def valida_opcao(self, opcao, num_opcoes):
        opcoes = [str(x) for x in range(1,num_opcoes+1)]
        if opcao not in opcoes:
            print('\nA opção escolhida não é válida!!!\n')
            return False
        else:
            return int(opcao)
    
    def opcoes_atualiza_cadastro(self):
        opcao_atualiza = input("""Como deseja identificar o cadastro?
                             (1) id
                             (2) Nome\n\nOpção: """)
        opcao_atualiza = self.valida_opcao(opcao_atualiza, 2)
        while type(opcao_atualiza) != type(1):
            opcao_atualiza = input("""Como deseja identificar o cadastro?
                             (1) id
                             (2) Nome\n\nOpção: """)
            opcao_atualiza = self.valida_opcao(opcao_atualiza, 2)
        return opcao_atualiza
    
    def opcoes_selecionar_cadastro(self, nome_colunas):
        print('Escolha o campo que será usado para pesquisa:\n')
        for n, campo in enumerate(nome_colunas, start=1):
            print('(%s) %s'%(n, campo.title()))
        opcao_selecionar = input('\nOpção: ')
        opcao_selecionar = self.valida_opcao(opcao_selecionar, len(nome_colunas))
        while not opcao_selecionar:
            for n, campo in enumerate(nome_colunas):
                print('(%s) %s'%(n, campo.title()))
                opcao_selecionar = input('\nOpção: ')
                opcao_selecionar = self.valida_opcao(opcao_selecionar, 
                                                     len(nome_colunas))
        return opcao_selecionar
        
    def apresenta_selecionados(self, fetch):
        print('\n|%s|%s|%s|%s|'%('id'.center(10), 'Nome'.center(25),
                               'Cargo'.center(15),'Salario'.center(10)))
        print('+'+'-'*10+'+'+'-'*25+'+'+'-'*15+'+'+'-'*10+'+')
        for linha in fetch:
            print('|%s|%s|%s|%s|'%(str(linha[0]).center(10), linha[1].center(25),
                                   linha[2].center(15), linha[3].center(10)))
        print('+'+'-'*10+'+'+'-'*25+'+'+'-'*15+'+'+'-'*10+'+')
    
class AvaliaOpcoes:
    
    def __init__(self, conexao, nome_tabela):
        self.conexao = conexao
        self.nome_tabela = nome_tabela
    
    def __call__(self):
        opcao = Imprime().inicio()
        controla_database = ControlaDatabase(opcao, self.conexao, self.nome_tabela)
        if opcao == 1:
            controla_database.inserir_cadastro()
        elif opcao == 2:
            controla_database.alterar_cadastro('atualizar')
        elif opcao == 3:
            controla_database.alterar_cadastro('remover')
        elif opcao == 4:
            controla_database.selecionar_cadastro()
        elif opcao == 5:
            controla_database.sair()
        
def cria_tabela(cursor):
     cursor.execute("""CREATE TABLE IF NOT EXISTS Funcionarios(
                          id SERIAL,
                          nome TEXT NOT NULL,
                          cargo TEXT NOT NULL,
                          salario TEXT NOT NULL);""")
    
def main():
  
    info_conexao = {'database':'postgres', 'user':'postgres', 
                   'password':'', 'host':'127.0.0.1', 'port':'5432'}
    conexao = Conexao(info_conexao)
    avalia_opcoes = AvaliaOpcoes(conexao, 'Funcionarios')
    avalia_opcoes()
    
if '__name__' == '__main__':
    main()
    