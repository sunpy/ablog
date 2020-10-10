---
blogpost: true
date: Oct 10, 2020
author: Nabil Freij
location: World
category: Manual
language: English
---

# Markdown Support

ABlog can support markdown pages using [myst-parser](https://pypi.org/project/myst-parser/).
This page is a markdown file underneath.

You will need to do a few things to get setup.

1. Install [myst-parser](https://pypi.org/project/myst-parser/)
2. Add these options to your config, ``conf.py``

```python
extensions = [
    ...
    "myst_parser",
    ...
]
myst_update_mathjax = False
```

Then use the new blogpost metadata format (with a slight twist):
```
---
blogpost: true
date: Oct 10, 2020
author: Nabil Freij
location: World
category: Manual
language: English
---
```

Notice here we do not have a ":" at the start since the markdown metadata format is different from rst.

Please be aware that adding "myst-parser" will mean it will read all markdown files and try to parse them.
You will need to use the following in your ``conf.py`` to prevent this:
```python
exclude_patterns = [
    "posts/*/.ipynb_checkpoints/*",
    ".github/*",
    ".history",
    "github_submodule/*",
    "LICENSE.md",
    "README.md",
]
```
