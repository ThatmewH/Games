import cx_Freeze, os
os.environ['TCL_LIBRARY'] = r'J:\Python\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'J:\Python\tcl\tk8.6'

executables = [cx_Freeze.Executable("J:\Project\Games\Connect-4\connect4.py")]

options = {"packages":["pygame", "random", "copy", "data", "functions"],
           "excludes":["tkinter", "asyncio",
                       "concurrent",
                       "curses",
                       "dateutil",
                       "http",
                       "xml"
                       "tcl",
                       "scipy",
                       "numpy",
                       "distutils",
                       "email",
                       "cffi",
                       "idna",
                       "_ssl",
                       "html",
                       "lib2to3",
                       "logging",
                       "pkg_resources",
                       "pydoc_data",
                       "pyzt",
                       "setuptools",
                       "unittest"]}
cx_Freeze.setup(
    name="Connnect 4",
    options={"build_exe": options},
    executables = executables
)
