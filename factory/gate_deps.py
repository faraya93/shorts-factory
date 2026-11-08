"""Element-scoped dependencies for the v2 gate (2026-11-08): what a scene script really uses from code3d/lib, at function level, hashed with comments and docstrings removed.
Editing real_kit.water no longer touches a scene that only uses real_kit.ice. Anything the walk cannot resolve (exec, importlib, getattr on a module, a module passed around as a value) widens to the whole module or, for dynamic imports, the whole production list: fail safe."""
import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "code3d" / "lib"
CORE = ("looks", "common", "composition", "pipeline_config")   # the shared colour/composition core is always a dependency, whole
_DYNAMIC = {"exec", "eval", "__import__", "import_module"}
_cache: dict[str, tuple] = {}


def _strip(node):
    for n in ast.walk(node):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)) and n.body and isinstance(n.body[0], ast.Expr) \
                and isinstance(getattr(n.body[0], "value", None), ast.Constant) and isinstance(n.body[0].value.value, str):
            n.body = n.body[1:] or [ast.Pass()]
    return node


def normalized(path: Path) -> str:
    return ast.dump(_strip(ast.parse(path.read_text(encoding="utf-8"))))


def _aliases(tree) -> tuple[dict, set, bool]:
    """alias -> lib module, names imported directly as (module, name), whether the code does anything dynamic."""
    alias, direct, dyn = {}, set(), False
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                if (LIB / f"{a.name}.py").exists():
                    alias[a.asname or a.name] = a.name
        elif isinstance(n, ast.ImportFrom) and n.module and (LIB / f"{n.module}.py").exists():
            for a in n.names:
                direct.add((n.module, None if a.name == "*" else a.name))
        elif isinstance(n, ast.Call):
            f = n.func
            name = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) and f.attr == "import_module" else "")
            if name == "__import__" and n.args and isinstance(n.args[0], ast.Constant):      # __import__("looks") is static
                if (LIB / f"{n.args[0].value}.py").exists():
                    direct.add((n.args[0].value, None))
                continue
            dyn |= name in _DYNAMIC
    return alias, direct, dyn


def _uses(node, alias: dict) -> set:
    """(module, name) pairs a node reads through a module alias; (module, None) when the module object itself escapes."""
    found, bases = set(), set()
    for n in ast.walk(node):
        if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id in alias:
            found.add((alias[n.value.id], n.attr))
            bases.add(id(n.value))
    for n in ast.walk(node):
        if isinstance(n, ast.Name) and n.id in alias and id(n) not in bases and isinstance(n.ctx, ast.Load):
            found.add((alias[n.id], None))
    return found


def _module(name: str):
    if name not in _cache:
        tree = _strip(ast.parse((LIB / f"{name}.py").read_text(encoding="utf-8")))
        defs = {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
        body = [n for n in tree.body if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
        alias, direct, dyn = _aliases(tree)
        _cache[name] = (tree, defs, body, alias, direct, dyn)
    return _cache[name]


def _local_refs(node, defs: dict) -> set:
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name) and n.id in defs}


def closure(script: Path) -> tuple[dict, bool]:
    """{module: set of top-level names, or None for the whole module}, dynamic flag."""
    tree = _strip(ast.parse(script.read_text(encoding="utf-8")))
    alias, direct, dyn = _aliases(tree)
    want: dict = {m: None for m in CORE}
    todo = list(_uses(tree, alias) | direct)

    def add(mod, name):
        nonlocal dyn
        if want.get(mod, "x") is None and mod in want:
            return
        if name is None:
            want[mod] = None
        else:
            s = want.setdefault(mod, set())
            if name in s:
                return
            s.add(name)
        _, defs, body, al, dr, d = _module(mod)
        dyn |= d
        nodes = list(defs.values()) if name is None else ([defs[name]] if name in defs else [])
        if name is None or mod not in _seen_body:
            _seen_body.add(mod)
            nodes += body                                  # module-level code runs on import, so what it references counts
            todo.extend(dr)
        for nd in nodes:
            todo.extend(_uses(nd, al))
            todo.extend((mod, r) for r in _local_refs(nd, defs))
    _seen_body: set = set()
    for m in CORE:
        add(m, None)
    while todo:
        add(*todo.pop())
    return want, dyn


def lib_digest(want: dict) -> str:
    h = hashlib.sha256()
    for mod in sorted(want):
        _, defs, body, *_ = _module(mod)
        h.update(mod.encode())
        h.update(ast.dump(ast.Module(body=body, type_ignores=[])).encode())
        for n in sorted(defs if want[mod] is None else (want[mod] & defs.keys())):
            h.update(n.encode())
            h.update(ast.dump(defs[n]).encode())
    return h.hexdigest()


def fresh():
    """Forget parsed libraries (tests edit them between calls)."""
    _cache.clear()
