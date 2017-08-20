from setuptools import setup,Extension

ext_module = Extension("_ModelOperations",sources=['ModelOperations_wrap.c',"ModelOperations.c"])

setup(
	name = "ModelOperations",
	author      = "Declan Atkins",
    description = """Builds and makes predictions based on the model""",
    ext_modules = [ext_module],
    py_modules = ["ModelOperations"],

)