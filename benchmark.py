import importlib.util
import os
import platform
import random
import statistics
import sys
import time
from datetime import date, timedelta


def carregar_modulo(nome, caminho):
    pasta = os.path.dirname(os.path.abspath(__file__))
    caminho_completo = os.path.join(pasta, caminho)
    spec = importlib.util.spec_from_file_location(nome, caminho_completo)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


base = carregar_modulo('tde1', 'TDE.ERP.FARMACIA.py')
otim = carregar_modulo('tde2', 'TDE2.ERP.FARMACIA.py')

SEMENTE = 42
VOLUMES = [100, 1000, 10000]
CENARIOS = ['aleatorio', 'ordenado', 'inverso']
REPETICOES = 5


def gerar_massa(n, cenario):
    """Gera sempre os mesmos registros para cada volume e cenário."""
    rng = random.Random(SEMENTE)
    data_base = date(2026, 1, 1)
    registros = []

    for i in range(n):
        registros.append({
            'codigo': f'MED{i:06d}',
            'nome': f'Medicamento {i}',
            'fornecedor': 'FORN001',
            'lote': f'L{i:04d}',
            'validade': data_base + timedelta(days=i),
            'criticidade': (i % 3) + 1,
            'preco': 500 + (i % 2000),
            'minimo': 10,
            'estoque': i % 100
        })

    if cenario == 'inverso':
        registros.reverse()
    elif cenario == 'aleatorio':
        rng.shuffle(registros)

    return registros


def gerar_pedidos(registros):
    lista = []
    for r in registros:
        lista.append({
            'codigo': r['codigo'],
            'quantidade': 10,
            'prioridade': (-r['criticidade'], r['validade'])
        })
    return lista


def verificar_equivalencia():
    """Confere se a versão otimizada entrega os mesmos resultados da versão base."""
    dados = gerar_massa(200, 'aleatorio')

    lista_base = []
    arvore_otim = otim.criar_arvore()
    for d in dados:
        base.inserir_ordenado(lista_base, dict(d))
        otim.inserir_avl(arvore_otim, dict(d))

    assert lista_base == otim.em_ordem(arvore_otim), 'Listagem em ordem diferente!'

    for d in dados[:30]:
        idx = base.buscar(lista_base, d['codigo'])
        achado = otim.buscar(arvore_otim, d['codigo'])
        assert lista_base[idx] == achado, 'Busca por código diferente!'

    assert base.buscar(lista_base, 'INEXISTENTE') == -1
    assert otim.buscar(arvore_otim, 'INEXISTENTE') is None

    idx_nome = base.buscar_por_nome(lista_base, dados[10]['nome'])
    achado_nome = otim.buscar_por_nome(arvore_otim, dados[10]['nome'])
    assert lista_base[idx_nome] == achado_nome, 'Busca por nome diferente!'

    ord_base = base.ordenar(lista_base, 'validade')
    ord_otim = otim.ordenar(otim.em_ordem(arvore_otim), 'validade')
    assert ord_base == ord_otim, 'Ordenação por validade diferente!'

    peds = gerar_pedidos(dados)
    fila_base = []
    fila_otim = otim.criar_heap()
    for p in peds:
        fila_base.append(dict(p))
        otim.inserir_heap(fila_otim, dict(p))

    while fila_base:
        melhor = 0
        for i in range(1, len(fila_base)):
            if fila_base[i]['prioridade'] < fila_base[melhor]['prioridade']:
                melhor = i
        p_base = fila_base.pop(melhor)
        p_otim = otim.remover_heap(fila_otim)
        assert p_base == p_otim, 'Ordem da fila de prioridade diferente!'

    for d in dados[:50]:
        idx = base.buscar(lista_base, d['codigo'])
        lista_base.pop(idx)
        otim.remover_avl(arvore_otim, d['codigo'])

    assert lista_base == otim.em_ordem(arvore_otim), 'Resultado após remoção diferente!'
    print('Teste de equivalência (Base vs Otimizada): OK (resultados idênticos)\n')


def medir_tempo(funcao):
    tempos = []
    for _ in range(REPETICOES):
        inicio = time.perf_counter()
        funcao()
        fim = time.perf_counter()
        tempos.append((fim - inicio) * 1000)
    return statistics.mean(tempos), statistics.stdev(tempos)


def contar_base_insercao(dados):
    lista = []
    comps = 0
    for reg in dados:
        inicio = 0
        fim = len(lista)
        while inicio < fim:
            meio = (inicio + fim) // 2
            comps += 1
            if lista[meio]['codigo'] < reg['codigo']:
                inicio = meio + 1
            else:
                fim = meio
        lista.insert(inicio, reg)
    return comps


def contar_base_busca(lista, codigos):
    comps = 0
    for codigo in codigos:
        inicio = 0
        fim = len(lista) - 1
        while inicio <= fim:
            meio = (inicio + fim) // 2
            comps += 1
            if lista[meio]['codigo'] == codigo:
                break
            elif lista[meio]['codigo'] < codigo:
                inicio = meio + 1
            else:
                fim = meio - 1
    return comps


def contar_base_ordenacao(lista, campo):
    copia = lista[:]
    comps = 0
    for i in range(1, len(copia)):
        atual = copia[i]
        j = i - 1
        while j >= 0:
            comps += 1
            if copia[j][campo] > atual[campo]:
                copia[j + 1] = copia[j]
                j -= 1
            else:
                break
        copia[j + 1] = atual
    return comps


def contar_base_fila(peds):
    fila = []
    for p in peds:
        fila.append(dict(p))
    comps = 0
    while fila:
        melhor = 0
        for i in range(1, len(fila)):
            comps += 1
            if fila[i]['prioridade'] < fila[melhor]['prioridade']:
                melhor = i
        fila.pop(melhor)
    return comps


def exibir_linha(op, n, cen, mb, db, mo, do, cb, co):
    ganho = mb / mo if mo > 0 else 0
    variacao = ((mb - mo) / mb) * 100 if mb > 0 else 0
    print(
        f'{op:<22} | {n:>6} | {cen:<9} | '
        f'{mb:>8.2f} +/- {db:>5.2f} | {mo:>8.2f} +/- {do:>5.2f} | '
        f'{ganho:>6.2f}x | {variacao:>+6.1f}% | {cb:>10} vs {co:>8}'
    )


def executar_experimentos():
    print('=== AMBIENTE ===')
    print('SO:', platform.platform())
    print('Processador:', platform.processor())
    print('Python:', sys.version.split()[0])
    print(f'Repetições por medição: {REPETICOES} | Semente: {SEMENTE}\n')

    verificar_equivalencia()

    cabecalho = (
        f'{"Operação":<22} | {"N":>6} | {"Cenário":<9} | '
        f'{"Base (ms)":>18} | {"Otimizada (ms)":>18} | '
        f'{"Ganho":>7} | {"Var.%":>7} | {"Comparações (Base vs Otim)"}'
    )
    print(cabecalho)
    print('-' * len(cabecalho))

    for n in VOLUMES:
        for cen in CENARIOS:
            dados = gerar_massa(n, cen)
            codigos_ex = []
            codigos_inex = []
            for i in range(n):
                codigos_ex.append(dados[i]['codigo'])
                codigos_inex.append(f'NAOEXISTE{i:06d}')
            peds = gerar_pedidos(dados)

            # 1. Inserção
            def b_ins():
                l = []
                for d in dados:
                    base.inserir_ordenado(l, d)

            def o_ins():
                a = otim.criar_arvore()
                for d in dados:
                    otim.inserir_avl(a, d)

            mb, db = medir_tempo(b_ins)
            mo, do = medir_tempo(o_ins)
            a_cnt = otim.criar_arvore()
            for d in dados:
                otim.inserir_avl(a_cnt, d)
            exibir_linha('Inserção', n, cen, mb, db, mo, do,
                         contar_base_insercao(dados), a_cnt['comparacoes'])

            # Prepara estruturas cheias
            lista_cheia = []
            arvore_cheia = otim.criar_arvore()
            for d in dados:
                base.inserir_ordenado(lista_cheia, d)
                otim.inserir_avl(arvore_cheia, d)

            # 2. Busca (existente)
            def b_bus_ex():
                for c in codigos_ex:
                    base.buscar(lista_cheia, c)

            def o_bus_ex():
                for c in codigos_ex:
                    otim.buscar(arvore_cheia, c)

            mb, db = medir_tempo(b_bus_ex)
            mo, do = medir_tempo(o_bus_ex)
            arvore_cheia['comparacoes'] = 0
            for c in codigos_ex:
                otim.buscar(arvore_cheia, c)
            exibir_linha('Busca (existente)', n, cen, mb, db, mo, do,
                         contar_base_busca(lista_cheia, codigos_ex), arvore_cheia['comparacoes'])

            # 3. Busca (inexistente)
            def b_bus_in():
                for c in codigos_inex:
                    base.buscar(lista_cheia, c)

            def o_bus_in():
                for c in codigos_inex:
                    otim.buscar(arvore_cheia, c)

            mb, db = medir_tempo(b_bus_in)
            mo, do = medir_tempo(o_bus_in)
            arvore_cheia['comparacoes'] = 0
            for c in codigos_inex:
                otim.buscar(arvore_cheia, c)
            exibir_linha('Busca (inexistente)', n, cen, mb, db, mo, do,
                         contar_base_busca(lista_cheia, codigos_inex), arvore_cheia['comparacoes'])

            # 4. Ordenação (validade)
            def b_ord():
                base.ordenar(dados, 'validade')

            def o_ord():
                otim.ordenar(dados, 'validade')

            mb, db = medir_tempo(b_ord)
            mo, do = medir_tempo(o_ord)
            cnt_ms = [0]
            otim.ordenar(dados, 'validade', cnt_ms)
            exibir_linha('Ordenação (validade)', n, cen, mb, db, mo, do,
                         contar_base_ordenacao(dados, 'validade'), cnt_ms[0])

            # 5. Remoção
            tempos_rem_base = []
            for _ in range(REPETICOES):
                l = lista_cheia[:]
                ini = time.perf_counter()
                for c in codigos_ex:
                    i = base.buscar(l, c)
                    l.pop(i)
                tempos_rem_base.append((time.perf_counter() - ini) * 1000)

            tempos_rem_otim = []
            for _ in range(REPETICOES):
                a = otim.criar_arvore()
                for d in dados:
                    otim.inserir_avl(a, d)
                ini = time.perf_counter()
                for c in codigos_ex:
                    otim.remover_avl(a, c)
                tempos_rem_otim.append((time.perf_counter() - ini) * 1000)

            mb = statistics.mean(tempos_rem_base)
            db = statistics.stdev(tempos_rem_base)
            mo = statistics.mean(tempos_rem_otim)
            do = statistics.stdev(tempos_rem_otim)

            a_rem = otim.criar_arvore()
            for d in dados:
                otim.inserir_avl(a_rem, d)
            a_rem['comparacoes'] = 0
            for c in codigos_ex:
                otim.remover_avl(a_rem, c)
            exibir_linha('Remoção', n, cen, mb, db, mo, do,
                         contar_base_busca(lista_cheia, codigos_ex), a_rem['comparacoes'])

            # 6. Fila de prioridade (inserir + processar todos)
            def b_fila():
                fila = []
                for p in peds:
                    fila.append(dict(p))
                while fila:
                    melhor = 0
                    for i in range(1, len(fila)):
                        if fila[i]['prioridade'] < fila[melhor]['prioridade']:
                            melhor = i
                    fila.pop(melhor)

            def o_fila():
                fila = otim.criar_heap()
                for p in peds:
                    otim.inserir_heap(fila, p)
                for _ in range(len(peds)):
                    otim.remover_heap(fila)

            mb, db = medir_tempo(b_fila)
            mo, do = medir_tempo(o_fila)
            f_cnt = otim.criar_heap()
            for p in peds:
                otim.inserir_heap(f_cnt, p)
            for _ in range(len(peds)):
                otim.remover_heap(f_cnt)
            exibir_linha('Fila de prioridade', n, cen, mb, db, mo, do,
                         contar_base_fila(peds), f_cnt['comparacoes'])

        print('-' * len(cabecalho))


if __name__ == '__main__':
    executar_experimentos()
