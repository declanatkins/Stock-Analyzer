import sys

sys.path.append("../C-Modules/ModelOperations")
import ModelOperations


vals = ModelOperations.doubleArray(150)
v = 1.01
change = 0.01

for i in range(0,150):
	v += change
	change += 0.01
	vals[i] = v
	

ModelOperations.add_values(vals,150,"Amazon","Neutral")