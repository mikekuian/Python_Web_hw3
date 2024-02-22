from multiprocessing import Pool, current_process, cpu_count
import time
import logging
import os

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def worker(x):
    if x == 1: return [1]  # Handle case for 1 explicitly
    divisors = set([1, x])  # Initialize with 1 and x, use a set to avoid duplicates
    for num in range(2, int(x ** 0.5) + 1):  # Iterate only up to the square root of x
        if x % num == 0:
            divisors.add(num)
            divisors.add(x // num)
    return sorted(divisors)  # Sort the divisors before returning


def factorize(*numbers):
    results = []
    for number in numbers:
        results.append(worker(number))

    return results

def parallel_factorize(*numbers):
    with Pool(processes=os.cpu_count()) as pool:
        results = pool.map(worker, numbers)
    return results


if __name__ == "__main__":

    start_time = time.time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)

    # Assertions to validate the results
    assert a == [1, 2, 4, 8, 16, 32, 64, 128], f"a: {a}"
    assert b == [1, 3, 5, 15, 17, 51, 85, 255], f"b: {b}"
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999], f"c: {c}"
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060], f"d: {d}"

    logger.debug('Assertions passed successfully.')
    end_time = time.time()
    print(f"Execution time without processing: {end_time - start_time} seconds")

    start_time = time.time()
    a, b, c, d = parallel_factorize(128, 255, 99999, 10651060)

    # Assertions to validate the results
    assert a == [1, 2, 4, 8, 16, 32, 64, 128], f"a: {a}"
    assert b == [1, 3, 5, 15, 17, 51, 85, 255], f"b: {b}"
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999], f"c: {c}"
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060], f"d: {d}"

    logger.debug('Assertions passed successfully.')
    end_time = time.time()
    print(f"Execution time without processing: {end_time - start_time} seconds")
