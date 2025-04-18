#!/usr/bin/python3

"""
Creates the release via a webhook, taking in inputs via the action.
@param auth_token: The authentication token for the webhook.
@param tag_name: The name of the tag for the release.
@param target_commitish: The commitish value to tag the release with.
@param name: The name of the release.
@param body: The body of the release.
@param draft: Boolean for the release being a draft or not.
@param prerelease: Boolean for the release being a prerelease or not.
@param generate_release_notes: Boolean for generating release notes automatically.
@param make_latest: Boolean for making the release the latest release. Cannot be set if prerelease or draft is true
"""
import json
import requests
import os
from typing import Dict, Union, List

def require_env(input : str, default : Union[str, None]) -> str | bool:
    """
    Raises a ValueError if the environment variable is not set or no default is passed.
    """
    init_value = os.environ.get(input) or default
    if input == 'INPUT_NAME' and init_value == "":
        value = require_env('INPUT_TAG_NAME', None)
    if init_value is None:
        raise ValueError(f'{input} is required')
    if input in IS_BOOL:
        value = True if init_value.lower() == 'true' else False
    else:
        value = init_value
    return value

IS_BOOL: List[str] = ['INPUT_DRAFT', 'INPUT_PRERELEASE', 'INPUT_GENERATE_RELEASE_NOTES']

KEYS_TO_DEFAULTS: Dict[str, Union[str, None]] = {
    'INPUT_AUTH_TOKEN': None,
    'INPUT_OWNER': None,
    'INPUT_REPO': None,
    'INPUT_TAG_NAME': None,
    'INPUT_TARGET_COMMITISH': None,
    'INPUT_NAME': "",
    'INPUT_BODY': "",
    'INPUT_DRAFT': "false",
    'INPUT_PRERELEASE': "false",
    'INPUT_GENERATE_RELEASE_NOTES': "false",
    'INPUT_MAKE_LATEST': "true"
}

def make_config() -> Dict[str, Union[str, bool]]:
    """
    Takes the environment variables and returns a dictionary of the configuration for mockability.
    """
    return {key: require_env(key, default) for key, default in KEYS_TO_DEFAULTS.items()}

def get_inputs(config : Dict[str, Union[str, bool]]) -> Dict[str, Union[str, bool]]:
    """
    Takes the configuration and returns a dictionary of the inputs.
    """
    return {
        'auth_token': config['INPUT_AUTH_TOKEN'],
        'owner': config['INPUT_OWNER'],
        'repo': config['INPUT_REPO'],
        'tag_name': config['INPUT_TAG_NAME'],
        'target_commitish': config['INPUT_TARGET_COMMITISH'],
        'name': config['INPUT_NAME'],
        'body': config['INPUT_BODY'],
        'draft': config['INPUT_DRAFT'],
        'prerelease': config['INPUT_PRERELEASE'],
        'generate_release_notes': config['INPUT_GENERATE_RELEASE_NOTES'],
        'make_latest': config['INPUT_MAKE_LATEST']
    }

def verify_inputs(inputs : Dict[str, Union[str, bool]]) -> bool:
    """
    Verifies the inputs and raises an error if they are invalid.
    """
    if (inputs['make_latest'] == "true" or inputs['make_latest'] == "legacy") and (inputs['prerelease'] or inputs['draft']):
        raise ValueError('Cannot make a release the latest if it is a prerelease or draft')
    print(inputs)
    return True

def create_payload(inputs) -> Dict[str, Union[str, bool, None]]:
    """
    Creates a payload for creating a release.
    """
    payload = {
        'tag_name': inputs['tag_name'],
        'target_commitish': inputs['target_commitish'],
        'name': inputs['name'],
        'body': inputs['body'],
        'draft': inputs['draft'],
        'prerelease': inputs['prerelease'],
        'generate_release_notes': inputs['generate_release_notes'],
        'make_latest': inputs['make_latest']
    }
    return payload

def create_release(inputs) -> Dict[str, Union[str, bool, None]]:
    payload = create_payload(inputs)
    response = requests.post(f'https://api.github.com/repos/{inputs["owner"]}/{inputs["repo"]}/releases', headers={
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'Bearer {inputs["auth_token"]}',
        'X-GitHub-Api-Version': '2022-11-28'
    }, json=payload)
    return response.json()

def main():
    try:
        config = make_config()
        inputs = get_inputs(config)
        verify_inputs(inputs)
        response = create_release(inputs)
        print(response)
    except Exception as e:
        raise SystemExit(f'Error creating release: {e}')

if __name__ == '__main__':
    main()
