# Claude Demo · Power BI + Fabric

Demo de la charla **Build with Claude Lima – Parte 3** (PUCP, 28 nov 2026): de una reunión y 3 CSV a un dashboard de
Power BI publicado, con Claude Code, Skills y el Power BI MCP sobre Microsoft Fabric.

La estructura sigue a [*The World of Peaches*](https://github.com/gusbavia/the-world-of-peaches) de Gus Bavia
(Power BI World Championship 2026): **el dashboard se diseña antes de abrir Power BI.**

## Qué hay en el repo

| Carpeta | Qué contiene | Paso |
|---|---|---|
| `data/demo-nomina/` | Los 3 CSV de AndinaTech (ficticios) y, en vivo, la transcripción y el `brief.md` | 1–2 |
| `checks/` | `anchors.py`: cifras verificadas en Python (PASS/FAIL) | 2 |
| `design/DESIGN.md` | Contrato de diseño: dirección, tokens, tipografía, layout, reglas de componentes | 3 |
| `design/tokens/` | `tokens.json` (fuente única) y `build_tokens.py`, que genera `tokens.css`, el tema y los tokens DAX | 3 |
| `design/theme/` | Tema de Power BI generado desde los tokens | 3 |
| `design/wireframe/` | Wireframe 1280×720 con el rectángulo de cada visual | 4 |
| `design/checkpoints/` | `brief.checkpoint.md`, respaldo si el brief en vivo falla | 1 |
| `html-components/` | Prototipos HTML aislados al tamaño del contenedor, CSS en `html-components/css/` | 5 |
| `dax/` | Medidas base, probes PASS/FAIL, tokens DAX y una medida por componente + su alt text | 5–6 |
| `src/` | Modelo (TMDL) y reporte (PBIR) cuando se crean en Fabric | 6–7 |
| `docs/screenshots/` | Capturas de QA | 8 |

## El flujo (8 pasos)

1. **Brief**: preguntas del comité, auditoría de datos (incluye lo que los CSV *no* pueden responder), escenas.
2. **Datos y anclas**: CSV en el Lakehouse de Fabric; anclas en PASS.
3. **Diseño**: `DESIGN.md` + tokens → CSS + tema + DAX. *Una paleta, dos motores.*
4. **Wireframe** en la grilla 1280×720.
5. **Componentes aislados**: HTML suelto → medida DAX + alt text.
6. **Modelo y DAX**: modelo Import, medidas base, probes en PASS.
7. **Ensamblar en Power BI**: PBIR siguiendo el wireframe. *Cuando Power BI se abre, el dashboard ya existe.*
8. **QA y publicar**: captura, revisión humana, *Publish to web*.

## Comandos

```bash
python3 checks/anchors.py              # cifras verificadas
python3 design/tokens/build_tokens.py  # regenera CSS, tema y tokens DAX + revisa contraste
python3 -m http.server 8765            # abre html-components/ en el navegador
```

## Datos

AndinaTech S.A.C. es una empresa ficticia. Los datos son sintéticos y se pueden publicar.
Nunca uses *Publish to web* con datos reales: expone los datos del modelo, no solo lo que muestran los visuales.

Créditos del método: Gus Bavia, [gusbavia.com](https://www.gusbavia.com). *The World of Peaches* tiene licencia MIT.
