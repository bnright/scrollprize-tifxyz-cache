"""Cache-contract regressions; real-surface end-to-end evidence lives in scripts.

The tiler is replaced here so each assertion isolates cache identity rather
than depending on a particular geometry or patch-count heuristic.
"""

from __future__ import annotations

import json

import numpy as np
import pytest

from vesuvius.tifxyz.types import Tifxyz


BASE_PARAMETERS = {
    "target_size": (64, 64, 64),
    "overlap_fraction": 0.25,
    "coarse_multiplier": 2.0,
    "num_calibration_samples": 200,
    "min_new_coverage": 0.5,
}

CHANGED_PARAMETERS = [
    ("target_size", (128, 128, 128)),
    ("overlap_fraction", 0.5),
    ("coarse_multiplier", 3.0),
    ("num_calibration_samples", 32),
    ("min_new_coverage", 0.2),
]


def surface(path=None, scale=(0.05, 0.05)):
    values = np.arange(9, dtype=np.float32).reshape(3, 3) + 100
    return Tifxyz(
        _x=values.copy(), _y=values.copy(), _z=values.copy(),
        _scale=scale, path=path,
    )


@pytest.fixture
def tiler_calls(monkeypatch):
    from vesuvius.tifxyz import hierarchical_tiling

    calls = []

    def recording_tiler(segment, **parameters):
        calls.append(parameters)
        # A different result per execution makes stale cache reuse observable.
        marker = float(len(calls))
        return [((0, 2, 0, 2), (marker, marker + 1, 0.0, 1.0, 0.0, 1.0))]

    monkeypatch.setattr(
        hierarchical_tiling, "multipass_hierarchical_tiling", recording_tiler
    )
    return calls


def test_identical_memory_request_reuses_result(tiler_calls):
    segment = surface()
    first = segment.get_patches_3d(**BASE_PARAMETERS)
    second = segment.get_patches_3d(**BASE_PARAMETERS)

    assert second is first
    assert len(tiler_calls) == 1


@pytest.mark.parametrize("name,value", CHANGED_PARAMETERS)
def test_changed_parameter_invalidates_memory_cache(name, value, tiler_calls):
    segment = surface()
    first = segment.get_patches_3d(**BASE_PARAMETERS)
    changed = {**BASE_PARAMETERS, name: value}
    second = segment.get_patches_3d(**changed)

    assert len(tiler_calls) == 2
    assert tiler_calls[-1][name] == value
    assert second != first
    assert segment.get_patches_3d(**changed) is second
    assert len(tiler_calls) == 2


def test_identical_disk_request_reuses_result(tmp_path, tiler_calls):
    first = surface(tmp_path).get_patches_3d(**BASE_PARAMETERS)
    reloaded = surface(tmp_path).get_patches_3d(**BASE_PARAMETERS)

    assert reloaded == first
    assert len(tiler_calls) == 1


@pytest.mark.parametrize("name,value", CHANGED_PARAMETERS)
def test_changed_parameter_invalidates_disk_cache(name, value, tmp_path, tiler_calls):
    first = surface(tmp_path).get_patches_3d(**BASE_PARAMETERS)
    changed = {**BASE_PARAMETERS, name: value}
    second = surface(tmp_path).get_patches_3d(**changed)

    assert len(tiler_calls) == 2
    assert tiler_calls[-1][name] == value
    assert second != first
    # Both request identities remain reusable across fresh instances.
    assert surface(tmp_path).get_patches_3d(**BASE_PARAMETERS) == first
    assert surface(tmp_path).get_patches_3d(**changed) == second
    assert len(tiler_calls) == 2


def test_different_scale_invalidates_disk_cache(tmp_path, tiler_calls):
    first = surface(tmp_path).get_patches_3d(**BASE_PARAMETERS)
    second = surface(tmp_path, scale=(0.1, 0.05)).get_patches_3d(**BASE_PARAMETERS)

    assert len(tiler_calls) == 2
    assert second != first


def test_legacy_disk_key_is_ignored(tmp_path, tiler_calls):
    # The old identity cannot tell which of four omitted layout parameters
    # produced these bounds; reusing it would preserve the original defect.
    legacy = {"64,64,64,0.05,0.05": [[[0, 2, 0, 2], [999, 1000, 0, 1, 0, 1]]]}
    (tmp_path / "patches_cache.json").write_text(json.dumps(legacy), encoding="utf-8")

    result = surface(tmp_path).get_patches_3d(**BASE_PARAMETERS)

    assert len(tiler_calls) == 1
    assert result[0][1][0] == 1.0
    assert surface(tmp_path).get_patches_3d(**BASE_PARAMETERS) == result
    assert len(tiler_calls) == 1


def test_force_recompute_refreshes_memory_and_disk(tmp_path, tiler_calls):
    segment = surface(tmp_path)
    first = segment.get_patches_3d(**BASE_PARAMETERS)
    refreshed = segment.get_patches_3d(**BASE_PARAMETERS, force_recompute=True)

    assert len(tiler_calls) == 2
    assert refreshed != first
    assert segment.get_patches_3d(**BASE_PARAMETERS) is refreshed
    assert surface(tmp_path).get_patches_3d(**BASE_PARAMETERS) == refreshed
    assert len(tiler_calls) == 2


def test_verbose_does_not_change_cache_identity(tiler_calls):
    segment = surface()
    first = segment.get_patches_3d(**BASE_PARAMETERS, verbose=False)

    assert segment.get_patches_3d(**BASE_PARAMETERS, verbose=True) is first
    assert len(tiler_calls) == 1


@pytest.mark.parametrize("disk", [False, True])
def test_numpy_float_does_not_collide_with_python_float(disk, tmp_path, tiler_calls):
    # Both print as '0.9', but their values (and tiler strides) can differ.
    segment = surface(tmp_path if disk else None)
    first = segment.get_patches_3d(**{**BASE_PARAMETERS, "overlap_fraction": 0.9})
    if disk:
        segment = surface(tmp_path)
    second = segment.get_patches_3d(**{**BASE_PARAMETERS, "overlap_fraction": np.float32(0.9)})
    assert float(np.float32(0.9)) != 0.9
    assert len(tiler_calls) == 2
    assert second != first


@pytest.mark.parametrize("disk", [False, True])
def test_resolution_mode_does_not_reuse_old_layout(disk, tmp_path, tiler_calls):
    # This isolates identity only; it does not claim full-resolution tiling
    # support for the current upstream numerical implementation.
    segment = surface(tmp_path if disk else None)
    first = segment.get_patches_3d(**BASE_PARAMETERS)
    if disk:
        segment = surface(tmp_path)
    segment.use_full_resolution()
    second = segment.get_patches_3d(**BASE_PARAMETERS)
    assert len(tiler_calls) == 2
    assert second != first
