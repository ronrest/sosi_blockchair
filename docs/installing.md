# Installing


```bash
# ------------------------------------------------------------------------------
# 1. INSTALL DEPENDENCIES (only run one of these)
# ------------------------------------------------------------------------------
#    NOTE: Dev dependencies are exactly the same, but with some aditional 
#    packages for running tests, checking formatting of code, etc.
# ------------------------------------------------------------------------------
#    NOTE: the `strict` versions ensure that your virtual environment ONLY has
#    the dependencies listed in the requrements file. Removes everything else.
#    Requires pip-tools to be installed: 
#        pip install pip-tools
# ------------------------------------------------------------------------------
# a. Prod dependencies (compatible with existing virtualenv)
pip install -r requirements.txt

# b. Dev dependencies (compatible with existing virtualenv)
pip install -r requirements-dev.txt

# c. Strict Prod dependencies (Warning: might delete libraries in virtualenv)
pip-sync

# d. Strict Dev dependencies (Warning: might delete libraries in virtualenv)
pip-sync requirements.txt requirements-dev.txt


# ------------------------------------------------------------------------------
# 2. INSTALL PACKAGE (only run one of these)
# ------------------------------------------------------------------------------
# a. Install package regularly
pip install .

# b. Install package in editable mode (for development)
pip install -e .

```
