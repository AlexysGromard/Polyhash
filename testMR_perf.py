from core.Arbitrator import Arbitrator
from testMR_Arb_opti import Arbitrator as Opti
from  core.models import Vector3, DataModel
import random
from time import *

d = DataModel.extract_data("./challenges/d_final.in")


a = Opti(d)
balls = [Vector3(random.randint(0, 74), random.randint(0, 299),1) for _  in range(d.num_balloons)]
startTime = time()
for _ in range(100):
    a.turn_score(balls)
endTime = time()
print(f"time opti: {endTime - startTime}")
a = Arbitrator(d)
startTime = time()
for _ in range(100):
    a.turn_score(balls)
endTime = time()
print(f"time non-opti: {endTime - startTime}")