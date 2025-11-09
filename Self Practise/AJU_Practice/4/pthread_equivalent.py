import threading

numbers = list(range(1, 21))

results = {"odd": 0, "even": 0, "prime": 0}

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def calc_even_avg():
    even_nums = [n for n in numbers if n % 2 == 0]
    avg = sum(even_nums) / len(even_nums)
    results["even"] = avg
    print(f"Even numbers: {even_nums} | Average: {avg}")

def calc_odd_avg():
    odd_nums = [n for n in numbers if n % 2 != 0]
    avg = sum(odd_nums) / len(odd_nums)
    results["odd"] = avg
    print(f"Odd numbers: {odd_nums} | Average: {avg}")

def calc_prime_avg():
    prime_nums = [n for n in numbers if is_prime(n)]
    avg = sum(prime_nums) / len(prime_nums)
    results["prime"] = avg
    print(f"Prime numbers: {prime_nums} | Average: {avg}")

if __name__ == "__main__":
    t1 = threading.Thread(target=calc_even_avg)
    t2 = threading.Thread(target=calc_odd_avg)
    t3 = threading.Thread(target=calc_prime_avg)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    print("\n--- Final Results ---")
    print(f"Even Avg: {results['even']}")
    print(f"Odd Avg: {results['odd']}")
    print(f"Prime Avg: {results['prime']}")
