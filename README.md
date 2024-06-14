# invite-members-to-github-org

Python script to invite multiple members from a CSV file to a GitHub organization.

## Usage

1. Prepare a CSV file with name and email columns.

    ```csv
    name,email
    John Doe,John.Doe@exmaple.com
    Jane Doe,Jane.Doe@exmaple.com
    ```

1. Run the script.

    ```bash
    python invite_members.py <INPUT_CSV> <ORGANIZATION> <GITHUB_TOKEN> -t <TEAM_NAMEs>
    ```

    - `<INPUT_CSV>`: Input CSV file.
    - `<ORGANIZATION>`: GitHub organization name.
    - `<GITHUB_TOKEN>`: GitHub personal access token. Required scope is `members:write`.
    - `<TEAM_NAMEs>`: Optional. Team names to add the members.

### Example

```bash
python invite_members.py members.csv my-org my-github-token -t team1 team2
```
