import sys

sys.path.append("../C-Modules/ModelOperations")
import ModelOperations

val = ModelOperations.get_predicted_values("Amazon", "Neutral")
val = ModelOperations.doubleArray_frompointer(val)
print(val[0])