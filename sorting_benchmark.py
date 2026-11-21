import time


def selection_sort(arr):
    """Selection Sort: In-place, Time: O(n^2), Auxiliary Space: O(1)"""
    a = arr.copy()
    n = len(a)
    comparisons = 0
    swaps = 0

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1

    return a, comparisons, swaps


def bubble_sort(arr):
    """Bubble Sort: In-place, Time: O(n^2) worst/avg, O(n) best, Auxiliary Space: O(1)"""
    a = arr.copy()
    n = len(a)
    comparisons = 0
    swaps = 0

    for i in range(n):
        swapped_in_pass = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped_in_pass = True
        if not swapped_in_pass:
            break

    return a, comparisons, swaps


def quick_sort(arr):
    """Quick Sort with median-of-three pivot to avoid O(n^2) degradation on sorted/reverse inputs"""
    a = arr.copy()
    stats = {"comparisons": 0, "swaps": 0}

    def median_of_three(low, high):
        mid = (low + high) // 2
        stats["comparisons"] += 1
        if a[low] > a[mid]:
            a[low], a[mid] = a[mid], a[low]
            stats["swaps"] += 1
        stats["comparisons"] += 1
        if a[low] > a[high]:
            a[low], a[high] = a[high], a[low]
            stats["swaps"] += 1
        stats["comparisons"] += 1
        if a[mid] > a[high]:
            a[mid], a[high] = a[high], a[mid]
            stats["swaps"] += 1
        a[mid], a[high - 1] = a[high - 1], a[mid]
        stats["swaps"] += 1
        return a[high - 1]

    def _quick_sort(low, high):
        if low < high:
            if high - low + 1 <= 3:
                for i in range(low + 1, high + 1):
                    key = a[i]
                    j = i - 1
                    while j >= low:
                        stats["comparisons"] += 1
                        if a[j] > key:
                            a[j + 1] = a[j]
                            stats["swaps"] += 1
                            j -= 1
                        else:
                            break
                    a[j + 1] = key
                return

            pivot = median_of_three(low, high)
            i = low
            j = high - 1

            while True:
                while True:
                    i += 1
                    stats["comparisons"] += 1
                    if a[i] >= pivot:
                        break
                while True:
                    j -= 1
                    stats["comparisons"] += 1
                    if a[j] <= pivot:
                        break
                if i >= j:
                    break
                a[i], a[j] = a[j], a[i]
                stats["swaps"] += 1

            a[i], a[high - 1] = a[high - 1], a[i]
            stats["swaps"] += 1

            _quick_sort(low, i - 1)
            _quick_sort(i + 1, high)

    if len(a) > 1:
        _quick_sort(0, len(a) - 1)

    return a, stats["comparisons"], stats["swaps"]


def merge_sort(arr):
    """Merge Sort: Time: O(n log n), Auxiliary Space: O(n)"""
    a = arr.copy()
    stats = {"comparisons": 0, "writes": 0}

    def _merge_sort(sub):
        if len(sub) <= 1:
            return sub
        mid = len(sub) // 2
        left = _merge_sort(sub[:mid])
        right = _merge_sort(sub[mid:])
        return _merge(left, right)

    def _merge(left, right):
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            stats["comparisons"] += 1
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
            stats["writes"] += 1

        while i < len(left):
            merged.append(left[i])
            i += 1
            stats["writes"] += 1

        while j < len(right):
            merged.append(right[j])
            j += 1
            stats["writes"] += 1

        return merged

    sorted_arr = _merge_sort(a)
    return sorted_arr, stats["comparisons"], stats["writes"]


def benchmark_algorithm(sort_func, base_array, runs=3):
    times = []
    last_comp = 0
    last_ops = 0

    for _ in range(runs):
        arr_copy = base_array.copy()
        start = time.perf_counter()
        sorted_res, comp, ops = sort_func(arr_copy)
        end = time.perf_counter()

        assert sorted_res == sorted(base_array), "Sorting failed!"
        times.append(end - start)
        last_comp = comp
        last_ops = ops

    avg_time = sum(times) / len(times)
    return avg_time, last_comp, last_ops


def main():
    test_cases = [
        ("Size 5 - Sorted", list(range(1, 6))),
        ("Size 5 - Reverse Sorted", list(range(5, 0, -1))),
        ("Size 100 - Sorted", list(range(1, 101))),
        ("Size 100 - Reverse Sorted", list(range(100, 0, -1))),
    ]

    algorithms = [
        ("Selection Sort", selection_sort, "O(1) auxiliary (in-place)"),
        ("Bubble Sort", bubble_sort, "O(1) auxiliary (in-place)"),
        ("Quick Sort", quick_sort, "O(log n) recursion stack (in-place partition)"),
        ("Merge Sort", merge_sort, "O(n) auxiliary arrays"),
    ]

    for case_name, data in test_cases:
        print(f"\n=== {case_name} ===")
        for alg_name, func, space_desc in algorithms:
            avg_t, comp, ops = benchmark_algorithm(func, data, runs=3)
            print(
                f"{alg_name:15s} | Avg Time: {avg_t*1e6:8.2f} us ({avg_t:.8f} s) "
                f"| Comparisons: {comp:4d} | Swaps/Writes: {ops:4d} | Space: {space_desc}"
            )


if __name__ == "__main__":
    main()
