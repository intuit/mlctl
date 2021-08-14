# Contributing

Find a bug, or have an additional feature you'd like to propose? We welcome your contributions! Please read through the guidelines below and submit a Pull Request from your fork.

## Contributing Code

### Cloning the repository
---
1. Fork this repository to your GitHub user space
2. Ensure your fork's master branch has the latest changes from this repository's master branch
3. Clone your fork's master branch to your local file system 
    ```
    git clone <YOURFORK>
    cd mlctl
    ```
4. Create a new local branch 

### Installing the repository
---
```
pip install --editable .
```

   This will install a version to an isolated environment in editable
   mode. As you update the code in the repository, the new code will
   immediately be available to run within the environment (without the
   need to `pip install` it again).


### Testing
---
1. Once your code changes are done, add tests [here](/tests)
2. Run the tests using `tox`:
    ```
    pip install tox
    tox
    ```

### Branching and Release Structure

`mlctl` project will follow this branching structure:

- `develop` - Features that are actively being developed on. Most unstable branch, builds might fail
- `canary` - As the `develop` branch matures, more stable code can move to the `canary` branch. In this branch, features work together, builds are green and the overall code is POC quality. From this branch, code can either go to `beta` or to `main`.
- `beta` - More polished POCs that maybe demo ready.
- `main` - Release version of the library. Well tested and stable with a high bar for engineering quality.

### Creating a Pull Request
---
1. Push your local branch with your tested changes to your forked repo
2. Open up a pull-request from your fork repo's branch to this repository's `develop` or `canary` branch, depending on the quality of the code
    - Include a brief summary of your changes
    - Ensure all CICD branch checks pass
    - Obtain at least one code review from a maintainer or trusted committer. See [CODEOWNERS](./.github/CODEOWNERS) for details.

## Reporting an Issue
Before submitting an issue, please verify that an existing issue has not been reported already. Reported issues can be found at [https://github.com/intuit/mlctl/issues](https://github.com/intuit/mlctl/issues).

When submitting an issue, please keep in mind to include the following: 
* A detailed description of the bug
* Steps to reproduce the bug
* Version of `mlctl` and dependencies invovled



