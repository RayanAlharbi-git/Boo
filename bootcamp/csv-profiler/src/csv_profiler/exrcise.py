import time

start = time.perf_counter_ns()

time.sleep(3)

end = time.perf_counter_ns()


elapsed_ms= (end - start ) / 1_000_0000

print(f"Elapsed time: {elapsed_ms:.2f}ms")