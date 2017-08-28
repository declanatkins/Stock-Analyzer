import sys

sys.path.append("../C-Modules/ModelOperations")
import ModelOperations


val = ModelOperations.get_expected_value("../Data/Amazon/Neutral/1.dat", 0.02)
print(val)