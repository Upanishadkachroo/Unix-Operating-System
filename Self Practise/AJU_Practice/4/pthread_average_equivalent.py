import threading

# Global list to store results
averages = []

def compute_average(thread_name):
    nums = input(f"Enter numbers for {thread_name} (space-separated): ").split()
    nums = [float(n) for n in nums]
    avg = sum(nums) / len(nums)
    print(f"{thread_name} average = {avg:.2f}")
    averages.append(avg)

if __name__ == "__main__":
    t1 = threading.Thread(target=compute_average, args=("Thread-1",))
    t2 = threading.Thread(target=compute_average, args=("Thread-2",))
    t3 = threading.Thread(target=compute_average, args=("Thread-3",))

    t1.start()
    t2.start()
    t3.start()

    # Wait for all threads to finish
    t1.join()
    t2.join()
    t3.join()

    total_avg = sum(averages) / len(averages)
    print(f"\nOverall average of all threads = {total_avg:.2f}")
