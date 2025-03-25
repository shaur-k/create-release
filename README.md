# Create Release Action

An action to create a GitHub release automatically given some inputs. Can be used to create a release in the current repository or a different one.

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
