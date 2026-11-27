# Declaração de autoria
# Autores: Cleiton Souza Santos, Davi Figueiredo Lima, Murilo Braz da Costa
# Declaro que este código foi desenvolvido por nós, com base no nosso próprio
# entendimento e esforço. Não houve plágio ou cópia integral de terceiros.
# Ferramentas de IA, quando utilizadas, foram apenas como apoio ao aprendizado
# e não para a geração integral deste código.

from datetime import date


# --- ÁRVORE AVL MANUAL (substitui as listas de cadastro) ---

def criar_arvore():
    return {'raiz': None, 'comparacoes': 0}


def altura_no(no):
    if no is None:
        return 0
    return no['altura']


def atualizar_altura(no):
    esq = altura_no(no['esq'])
    dir = altura_no(no['dir'])
    if esq > dir:
        no['altura'] = esq + 1
    else:
        no['altura'] = dir + 1


def fator_balanceamento(no):
    if no is None:
        return 0
    return altura_no(no['esq']) - altura_no(no['dir'])


def rotacao_direita(y):
    x = y['esq']
    t2 = x['dir']
    x['dir'] = y
    y['esq'] = t2
    atualizar_altura(y)
    atualizar_altura(x)
    return x


def rotacao_esquerda(x):
    y = x['dir']
    t2 = y['esq']
    y['esq'] = x
    x['dir'] = t2
    atualizar_altura(x)
    atualizar_altura(y)
    return y


def balancear(no):
    atualizar_altura(no)
    fb = fator_balanceamento(no)

    if fb > 1:
        if fator_balanceamento(no['esq']) < 0:
            no['esq'] = rotacao_esquerda(no['esq'])
        return rotacao_direita(no)

    if fb < -1:
        if fator_balanceamento(no['dir']) > 0:
            no['dir'] = rotacao_direita(no['dir'])
        return rotacao_esquerda(no)

    return no


def buscar(arvore, codigo):
    """Busca manual diretamente na árvore AVL pelo código."""
    atual = arvore['raiz']
    while atual is not None:
        arvore['comparacoes'] += 1
        codigo_atual = atual['dado']['codigo']
        if codigo == codigo_atual:
            return atual['dado']
        elif codigo < codigo_atual:
            atual = atual['esq']
        else:
            atual = atual['dir']
    return None


def buscar_por_nome_no(no, nome, arvore):
    if no is None:
        return None
    achado = buscar_por_nome_no(no['esq'], nome, arvore)
    if achado is not None:
        return achado
    arvore['comparacoes'] += 1
    if no['dado']['nome'].lower() == nome:
        return no['dado']
    return buscar_por_nome_no(no['dir'], nome, arvore)


def buscar_por_nome(arvore, nome):
    """Busca manual direta na árvore pelo nome do medicamento."""
    nome = nome.strip().lower()
    return buscar_por_nome_no(arvore['raiz'], nome, arvore)


def inserir_no(no, registro, arvore):
    if no is None:
        return {'dado': registro, 'esq': None, 'dir': None, 'altura': 1}
    arvore['comparacoes'] += 1
    if registro['codigo'] < no['dado']['codigo']:
        no['esq'] = inserir_no(no['esq'], registro, arvore)
    elif registro['codigo'] > no['dado']['codigo']:
        no['dir'] = inserir_no(no['dir'], registro, arvore)
    else:
        raise ValueError('Código já cadastrado.')
    return balancear(no)


def inserir_avl(arvore, registro):
    arvore['raiz'] = inserir_no(arvore['raiz'], registro, arvore)


def atualizar_avl(arvore, codigo, novo):
    atual = arvore['raiz']
    while atual is not None:
        arvore['comparacoes'] += 1
        if codigo == atual['dado']['codigo']:
            atual['dado'] = novo
            return
        elif codigo < atual['dado']['codigo']:
            atual = atual['esq']
        else:
            atual = atual['dir']


def menor_no(no):
    atual = no
    while atual['esq'] is not None:
        atual = atual['esq']
    return atual


def remover_no(no, codigo, arvore):
    if no is None:
        return None
    arvore['comparacoes'] += 1
    if codigo < no['dado']['codigo']:
        no['esq'] = remover_no(no['esq'], codigo, arvore)
    elif codigo > no['dado']['codigo']:
        no['dir'] = remover_no(no['dir'], codigo, arvore)
    else:
        if no['esq'] is None:
            return no['dir']
        if no['dir'] is None:
            return no['esq']
        sucessor = menor_no(no['dir'])
        no['dado'] = sucessor['dado']
        no['dir'] = remover_no(no['dir'], sucessor['dado']['codigo'], arvore)
    return balancear(no)


def remover_avl(arvore, codigo):
    arvore['raiz'] = remover_no(arvore['raiz'], codigo, arvore)


# --- TRAVESSIAS DA ÁRVORE ---

def em_ordem_no(no, resultado):
    if no is not None:
        em_ordem_no(no['esq'], resultado)
        resultado.append(no['dado'])
        em_ordem_no(no['dir'], resultado)


def em_ordem(arvore):
    resultado = []
    em_ordem_no(arvore['raiz'], resultado)
    return resultado


def pre_ordem_no(no, resultado):
    if no is not None:
        resultado.append(no['dado'])
        pre_ordem_no(no['esq'], resultado)
        pre_ordem_no(no['dir'], resultado)


def pre_ordem(arvore):
    resultado = []
    pre_ordem_no(arvore['raiz'], resultado)
    return resultado


def pos_ordem_no(no, resultado):
    if no is not None:
        pos_ordem_no(no['esq'], resultado)
        pos_ordem_no(no['dir'], resultado)
        resultado.append(no['dado'])


def pos_ordem(arvore):
    resultado = []
    pos_ordem_no(arvore['raiz'], resultado)
    return resultado


# --- ORDENAÇÃO POR DIVISÃO E CONQUISTA (MERGE SORT MANUAL) ---

def intercalar(esquerda, direita, campo, contador=None):
    resultado = []
    i = 0
    j = 0
    while i < len(esquerda) and j < len(direita):
        if contador is not None:
            contador[0] += 1
        if esquerda[i][campo] <= direita[j][campo]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1
    while i < len(esquerda):
        resultado.append(esquerda[i])
        i += 1
    while j < len(direita):
        resultado.append(direita[j])
        j += 1
    return resultado


def ordenar(lista, campo, contador=None):
    """Merge Sort manual: ordena uma cópia pelo campo informado."""
    if len(lista) <= 1:
        return lista[:]
    meio = len(lista) // 2
    esquerda = ordenar(lista[:meio], campo, contador)
    direita = ordenar(lista[meio:], campo, contador)
    return intercalar(esquerda, direita, campo, contador)


# --- OTIMIZAÇÃO ADICIONAL: MIN-HEAP MANUAL PARA FILA DE PEDIDOS ---

def criar_heap():
    return {'itens': [], 'sequencia': 0, 'comparacoes': 0}


def subir_heap(heap, i):
    itens = heap['itens']
    while i > 0:
        pai = (i - 1) // 2
        heap['comparacoes'] += 1
        if itens[i]['chave'] < itens[pai]['chave']:
            temp = itens[i]
            itens[i] = itens[pai]
            itens[pai] = temp
            i = pai
        else:
            break


def descer_heap(heap, i):
    itens = heap['itens']
    tamanho = len(itens)
    while True:
        esq = 2 * i + 1
        dir = 2 * i + 2
        menor = i
        if esq < tamanho:
            heap['comparacoes'] += 1
            if itens[esq]['chave'] < itens[menor]['chave']:
                menor = esq
        if dir < tamanho:
            heap['comparacoes'] += 1
            if itens[dir]['chave'] < itens[menor]['chave']:
                menor = dir
        if menor != i:
            temp = itens[i]
            itens[i] = itens[menor]
            itens[menor] = temp
            i = menor
        else:
            break


def inserir_heap(heap, pedido):
    # A sequência mantém o pedido mais antigo na frente quando empata.
    item = {
        'chave': (pedido['prioridade'], heap['sequencia']),
        'pedido': pedido
    }
    heap['sequencia'] += 1
    heap['itens'].append(item)
    subir_heap(heap, len(heap['itens']) - 1)


def remover_heap(heap):
    itens = heap['itens']
    if not itens:
        raise ValueError('Fila vazia.')
    topo = itens[0]['pedido']
    ultimo = itens.pop()
    if itens:
        itens[0] = ultimo
        descer_heap(heap, 0)
    return topo


def listar_pedidos(heap):
    ordenados = ordenar(heap['itens'], 'chave')
    resultado = []
    for i in range(len(ordenados)):
        resultado.append(ordenados[i]['pedido'])
    return resultado


# ÁRVORES AVL de cadastro; PILHA de movimentos; MIN-HEAP de pedidos.
fornecedores = criar_arvore()
medicamentos = criar_arvore()
historico = []
pedidos = criar_heap()


def ler_texto(pergunta):
    valor = input(pergunta).strip()
    if not valor:
        raise ValueError('Campo obrigatório não preenchido.')
    return valor


def ler_numero(pergunta, minimo):
    valor = int(input(pergunta))
    if valor < minimo:
        raise ValueError(f'O valor mínimo é {minimo}.')
    return valor


def selecionar(arvore):
    codigo = ler_texto('Código: ')
    registro = buscar(arvore, codigo)
    if registro is None:
        raise ValueError('Código não encontrado.')
    return registro


def mostrar(lista):
    if not lista:
        print('Nenhum registro.')
    for registro in lista:
        print(registro)


def tem_pedido(codigo):
    for item in pedidos['itens']:
        if item['pedido']['codigo'] == codigo:
            return True
    return False


def tem_historico(codigo):
    for movimento in historico:
        if movimento['medicamento']['codigo'] == codigo:
            return True
    return False


def ler_cadastro(tipo, codigo):
    """Lê e valida tudo antes de inserir ou substituir o registro."""
    registro = {'codigo': codigo, 'nome': ler_texto('Nome: ')}
    if tipo == 'fornecedor':
        registro['contato'] = ler_texto('Contato: ')
        return registro
    registro['fornecedor'] = ler_texto('Código do fornecedor: ')
    if buscar(fornecedores, registro['fornecedor']) is None:
        raise ValueError('Cadastre o fornecedor primeiro.')
    registro['lote'] = ler_texto('Lote: ')
    registro['validade'] = date.fromisoformat(ler_texto('Validade (AAAA-MM-DD): '))
    registro['criticidade'] = ler_numero('Criticidade (1 baixa, 2 média, 3 alta): ', 1)
    if registro['criticidade'] > 3:
        raise ValueError('Criticidade deve ser de 1 a 3.')
    registro['preco'] = ler_numero('Preço em centavos (1250 = R$ 12,50): ', 1)
    registro['minimo'] = ler_numero('Estoque mínimo: ', 0)
    registro['estoque'] = 0
    return registro


def cadastros(tipo, arvore):
    """Mesmo menu CRUD para fornecedores e medicamentos."""
    acao = input('1 Cadastrar | 2 Consultar | 3 Alterar | 4 Remover | 5 Listar: ')
    if acao == '1':
        codigo = ler_texto('Novo código: ')
        if buscar(arvore, codigo) is not None:
            raise ValueError('Código já cadastrado.')
        inserir_avl(arvore, ler_cadastro(tipo, codigo))
    elif acao == '5':
        mostrar(em_ordem(arvore))
    elif acao == '2' or acao == '3' or acao == '4':
        if acao == '2' and tipo == 'medicamento':
            metodo = input('1 - Buscar por código | 2 - Buscar por nome: ').strip()

            if metodo == '1':
                registro = selecionar(arvore)
            elif metodo == '2':
                nome = ler_texto('Nome do medicamento: ')
                registro = buscar_por_nome(arvore, nome)
                if registro is None:
                    raise ValueError('Medicamento não encontrado pelo nome.')
            else:
                raise ValueError('Opção de busca inválida.')

            print(registro)
            return

        registro = selecionar(arvore)
        if acao == '2':
            print(registro)
            return
        if tipo == 'medicamento':
            # Protege as referências da pilha e os dados de prioridade.
            if tem_pedido(registro['codigo']) or tem_historico(registro['codigo']):
                raise ValueError('Há pedido ou histórico ligado ao medicamento.')
            if registro['estoque'] != 0:
                raise ValueError('Alteração ou remoção exige estoque zero.')
        if acao == '3':
            novo = ler_cadastro(tipo, registro['codigo'])
            atualizar_avl(arvore, registro['codigo'], novo)
        else:
            if tipo == 'fornecedor':
                lista_meds = em_ordem(medicamentos)
                for m in lista_meds:
                    if m['fornecedor'] == registro['codigo']:
                        raise ValueError('Fornecedor ligado a medicamento.')
            remover_avl(arvore, registro['codigo'])
    else:
        raise ValueError('Opção inválida.')


def movimentar():
    m = selecionar(medicamentos)
    quantidade = int(input('Quantidade (+ entrada / - saída): '))
    motivo = ler_texto('Motivo: ')
    if quantidade == 0 or m['estoque'] + quantidade < 0:
        raise ValueError('Quantidade zero ou estoque insuficiente.')
    if quantidade < 0 and m['validade'] < date.today():
        if motivo.strip().lower() != 'descarte':
            raise ValueError('Lote vencido só pode sair por descarte.')
    m['estoque'] += quantidade
    # PILHA: insere apenas no topo (fim da lista).
    historico.append({'medicamento': m, 'quantidade': quantidade, 'motivo': motivo})


def desfazer():
    if not historico:
        raise ValueError('Histórico vazio.')
    # PILHA: remove apenas o topo; LIFO = último a entrar, primeiro a sair.
    movimento = historico.pop()
    movimento['medicamento']['estoque'] -= movimento['quantidade']
    print('Última movimentação desfeita.')


def solicitar():
    m = selecionar(medicamentos)
    if tem_pedido(m['codigo']):
        raise ValueError('Já existe pedido para esse medicamento.')
    quantidade = ler_numero('Quantidade para comprar: ', 1)
    # Menor chave vence: criticidade alta, depois validade mais próxima.
    inserir_heap(pedidos, {'codigo': m['codigo'], 'quantidade': quantidade,
                           'prioridade': (-m['criticidade'], m['validade'])})


def processar():
    pedido = remover_heap(pedidos)
    print('Compra encaminhada:', pedido)
    print('O estoque só muda quando o recebimento for lançado no menu 3.')


def relatorios():
    acao = input(
        '1 Estoque baixo | 2 Ordenar por validade | 3 Ver fila | '
        '4 Histórico | 5 Ranking de estoque | 6 Medicamentos | '
        '7 Fornecedores | 8 Travessias da árvore: '
    )
    if acao == '1':
        resultado = []
        for m in em_ordem(medicamentos):
            if m['estoque'] < m['minimo']:
                resultado.append(m)
        mostrar(resultado)
    elif acao == '2':
        mostrar(ordenar(em_ordem(medicamentos), 'validade'))
    elif acao == '3':
        mostrar(listar_pedidos(pedidos))
    elif acao == '4':
        if not historico:
            print('Histórico vazio.')
        for i in range(len(historico) - 1, -1, -1):
            movimento = historico[i]
            print(movimento['medicamento']['codigo'],
                  movimento['quantidade'], movimento['motivo'])
    elif acao == '5':
        ordenados = ordenar(em_ordem(medicamentos), 'estoque')
        for i in range(len(ordenados) - 1, -1, -1):
            print(ordenados[i])
    elif acao == '6':
        mostrar(em_ordem(medicamentos))
    elif acao == '7':
        mostrar(em_ordem(fornecedores))
    elif acao == '8':
        tipo = input('1 Em ordem | 2 Pré-ordem | 3 Pós-ordem: ').strip()
        if tipo == '1':
            mostrar(em_ordem(medicamentos))
        elif tipo == '2':
            mostrar(pre_ordem(medicamentos))
        elif tipo == '3':
            mostrar(pos_ordem(medicamentos))
        else:
            raise ValueError('Opção inválida.')
    else:
        raise ValueError('Opção inválida.')


def main():
    print('ERP DE FARMÁCIA - otimizado | Dados descartados ao sair')
    while True:
        try:
            print('\n1 Fornecedores | 2 Medicamentos | 3 Movimentar estoque'
                  '\n4 Desfazer | 5 Solicitar reposição | 6 Processar reposição'
                  '\n7 Relatórios | 0 Sair')
            opcao = input('Opção: ')
            if opcao == '0':
                break
            elif opcao == '1':
                cadastros('fornecedor', fornecedores)
            elif opcao == '2':
                cadastros('medicamento', medicamentos)
            elif opcao == '3':
                movimentar()
            elif opcao == '4':
                desfazer()
            elif opcao == '5':
                solicitar()
            elif opcao == '6':
                processar()
            elif opcao == '7':
                relatorios()
            else:
                raise ValueError('Opção inválida.')
        except ValueError as erro:
            print('Atenção:', erro)
        except (EOFError, KeyboardInterrupt):
            break
    print('Programa encerrado. Dados da sessão descartados.')


if __name__ == '__main__':
    main()
