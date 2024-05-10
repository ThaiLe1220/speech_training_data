import os
import multiprocessing

# Using os
cpu_cores_os = os.cpu_count()

# Using multiprocessing
cpu_cores_mp = multiprocessing.cpu_count()

print(f"Number of CPU cores (os): {cpu_cores_os}")
print(f"Number of CPU cores (multiprocessing): {cpu_cores_mp}")
