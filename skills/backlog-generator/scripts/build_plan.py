#!/usr/bin/env python3
"""Valida backlog.json y genera plan.xlsx con olas paralelas y camino crítico.

Uso: python3 build_plan.py backlog.json plan.xlsx [--check]

  --check   solo valida (no requiere openpyxl). Código de salida 1 si hay errores.

Unidad de trabajo = tarea `module` (con sus subtareas) o tarea suelta (parent null).
Las olas se calculan entre unidades: dentro de un módulo el orden es secuencial
en la misma rama, así que no aporta paralelismo.
"""
import json
import sys
from collections import defaultdict

AREA_ORDER = {"db": 0, "backend": 1, "frontend": 2, "tests": 3}


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def validate(data):
    errors, warnings = [], []
    tasks = data.get("tasks", [])
    by_key = {}
    for t in tasks:
        k = t.get("key")
        if k in by_key:
            errors.append(f"{k}: key duplicada")
        by_key[k] = t

    for t in tasks:
        k, typ, area = t["key"], t["type"], t["area"]
        parent = t.get("parent")

        # Repo único (o ninguno solo en diseño)
        if area == "design":
            if t["repo"] is not None:
                warnings.append(f"{k}: diseño con repo; dev-flow no ejecuta tareas de diseño")
            if parent:
                errors.append(f"{k}: el diseño es tarea suelta, no subtarea de un módulo")
        elif not t["repo"]:
            errors.append(f"{k}: tarea ejecutable sin repo (exactamente uno)")

        if typ == "module":
            if area != "module" or parent:
                errors.append(f"{k}: un module tiene area 'module' y parent null")
        else:
            # Estándar de definición
            if len(t["acceptance"]) < 2:
                errors.append(f"{k}: mínimo 2 criterios de aceptación")
            if len(t["out_of_scope"]) < 1:
                errors.append(f"{k}: falta 'fuera de alcance'")
            if area != "design" and len(t["tests"]) < 1:
                errors.append(f"{k}: faltan pruebas")
            if area in ("backend", "frontend") and not t.get("contract"):
                warnings.append(f"{k}: {area} sin contrato")
            if typ == "bug":
                r = t.get("repro") or {}
                if not (r.get("steps") and r.get("actual") and r.get("expected")):
                    errors.append(f"{k}: bug sin pasos / actual / esperado")
                if len(t["tests"]) != 1:
                    errors.append(f"{k}: un bug lleva exactamente una prueba de regresión")
            if t.get("estimate_h", 0) > 8:
                warnings.append(f"{k}: {t['estimate_h']} h — considera partirla")

        if parent:
            p = by_key.get(parent)
            if not p or p["type"] != "module":
                errors.append(f"{k}: parent {parent} no existe o no es module")
            elif p["repo"] != t["repo"]:
                errors.append(f"{k}: repo distinto al de su módulo {parent}")
            for d in t["depends_on"]:
                if by_key.get(d, {}).get("parent") == parent:
                    warnings.append(f"{k}: depende de {d} del mismo módulo; el orden ya es implícito")

        for d in t["depends_on"]:
            if d not in by_key:
                errors.append(f"{k}: depende de {d}, que no existe")

    # Subtareas: orden por área y `tests` al final
    children = defaultdict(list)
    for t in tasks:
        if t.get("parent"):
            children[t["parent"]].append(t)
    for mk, subs in children.items():
        areas = [s["area"] for s in subs]
        if areas[-1] != "tests":
            errors.append(f"{mk}: la última subtarea debe ser area 'tests'")
        ranks = [AREA_ORDER.get(a, 9) for a in areas]
        if ranks != sorted(ranks):
            warnings.append(f"{mk}: subtareas fuera del orden db → backend → frontend → tests")
    for t in tasks:
        if t["type"] == "module" and t["key"] not in children:
            errors.append(f"{t['key']}: módulo sin subtareas")

    # Cobertura del MVP: cada RF/RNF declarado en mvp_rf aparece en alguna tarea
    covered = {r for t in tasks for r in t.get("rf", [])}
    missing = [r for r in data.get("mvp_rf", []) if r not in covered]
    if missing:
        errors.append(f"requerimientos del MVP sin tarea: {', '.join(missing)}")
    elif "mvp_rf" not in data:
        warnings.append("sin mvp_rf: no se puede verificar que el MVP quede cubierto")

    return errors, warnings, by_key, children


def units(tasks, by_key, children):
    """Agrupa en unidades de trabajo con dependencias externas y horas."""
    def unit_of(key):
        t = by_key[key]
        return t.get("parent") or key

    top = {t["key"] for t in tasks if not t.get("parent")}
    result = {}
    for t in tasks:
        if t.get("parent"):
            continue
        k = t["key"]
        members = [t] + children.get(k, [])
        deps = set()
        for m in members:
            for d in m["depends_on"]:
                if d in by_key and unit_of(d) != k and unit_of(d) in top:
                    deps.add(unit_of(d))
        hours = sum(m.get("estimate_h", 0) for m in members)
        result[k] = {"task": t, "deps": sorted(deps), "hours": hours, "n": len(members)}
    return result


def waves(us):
    """Nivel topológico + camino crítico (en horas). Lanza ValueError si hay ciclo."""
    level, finish, prev = {}, {}, {}
    state = {}

    def visit(k):
        if state.get(k) == 1:
            raise ValueError(f"ciclo de dependencias que pasa por {k}")
        if state.get(k) == 2:
            return
        state[k] = 1
        lv, start, best = 0, 0.0, None
        for d in us[k]["deps"]:
            visit(d)
            lv = max(lv, level[d] + 1)
            if finish[d] > start:
                start, best = finish[d], d
        level[k], finish[k], prev[k] = lv, start + us[k]["hours"], best
        state[k] = 2

    for k in us:
        visit(k)
    end = max(finish, key=finish.get)
    path = []
    while end:
        path.append(end)
        end = prev[end]
    return level, finish, list(reversed(path))


def write_xlsx(data, us, level, finish, critical, by_key, out):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.utils import get_column_letter

    head_font = Font(bold=True, color="FFFFFF")
    head_fill = PatternFill("solid", fgColor="1E00B4")
    crit_fill = PatternFill("solid", fgColor="E3F4FB")

    def sheet(ws, headers, rows, widths):
        ws.append(headers)
        for c in ws[1]:
            c.font, c.fill = head_font, head_fill
        for r in rows:
            ws.append(r)
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions

    wb = Workbook()
    ws = wb.active
    ws.title = "Plan"
    order = sorted(us, key=lambda k: (level[k], k))
    rows = []
    for k in order:
        u, t = us[k], us[k]["task"]
        rows.append([level[k] + 1, k, t["title"], t["area"], t["repo"] or "—", t["module"],
                     u["n"], u["hours"], ", ".join(u["deps"]) or "—",
                     finish[k], "Sí" if k in critical else ""])
    sheet(ws, ["Ola", "Unidad", "Título", "Área", "Repo", "Módulo", "Tareas", "Horas",
               "Depende de", "Fin acumulado (h)", "Camino crítico"],
          rows, [6, 12, 44, 10, 26, 22, 8, 8, 22, 16, 14])
    for row in ws.iter_rows(min_row=2):
        if row[10].value == "Sí":
            for c in row:
                c.fill = crit_fill

    ws2 = wb.create_sheet("Tareas")
    rows = []
    for t in data["tasks"]:
        unit = t.get("parent") or t["key"]
        rows.append([level[unit] + 1, t["key"], t.get("parent") or "", t["type"], t["area"],
                     t["title"], t["repo"] or "—", t.get("estimate_h", ""),
                     ", ".join(t["depends_on"]), ", ".join(t.get("rf", [])),
                     "\n".join(t["acceptance"]), "\n".join(t["out_of_scope"]),
                     "\n".join(t["tests"])])
    sheet(ws2, ["Ola", "Key", "Módulo padre", "Tipo", "Área", "Título", "Repo", "Horas",
                "Depende de", "RF", "Criterios", "Fuera de alcance", "Pruebas"],
          rows, [6, 12, 12, 9, 10, 44, 26, 7, 18, 14, 50, 36, 36])
    for row in ws2.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")

    ws3 = wb.create_sheet("Olas")
    by_wave = defaultdict(list)
    for k in us:
        by_wave[level[k]].append(k)
    rows = []
    for lv in sorted(by_wave):
        ks = sorted(by_wave[lv])
        rows.append([lv + 1, len(ks), ", ".join(ks), sum(us[k]["hours"] for k in ks),
                     max(us[k]["hours"] for k in ks)])
    sheet(ws3, ["Ola", "Unidades en paralelo", "Unidades", "Horas totales", "Horas de la más larga"],
          rows, [6, 20, 60, 14, 22])
    ws3.append([])
    ws3.append(["Camino crítico", " → ".join(critical)])
    ws3.append(["Duración mínima (h)", max(finish.values())])

    wb.save(out)


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    data = load(argv[1])
    errors, warnings, by_key, children = validate(data)
    us = units(data["tasks"], by_key, children)
    try:
        level, finish, critical = waves(us) if us else ({}, {}, [])
    except ValueError as e:
        errors.append(str(e))

    for w in warnings:
        print(f"ADVERTENCIA  {w}")
    for e in errors:
        print(f"ERROR        {e}")
    if errors:
        print(f"\n{len(errors)} error(es). Corrige backlog.json y vuelve a ejecutar.")
        return 1

    n_waves = max(level.values()) + 1
    total = sum(u["hours"] for u in us.values())
    print(f"OK — {len(data['tasks'])} tareas, {len(us)} unidades, {n_waves} olas, {total:g} h")
    print(f"Camino crítico: {' → '.join(critical)} ({max(finish.values()):g} h)")

    if "--check" not in argv and len(argv) >= 3:
        write_xlsx(data, us, level, finish, critical, by_key, argv[2])
        print(f"Plan escrito en {argv[2]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
