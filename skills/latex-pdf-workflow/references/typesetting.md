# Typesetting requirements

Apply these report defaults when the user requests this style and no supplied assignment or journal template takes precedence.

- Chinese body: SimSun, 10.5 bp; Latin text and digits: Times New Roman.
- Section levels: SimHei bold at 18 bp, 13 bp and 10.5 bp; lower levels use SimSun 10.5 bp.
- Table body: mainly 8.5 bp. Use booktabs top/mid/bottom rules, white background, no vertical or interior grid lines. Keep short tables whole; repeat headers and continuation labels for real long tables.
- Captions: mainly SimHei bold 8.5 bp.
- Mathematics: Cambria Math, visually coordinated with the body. Nominal size alone is not an acceptance check.

## Equations

For PDF deliverables use LaTeX's actual math layout: \frac, scripts, suitable delimiters, equation/aligned/split environments. Variables use mathematical italic; units and descriptive labels use upright type.

Let the engine size fractions, scripts, radicals and delimiters. Do not draw fraction rules or place symbols by hand, turn equations into plain text, or shrink a complete long equation to fit. Break at logical operators. Keep a right-aligned single-line number with its formula.

For Word deliverables use native OMML via the document workflow, and inspect the export. A PDF-first workflow does not replace a requested editable Word file.

At the intended print size check fraction-bar length, operator spacing, script position, variable style, tall symbols, equation numbers and visual relation to body text. Compile success and font audits are separate from this check.

## Local and cloud fonts

The native profile requires the named Windows fonts and fails if absent. It does not silently substitute.

The portable profile uses Fandol, TeX Gyre Termes and TeX Gyre Termes Math from TeX Live. Its metrics and appearance differ; do not claim it matches native typography exactly. Never commit proprietary system font files.

With unicode-math, use its native symbol commands such as \symbf and \symbfit for bold math symbols, rather than triggering a missing legacy bold font shape. Inspect the log for substituted font shapes.
