# LaTeX PDF authoring and team compilation

The reusable skill is at skills/latex-pdf-workflow/SKILL.md. It supplies a Chinese report template, new-project helper and existing-toolchain compiler driver.

On the current Windows setup, the skill body and work projects live on D. A link in the user's skill discovery folder points to that body. To install on another machine, use its actual user skill directory; do not install the same named skill in two discovery locations.

From a copy of the skill, run:
    python scripts/new_project.py --name my-report --directory D:/LaTeX-Projects
    python scripts/build.py D:/LaTeX-Projects/my-report/main.tex --profile native

The native profile requires the named Windows fonts. The portable profile uses TeX Live's open fonts; choose --profile portable when appropriate. They are different typesetting profiles.

The sample is examples/chinese-report. The root latex-demo workflow compiles this sample with portable fonts and uploads the PDF. Template projects include a root-file workflow ready for a separate team repository.

Use real equation environments, source references, branches and PR review. Download the PDF artifact from a successful workflow run. Exact licensed Windows typography in Linux CI is a separate provisioning task, not an automatic font substitution.

The original migration tools remain unchanged. Only the reviewed note under memory/imported and generic skill files are part of this export.
