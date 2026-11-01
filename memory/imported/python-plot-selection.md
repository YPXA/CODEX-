# Python scientific plot selection
Source: explicit user request to retain reusable figure-selection knowledge, 2026-11-01.

Choose by the question and data structure:
- Ordered x/y dynamics: line; unordered paired observations: scatter.
- Models or scenarios: comparable multi-lines or small multiples.
- Prediction/reference comparison: shared-x trajectory and residual panels.
- Defined lower/upper bounds: estimate line and interval band, with its actual statistical meaning.
- Additive same-unit components: stacked bars; continuous composition can use stacked area.
- Endpoint ranking or ablation: horizontal bars with a declared baseline and gain definition.
- Parameter effects: controlled parameter scans plus signed sensitivity bars.
- Two inputs and one response: heatmap/contours from a real grid or documented XYZ processing.
- Different units on one time axis: prefer linked panels; use double-Y only with explicit correspondence.
- Methods/mechanisms: nodes and edges, not numerical curves.

Save data, transformations, plotting script and figure provenance. Do not infer measurements or confidence intervals from appearance.
Detailed data schemas and Matplotlib mappings: docs/plotting/python-selection.md.
