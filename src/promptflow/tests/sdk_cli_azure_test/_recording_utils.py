# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import functools
import inspect
import os
import unittest

import vcr

REGISTERED_FIXTURES = [
    "ml_client",
    "remote_client",
    "pf",
    "remote_web_classification_data",
    "runtime",
    "ml_client_with_acr_access",
]


def fixture_provider(testcase_func):
    # pytest fixture does not work with unittest.TestCase, except for autouse fixtures
    # use this decorator to inject fixtures so that the experience is consistent with pytest
    # reference: https://pytest.org/en/latest/how-to/unittest.html
    @functools.wraps(testcase_func)
    def wrapper(test_class_instance):
        injected_params = {}
        params = inspect.signature(testcase_func).parameters
        for name, param in params.items():
            if name not in REGISTERED_FIXTURES:
                injected_params[name] = param
            else:
                injected_params[name] = getattr(test_class_instance, name)
        testcase_func(**injected_params)

    return wrapper


class PFAzureIntegrationTestCase(unittest.TestCase):
    FILTER_HEADERS = [
        "authorization",
        "client-request-id",
        "retry-after",
        "x-ms-client-request-id",
        "x-ms-correlation-request-id",
        "x-ms-ratelimit-remaining-subscription-reads",
        "x-ms-request-id",
        "x-ms-routing-request-id",
        "x-ms-gateway-service-instanceid",
        "x-ms-ratelimit-remaining-tenant-reads",
        "x-ms-served-by",
        "x-ms-authorization-auxiliary",
    ]

    def __init__(self, method_name: str) -> None:
        super(PFAzureIntegrationTestCase, self).__init__(method_name)

        test_file_path = inspect.getfile(self.__class__)
        recording_dir = os.path.join(os.path.dirname(test_file_path), "recordings")
        self.vcr = vcr.VCR(
            cassette_library_dir=recording_dir,
            record_mode="none",
            filter_headers=self.FILTER_HEADERS,
        )
        self.recording_file = os.path.join(recording_dir, f"{method_name}.yaml")

    def setUp(self) -> None:
        super(PFAzureIntegrationTestCase, self).setUp()

        # set up cassette
        cm = self.vcr.use_cassette(self.recording_file, allow_playback_repeats=True)
        self.cassette = cm.__enter__()
        self.addCleanup(cm.__exit__)
