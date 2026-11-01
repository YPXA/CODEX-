# Origin scientific plot selection
Source: explicit user request for a separate Origin plotting memory, 2026-11-01.

Use the same question/data logic as Python, while keeping Origin-specific structure:
- Designate X/Y and uncertainty columns explicitly; multiple models usually need one X and several Y columns or grouped data.
- Model intervals given as lower/upper bounds can be filled between curves; bounds are not automatically Y-error magnitudes.
- Stacked bars require additive, common-unit component columns.
- Input/response and trajectory/residual panels link their X axes; distinct units need distinct labels.
- Signed ranking uses a declared zero/baseline; parameter scans preserve their conditions.
- Heatmaps/contours require XYZ or a coordinate-bearing Z matrix. Document gridding/interpolation.
- Insets retain full-data context; purely illustrative mechanisms are not data plots.
- Read the actual Origin session before editing and verify tool capabilities. Do not claim an editable project unless an OPJU with bound data was actually saved.

Detailed worksheet and plot mappings: docs/plotting/origin-selection.md.
No original paper images, identifying metadata or unverified result values are included.
