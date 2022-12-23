"""Resolver interface"""

from abc import ABCMeta, abstractmethod
from pathspec import PathSpec

RESOLVER_FOR_URI_SCHEME = {}


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
    scheme = generic_uri.split(":")[0]
    if scheme not in RESOLVER_FOR_URI_SCHEME:
      raise ValueError(f"Unsupported in-toto resolver scheme '{scheme}'")

    resolver = RESOLVER_FOR_URI_SCHEME[scheme]
    return resolver.resolve_uri(generic_uri, **kwargs)

  @classmethod
  @abstractmethod
  def hash_artifacts(cls, resolved_uri, hash_algorithms=None, **kwargs):
    """Return dictionary of hash digests"""
    scheme = resolved_uri.split(":")[0]
    if scheme not in RESOLVER_FOR_URI_SCHEME:
      raise ValueError(f"Unsupported in-toto resolver scheme '{scheme}'")

    resolver = RESOLVER_FOR_URI_SCHEME[scheme]
    return resolver.hash_artifacts(
        resolved_uri, hash_algorithms=hash_algorithms, **kwargs)
