#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 10:04:43 2021

@author: matheus
"""
from controle_funcionario import Conexao, cria_tabela, Imprime
import pytest

info_conexao = {'database':'postgres', 'user':'postgres', 'password':'Mat-021090', 'host':'127.0.0.1', 'port':'5432'} 
conexao1 = Conexao(info_conexao)
conexao2 = Conexao(info_conexao)

class TestConexao:
    
    def test_duplicidade(self):
        assert conexao1 == conexao2

    def test_fecha_conexao(self):
        conexao1.fechar_conexao()
        conexao2.fechar_conexao()
        assert conexao1.conexao.closed == conexao2.conexao.closed == 1

class TestImprime:

    def test_valida_opcao(self):
        valores_verdadeiros = [str(x) for x in range(1,6)]
        retorno_verdadeiro = []
        retorno_falso = []
        for i in valores_verdadeiros:
            retorno_verdadeiro.append(Imprime().valida_opcao(i,5))
        valores_falsos = ['a','7','#',',','','*']
        for i in valores_falsos:
            retorno_falso.append(Imprime().valida_opcao(i,5))
        assert (retorno_verdadeiro == [x for x in range(1,6)] and
               retorno_falso.count(False) == 6)

class TestControlaDatabase:

    def test_inserir(self):
        conexao = Conexao(info_conexao)
        cursor = conexao.cursor
        cursor.execute("INSERT INTO Funcionarios (nome, cargo, salario) VALUES ('Lucas','Estudante','2200,00');")
        mensagem = cursor.statusmessage
        conexao.conexao.commit()
        conexao.fechar_conexao()
        assert mensagem == 'INSERT 0 1'

class TestCriaTabela:

    def test_cria_tabela(self):
        conexao = Conexao(info_conexao)
        cria_tabela(conexao.cursor)
        mensagem = conexao.cursor.statusmessage
        conexao.fechar_conexao()
        assert mensagem == 'CREATE TABLE'


