"""
resolver contains all default artifact resolvers
"""

from in_toto.resolver._docker_resolver import DockerResolver
from in_toto.resolver._file_resolver import FileResolver
from in_toto.resolver._git_resolver import GitResolver
from in_toto.resolver._podman_resolver import PodmanResolver
from in_toto.resolver._resolver import (
  DEFAULT_SCHEME,
  RESOLVER_FOR_URI_SCHEME,
  Resolver,
)

RESOLVER_FOR_URI_SCHEME.update(
    {
      DEFAULT_SCHEME: FileResolver,
      DockerResolver.SCHEME: DockerResolver,
      FileResolver.SCHEME: FileResolver,
      GitResolver.SCHEME: GitResolver,
      PodmanResolver.SCHEME: PodmanResolver,
    }
)
