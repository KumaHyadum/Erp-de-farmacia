# ERP de Farmácia — Otimização Algorítmica e Estrutural (TDE 2)

Projeto desenvolvido para a disciplina de **Algoritmos e Estruturas de Dados** (Engenharia de Software — UNIFAN).

## Autores
- Cleiton Souza Santos
- Davi Figueiredo Lima
- Murilo Braz da Costa

## Estrutura do Repositório
- `TDE.ERP.FARMACIA.py` — Versão base (Parte 1) utilizando listas ordenadas, busca binária, busca linear, pilha de histórico, fila linear de prioridade e Insertion Sort.
- `TDE2.ERP.FARMACIA.py` — Versão otimizada (Parte 2) mantendo todas as regras de negócio da versão base e adicionando estruturas e algoritmos implementados manualmente.
- `benchmark.py` — Script reprodutível de validação de equivalência e medição de desempenho (tempo médio, desvio padrão e número de comparações).

## Otimizações Implementadas na Parte 2
- **Árvore Balanceada AVL (manual):** Substituiu as listas ordenadas de fornecedores e medicamentos, com rotações simples e duplas (`rotacao_direita`, `rotacao_esquerda`, `balancear`).
- **Busca Manual na Árvore:** Busca iterativa por código (`buscar`) e busca recursiva por nome (`buscar_por_nome`) diretamente nos nós da AVL.
- **Travessias da Árvore:** Percursos em ordem (`em_ordem`), pré-ordem (`pre_ordem`) e pós-ordem (`pos_ordem`) disponíveis no menu de relatórios (opção 8).
- **Ordenação por Divisão e Conquista (Merge Sort manual):** Substituiu o Insertion Sort na ordenação de relatórios de validade, fila e ranking de estoque.
- **Otimização Adicional — Min-Heap Binário (manual):** Substituiu a fila de pedidos linear na reposição de estoque, mantendo desempate por ordem de chegada via contador de sequência.

## Como Executar
Certifique-se de ter o Python 3 instalado e os três arquivos `.py` na mesma pasta:

```bash
# Executar o sistema ERP otimizado
python TDE2.ERP.FARMACIA.py

# Executar os testes de equivalência e benchmark
python benchmark.py
```
