import time
import sys

nl=123456789
if len(sys.argv) > 1:
    nl = int(sys.argv[1])

def p702():
    f_cache = {}

    def f(x, m):
        # number of inversions in {a*x % m} for 0 < a < m
        # requires gcd(x, m) = 1
        x %= m
        if x <= 1:
            return 0
        if (x, m) in f_cache:
            return f_cache[x, m]
        t, y = divmod(m, x)
        res = t * (t + 1) * x * (x - 1) // 4 + (t + 1) * f(x, y) - t * f(x, x - y)
        f_cache[x, m] = res
        return res

    def g(x, m):
        return (m - 1) * (m - 2) - f(x, m)

    def main(N):  # assume N is odd
        D = N.bit_length()
        return N * (3 * N + 1) // 2 * (D + 1) - sum(g(N, 2 ** d) for d in range(2, D + 1)) + 2 * g(N, 2 ** D - N)

    t0 = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
    res=main(nl)
    clk = (time.clock_gettime_ns(time.CLOCK_MONOTONIC) - t0) / 1000000
    print(res)
    print(" {:.3f}ms ".format(clk))
 #   print(f_cache)


p702()