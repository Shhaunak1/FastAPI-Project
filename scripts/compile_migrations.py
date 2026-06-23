import py_compile, glob, sys

files = glob.glob(r'c:\FastAPI\alembic\versions\*.py')
if not files:
    print("No migration files found")
    sys.exit(0)

ok = True
for f in files:
    try:
        py_compile.compile(f, doraise=True)
        print("Compiled", f)
    except Exception as e:
        print("Error compiling", f, e)
        ok = False

if not ok:
    sys.exit(1)
