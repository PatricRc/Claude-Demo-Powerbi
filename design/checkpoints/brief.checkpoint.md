# brief.md (checkpoint) · Nómina AndinaTech

> Checkpoint de respaldo para la demo. En vivo, Claude Code genera `data/demo-nomina/brief.md` desde la transcripción
> y los 3 CSV. Si en el escenario tarda o falla, se abre este archivo. Gus Bavia, Ep. 01: *Data first. Pixels later.*
> *Cuando Power BI se abre, el dashboard ya existe.*

## A) Preguntas que el tablero debe responder

1. ¿Cerramos el mes dentro del presupuesto de nómina?
2. ¿Qué departamento explica el sobrecosto y desde cuándo?
3. ¿El sobrecosto viene de más personas o de más costo por persona (horas extra, bonos)?
4. ¿Por qué la nómina se dispara en julio y diciembre?
5. ¿Cuánto costaron las liquidaciones del año?
6. ¿Cuánta rotación es voluntaria y cuánta involuntaria, y por qué se van?
7. ¿Cómo se relaciona el costo con la evaluación de desempeño trimestral?

## B) Auditoría de datos crudos

| Archivo | Grano | Filas | Llave | Rango |
|---|---|---|---|---|
| `dim_empleados.csv` | 1 fila por empleado | 160 | `id_empleado` | ingresos y ceses hasta 2026-10 |
| `hechos_nomina_mensual.csv` | 1 fila por empleado-mes | 1,839 | `id_nomina` | 2025-11 a 2026-10 |
| `presupuesto_departamentos.csv` | 1 fila por departamento-mes | 72 | `id_presupuesto` | 2025-11 a 2026-10 |

- Moneda: PEN en todas las filas. `costo_total_nomina` = sueldo + horas extra + bono + gratificación + liquidación + aportes.
- El presupuesto está a nivel departamento-mes: se compara con la nómina sumada por departamento y mes, nunca por empleado.
- Anclas verificadas en Python (`checks/anchors.py`): costo S/ 23,098,225.79 · presupuesto S/ 23,105,910.00 · variación S/ −7,684.21 · Operaciones +S/ 68,460.04.

**Se pueden responder:** 1, 2, 3, 4, 5.

**No se pueden responder con estos CSV (decirlo en voz alta):**
- **6.** No hay campo de motivo de salida ni tipo de cese (voluntario / involuntario). Solo `fecha_cese` y `estado`.
- **7.** No hay evaluación de desempeño trimestral. `bono_desempeno` es un monto pagado, no una calificación.

## C) Tokens bloqueados (una paleta, dos motores)

Fuente única: `design/tokens/tokens.json` → `tokens.css` (HTML) + `andinatech-theme.json` (Power BI) + `dax/_tokens.dax`.
Rojo `#B23A3A` = sobrecosto · Verde `#2A7349` = ahorro · Acento azul `#2F5D8A` · Gratificación dorado `#9A6B1F`.
Fuentes del sistema (Georgia + Segoe UI) porque HTML Content Secure bloquea fuentes web. Detalle en `design/DESIGN.md`.

## D) Wireframe

Ver `design/wireframe/wireframe.md`: una página 1280×720, tarjeta héroe HTML, 2 tarjetas nativas,
barras real vs presupuesto por departamento, tendencia mensual con los picos de julio y diciembre, slicers de departamento y período.

## E) Escenas

| Escena | Qué debe probar |
|---|---|
| Tarjeta héroe | A nivel empresa cerramos S/ 7.7 mil por debajo del presupuesto, pero el consolidado esconde un problema. |
| Real vs presupuesto por departamento | Operaciones es el que se pasa: +S/ 68.5 mil en el año. |
| Tendencia mensual | Julio y diciembre suben por gratificación, no por contrataciones; ago–oct se ponen en rojo por horas extra de Operaciones. |
| Headcount vs planificado | Si el sobrecosto viene de tener más gente que lo planificado (verificar con la medida antes de afirmarlo). |
| Costo por empleado | El costo por persona en Tecnología sube después del aumento de abril. |
