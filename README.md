## Getting started
Instructions for the **Developers**

### VS Code
In order to have a consistent coding style, formatting on save, good spelling:

1. Let's use the **workspace** feature.

    File -> Open Workspace -> .vscode/python-dev.code-workspace
2. Install the recommended extensions (feel free to propose new ones).
    

### Prerequisites
    pip install -r requirements/dev.txt
    
### Running
    export FLASK_APP=monolith/app.py 
    flask run

### Manually generate mock data in the database
    flask shell
    from monolith import mock
    mock.restaurant()
    mock.restaurant()

### To run tests
    pytest

To run with coverage:

    pytest --cov monolith/

## User stories
![](docs/user-stories.png)

## E-R Diagram in PlantUML
![](docs/plantUML-er.png)