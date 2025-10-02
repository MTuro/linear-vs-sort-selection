import random
import time
import math
import pandas as pd
import matplotlib.pyplot as plt

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

def bubble_sort(arr):
    """BubbleSort (retorna nova lista ordenada)."""
    A = arr.copy()
    n = len(A)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if A[j] > A[j + 1]:
                A[j], A[j + 1] = A[j + 1], A[j]
                swapped = True
        if not swapped:
            break
    return A

def SortSelection(A, k):
    """Seleciona o k-ésimo menor (1-based) usando BubbleSort."""
    if k <= 0 or k > len(A):
        raise IndexError("k out of bounds")
    return bubble_sort(A)[k-1]

def run_experiments(n_values, instances_per_n=10, value_range=(1,100000),
                    seed=42, save_csv="selection_results.csv", save_plot="selection_plot.png"):
    """Roda os experimentos comparando LinearSelection e SortSelection."""
    random.seed(seed)
    results = []
    total_steps = len(n_values)
    for i, n in enumerate(n_values, 1):
        k = n // 2  # conforme enunciado (k = floor(n/2), 1-based)
        linear_times = []
        bubble_times = []
        for inst in range(instances_per_n):
            print(f"  Processando n={n}, instância {inst+1}/{instances_per_n}")
            A = [random.randint(value_range[0], value_range[1]) for _ in range(n)]
            A1 = A.copy()
            A2 = A.copy()

            t0 = time.perf_counter()
            val_linear = LinearSelection(A1, k)
            t1 = time.perf_counter()
            linear_times.append(t1 - t0)
            print(f"    LinearSelection: {(t1-t0)*1000:.3f}ms")

            t0 = time.perf_counter()
            val_bubble = SortSelection(A2, k)
            t1 = time.perf_counter()
            bubble_times.append(t1 - t0)
            print(f"    SortSelection: {(t1-t0)*1000:.1f}ms")

            # verificação de corretude
            ref = sorted(A)[k-1]
            if not (val_linear == ref == val_bubble):
                raise AssertionError(f"Resultados divergentes n={n} inst={inst}: linear={val_linear}, bubble={val_bubble}, ref={ref}")

        avg_linear = sum(linear_times) / len(linear_times)
        avg_bubble = sum(bubble_times) / len(bubble_times)
        results.append({
            "n": n,
            "k": k,
            "avg_time_linear": avg_linear,
            "avg_time_bubble": avg_bubble,
            "linear_times": linear_times,
            "bubble_times": bubble_times
        })
        # Formatação inteligente baseada na magnitude dos tempos
        linear_str = f"{avg_linear*1000:.3f}ms" if avg_linear >= 0.001 else f"{avg_linear*1000000:.1f}μs"
        bubble_str = f"{avg_bubble*1000:.1f}ms" if avg_bubble >= 0.001 else f"{avg_bubble*1000000:.1f}μs"
        
        print(f"[{i}/{total_steps}] n={n}:")
        print(f"  LinearSelection: {linear_str} (média)")
        print(f"  SortSelection: {bubble_str} (média)")
        print(f"  Razão Bubble/Linear: {avg_bubble/avg_linear:.1f}x mais lento")
        print()

    # salvar resumo em CSV
    df = pd.DataFrame([{"n": r["n"], "k": r["k"],
                        "avg_time_linear": r["avg_time_linear"],
                        "avg_time_bubble": r["avg_time_bubble"]} for r in results])
    df.to_csv(save_csv, index=False)
    print(f"Resultados salvos em: {save_csv}")

    # plot com múltiplas visualizações para melhor compreensão
    plt.figure(figsize=(15,10))
    
    # Gráfico: Comparação com escala logarítmica
    plt.subplot(2, 2, 1)
    plt.plot(df["n"], df["avg_time_linear"], marker='o', linewidth=2, markersize=6, 
             label="LinearSelection", color='blue')
    plt.plot(df["n"], df["avg_time_bubble"], marker='s', linewidth=2, markersize=6,
             label="SortSelection", color='red')
    plt.xlabel("Tamanho da entrada n")
    plt.ylabel("Tempo médio (segundos)")
    plt.title("Comparação - Escala Logarítmica")
    plt.yscale('log')
    plt.legend()
    plt.grid(True, alpha=0.3)
    return results, df

# --- Bloco principal para executar os experimentos (adicione ao final do arquivo):

if __name__ == "__main__":
    # Reduzido para evitar lentidão extrema do BubbleSort O(n²)
    n_values = list(range(1000, 6001, 1000))  # até 6000 ao invés de 10000
    instances_per_n = 5  # reduzido de 10 para 5 instâncias
    results, df_summary = run_experiments(n_values, instances_per_n=instances_per_n)
#todo: BubbleSort ,SortSelection e comparações  