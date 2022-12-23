"""Resolver implementation for podman"""

import podman
import logging

from in_toto.resolver._resolver import Resolver

LOG = logging.getLogger(__name__)


class PodmanResolver(Resolver):
  """Resolver for podman containers"""

  SCHEME = "podman"

  client = podman.PodmanClient()

  @classmethod
  def resolve_uri(cls, generic_uri, **kwargs):
    return [generic_uri]

  @classmethod
  def hash_artifacts(cls, resolved_uri, hash_algorithms=None, **kwargs):
    image = cls.client.images.get(resolved_uri[6:])
    try:
      algorithm, digest = image.id.split(':')
    except Exception as e:
      raise e
    return {algorithm: digest}
