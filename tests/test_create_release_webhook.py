from enum import verify
from typing import Dict, Union
from _pytest.python_api import raises
from src.create_release_webhook import (
    get_inputs,
    make_config,
    verify_inputs,
    require_env,
    create_payload,
    create_release,
    IS_BOOL
)
import pytest
from unittest import mock
import os

def make_mock_config():
    mock_config : Dict[str, Union[str, bool]] = {
        'INPUT_AUTH_TOKEN': "test_token",
        'INPUT_OWNER': "test_owner",
        'INPUT_REPO': "test_repo",
        'INPUT_TAG_NAME': "",
        'INPUT_TARGET_COMMITISH': "test_commitish",
        'INPUT_NAME': "test_name",
        'INPUT_BODY': "test_body",
        'INPUT_DRAFT': "false",
        'INPUT_PRERELEASE': "false",
        'INPUT_GENERATE_RELEASE_NOTES': "false",
        'INPUT_MAKE_LATEST': "true"
    }
    with mock.patch.dict('src.create_release_webhook.KEYS_TO_DEFAULTS', mock_config):
        return make_config()

@pytest.mark.parametrize(
    "should_pass",
    [
        True,
        False
    ]
)
def test_require_env(should_pass):
    name = "test"
    mocked_value = "mocked" if should_pass else None
    if should_pass:
        assert require_env(name, mocked_value) == mocked_value
    else:
        with pytest.raises(Exception):
            require_env(name, mocked_value)

@pytest.mark.parametrize("field", IS_BOOL)
def test_require_env_bool(field):
    name = field
    mocked_value = "true"
    assert require_env(name, mocked_value) is True
    mocked_value = "false"
    assert require_env(name, mocked_value) is False
    mocked_value = None
    with pytest.raises(Exception):
        require_env(name, mocked_value)

@pytest.mark.parametrize(
    "is_latest, is_prerelease, is_draft, should_pass",
    [
        (True, True, True, False),
        (True, True, False, False),
        (True, True, None, False),
        (True, False, True, False),
        (True, False, False, True),
        (True, False, None, True),
        (True, None, True, False),
        (True, None, False, True),
        (True, None, None, True),
        (False, True, True, True),
        (False, True, False, True),
        (False, True, None, True),
        (False, False, True, True),
        (False, False, False, True),
        (False, False, None, True),
        (False, None, True, True),
        (False, None, False, True),
        (False, None, None, True),
        (None, True, True, False),
        (None, True, False, False),
        (None, True, None, False),
        (None, False, True, False),
        (None, False, False, True),
        (None, False, None, True),
        (None, None, True, False),
        (None, None, False, True),
        (None, None, None, True),
    ]
)
def test_get_inputs(is_latest, is_prerelease, is_draft, should_pass):
    mock_config = make_mock_config()
    inputs = get_inputs(mock_config)
    if is_draft is not None:
        inputs['draft'] = is_draft
    if is_prerelease is not None:
        inputs['prerelease'] = is_prerelease
    if is_latest is not None:
        inputs['make_latest'] = str(is_latest).lower()
    if should_pass:
        assert verify_inputs(inputs)
    else:
        with pytest.raises(Exception):
            verify_inputs(inputs)

def test_create_payload():
    mock_config = make_mock_config()
    inputs = get_inputs(mock_config)
    payload = create_payload(inputs)
    assert payload['tag_name'] == inputs['tag_name']
    assert payload['target_commitish'] == inputs['target_commitish']
    assert payload['name'] == inputs['name']
    assert payload['body'] == inputs['body']
    assert payload['draft'] == inputs['draft']
    assert payload['prerelease'] == inputs['prerelease']
    assert payload['make_latest'] == inputs['make_latest']
