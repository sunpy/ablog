from pkg_resources import DistributionNotFound, get_distribution

try:
    version = get_distribution("ablog").version
except DistributionNotFound:
    version = "unknown.dev"
