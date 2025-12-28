import time
def pb179():
    divisors = [2] * (10 ** 7 + 1)  # Invalid for indexes 0 and 1
    for i in range(2, (len(divisors) + 1) // 2):
        for j in range(i * 2, len(divisors), i):
            divisors[j] += 1

    ans = sum((1 if divisors[i] == divisors[i + 1] else 0) for i in range(2, len(divisors) - 1))
    return str(ans)

t0=time.CLOCK_PROCESS_CPUTIME_ID
print(pb179())
clk = (time.clock_gettime_ns(time.CLOCK_PROCESS_CPUTIME_ID) - t0) / 1000000000;
print("{:.6f}s ".format(clk), end='')

