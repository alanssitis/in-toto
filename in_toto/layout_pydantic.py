# Copyright New York University and the in-toto contributors
# SPDX-License-Identifier: Apache-2.0

"""
<Program Name>
  layout_pydantic.py
<Author>
  Alan Chung Ma <achungma@purdue.edu>
<Started>
  March 30, 2023
<Copyright>
  See LICENSE for licensing information.
<Purpose>
  Pydantic classes for in-toto layouts.
"""

from datetime import date, datetime
from pydantic import BaseModel


class PrivKey(BaseModel):
  """Private Key.
  """
  path: str
  key_type: str | None = None


class PubKey(BaseModel):
  """Public Key.
  """
  path: str
  key_type: str


class Step(BaseModel):
  """Step unit.
  """
  name: str
  threshold: int = 1
  expected_materials: list[str] = []
  expected_products: list[str] = []
  pubkeys: list[str]
  expected_command: str = ''


class Inspection(BaseModel):
  """Inspection step unit.
  """
  name: str
  expected_materials: list[str] = []
  expected_products: list[str] = []
  run: str


class Config(BaseModel):
  """Config.
  """
  signer: PrivKey | None = None
  expires: datetime | date | str | None = None
  readme: str | None = None
  keys: dict[str, PubKey]
  steps: list[Step]
  inspect: list[Inspection]
