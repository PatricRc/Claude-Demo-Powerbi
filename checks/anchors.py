"""PASS/FAIL anchors for the AndinaTech payroll kit.

Run before the demo and after any data change:
    python3 checks/anchors.py

Every number the dashboard shows must match one of these anchors first.
The DAX probes in dax/_probes.dax ask the semantic model for the same values.
"""
import csv
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "demo-nomina"

EXPECTED = {
    "empleados_unicos": 160,
    "filas_nomina": 1839,
    "filas_presupuesto": 72,
    "costo_total_nomina": 23098225.79,
    "presupuesto_total": 23105910.00,
    "variacion_total": -7684.21,
    "pago_horas_extra": 369633.84,
    "bono_desempeno": 510140.00,
    "gratificacion": 2668844.00,
    "monto_liquidacion": 52614.80,
    "aportes_empleador": 2283799.15,
    "sobrecosto_operaciones": 68460.04,
}


def read(name):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    emp = read("dim_empleados.csv")
    nom = read("hechos_nomina_mensual.csv")
    pre = read("presupuesto_departamentos.csv")

    total = lambda rows, col: round(sum(float(r[col]) for r in rows), 2)
    dept_of = {e["id_empleado"]: e["departamento"] for e in emp}

    costo_dep = defaultdict(float)
    for r in nom:
        costo_dep[dept_of[r["id_empleado"]]] += float(r["costo_total_nomina"])
    pres_dep = defaultdict(float)
    for r in pre:
        pres_dep[r["departamento"]] += float(r["presupuesto_nomina"])
    variacion_dep = {d: round(costo_dep[d] - pres_dep[d], 2) for d in pres_dep}
    peor = max(variacion_dep, key=variacion_dep.get)

    actual = {
        "empleados_unicos": len({e["id_empleado"] for e in emp}),
        "filas_nomina": len(nom),
        "filas_presupuesto": len(pre),
        "costo_total_nomina": total(nom, "costo_total_nomina"),
        "presupuesto_total": total(pre, "presupuesto_nomina"),
        "variacion_total": round(total(nom, "costo_total_nomina") - total(pre, "presupuesto_nomina"), 2),
        "pago_horas_extra": total(nom, "pago_horas_extra"),
        "bono_desempeno": total(nom, "bono_desempeno"),
        "gratificacion": total(nom, "gratificacion"),
        "monto_liquidacion": total(nom, "monto_liquidacion"),
        "aportes_empleador": total(nom, "aportes_empleador"),
        "sobrecosto_operaciones": variacion_dep.get("Operaciones"),
    }

    failures = 0
    for key, expected in EXPECTED.items():
        ok = abs(actual[key] - expected) < 0.005
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {key:<24} esperado {expected:>16,.2f}  real {actual[key]:>16,.2f}")
    print(f"{'PASS' if peor == 'Operaciones' else 'FAIL'}  departamento con mayor sobrecosto: {peor}")
    failures += peor != "Operaciones"
    print("\nOVERALL:", "PASS" if failures == 0 else f"FAIL ({failures})")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
