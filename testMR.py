from core.models import *
from core.algorithms.R_SMT.r_smt import *
from core.algorithms.R_SMT.r_smt_v2 import *
from time import *
from testMR_Arb_opti import *
import multiprocessing
d = DataModel.extract_data("challenges/c_medium.in")


arb = Arbitrator(d)
startTime = time()
#result = a.compute(d)
endTime = time()

#Calcul du score:
def get_best(tours):
    best_score = -1
    min_score = 10000000
    best_result = None
    algo = RSMTv2()
    for _ in range(tours):
        score = 0
        result = algo.compute(d)
       
        score = result[3]
    
       
        min_score = min(min_score, score)
        if score > best_score:
            best_score = score
            best_result = result[1]
    
        
    print(f"best_score: {best_score}, min_score = {min_score}")
    #print(best_result)
    return [best_score, min_score, best_result]

if __name__ == "__main__":
    with multiprocessing.Pool(4) as pool:
        n = 1
        results = pool.map(get_best, [n for i in range(4)])
    min = 0
    path = None
    for r in results:
        print(f"best: {r[0]}, min: {r[1]}")
        if r[0] > min:
            min = r[0]
            path = r[2] 
    
    print(f"best: {min}")
   
    o = OutputModel(0, 0, path)
    o.export_output_file("test.txt")

