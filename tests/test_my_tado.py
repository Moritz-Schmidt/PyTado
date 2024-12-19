"""Test the interface.api.Tado object."""

import json
import unittest
from unittest import mock

from . import common

from PyTado.http import Http
from PyTado.interface.api import Tado


class TadoTestCase(unittest.TestCase):
    """Test cases for tado class"""

    def setUp(self) -> None:
        super().setUp()
        login_patch = mock.patch(
            "PyTado.http.Http._login", return_value=(1, "foo")
        )
        get_me_patch = mock.patch("PyTado.interface.api.Tado.get_me")
        login_patch.start()
        get_me_patch.start()
        self.addCleanup(login_patch.stop)
        self.addCleanup(get_me_patch.stop)

        self.http = Http("my@username.com", "mypassword")
        self.tado_client = Tado(self.http)

    def test_home_set_to_manual_mode(
        self,
    ):
        # Test that the Tado home can be set to auto geofencing mode when it is
        # supported and currently in manual mode.
        with mock.patch(
            "PyTado.http.Http.request",
            return_value=json.loads(
                common.load_fixture(
                    "tadov2.home_state.auto_supported.manual_mode.json"
                )
            ),
        ):
            self.tado_client.get_home_state()

        with mock.patch("PyTado.http.Http.request"):
            self.tado_client.set_auto()

    def test_home_already_set_to_auto_mode(
        self,
    ):
        # Test that the Tado home remains set to auto geofencing mode when it is
        # supported, and already in auto mode.
        with mock.patch(
            "PyTado.http.Http.request",
            return_value=json.loads(
                common.load_fixture(
                    "tadov2.home_state.auto_supported.auto_mode.json"
                )
            ),
        ):
            self.tado_client.get_home_state()

        with mock.patch("PyTado.http.Http.request"):
            self.tado_client.set_auto()

    def test_home_cant_be_set_to_auto_when_home_does_not_support_geofencing(
        self,
    ):
        # Test that the Tado home can't be set to auto geofencing mode when it
        # is not supported.
        with mock.patch(
            "PyTado.http.Http.request",
            return_value=json.loads(
                common.load_fixture("tadov2.home_state.auto_not_supported.json")
            ),
        ):
            self.tado_client.get_home_state()

        with mock.patch("PyTado.http.Http.request"):
            with self.assertRaises(Exception):
                self.tado_client.set_auto()