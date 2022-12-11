import numpy as np
import time
from mpi4py import MPI

comm = MPI.COMM_WORLD
s = comm.Get_size()
r = comm.Get_rank()
point_of_dispersed = 0

def circle(points):
    p = pow(pow((points[0]), 2) + pow((points[1]), 2), 0.5)
    if p > 1:
        return False
    else:
        return True
def Morte_Carlo(point):
    in_circle = np.count_nonzero(pow(pow((point.T[0]),2) + pow((point.T[1]), 2), 0.5) <= 1)
    products = (in_circle/len(point))*4

    return products

if r == 0:
        amount = 1000000
        array = np.random.rand(amount, 2)
        divide_size = int(amount/s)
        dispersed_points = [array[0: (i+1) * divide_size]for i in range(0, s)]

points = comm.scatter(dispersed_points, root=0)

start_time = time.perf_counter()
pi_number = Morte_Carlo(points)
end_time = time.perf_counter()

processes = comm.gather({"PI": pi_number,"ExecutionTime": (end_time - start_time)}, root=0)

if r == 0:
    for process in processes:
            print(f'Pi number: {process["PI"]:10f} Execution time: {process["ExecutionTime"]:0.6f}')

#The OS used : Ubuntu
#command for execution: # mpiexec -n 2 python3 main.py