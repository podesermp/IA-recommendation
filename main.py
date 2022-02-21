from math import sqrt
from data_base import *


def distEuclidiana(base,user1, user2):
    si = {}
    for item in base[user1]:
        if item in base[user2]:
            si[item] = 1
    if len(si) == 0:
        return 0
    
    soma = sum([pow(base[user1][item] - base[user2][item], 2)
                for item in base[user1] if item in base[user2]])
    return 1/(1+sqrt(soma))

def getSimilaridade(base, user):
    similaridade = [(distEuclidiana(base, user, outro), outro)
                    for outro in base if outro != user]
    similaridade.sort()
    similaridade.reverse()
    return similaridade[:30]

def getRecomendacoesUsuario(base,user):
    totais = {}
    somaSimilaridade = {}
    for outro in base:
        if outro == user:
            continue
        similaridade = distEuclidiana(base, user, outro)
        if similaridade <= 0:
            continue

        for item in base[outro]:
            if item not in base[user]:
                totais.setdefault(item, 0)
                totais[item] += base[outro][item] * similaridade
                somaSimilaridade.setdefault(item, 0)
                somaSimilaridade[item] += similaridade
    rankings = [(total / somaSimilaridade[item], item) for item,total in totais.items()]
    rankings.sort()
    rankings.reverse()
    return rankings[:30]

def carregaMovieLens(path='./data/ml-100k'):
    filmes = {}
    for linha in open(path + '/u.item'):
        (id, titulo) = linha.split('|')[0:2]
        filmes[id] = titulo
    base = {}
    for linha in open(path + '/u.data'):
        (usuario, idFilme, nota, tempo) = linha.split('\t')
        base.setdefault(usuario, {})
        base[usuario][filmes[idFilme]] = float(nota)
    return base

def calculaItensSimilares(base):
    result = {}
    for item in base:
        notas = getSimilaridade(base, item)
        result[item] = notas
    return result

def getRecomendacoesItens(baseUser, similaridadeItens, user):
    notasUsuario = baseUser[user]
    notas = {}
    totalSimilaridade = {}
    for (item, nota) in notasUsuario.items():
        for (similaridade, item2) in similaridadeItens[item]:
            if item2 in notasUsuario: continue
            notas.setdefault(item2, 0)
            notas[item2] += similaridade * nota
            totalSimilaridade.setdefault(item2,0)
            totalSimilaridade[item2] += similaridade
    rankings=[(score/totalSimilaridade[item], item) for item, score in notas.items()]
    rankings.sort()
    rankings.reverse()
    return rankings


# base = carregaMovieLens()
# print(getRecomendacoes(base, '212'))

# print(avaliacoesUsuario['Leonardo'])
# print(getSimilaridade(avaliacoesFilme, 'O Ultimato Bourne'))
# itensSimilares = calculaItensSimilares(avaliacoesFilme)
# print(itensSimilares['Norbit'])
print(getRecomendacoesUsuario(avaliacoesUsuario, 'Leonardo'))
listaItens = calculaItensSimilares(avaliacoesFilme)
print(getRecomendacoesItens(avaliacoesUsuario, listaItens, 'Leonardo'))