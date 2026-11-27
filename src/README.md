# src/ · proyecto Power BI (PBIP)

Aquí aterrizan el modelo y el reporte como archivos, igual que `src/Model` y `src/Report` en *The World of Peaches*.
Se crean en los pasos 6 y 7, **después** de que existen el brief, los tokens, el wireframe y los componentes.

```
src/
├── NominaAndinaTech.SemanticModel/   TMDL: tablas, relaciones, _Measures (desde dax/)
└── NominaAndinaTech.Report/          PBIR: definition/report.json, páginas, visuales, tema (desde design/theme/)
```

- Modelo: **Import** (no Direct Lake), `Departamentos` filtra `Empleados → Nomina` y `Presupuesto`, tabla `Calendario` marcada como tabla de fechas, sin auto fecha/hora.
- Medidas: en `_Measures`, carpetas por página (`00 Base`, `01 Personas`, `02 Componentes del costo`, `Page 1 - Componentes`).
- Reporte: un visual por rectángulo de `design/wireframe/wireframe.md`. HTML Content **Secure** registrado en `publicCustomVisuals`.
- Se baja con `getDefinition` y se sube con `updateDefinition` (Fabric REST) o con el Power BI MCP hospedado.
