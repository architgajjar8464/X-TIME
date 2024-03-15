###
# Copyright (2023) Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###
import logging
import typing as t

__all__ = [
    "maybe_suggest_debug_level",
    "ErrorCode",
    "XTimeError",
    "ConfigurationError",
    "EstimatorError",
    "DatasetError",
]


def maybe_suggest_debug_level(logger: t.Optional[logging.Logger] = None, prefix: str = " ", suffix: str = ".") -> str:
    if logger is None or not logger.isEnabledFor(logging.DEBUG):
        return (
            f"{prefix}Detailed information is logged when logging level is "
            f"set to `debug` (rerun with --log-level=debug){suffix}"
        )
    return ""


def exception_if_debug(error: Exception, logger: logging.Logger) -> t.Optional[Exception]:
    return error if logger.isEnabledFor(logging.DEBUG) else None


class ErrorCode:
    GENERIC_ERROR = 2
    CONFIGURATION_ERROR = 50
    ESTIMATOR_ERROR = 100
    DATASET_ERROR = 150
    DATASET_MISSING_PREREQUISITES_ERROR = 151


class XTimeError(Exception):
    def __init__(self, message: str, error_code: int = ErrorCode.GENERIC_ERROR) -> None:
        super().__init__(message)
        self._error_code = error_code

    @property
    def error_code(self) -> int:
        return self._error_code


class ConfigurationError(XTimeError):
    def __init__(self, message: str) -> None:
        super().__init__(message, error_code=ErrorCode.CONFIGURATION_ERROR)


class EstimatorError(XTimeError):
    def __init__(self, message: str) -> None:
        super().__init__(message, error_code=ErrorCode.ESTIMATOR_ERROR)


class DatasetError(XTimeError):
    def __init__(self, message: str) -> None:
        super().__init__(message, error_code=ErrorCode.DATASET_ERROR)

    @classmethod
    def missing_prerequisites(cls, message: str) -> "DatasetError":
        error = DatasetError(message)
        error._error_code = ErrorCode.DATASET_MISSING_PREREQUISITES_ERROR
        return error
