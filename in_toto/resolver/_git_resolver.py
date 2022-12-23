"""Resolver implementation for git"""

import os
import logging

from in_toto.resolver._resolver import Resolver

LOG = logging.getLogger(__name__)


class GitResolver(Resolver):
  """Resolver for podman containers"""

  SCHEME = "git"

  @classmethod
  def resolve_uri(cls, generic_uri, **kwargs):
    return [generic_uri]

  @classmethod
  def hash_artifacts(cls, resolved_uri, hash_algorithms=None, **kwargs):
    parts = resolved_uri.split(':')
    ret = {}
    if len(parts) < 2:
      return ret

    if parts[1] == 'commit':
      ret['sha1'] = os.popen('git rev-parse HEAD').read().replace('\n', '')

    elif len(parts) > 2 and parts[1] == 'tag':
      ret['sha1'] = os.popen(
          f'git rev-parse {parts[2]}').read().replace('\n', '')

    return ret
