#  Licensed to the Apache Software Foundation (ASF) under one or more
#  contributor license agreements.  See the NOTICE file distributed with
#  this work for additional information regarding copyright ownership.
#  The ASF licenses this file to You under the Apache License, Version 2.0
#  (the "License"); you may not use this file except in compliance with
#  the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import os
from io import StringIO
from typing import List, Tuple

import ruamel
import ruamel.yaml


def get_project_root():
    """Get the absolute path to the root directory of the project"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def safe_load_yaml(path: str):
    """Load a yaml file safely"""
    yaml = ruamel.yaml.YAML(typ='safe')
    with open(path, 'r', encoding='utf-8') as fp:
        return yaml.load(fp)


def dump_yaml(value: dict) -> str:
    """Dump a yaml file safely"""
    ruamel_yaml = ruamel.yaml.YAML(typ='safe')
    ruamel_yaml.explicit_start = True  # type: ignore[assignment]
    ruamel_yaml.preserve_quotes = True  # type: ignore[assignment]
    ruamel_yaml.indent(mapping=2, sequence=4, offset=2)
    with StringIO() as stream:
        ruamel_yaml.dump(value, stream)
        return stream.getvalue()


def is_future_date(base_date, compared_date) -> bool:
    """Check date1 is greater than date2"""
    if base_date < compared_date:
        return True
    return False


def get_list_differences(
        old_list,
        new_list,
        ignore_none: bool = True
) -> Tuple[List[str], List[str], List[str]]:
    """Compare two lists and return the difference

    Returns:
        Tuple[List[str], List[str], List[str]]: a tuple of three lists
    """
    # Initialize the lists if they are None
    if old_list is None:
        old_list = []
    if new_list is None:
        new_list = []
    # Deduplicate and removes None if ignore_none is True
    old_list_set = set(exclude_none(old_list)) if ignore_none else set(old_list)
    new_list_set = set(exclude_none(new_list)) if ignore_none else set(new_list)
    # Get the difference
    intersections = old_list_set & new_list_set
    old_elements = old_list_set - intersections
    new_elements = new_list_set - intersections
    return list(intersections), list(old_elements), list(new_elements)


def exclude_none(value):
    """Exclude None from a list"""
    return [x for x in value if x is not None]


def mask_text(text: str, left_mask_len=4, right_mask_len=4, masking_char='*') -> str:
    """Mask a text with a masking character

    Args:
        text (str): the text to mask
        left_mask_len (int, optional): the number of characters to mask on the left. Defaults to 4.
        right_mask_len (int, optional): the number of characters to mask on the right. Defaults to 4.
        masking_char (str, optional): the masking character. Defaults to '*'.

    Returns:
        str: the masked text
    """
    # Mask all the characters if the text is too short
    if len(text) <= 8:
        return masking_char * len(text)
    # Mask the text
    masked_text = text[4:-4]
    masked_text = masking_char * left_mask_len + masked_text + masking_char * right_mask_len
    return masked_text
