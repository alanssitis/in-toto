"""Resolver implementation for Docker"""
import docker
import logging

from in_toto.resolver._resolver import Resolver

LOG = logging.getLogger(__name__)


class DockerResolver(Resolver):
  """Resolver for docker containers"""

  SCHEME = "docker"

  client = docker.from_env()

  @classmethod
  def resolve_uri(cls, generic_uri, **_):
    return [generic_uri]

  @classmethod
  def hash_artifacts(cls, resolved_uri, hash_algorithms=None, **kwargs):
    image = cls.client.images.get(resolved_uri[9:])
    try:
      algorithm, digest = image.id.split(':')
    except Exception as e:
      raise e
    return {algorithm: digest}
