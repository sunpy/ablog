try:
    from ._version import version
except Exception:
    import warnings

    warnings.warn(f"could not determine {__name__.split('.')[0]} package version; this indicates a broken installation")
    del warnings

    version = "0.0.0"

from packaging.version import parse as _parse

_version = _parse(version)
major, minor, bugfix = [*_version.release, 0][:3]
release = not _version.is_devrelease

__all__ = ["version", "major", "minor", "bugfix", "release"]
