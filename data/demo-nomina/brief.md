# Brief · Dashboard de nómina AndinaTech S.A.C. (ficticio)

**Fuentes:** `transcripcion_reunion_nomina.md` (kickoff del 10 nov 2026) y los CSV `dim_empleados.csv` (160 filas), `hechos_nomina_mensual.csv` (1,839 filas) y `presupuesto_departamentos.csv` (72 filas). Moneda PEN, períodos 2025-11 a 2026-10.
**Método:** Gus Bavia, *Data first. Pixels later.* Este documento no contiene TMDL, DAX ni PBIR.
**Estado:** borrador para revisión. Las secciones 2, 3 y 8 tienen preguntas abiertas que requieren decisión humana.

---

## 1. Objetivo en una frase

El comité ejecutivo de cierre de mes usa el tablero para decidir si la variación de la planilla contra presupuesto, sobre todo en Operaciones, se corrige con contrataciones o se sigue pagando con horas extra, sin reconciliar cuatro o cinco Excel.

---

## 2. Preguntas de negocio

Las ocho preguntas salen de la transcripción. La columna *Pidió* indica quién las planteó. Las marcadas como **v1** son las cinco que el tablero responde en su primera versión.

| # | Pregunta | Pidió | Prioridad |
|---|---|---|---|
| P1 | ¿Cuál fue el costo total de nómina del mes y cómo viene en el año, en soles? | Sofía Mendoza (CFO); Patricio la resume en la reunión | **v1** |
| P2 | ¿Cómo vamos real versus presupuesto, por departamento y en el consolidado? ¿Qué pasa en Operaciones en los meses recientes? | Sofía Mendoza; Diego Quispe | **v1** |
| P3 | ¿Por qué se movió el costo contra el mes anterior o contra lo esperado: gratificación, horas extra, bonos, liquidaciones o sueldo base? | Sofía Mendoza | **v1** |
| P4 | ¿Cuánto pesan las horas extra sobre el costo y en qué área se concentran? | Diego Quispe | **v1** |
| P5 | ¿Cómo está el headcount real versus el planificado? | Carlos Paredes (People) | **v1** |
| P6 | ¿Dónde se concentran los bonos de desempeño? Ej. Comercial. | Carlos Paredes | v2 · Sofía pidió bonos en una vista propia (ver pregunta abierta A3) |
| P7 | ¿Cuál es el costo por empleado, sobre todo en Tecnología, y cómo evoluciona? | Carlos Paredes | v2 |
| P8 | ¿Quiénes cesaron, en qué mes y cuánto costó su liquidación? | Patricio (resumen de la reunión) | v2 · el monto total de liquidaciones sí aparece en P3 |

**Fuera de alcance del informe (lo dijo el propio cliente):**
- Tasa de rotación voluntaria versus involuntaria, y motivo de salida. Viven en formularios de offboarding que no están en la planilla.
- Cruce del costo con la evaluación de desempeño trimestral. Vive en otra herramienta.

---

## 3. Auditoría de datos crudos

Para cada pregunta, la tabla y columnas que la responden. *Sí* significa que se responde con los CSV; *Parcial* significa que tiene un límite que se muestra en el tablero; *No se puede responder con estos datos* significa que falta un dato.

| Pregunta | Tabla · columnas | ¿Responde? | Notas |
|---|---|---|---|
| P1 Costo total del mes y del año | `hechos_nomina_mensual`: `costo_total_nomina`, `periodo`, `anio`, `mes`. `presupuesto_departamentos`: `presupuesto_nomina` | **Sí** | Costo total y presupuesto suman casi lo mismo en el año. Ver sección 4. |
| P2 Real vs presupuesto por departamento | `hechos_nomina_mensual.costo_total_nomina` + `dim_empleados.departamento` (vía `id_empleado`). `presupuesto_departamentos`: `departamento`, `presupuesto_nomina`, `periodo` | **Sí** | `hechos` no tiene departamento: se toma de `dim_empleados`, que guarda solo el departamento actual (ver riesgo R2). |
| P3 Qué mueve el costo (componentes) | `hechos_nomina_mensual`: `sueldo_base`, `pago_horas_extra`, `bono_desempeno`, `gratificacion`, `monto_liquidacion`, `aportes_empleador` | **Sí** para la composición del costo real. **Parcial** para la variación contra presupuesto. | El presupuesto solo tiene `presupuesto_nomina` (total) y `presupuesto_horas_extra`. **No se puede responder con estos datos:** cuánto de la desviación es sueldo base, bono, gratificación o liquidación, porque no hay presupuesto por componente. Solo horas extra tiene su propio presupuesto. |
| P3 Efecto headcount en el costo | `hechos_nomina_mensual`: `id_empleado` (conteo por `periodo`) vs `presupuesto_departamentos.headcount_planificado` | **Sí** | Ver pregunta abierta A2 sobre la definición de headcount real. |
| P4 Peso de horas extra y área | `hechos_nomina_mensual.pago_horas_extra` / `costo_total_nomina`; `presupuesto_departamentos.presupuesto_horas_extra`; `departamento` | **Sí** | `horas_extra` (horas) y `pago_horas_extra` (soles) son columnas distintas. Se usa la segunda. |
| P5 Headcount real vs plan | `hechos_nomina_mensual` (conteo de `id_empleado`) vs `presupuesto_departamentos.headcount_planificado` | **Sí** | Mismo supuesto de definición que P3 (A2). |
| P6 Bonos de desempeño por área | `hechos_nomina_mensual.bono_desempeno` + `departamento` | **Sí** | Comercial concentra el bono. El presupuesto no tiene bonos, así que no hay comparación. |
| P7 Costo por empleado | `hechos_nomina_mensual.costo_total_nomina` / conteo de `id_empleado` | **Sí** | Las gratificaciones (jul y dic) distorsionan el promedio: hay que mostrarlo con y sin gratificación. |
| P8 Ceses y liquidación | `dim_empleados`: `estado`, `fecha_ingreso`, `fecha_cese`; `hechos_nomina_mensual`: `tipo_registro` = "Liquidación", `monto_liquidacion` | **Sí** | Solo hay 2 ceses. Mostrar nombres de personas es un tema de privacidad (A5). |
| Rotación voluntaria vs involuntaria | — | **No se puede responder con estos datos** | Falta: un campo `tipo_rotacion` y un campo `motivo_salida` integrados desde los formularios de offboarding. |
| Motivo de salida | — | **No se puede responder con estos datos** | Falta: `motivo_salida` integrado a la planilla. |
| Bono vs desempeño trimestral | — | **No se puede responder con estos datos** | Falta: una exportación de evaluaciones de desempeño con `id_empleado`, período y calificación. |

**Lo que los CSV muestran y no dicen:**
- No dicen por qué una persona salió. Solo dicen en qué mes dejó de aparecer.
- No dicen qué parte de la desviación contra presupuesto es de una causa concreta, salvo horas extra.

---

## 4. Anclas de validación

Cifras calculadas en Python desde los CSV, con la misma lógica de la sección 2. Estas son las cifras que el modelo debe reproducir. Coinciden con las constantes de `checks/anchors.py`.

| Ancla | Valor exacto (PEN) |
|---|---|
| Costo total de nómina (12 meses, 1,839 filas, 160 empleados) | **23,098,225.79** |
| Presupuesto de nómina total (72 filas) | **23,105,910.00** |
| Variación real − presupuesto | **−7,684.21** (−0.03 %) |
| Departamento con mayor sobrecosto | **Operaciones: +68,460.04** (+1.36 %; real 5,086,460.04 vs presupuesto 5,018,000.00) |

Cifras adicionales que el tablero usa, todas calculadas desde los CSV:

| Medida | Valor |
|---|---|
| Variación por departamento | Operaciones +68,460.04 · Comercial −3,449.75 · Tecnología −31,969.13 · Finanzas −15,015.15 · Administración −12,850.58 · People −12,859.64 |
| Horas extra pagadas (año) | 369,633.84 = 1.60 % del costo |
| Horas extra de Operaciones (año) | Real 168,408.70 vs presupuesto 79,260.00 · Operaciones explica el 45.6 % de las horas extra pagadas |
| Operaciones, agosto a octubre 2026 | Variación +75,162.50 · horas extra real 124,130.93 vs presupuesto 43,460.00 (+80,670.93) |
| Consolidado, agosto a octubre 2026 | Variación +69,172.21 (el resto de áreas suma −5,990.29) |
| Gratificación | Dic 2025: 1,272,050.00 · Jul 2026: 1,396,794.00 · total 2,668,844.00 |
| Costo de julio 2026 sin gratificación | 1,900,445.68 (vs 3,297,239.68 con gratificación) |
| Bonos de desempeño (año) | 510,140.00 · Comercial 450,930.00 (88.4 %) |
| Bonos de Comercial por nivel | Senior 198,670 · Lead 127,090 · Semi-senior 53,800 · Gerencia 52,290 · Junior 19,080 |
| Liquidaciones (año) | 52,614.80 · 2 casos: Operaciones jun 2026 (18,530.12) y Tecnología sep 2026 (34,084.68) |
| Headcount octubre 2026 | Real 158 vs planificado 157 · Operaciones real 41 vs planificado 40 |
| Aumento salarial Tecnología, abril 2026 | +8.0 % promedio en las 52 personas que estaban en marzo y abril |

**Cuadre con la fuente cargada:** las sumas por año en el SQL endpoint de NominasLakehouse dan 23,098,226 y 23,105,910 en nómina y presupuesto, y las filas son 160 / 1,839 / 72. Coinciden con los CSV.

**Verificación de integridad:** `costo_total_nomina` = suma de sus componentes en las 1,839 filas. Las personas cesadas no aparecen en nómina después de su mes de cese.

---

## 5. Escenas

El dashboard tiene tres páginas. Cada una responde a preguntas de la sección 2. Los títulos son hallazgos provisionales: se reemplazan por los que devuelvan las medidas al probarlas.

### Página 1 · Cierre de mes (Sofía)

- **Responde:** P1, P2 (consolidado), P3 (movimiento mensual).
- **Título (provisional):** "El consolidado cierra a −0.03 % del presupuesto; Operaciones lo supera en S/ 68.5 mil".
- **Visuales:**
  - Cuatro tarjetas: costo del mes, presupuesto del mes, variación (con signo y color), headcount real vs plan.
  - Frase del mes, generada por medida (texto corto, no párrafo).
  - Barras real vs presupuesto por departamento, ordenadas por variación.
  - Columnas de costo mensual, con la gratificación en un color separado (`accent-gold`) para ver jul y dic sin explicarlos de memoria.
- **Medidas:** `Costo total`, `Presupuesto nómina`, `Variación S/`, `Variación %`, `Gratificación`, `Costo sin gratificación`, `Headcount real`, `Headcount planificado`.
- **Filtros:** período (por defecto octubre 2026, ver A1) y departamento.

### Página 2 · Operaciones: horas extra (Diego)

- **Responde:** P2 (Operaciones), P4, P5 (Operaciones).
- **Título (provisional):** "Operaciones superó el presupuesto de agosto a octubre; las horas extra superan toda la brecha".
- **Visuales:**
  - Línea del costo real vs presupuesto de Operaciones, 12 meses.
  - Columnas de horas extra real vs presupuesto, por mes.
  - Línea de horas extra como % del costo de Operaciones, por mes.
  - Headcount real vs plan de Operaciones, por mes.
- **Medidas:** `Costo total` y `Presupuesto nómina` filtrados a Operaciones, `Horas extra pagadas`, `Presupuesto horas extra`, `% horas extra sobre costo`, `Headcount real`, `Headcount planificado`.
- **Filtro:** la página está fija en Operaciones; el filtro de período aplica.

### Página 3 · Qué mueve el costo (Sofía, Diego)

- **Responde:** P3 (composición del costo), P4 (consolidado y por área).
- **Título (provisional):** "El costo sube en jul y dic por la gratificación; en el resto del año sube con horas extra y liquidaciones".
- **Visuales:**
  - Columnas apiladas de costo por componente y mes: sueldo base, horas extra, bono, gratificación, liquidación, aportes.
  - Tabla de horas extra y % del costo por departamento.
- **Medidas:** `Sueldo base`, `Horas extra pagadas`, `Bono desempeño`, `Gratificación`, `Liquidación`, `Aportes empleador`, `% horas extra sobre costo`.
- **Nota:** no se compara la composición contra el presupuesto, porque el presupuesto no tiene componentes (ver sección 3).

**Diferido a v2:** costo por empleado (P7), bonos por nivel en su propio visual (P6) y la lista de ceses (P8).

---

## 6. Tokens de diseño

Los tokens ya existen en `design/tokens/tokens.json` y en `design/DESIGN.md`. Este brief los confirma sin cambiar valores. Para modificarlos se edita `tokens.json` y se corre `python3 design/tokens/build_tokens.py`, que genera el CSS, el tema JSON de Power BI y los tokens DAX.

| Rol | Token | Hex | Uso |
|---|---|---|---|
| Fondo de página | `page` | `#F4F5F7` | Fondo |
| Tarjeta | `card` | `#FFFFFF` | Superficie de tarjetas |
| Texto principal | `ink` | `#1F2A37` | Títulos y números |
| Texto secundario | `sub` | `#4B5563` | Etiquetas |
| Texto de nota | `muted` | `#6B7280` | Ejes y notas |
| Acento (real) | `accent` | `#2F5D8A` | Serie "real" y selección |
| Presupuesto | `accent-2` | `#6E93B8` | Serie "presupuesto" |
| Gratificación | `accent-gold` | `#9A6B1F` | Solo gratificación (jul y dic) |
| Positivo (ahorro) | `good` / `good-bg` | `#2A7349` / `#E8F3EC` | Variación negativa (bajo presupuesto) |
| Negativo (sobrecosto) | `bad` / `bad-bg` | `#B23A3A` / `#F8E9E9` | Variación positiva (sobre presupuesto) |
| Separadores | `divider` / `border` | `#E6E8EC` / `#D2D6DC` | Líneas |
| Barra lateral | `sidebar` → `sidebar-2` | `#1B2430` → `#111821` | Imagen de fondo |

- **Tipografía:** título Georgia 32 px, número héroe Georgia 40 px, número de tarjeta Segoe UI Light 28 px, etiqueta Segoe UI 10 px en mayúsculas, texto Segoe UI 11 px.
- **Espaciado:** ritmo de 8 px, padding 16/24, gaps 8/16. Radio de tarjeta 12 px.
- **Reglas de color:** rojo y verde solo para sobre y bajo presupuesto. El color nunca es la única señal: cada delta lleva signo y texto.

---

## 7. Wireframe anotado

Página 1 · Cierre de mes (grilla 1280×720):

```
+-----------------------------------------------------------------------+
| [Título: hallazgo]                    [Filtro período] [Filtro área]  |
| [Frase del mes: texto generado por medida]                            |
+---------------+---------------+---------------+-----------------------+
| [Costo total] | [Presup.      | [Variación    | [Headcount real /     |
|  del mes      |  nómina]      |  S/ y %]      |  planificado]         |
+-------------------------------+-------------------------------------- +
| [Real vs presupuesto por departamento]    | [Costo mensual con    |
|  Real · Presupuesto · Variación           |  Gratificación en oro]|
+-------------------------------------------+-----------------------+
```

Página 2 · Operaciones: horas extra:

```
+-----------------------------------------------------------------------+
| [Título: hallazgo de Operaciones]                 [Filtro período]    |
+-------------------------------------+---------------------------------+
| [Costo Operaciones real vs pres.]   | [Horas extra real vs pres.]     |
|  Costo total · Presupuesto nómina   |  Horas extra · Pres. horas extra|
+-------------------------------------+---------------------------------+
| [% horas extra sobre costo]         | [Headcount real vs plan]        |
|  % horas extra sobre costo          |  Headcount real · planificado   |
+-------------------------------------+---------------------------------+
```

Página 3 · Qué mueve el costo:

```
+-----------------------------------------------------------------------+
| [Título: hallazgo de composición]                 [Filtro período]    |
+-----------------------------------------------------------------------+
| [Columnas apiladas: costo por componente y mes]                       |
|  Sueldo base · Horas extra · Bono · Gratificación · Liquidación ·     |
|  Aportes empleador                                                    |
+-----------------------------------------------------------------------+
| [Tabla por departamento: horas extra y % del costo]                   |
+-----------------------------------------------------------------------+
```

---

## 8. Fuera de alcance, riesgos y preguntas abiertas

### Fuera de alcance en v1

- Rotación voluntaria versus involuntaria, y motivo de salida (sección 3).
- Cruce con evaluación de desempeño (sección 3).
- Costo por empleado (P7), bonos por nivel (P6 en su propio visual) y lista de ceses (P8).
- Publicar en la web. Los datos son ficticios, pero el flujo *Publish to web* lo decide la persona, no el dashboard.
- Pronósticos y recomendaciones de contratación.

### Lo que el dato no puede afirmar

- **Una variación no explica su causa por sí sola.** Que Operaciones esté sobre presupuesto no dice que la causa sean las horas extra. Solo se puede decir que las horas extra pagadas superan el presupuesto de horas extra en ese período.
- **No se puede atribuir la variación total por componente** (salvo horas extra), porque el presupuesto no tiene desglose.
- **El headcount real no mide la causa de un salto** ni distingue contrataciones de promociones.

### Riesgos

- **R1. Gratificación en jul y dic.** Distorsiona el costo mensual. Por eso se muestra en color aparte y con su versión sin gratificación.
- **R2. Departamento actual, no histórico.** `dim_empleados` guarda un solo departamento por persona. Si alguien cambió de área, su costo histórico aparece en el área actual. Los CSV no permiten comprobarlo.
- **R3. Liquidaciones inflan un mes.** Operaciones en jun 2026 y Tecnología en sep 2026 tienen pagos de liquidación que pueden parecer un desborde del área.
- **R4. Segoe UI no existe en macOS.** El HTML Content se verá con la tipografía de respaldo en Mac. Hay que validar la maqueta en Windows o en el servicio de Power BI.
- **R5. Datos ficticios.** Son sintéticos y se pueden publicar. Si en el futuro se reemplazan por datos reales, este brief se revisa antes.
- **R6. Pocas personas por área.** Operaciones tiene 41 personas: una persona de diferencia cambia el headcount un 2.4 %. Los porcentajes de headcount deben mostrarse con el número absoluto.

### Preguntas abiertas (para decidir antes de diseñar)

- **A1.** ¿El cierre por defecto es **octubre 2026** (último período de los CSV)? La reunión de Sofía era el cierre del 10 de noviembre.
- **A2.** ¿El headcount real cuenta a la persona en el mes de su liquidación? Hoy el modelo la cuenta (EMP-0066 aparece en jun 2026, su mes de cese). Carlos dijo que después del cese no debería aparecer en planilla, pero no dijo si el mes de salida cuenta como headcount.
- **A3.** Sofía pidió que bonos, gratificaciones y horas extra estén en vistas separadas. ¿Bonos entra en v1 (dentro de la página 3) o se diferido a v2 como P6?
- **A4.** ¿`presupuesto_nomina` incluye las horas extra y `presupuesto_horas_extra` es un subconjunto, o son dos montos que se suman? Afecta la comparación de Operaciones y no se puede confirmar con los CSV.
- **A5.** ¿Mostramos los nombres de los dos cesados en el tablero, o solo el conteo y el monto de la liquidación? Lo segundo es más seguro para un informe que se podría publicar.
- **A6.** ¿Confirman con People que el campo `estado` y `fecha_cese` son la fuente oficial de ceses, o hay que cruzar con el formulario de offboarding?
- **A7.** ¿Sofía quiere ver el presupuesto de gratificación si existe? Hoy no hay ese dato. Si no existe, la gratificación se compara contra cero.

---

## Listo para el siguiente paso

Cuando este brief esté aprobado, el siguiente paso es el perfil de datos y la validación con `checks/anchors.py` (CLAUDE.md, paso 2). Hasta entonces no se escribe TMDL, DAX ni PBIR.
