from setuptools import setup,Extension

ext_module = Extension("_ArticleSearch",sources=['ArticleSearch_wrap.c',"ArticleSearch.c"])

setup(
	name = "ArticleSearch",
	author      = "Declan Atkins",
    description = """Searches for the Article Search Module""",
    ext_modules = [ext_module],
    py_modules = ["ArticleSearch"],

)