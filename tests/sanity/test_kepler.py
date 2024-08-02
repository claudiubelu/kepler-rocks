#
# Copyright 2024 Canonical, Ltd.
# See LICENSE file for licensing details
#

import pytest
from k8s_test_harness.util import docker_util, env_util

# In the future, we may also test ARM
IMG_PLATFORM = "amd64"
IMG_NAME = "kepler"

EXPECTED_FILES = [
    "/usr/bin/kepler",
    "/var/lib/kepler/data/cpus.yaml",
    "/var/lib/kepler/bpfassets/amd64_kepler.bpf.o",
    "/var/lib/kepler/data/acpi_AbsPowerModel.json",
    "/var/lib/kepler/data/acpi_DynPowerModel.json",
    "/var/lib/kepler/data/intel_rapl_AbsPowerModel.json",
    "/var/lib/kepler/data/intel_rapl_DynPowerModel.json",
]

EXPECTED_HELPSTR = "Usage of /usr/bin/kepler:"


@pytest.mark.parametrize("version", ["0.7.8"])
def test_kepler_0_7_8(version: str):
    rock = env_util.get_build_meta_info_for_rock_version(
        IMG_NAME, version, IMG_PLATFORM
    )

    docker_run = docker_util.run_in_docker(rock.image, ["/usr/bin/kepler", "--help"])
    assert EXPECTED_HELPSTR in docker_run.stderr

    # check rock filesystem
    docker_util.ensure_image_contains_paths(rock.image, EXPECTED_FILES)
