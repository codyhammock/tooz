# -*- coding: utf-8 -*-

#    Copyright (C) 2014 Yahoo! Inc. All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import msgpack
from oslo_serialization import msgpackutils
import six

from tooz import coordination


def exception_message(exc):
    """Return the string representation of exception."""
    try:
        return six.text_type(exc)
    except UnicodeError:
        return str(exc)


def to_binary(text, encoding='ascii'):
    """Return the binary representation of string (if not already binary)."""
    if not isinstance(text, six.binary_type):
        text = text.encode(encoding)
    return text


def dumps(data, excp_cls=coordination.ToozError):
    """Serializes provided data using msgpack into a byte string."""
    try:
        return msgpackutils.dumps(data)
    except (msgpack.PackException, ValueError) as e:
        coordination.raise_with_cause(excp_cls, exception_message(e),
                                      cause=e)


def loads(blob, excp_cls=coordination.ToozError):
    """Deserializes provided data using msgpack (from a prior byte string)."""
    try:
        return msgpackutils.loads(blob)
    except (msgpack.UnpackException, ValueError) as e:
        coordination.raise_with_cause(excp_cls, exception_message(e),
                                      cause=e)
