"""Resolver interface"""

from abc import ABCMeta, abstractmethod
from pathspec import PathSpec
import re

DEFAULT_SCHEME = "default"
RESOLVER_FOR_URI_SCHEME = {}


def _get_scheme(uri):
  match = re.fullmatch(r"(\w+\:)?(.*)", uri)
  if not match:
    raise ValueError(f"Artifact URI '{uri}' could not be parsed")
  groups = match.groups()
  if not groups[0]:
    return DEFAULT_SCHEME
  return groups[0]


class Resolver(metaclass=ABCMeta):
  """Interface for resolvers"""

  @classmethod
  def apply_exclude_patterns(cls, names, exclude_filter):
    """Exclude matched patterns from passed names."""
    included = set(names)

    # Assume old way for easier testing
    if hasattr(exclude_filter, '__iter__'):
      exclude_filter = PathSpec.from_lines('gitwildmatch', exclude_filter)

    for excluded in exclude_filter.match_files(names):
      included.discard(excluded)

    return sorted(included)

  @classmethod
  @abstractmethod
  def resolve_uri(cls, generic_uri, **kwargs):
    """Normalize and resolve artifact URIs"""
    scheme = _get_scheme(generic_uri)

    if scheme not in RESOLVER_FOR_URI_SCHEME:
      raise ValueError(f"Unsupported in-toto resolver scheme '{scheme}'")
    resolver = RESOLVER_FOR_URI_SCHEME[scheme]

    return resolver.resolve_uri(generic_uri, **kwargs)

  @classmethod
  @abstractmethod
  def hash_artifacts(cls, resolved_uri, hash_algorithms=None, **kwargs):
    """Return dictionary of hash digests"""
    scheme = _get_scheme(resolved_uri)

    if scheme not in RESOLVER_FOR_URI_SCHEME:
      raise ValueError(f"Unsupported in-toto resolver scheme '{scheme}'")
    resolver = RESOLVER_FOR_URI_SCHEME[scheme]

    return resolver.hash_artifacts(
        resolved_uri, hash_algorithms=hash_algorithms, **kwargs)
