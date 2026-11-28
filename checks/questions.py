"""Expected answers for the brief's questions, computed in Python from the raw CSVs.

Run: python3 checks/questions.py
These are the values dax/_probes-preguntas.dax checks the DAX measures against.
Grain notes: Nomina is one row per employee-month (verified below); Presupuesto is one row per department-month.
"""
import csv
import collections
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "demo-nomina"
F = float


def load(name):
    with open(DATA / name, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


nomina = load("hechos_nomina_mensual.csv")
presupuesto = load("presupuesto_departamentos.csv")
empleados = {r["id_empleado"]: r for r in load("dim_empleados.csv")}

# Grain check: one payroll row per employee-month
dups = [k for k, v in collections.Counter((r["id_empleado"], r["periodo"]) for r in nomina).items() if v > 1]
assert not dups, f"Nomina is not one row per employee-month: {dups[:3]}"

meses = sorted({r["periodo"] for r in presupuesto})
deps = sorted({r["departamento"] for r in presupuesto})

real = collections.defaultdict(float)
for r in nomina:
    real[(empleados[r["id_empleado"]]["departamento"], r["periodo"])] += F(r["costo_total_nomina"])
plan = {(r["departamento"], r["periodo"]): F(r["presupuesto_nomina"]) for r in presupuesto}
hc_plan = {(r["departamento"], r["periodo"]): int(r["headcount_planificado"]) for r in presupuesto}

costo_mes = {m: sum(real[(d, m)] for d in deps) for m in meses}
ppto_mes = {m: sum(plan[(d, m)] for d in deps) for m in meses}
var_mes = {m: costo_mes[m] - ppto_mes[m] for m in meses}

out = []


def show(name, value):
    out.append((name, value))
    if isinstance(value, float):
        print(f"{name:<44} {value:>18,.2f}")
    else:
        print(f"{name:<44} {value!s:>18}")


print("== P1 ¿Cerramos dentro del presupuesto?")
show("Variación vs Presupuesto (total)", sum(var_mes.values()))
show("Meses en Sobrecosto (empresa)", sum(1 for v in var_mes.values() if v > 0))
show("Departamentos en Sobrecosto (total)",
     sum(1 for d in deps if sum(real[(d, m)] - plan[(d, m)] for m in meses) > 0))
show("Sobrecosto Bruto (solo depto-mes > 0)",
     sum(max(0.0, real[(d, m)] - plan[(d, m)]) for d in deps for m in meses))

print("== P2 ¿Qué departamento y desde cuándo?")
var_dep = {d: sum(real[(d, m)] - plan[(d, m)] for m in meses) for d in deps}
top = max(var_dep, key=var_dep.get)
show("Departamento Mayor Sobrecosto", top)
show("Sobrecosto Mayor Departamento", var_dep[top])
show(f"Primer Mes en Sobrecosto ({top})", min(m for m in meses if real[(top, m)] - plan[(top, m)] > 0))
show("Primer Mes en Sobrecosto (empresa)", min(m for m in meses if var_mes[m] > 0))

print("== P3 ¿Más personas o más costo por persona?")
pm_real = len(nomina)
pm_plan = sum(hc_plan.values())
cpp_real = sum(costo_mes.values()) / pm_real
cpp_plan = sum(ppto_mes.values()) / pm_plan
vol = (pm_real - pm_plan) * cpp_plan
pre = (cpp_real - cpp_plan) * pm_real
show("Personas-Mes Real", pm_real)
show("Personas-Mes Plan", pm_plan)
show("Costo por Persona-Mes Real", cpp_real)
show("Costo por Persona-Mes Plan", cpp_plan)
show("Efecto Volumen", vol)
show("Efecto Costo por Persona", pre)
assert abs((vol + pre) - sum(var_mes.values())) < 0.01, "volume + price must equal the variance"

print("== P4 ¿Por qué julio y diciembre?")
grat_mes = collections.defaultdict(float)
for r in nomina:
    grat_mes[r["periodo"]] += F(r["gratificacion"])
for m in ("2025-12", "2026-06", "2026-07"):
    show(f"Costo Total Nómina {m}", costo_mes[m])
    show(f"Gratificación {m}", grat_mes[m])
    show(f"Costo sin Gratificación {m}", costo_mes[m] - grat_mes[m])
hc_mes = collections.Counter(r["periodo"] for r in nomina)
show("Headcount 2026-06", hc_mes["2026-06"])
show("Headcount 2026-07", hc_mes["2026-07"])
show("Variación MoM 2026-07", costo_mes["2026-07"] - costo_mes["2026-06"])

print("== P5 ¿Cuánto costaron las liquidaciones?")
liq = sum(F(r["monto_liquidacion"]) for r in nomina)
ceses = [e for e in empleados.values() if e["fecha_cese"] and meses[0] <= e["fecha_cese"][:7] <= meses[-1]]
show("Monto Liquidación", liq)
show("Ceses", len(ceses))
show("Liquidación Promedio por Cese", liq / len(ceses))
altas = [e for e in empleados.values() if meses[0] <= e["fecha_ingreso"][:7] <= meses[-1]]
show("Altas (ingresos en el período)", len(altas))

print("== Time intelligence")
ytd_2026 = [m for m in meses if m.startswith("2026")]
show("Costo YTD a 2026-10", sum(costo_mes[m] for m in ytd_2026))
show("Presupuesto YTD a 2026-10", sum(ppto_mes[m] for m in ytd_2026))
show("Costo Últimos 12 Meses a 2026-10", sum(costo_mes.values()))
show("Costo Q3 2026 (jul-sep)", sum(costo_mes[m] for m in ("2026-07", "2026-08", "2026-09")))
show("Promedio Móvil 3M a 2026-10", sum(costo_mes[m] for m in ("2026-08", "2026-09", "2026-10")) / 3)
acum = 0.0
peor = (None, 0.0)
for m in meses:
    acum += var_mes[m]
    if acum < peor[1]:
        peor = (m, acum)
show("Variación Acumulada a 2026-10", acum)
show("Variación Acumulada mínima (mes)", peor[0])
show("Variación Acumulada mínima", peor[1])
