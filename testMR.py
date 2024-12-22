from core.models import *
from core.models.OutputModel import *
from core.algorithms.Mathis.algoMathis import *
from core.algorithms.Recursivo.Recursivo import *


d = DataModel.extract_data("challenges/b_small.in")
a = Arbitrator(d.rows, d.cols)
algo = Recursivo()
from testMRArbitre import *
a = ArbitatorMR(d)

#Calcul du score:
def get_best(tours):
    best_score = -1
    min_score = 10000000
    best_result = None
    algo = RSMTv2()
    for _ in range(tours):
        score = 0
        result = algo.compute(d)
        print(result)
        places = [Vector3(d.starting_cell.x, d.starting_cell.y, 0) for i in range(d.num_balloons)]
        
        for turn in result["path"]:
            for i in range(len(places)):
                places[i].z += turn[i]
                places[i] = algo.nextPlace(d,places[i])
            score += a.turnScore(places)

        min_score = min(min_score, score)
        if score > best_score:
            best_score = score
            best_result = result[1]
    
        
    print(f"best_score: {best_score}, min_score = {min_score}")
    #print(best_result)
    return [best_score, min_score, best_result]

print(get_best(1))
""" 
if __name__ == "__main__":
    with multiprocessing.Pool(8) as pool:
        results = pool.map(get_best, [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000])
    min = 0
    path = None
    for r in results:
        print(f"best: {r[0]}, min: {r[1]}")
        if r[0] > min:
            min = r[0]
            path = r[2]
    print(f"best: {min}")
    o = OutputModel(d.turns, d.num_balloons, path)
    o.export_output_file('test.txt')
 """