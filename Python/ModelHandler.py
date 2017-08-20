import sys

sys.path.append("../C-Modules/ModelOperations")
import ModelOperations


vals = ModelOperations.doubleArray(3)
vals[0] = 1.03
vals[1] = 1.07
vals[2] = 1.08

ModelOperations.add_values(vals,"Amazon","Neutral")