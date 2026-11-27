# CLAUDE.md · reglas para Claude Code en este repo

Proyecto: dashboard de nómina de AndinaTech S.A.C. (datos ficticios) en Microsoft Fabric + Power BI, con el método de Gus Bavia.

## Orden de trabajo (no saltarse pasos)

1. **Brief** → `data/demo-nomina/brief.md` desde la transcripción y los 3 CSV. Incluye qué preguntas NO se pueden responder.
2. **Datos y anclas** → los CSV ya están en el Lakehouse de Fabric. Corre `python3 checks/anchors.py`; todo debe dar PASS.
3. **Diseño** → lee `design/DESIGN.md`. Cambia colores solo en `design/tokens/tokens.json` y corre `python3 design/tokens/build_tokens.py`.
4. **Wireframe** → `design/wireframe/wireframe.md`. Cada visual tiene un rectángulo en la grilla 1280×720.
5. **Componentes** → prototipo HTML en `html-components/` (con `tokens.css`), revisado en navegador, luego medida DAX en `dax/` + alt text.
6. **Modelo y DAX** → modelo Import, medidas de `dax/_base-measures.dax`, después `dax/_probes.dax` hasta PASS.
7. **Ensamblar en Power BI** → PBIR en `src/`, un visual por rectángulo del wireframe, tema desde `design/theme/`.
8. **QA y publicar** → captura, revisión contra el brief, la persona aprueba. *Publish to web* es un clic humano.

**No escribas TMDL, DAX ni PBIR hasta que existan el brief, los tokens y el wireframe.**

## Skills que debes usar

- `gus-bavia-dashboards`: brief, tokens, wireframe, componentes HTML/DAX, QA.
- `fabric-semantic-model` / `semantic-model-authoring`: modelo, relaciones, DAX, TMDL.
- `powerbi-report` / `powerbi-report-cli`: PBIR, validación, preview y publicación.
- `data-analytics-project`: perfil y auditoría de los CSV.

## Límites

- Solo datos de `data/demo-nomina/`. Nunca datos reales ni de MoneyGeek.
- HTML Content **Secure**: sin `<script>`, sin `on*`, sin URLs remotas, sin fuentes web, estilos en línea.
- No inventes números: cada cifra del reporte sale de una medida que pasó su probe.
- No publiques ni compartas nada sin que la persona lo apruebe.
