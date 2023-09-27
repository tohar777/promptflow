import pytest

from promptflow._sdk.entities import CustomStrongTypeConnection
from promptflow._utils.connection_utils import (
    generate_custom_strong_type_connection_spec,
    generate_custom_strong_type_connection_template
)
from promptflow.contracts.types import Secret


class MyCustomConnectionWithNoComments(CustomStrongTypeConnection):
    api_key: Secret
    api_base: str


class MyCustomConnectionWithDefaultValue(CustomStrongTypeConnection):
    api_key: Secret
    api_base: str

    def __init__(self, api_base: str = "api-base"):
        self.api_base = api_base


class MyCustomConnectionWithInvalidComments(CustomStrongTypeConnection):
    """Custom connection.

    :param api_key: The api key.
    :type api_key: String
    :param api_base: The api base.
    :type api_base: String
    :param api_key_2: The api key 2.
    :type api_key_2: String
    """
    api_key: Secret
    api_base: str


class MyCustomConnectionMissingTypeComments(CustomStrongTypeConnection):
    """Custom connection.

    :param api_key: The api key.
    """
    api_key: Secret
    api_base: str


class MyCustomConnectionMissingParamComments(CustomStrongTypeConnection):
    """Custom connection.

    :type api_key: String
    """
    api_key: Secret
    api_base: str


@pytest.mark.unittest
class TestConnectionUtils:
    @pytest.mark.parametrize(
        "cls, expected_str_in_template",
        [
            (MyCustomConnectionWithNoComments,
             ['api_base: "to_replace_with_api_base"\n', 'api_key: "to_replace_with_api_key"\n']),
            (MyCustomConnectionWithInvalidComments, ["api_base: to_replace_with_api_base  # String, The api base.\n",
                                                     "api_key: to_replace_with_api_key  # String, The api key.\n"]),
            (MyCustomConnectionMissingTypeComments, ["api_key: to_replace_with_api_key  # The api key."]),
            (MyCustomConnectionMissingParamComments, ["api_key: to_replace_with_api_key  # String"]),
        ]
    )
    def test_generate_custom_strong_type_connection_template_with_comments(self, cls, expected_str_in_template):
        package = "test-package"
        package_version = "0.0.1"
        spec = generate_custom_strong_type_connection_spec(cls, package, package_version)
        template = generate_custom_strong_type_connection_template(cls, spec, package, package_version)
        for comment in expected_str_in_template:
            assert comment in template

    def test_generate_custom_strong_type_connection_template_with_default_value(self):
        package = "test-package"
        package_version = "0.0.1"
        spec = generate_custom_strong_type_connection_spec(MyCustomConnectionWithDefaultValue, package, package_version)
        template = generate_custom_strong_type_connection_template(MyCustomConnectionWithDefaultValue, spec, package, package_version)
        print(template)
        assert 'api_base: "api-base"' in template

