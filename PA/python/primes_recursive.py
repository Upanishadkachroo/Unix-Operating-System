# primes_recursive.py

def is_prime(n, i=2):
    if n <= 2:
        return n == 2
    if n % i == 0:
        return False
    if i * i > n:
        return True
    return is_prime(n, i + 1)

def generate_primes(limit, current=2):
    if current > limit:
        return []
    if is_prime(current):
        return [current] + generate_primes(limit, current + 1)
    else:
        return generate_primes(limit, current + 1)

# Driver code
limit = int(input("Enter limit: "))
print(f"Prime numbers up to {limit}:")
print(generate_primes(limit))
