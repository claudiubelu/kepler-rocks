#
# Copyright 2024 Canonical, Ltd.
# See LICENSE file for licensing details
#

import pytest
from k8s_test_harness import harness
from k8s_test_harness.util import constants, env_util, k8s_util
from k8s_test_harness.util.k8s_util import HelmImage

IMG_PLATFORM = "amd64"
INSTALL_NAME = "kepler"


def _get_rock_image(name: str, version: str):
    rock = env_util.get_build_meta_info_for_rock_version(name, version, IMG_PLATFORM)
    return rock.image


@pytest.mark.parametrize("version", ["0.7.8"])
def test_kepler(function_instance: harness.Instance, version: str):
    images = [
        HelmImage(uri=_get_rock_image("kepler", version)),
    ]

    helm_command = k8s_util.get_helm_install_command(
        name=INSTALL_NAME,
        chart_name="kepler",
        images=images,
        namespace=constants.K8S_NS_KUBE_SYSTEM,
        repository="https://sustainable-computing-io.github.io/kepler-helm-chart",
        chart_version="0.5.8",
    )
    function_instance.exec(helm_command)

    k8s_util.wait_for_daemonset(
        function_instance, "kepler", constants.K8S_NS_KUBE_SYSTEM
    )
