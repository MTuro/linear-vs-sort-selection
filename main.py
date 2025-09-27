import random
import time
import math

# Funções Auxiliares

def partition(arr, left, right, pivot):
    """ Particiona arr[left:right] em torno de pivot_value """
    pivot_value = pivot
    # move o pivot para o final
    for i in range(left, right+1):
        if arr[i] == pivot_value:
            arr[i], arr[right] = arr[right], arr[i]   # <--- troca
            break
    store = left
    for i in range(left, right):
        if arr[i] < pivot_value:
            arr[store], arr[i] = arr[i], arr[store]
            store += 1
    arr[store], arr[right] = arr[right], arr[store]
    return store


def select_median_of_medians(arr, left, right, k):
    """ Retorna o k-ésimo menor (0-based) de arr[left:right] usando median of medians """
    while True:
        n = right - left + 1
        if k < 0 or k >= n:
            raise IndexError("k out of bounds")
        # caso base: array pequeno -> ordena direto
        if n <= 10:
            sub = sorted(arr[left:right+1])
            return sub[k]
        # divide em grupos de 5 e pega as medianas
        medians = []
        i = left
        while i <= right:
            group = arr[i:min(i+5, right+1)]
            group.sort()
            medians.append(group[len(group)//2])
            i += 5
        # encontra mediana das medianas recursivamente
        mom = select_median_of_medians(medians, 0, len(medians)-1, len(medians)//2)
        pivot_index = partition(arr, left, right, mom)
        rank = pivot_index - left
        if k == rank:
            return arr[pivot_index]
        elif k < rank:
            right = pivot_index - 1
        else:
            k = k - rank - 1
            left = pivot_index + 1
            
            
# Algoritmo de Seleção

def LinearSelection(A, k):
    """ Retorna o k-ésimo menor (1-based) usando median of medians """
    if k <= 0 or k > len(A):
        raise IndexError("k out of bounds")
    arr = list(A)  # copia
    return select_median_of_medians(arr, 0, len(arr)-1, k-1)

#todo: BubbleSort ,SortSelection e comparações  