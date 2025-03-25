# Create Release Action

An action to create a GitHub release.
Can be used to create a release in the current repository or a different one.

Usage:
```yaml
jobs:
  create-release:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Create release
        uses: shaur-k/create-release@v1
        with:
          auth_token: ${{ secrets.GITHUB_TOKEN }}
          owner: ${{ github.repository_owner }}
          repo: ${{ github.repository }}
          tag_name: ${{ github.ref }}
          target_commitish: ${{ github.ref }}
          name: ${{ github.ref }}
          body: blahblahblah
```

## Inputs

### Required

- `auth_token`: The GitHub token to use for authentication.
- `owner`: The owner of the repository to create the release in.
- `repo`: The repository to create the release in.
- `tag_name`: The tag name to use for the release.
- `target_commitish`: The commitish to use for the release.

### Optional

- `name`: The name of the release. Defaults to the tag name if not provided.
- `body`: The body of the release. Defaults to nothing if not provided.
- `draft`: Whether the release should be a draft. Defaults to false if not provided.
- `prerelease`: Whether the release should be a prerelease. Defaults to false if not provided.
- `generate_release_notes`: Whether to generate release notes. Defaults to true if not provided.
