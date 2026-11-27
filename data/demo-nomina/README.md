# Kit de datos · AndinaTech S.A.C. (ficticio)

Datos **sintéticos** de nómina para la demo. No contienen datos reales de personas ni de empresas.
Se pueden publicar con *Publish to web* porque son ficticios; nunca uses este flujo con datos reales.

| Archivo | Grano | Filas |
|---|---|---|
| `dim_empleados.csv` | 1 fila por empleado | 160 |
| `hechos_nomina_mensual.csv` | 1 fila por empleado-mes | 1,839 |
| `presupuesto_departamentos.csv` | 1 fila por departamento-mes | 72 |

Moneda PEN. Períodos 2025-11 a 2026-10.

Los 3 CSV ya están cargados en el Lakehouse de Fabric (`Files/demo/nomina/`). El modelo semántico es **Import**.

## Falta en esta carpeta

- `transcripcion_reunion_nomina.md`: la transcripción de la reunión con el comité. Es la entrada del paso 1 (brief).
  Cópiala aquí antes de la demo.
- `brief.md`: lo genera Claude Code en vivo. El respaldo está en `design/checkpoints/brief.checkpoint.md`.

## Verificar

```bash
python3 checks/anchors.py
```
