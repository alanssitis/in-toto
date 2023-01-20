"""Resolver implementation for files"""

import os
import logging

import securesystemslib.formats
import securesystemslib.hash

from in_toto.resolver._resolver import Resolver

LOG = logging.getLogger(__name__)


class FileResolver(Resolver):
  """Resolver for files"""

  SCHEME = "file"

  @classmethod
  def resolve_uri(cls, generic_uri, **kwargs):
    exclude_patterns = kwargs.get('exclude_patterns', None)
    follow_symlink_dirs = kwargs.get('follow_symlink_dirs', False)
    print(exclude_patterns, follow_symlink_dirs)
    norm_paths = []

    for norm_path in super().apply_exclude_patterns(
        [os.path.normpath(generic_uri)], exclude_patterns):

      if os.path.isfile(norm_path):
        norm_path = norm_path.replace('\\', '/')
        norm_paths.append(norm_path)

      elif os.path.isdir(norm_path):
        for root, dirs, files in os.walk(norm_path,
                                         followlinks=follow_symlink_dirs):
          dirpaths = []
          for dirname in dirs:
            npath = os.path.normpath(os.path.join(root, dirname))
            dirpaths.append(npath)

          if exclude_patterns:
            dirpaths = super().apply_exclude_patterns(dirpaths,
                                                      exclude_patterns)

          dirs[:] = []
          for dirpath in dirpaths:
            name = os.path.basename(dirpath)
            dirs.append(name)

          filepaths = []
          for filename in files:
            norm_filepath = os.path.normpath(os.path.join(root, filename))

            if os.path.isfile(norm_filepath):
              filepaths.append(norm_filepath)

            else:
              LOG.info("File '{}' appears to be a broken symlink. Skipping..."
                  .format(norm_filepath))

          if exclude_patterns:
            filepaths = super().apply_exclude_patterns(filepaths,
                                                exclude_patterns)

          for filepath in filepaths:
            normalized_filepath = filepath.replace("\\", "/")
            norm_paths.append(normalized_filepath)

      else:
        LOG.info("path: {} does not exist, skipping..".format(norm_path))

    return norm_paths

  @classmethod
  def hash_artifacts(cls, resolved_uri, hash_algorithms=None, **kwargs):
    """Internal helper that takes a filename and hashes the respective file's
    contents using the passed hash_algorithms and returns a hashdict conformant
    with securesystemslib.formats.HASHDICT_SCHEMA. """
    if not hash_algorithms:
      hash_algorithms = ['sha256']

    normalize_line_endings = kwargs.get('normalize_line_endings', False)

    securesystemslib.formats.HASHALGORITHMS_SCHEMA.check_match(hash_algorithms)
    hash_dict = {}

    for algorithm in hash_algorithms:
      digest_object = securesystemslib.hash.digest_filename(
          resolved_uri, algorithm,
          normalize_line_endings=normalize_line_endings)
      hash_dict.update({algorithm: digest_object.hexdigest()})

    return hash_dict
