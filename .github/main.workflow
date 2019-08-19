workflow "Release to PyPi" {
  on = "release"
  resolves = ["upload"]
}

action "tag-filter" {
  uses = "actions/bin/filter@master"
  args = "tag"
}

action "check" {
  uses = "ross/python-actions/setup-py/3.7@master"
  args = "check"
  needs = "tag-filter"
}

action "sdist" {
  uses = "ross/python-actions/setup-py/3.7@master"
  args = "sdist"
  needs = "check"
}

action "upload" {
  uses = "ross/python-actions/twine@master"
  args = "upload ./dist/sunpy-sphinx-theme-*.tar.gz"
  secrets = ["TWINE_PASSWORD", "TWINE_USERNAME"]
  needs = "sdist"
}
