# Declaração de autoria
# Autores: Cleiton Souza Santos, Davi Figueiredo Lima, Murilo Braz da Costa
# Declaro que este código foi desenvolvido por nós, com base no nosso próprio
# entendimento e esforço. Não houve plágio ou cópia integral de terceiros.
# Ferramentas de IA, quando utilizadas, foram apenas como apoio ao aprendizado
# e não para a geração integral deste código.

from datetime import date

# LISTAS de cadastro; PILHA de movimentos; FILA de pedidos.
fornecedores = []
medicamentos = []
historico = []
pedidos = []


def buscar(lista, codigo):
    """Busca binária manual pelo código. A lista precisa estar ordenada."""
    inicio = 0
    fim = len(lista) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        codigo_meio = lista[meio]['codigo']

        if codigo_meio == codigo:
            return meio
        elif codigo_meio < codigo:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1


def buscar_por_nome(lista, nome):
    """Busca manual linear pelo nome do medicamento."""
    nome = nome.strip().lower()

    for i in range(len(lista)):
        if lista[i]['nome'].lower() == nome:
            return i

    return -1


def inserir_ordenado(lista, registro):
    """Insere manualmente pelo código, mantendo a lista pronta para busca binária."""
    inicio = 0
    fim = len(lista)

    while inicio < fim:
        meio = (inicio + fim) // 2
        if lista[meio]['codigo'] < registro['codigo']:
            inicio = meio + 1
        else:
            fim = meio

    lista.insert(inicio, registro)


def ordenar(lista, campo):
    """Insertion Sort manual: ordena uma cópia pelo campo informado."""
    copia = lista[:]
    for i in range(1, len(copia)):
        atual = copia[i]
        j = i - 1
        while j >= 0 and copia[j][campo] > atual[campo]:
            copia[j + 1] = copia[j]
            j -= 1
        copia[j + 1] = atual
    return copia


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


def selecionar(lista):
    codigo = ler_texto('Código: ')
    indice = buscar(lista, codigo)
    if indice == -1:
        raise ValueError('Código não encontrado.')
    return indice


def mostrar(lista):
    if not lista:
        print('Nenhum registro.')
    for registro in lista:
        print(registro)


def tem_pedido(codigo):
    for pedido in pedidos:
        if pedido['codigo'] == codigo:
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
    if buscar(fornecedores, registro['fornecedor']) == -1:
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


def cadastros(tipo, lista):
    """Mesmo menu CRUD para fornecedores e medicamentos."""
    acao = input('1 Cadastrar | 2 Consultar | 3 Alterar | 4 Remover | 5 Listar: ')
    if acao == '1':
        codigo = ler_texto('Novo código: ')
        if buscar(lista, codigo) != -1:
            raise ValueError('Código já cadastrado.')
        inserir_ordenado(lista, ler_cadastro(tipo, codigo))
    elif acao == '5':
        mostrar(lista)
    elif acao == '2' or acao == '3' or acao == '4':
        if acao == '2' and tipo == 'medicamento':
            metodo = input('1 - Buscar por código | 2 - Buscar por nome: ').strip()

            if metodo == '1':
                i = selecionar(lista)
            elif metodo == '2':
                nome = ler_texto('Nome do medicamento: ')
                i = buscar_por_nome(lista, nome)
                if i == -1:
                    raise ValueError('Medicamento não encontrado pelo nome.')
            else:
                raise ValueError('Opção de busca inválida.')

            print(lista[i])
            return

        i = selecionar(lista)
        registro = lista[i]
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
            lista[i] = novo
        else:
            if tipo == 'fornecedor':
                for m in medicamentos:
                    if m['fornecedor'] == registro['codigo']:
                        raise ValueError('Fornecedor ligado a medicamento.')
            lista.pop(i)
    else:
        raise ValueError('Opção inválida.')


def movimentar():
    m = medicamentos[selecionar(medicamentos)]
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
    m = medicamentos[selecionar(medicamentos)]
    if tem_pedido(m['codigo']):
        raise ValueError('Já existe pedido para esse medicamento.')
    quantidade = ler_numero('Quantidade para comprar: ', 1)
    # Menor chave vence: criticidade alta, depois validade mais próxima.
    pedidos.append({'codigo': m['codigo'], 'quantidade': quantidade,
                    'prioridade': (-m['criticidade'], m['validade'])})


def processar():
    if not pedidos:
        raise ValueError('Fila vazia.')
    melhor = 0
    for i in range(1, len(pedidos)):
        # < mantém o pedido mais antigo quando as prioridades empatam.
        if pedidos[i]['prioridade'] < pedidos[melhor]['prioridade']:
            melhor = i
    pedido = pedidos.pop(melhor)
    print('Compra encaminhada:', pedido)
    print('O estoque só muda quando o recebimento for lançado no menu 3.')


def relatorios():
    acao = input(
        '1 Estoque baixo | 2 Ordenar por validade | 3 Ver fila | '
        '4 Histórico | 5 Ranking de estoque | 6 Medicamentos | 7 Fornecedores: '
    )
    if acao == '1':
        resultado = []
        for m in medicamentos:
            if m['estoque'] < m['minimo']:
                resultado.append(m)
        mostrar(resultado)
    elif acao == '2':
        mostrar(ordenar(medicamentos, 'validade'))
    elif acao == '3':
        mostrar(ordenar(pedidos, 'prioridade'))
    elif acao == '4':
        if not historico:
            print('Histórico vazio.')
        for i in range(len(historico) - 1, -1, -1):
            movimento = historico[i]
            print(movimento['medicamento']['codigo'],
                  movimento['quantidade'], movimento['motivo'])
    elif acao == '5':
        ordenados = ordenar(medicamentos, 'estoque')
        for i in range(len(ordenados) - 1, -1, -1):
            print(ordenados[i])
    elif acao == '6':
        mostrar(medicamentos)
    elif acao == '7':
        mostrar(fornecedores)
    else:
        raise ValueError('Opção inválida.')


def main():
    print('ERP DE FARMÁCIA - simples | Dados descartados ao sair')
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
