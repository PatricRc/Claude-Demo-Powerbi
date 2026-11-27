# DESIGN.md · Nómina AndinaTech

Este archivo es el contrato de diseño. Claude Code lo lee antes de escribir CSS, el tema, medidas HTML o PBIR.
Sigue el método de Gus Bavia (*The World of Peaches*, Power BI World Championship 2026): **el dashboard se diseña antes de abrir Power BI**.

> Regla: si algo no está en este archivo o en `design/tokens/tokens.json`, no se inventa. Se propone aquí primero.

## 1. Dirección

- **Tono:** ejecutivo financiero, sobrio, sin estilo de marketing. Un comité de cierre de mes lo lee en 30 segundos.
- **Color con significado:** rojo = sobrecosto vs presupuesto, verde = ahorro. Ningún otro uso de rojo o verde.
- **Un solo acento por página:** azul acero `accent`. El dorado `accent-gold` solo marca la gratificación (julio y diciembre).
- **El color nunca es la única señal:** signo (+/−), flecha y texto en cada delta.
- **Sin títulos en los visuales:** el título vive dentro del componente y dice el hallazgo, no el tema.

## 2. Tokens (una paleta, dos motores)

La fuente única es [`tokens/tokens.json`](tokens/tokens.json). El script [`tokens/build_tokens.py`](tokens/build_tokens.py) genera:

| Motor | Archivo generado | Lo usa |
|---|---|---|
| CSS | `tokens/tokens.css` | Prototipos HTML en `html-components/` |
| Tema de Power BI | `theme/andinatech-theme.json` | Visuales nativos (slicers, barras, líneas, tarjetas) |
| DAX | `../dax/_tokens.dax` | Bloque `VAR` al inicio de cada medida HTML |

El script también revisa contraste (texto ≥ 4.5:1). Si un token falla, el script sale con error.

| Token | Hex | Uso |
|---|---|---|
| `ink` | `#1F2A37` | Títulos, números grandes |
| `sub` | `#4B5563` | Etiquetas y texto secundario |
| `muted` | `#6B7280` | Notas y ejes |
| `accent` | `#2F5D8A` | Acento único: real, selección, regla del encabezado |
| `accent-2` | `#6E93B8` | Presupuesto (serie secundaria) |
| `accent-gold` | `#9A6B1F` | Gratificación (jul / dic) |
| `warm` | `#EEF3F8` | Fondo de tarjeta activa y overlays |
| `divider` / `border` | `#E6E8EC` / `#D2D6DC` | Separadores internos |
| `card` / `page` | `#FFFFFF` / `#F4F5F7` | Tarjeta / fondo de página |
| `good` / `good-bg` | `#2A7349` / `#E8F3EC` | Ahorro |
| `bad` / `bad-bg` | `#B23A3A` / `#F8E9E9` | Sobrecosto |
| `sidebar` → `sidebar-2` | `#1B2430` → `#111821` | Barra lateral oscura (va en la imagen de fondo) |

## 3. Tipografía

HTML Content **Secure** bloquea fuentes web y URLs remotas, así que solo usamos fuentes del sistema
(Gus usa Google Fonts con el visual Regular; aquí no se puede).

| Rol | Fuente | Tamaño / peso |
|---|---|---|
| Título de página | Georgia (serif) | 32px, 700 |
| Número héroe | Georgia | 40px, 400 |
| Número de tarjeta | Segoe UI Light | 28px |
| Etiqueta | Segoe UI | 10px, 600, MAYÚSCULAS, tracking 2px |
| Texto / pista | Segoe UI | 11px, 400, interlineado 1.5 |

## 4. Espaciado y forma

- Ritmo de 8 px: paddings 16 / 24, gaps 8 / 16.
- Radios: tarjeta 12px, pill 999px, botón 8px. Sin sombras ni bordes en visuales nativos (lo hace el tema).

## 5. Layout

Una página ejecutiva 1280×720, detallada en [`wireframe/wireframe.md`](wireframe/wireframe.md).
Barra lateral oscura 0–228 px como imagen de fondo; contenido en x 272–1250, y 140–690; máximo 2 filas.

## 6. Componentes

| Componente | Prototipo | Medida DAX | Visual |
|---|---|---|---|
| Tarjeta héroe: costo, variación y pista | `html-components/Page-1---001---KPI-Card.html` | `dax/Page-1---001---KPI-Card-HTML.dax` | HTML Content **Secure** |
| Alt text de la tarjeta | — | `dax/Page-1---0011---KPI-Card-Alt-Text.dax` | Alt text del visual |

Flujo de cada componente (paso 5 de Gus):
1. Se prototipa como HTML suelto al tamaño exacto del contenedor, con datos de ejemplo y `tokens.css`.
2. Se revisa en el navegador y se corrige.
3. Se convierte en una medida DAX: tokens como `VAR`, estilos **en línea** (Secure no garantiza `<style>`), valores marcados con `<!--{DAX}-->` en el prototipo.
4. Se crea su medida de alt text.

Restricciones de HTML Content Secure: sin `<script>`, sin `on*`, sin URLs remotas, sin fuentes web. Solo `div`, `span`, `p`, `strong`, `h1`–`h3` y SVG simple ensayado.

## 7. Formato de números

- Soles con prefijo `S/` y escala explícita: `S/ 23.10 M`, `S/ 68.5 mil`.
- Deltas con signo y período de comparación: `−S/ 7.7 mil vs presupuesto`.
- Blancos como `—`, nunca `0`.
