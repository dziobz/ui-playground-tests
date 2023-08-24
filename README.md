
# Python Website Automation

This repository was created to showcase usage of Playwright with Python in order to automate almost every test case included on http://uitestingplayground.com/ website. Tests run using the pytest plugin. 


## Requirements

* Python
* Pip
* Playwright
* Pytest

## Installation

Create virtual environment with ```python -m venv venv``` and activate it with ```.\venv\Scripts\activate```. Then install the requirements with commands below:

```bash
    pip install playwright
```

```bash
    pip install pytest-playwright
```
```bash
    playwright install
```
    
## Run Locally

To run the tests simply type 

```bash
  pytest
```

Tests are set to run in ```--headed``` mode and use chromium by default. Properties can be changed, for example ```--firefox``` or ```--webkit``` if you want to use different browser. 

To run a single test type

```bash
  pytest -k <name of the function>
```

