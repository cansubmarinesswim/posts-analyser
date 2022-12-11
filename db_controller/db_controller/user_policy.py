import re

from grpc import StatusCode
from password_strength import PasswordPolicy

from db_controller.exceptions import ManageUserError


class PolicyNotMet(ManageUserError):
    def __init__(self, message):
        super().__init__(StatusCode.INVALID_ARGUMENT, message)


class UserPolicy:
    def __init__(
        self,
        passwd_min_length,
        passwd_max_length,
        passwd_uppercase,
        passwd_numbers,
        passwd_special,
    ):
        self._passwd_min_length = passwd_min_length
        self._passwd_max_length = passwd_max_length
        self._passwd_uppercase = passwd_uppercase
        self._passwd_numbers = passwd_numbers
        self._passwd_special = passwd_special
        self._user_name_regex_rules = "^[a-zA-Z0-9_.-]+$"
        self._user_name_max_len = 32
        self._user_name_min_len = 4

    def validate_user_policy(self, user_name, password):
        self._validate_username(user_name)
        self._validate_password(password)

    def _validate_username(self, user_name):
        if len(user_name) < self._user_name_min_len:
            raise PolicyNotMet(
                "User name must have at least %s characters." % self._user_name_min_len
            )
        if len(user_name) > self._user_name_max_len:
            raise PolicyNotMet(
                "User name must have at most %s characters." % self._user_name_max_len
            )
        if re.match(self._user_name_regex_rules, user_name) is None:
            raise PolicyNotMet(
                'Username can only contain alphanumeric characters and ".","_","-"'
            )

    def _validate_password(self, password):
        passwd_policy_eval = PasswordPolicy().password(password)
        if (
            passwd_policy_eval.length < self._passwd_min_length
            or passwd_policy_eval.length > self._passwd_max_length
        ):
            raise PolicyNotMet(
                "Password must have between %s and %s characters."
                % (self._passwd_min_length, self._passwd_max_length)
            )
        if passwd_policy_eval.letters_uppercase < self._passwd_uppercase:
            raise PolicyNotMet(
                "Password must have at least %s uppercase letters."
                % self._passwd_uppercase
            )
        if passwd_policy_eval.numbers < self._passwd_numbers:
            raise PolicyNotMet(
                "Password must have at least %s number(s)." % self._passwd_numbers
            )
        if passwd_policy_eval.special_characters < self._passwd_special:
            raise PolicyNotMet(
                "Password must have at least %s special characters."
                % self._passwd_special
            )
