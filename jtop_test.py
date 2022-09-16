from jtop import jtop

with jtop() as jetson:
    d = jetson.ram
    cpu_mem = (d['use'] - d['shared']) * 10**3      # CPU Memory (Byte)
    gpu_mem = d['shared'] * 10**3                   # GPU Memory (Byte)

    print(cpu_mem)
    print(gpu_mem)
    print(cpu_mem / 2 ** 20)
    print(gpu_mem / 2 ** 20)
