"""WSU-COS 207 setup check: run inside your activated virtual environment."""
import platform, shutil, subprocess, sys
from importlib.metadata import version, PackageNotFoundError

problems = 0
print(f"Operating system : {platform.system()} {platform.release()}")
ok = sys.version_info >= (3, 12)
problems += not ok
print(f"Python           : {platform.python_version()}  {'OK' if ok else 'NEED 3.12 OR LATER'}")
in_venv = sys.prefix != sys.base_prefix
problems += not in_venv
print(f"Virtual env      : {'active' if in_venv else 'NOT ACTIVE (activate .venv first)'}")
for pkg in ("numpy", "pandas", "scipy", "matplotlib", "jupyterlab"):
    try:
        print(f"{pkg:<17}: {version(pkg)}")
    except PackageNotFoundError:
        problems += 1
        print(f"{pkg:<17}: MISSING (python -m pip install {pkg})")
git = shutil.which("git")
if git:
    out = subprocess.run([git, "--version"], capture_output=True, text=True).stdout.strip()
    print(f"Git              : {out}")
else:
    problems += 1
    print("Git              : NOT FOUND on PATH")
print("ALL CHECKS PASSED" if problems == 0 else f"{problems} PROBLEM(S): fix them before Practical 1")
