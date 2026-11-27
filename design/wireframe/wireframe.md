# Wireframe · Página 1 · Cierre de nómina (1280×720)

Pregunta de la página: **¿Cerramos el mes dentro del presupuesto de nómina, y si no, dónde y por qué?**

```
0        228 272                                                  1250 1280
┌─────────┬──────────────────────────────────────────────────────────┐ 0
│ ANDINA  │ AndinaTech S.A.C. — Nómina (Georgia 32)  [Depto ▾] [Período ▾]│ slicers y53
│ TECH    │ Cierre de mes · datos de demostración · soles (PEN)          │
│         │ ─────────────── regla accent (y≈115) ─────────────────────── │
│ Cierre  │ ┌───────── A ─────────┐ ┌──── B ────┐ ┌──── C ─────┐          │ 140
│ de mes  │ │ COSTO TOTAL NÓMINA  │ │ HEADCOUNT │ │ COSTO POR  │          │
│         │ │ S/ 23.10 M          │ │ (valor)   │ │ EMPLEADO   │          │
│         │ │ −S/ 7.7 mil vs ppto │ │ vs plan   │ │ (valor)    │          │
│         │ │ pista: horas extra  │ │           │ │            │          │
│ Cómo    │ └─────────────────────┘ └───────────┘ └────────────┘          │ 330
│ leer    │ ┌───────── D ─────────┐ ┌───────────── E ───────────────┐     │ 350
│         │ │ Real vs presupuesto │ │ Costo mensual vs presupuesto  │     │
│         │ │ por departamento    │ │ (picos jul y dic = gratific.) │     │
│ Datos   │ │ (barras)            │ │ (columnas + línea)            │     │
│ ficticios│└─────────────────────┘ └───────────────────────────────┘     │ 690
└─────────┴──────────────────────────────────────────────────────────┘ 720
```

## Rectángulos (x, y, w, h)

| Id | Visual | Tipo | x, y, w, h | Qué debe probar |
|---|---|---|---|---|
| — | Barra lateral, título, regla | Imagen de fondo (2560×1440, Fit) | 0, 0, 1280, 720 | — |
| S1 | Departamento | Slicer nativo (dropdown) | 952, 53, 140, 40 | — |
| S2 | Período | Slicer nativo (dropdown) | 1105, 53, 145, 40 | — |
| A | Tarjeta héroe | HTML Content Secure ← `[KPI Card HTML]` | 272, 140, 470, 190 | Si el mes cerró dentro del presupuesto y la causa principal |
| B | Headcount vs planificado | Tarjeta nativa | 758, 140, 236, 190 | Si el sobrecosto viene de más gente o no |
| C | Costo por empleado | Tarjeta nativa | 1010, 140, 240, 190 | El efecto del aumento de abril en Tecnología |
| D | Real vs presupuesto por departamento | Barras agrupadas | 272, 350, 470, 340 | Que Operaciones es el único departamento con sobrecosto relevante |
| E | Costo mensual vs presupuesto | Columnas + línea | 758, 350, 492, 340 | Que julio y diciembre suben por gratificación, no por contrataciones |

Reglas: gutters de 16 px, margen derecho 30 px, una tarjeta oscura como máximo, visuales sin título (el tema los apaga).
