# DevOps Capstone Project

![Build Status](https://github.com/edensitko/devops-capstone-project/actions/workflows/ci-build.yaml/badge.svg)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.9](https://img.shields.io/badge/Python-3.9-green.svg)](https://shields.io/)

A production-ready RESTful microservice for account management, built with Flask and deployed using modern DevOps practices including CI/CD pipelines, containerization, and Kubernetes orchestration.

This project demonstrates enterprise-level DevOps practices as part of the [**IBM DevOps and Software Engineering Professional Certificate**](https://www.coursera.org/professional-certificates/devops-and-software-engineering).

## Features

- RESTful API for account management (CRUD operations)
- PostgreSQL database integration
- Test-Driven Development (TDD) with 95%+ code coverage
- CI/CD pipeline using GitHub Actions
- Containerized deployment with Docker
- Kubernetes manifests for cloud deployment
- Tekton pipelines for automated builds and deployments
- Comprehensive error handling and logging

## Tech Stack

- **Backend**: Python 3.9, Flask
- **Database**: PostgreSQL
- **Testing**: Pytest, Factory Boy
- **CI/CD**: GitHub Actions, Tekton
- **Containerization**: Docker
- **Orchestration**: Kubernetes (K3D for local development)
- **Development**: VS Code with Remote Containers

## Quick Start

### Prerequisites

- Python 3.9+
- Docker Desktop
- Git

### Setup

1. Clone the repository:
```bash
git clone https://github.com/edensitko/devops-capstone-project.git
cd devops-capstone-project
```

2. Initialize the development environment:
```bash
source bin/setup.sh
```

This script will:
- Install and configure Python 3.9
- Create and activate a virtual environment
- Install all dependencies
- Set up the development environment

Your prompt should now look like: `(venv) theia:project$`

3. Start the PostgreSQL database:
```bash
make db
```

4. Run the application:
```bash
flask run
```

The API will be available at `http://localhost:5000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/accounts` | List all accounts |
| GET | `/accounts/{id}` | Get account by ID |
| POST | `/accounts` | Create new account |
| PUT | `/accounts/{id}` | Update account |
| DELETE | `/accounts/{id}` | Delete account |

## Development Commands

```bash
# Install dependencies
make install

# Run tests
make test

# Run tests with coverage report
make coverage

# Lint code
make lint

# Start PostgreSQL database
make db

# Run the application
flask run
```

## Project layout

The code for the microservice is contained in the `service` package. All of the test are in the `tests` folder. The code follows the **Model-View-Controller** pattern with all of the database code and business logic in the model (`models.py`), and all of the RESTful routing on the controller (`routes.py`).

```text
├── service         <- microservice package
│   ├── common/     <- common log and error handlers
│   ├── config.py   <- Flask configuration object
│   ├── models.py   <- code for the persistent model
│   └── routes.py   <- code for the REST API routes
├── setup.cfg       <- tools setup config
└── tests                       <- folder for all of the tests
    ├── factories.py            <- test factories
    ├── test_cli_commands.py    <- CLI tests
    ├── test_models.py          <- model unit tests
    └── test_routes.py          <- route unit tests
```

## Data Model

The Account model represents user accounts with the following schema:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | Integer | Yes | Unique identifier |
| name | String(64) | Yes | Account holder name |
| email | String(64) | Yes | Email address |
| address | String(256) | Yes | Physical address |
| phone_number | String(32) | No | Contact number |
| date_joined | Date | Yes | Account creation date |

## Testing

This project follows Test-Driven Development (TDD) principles with comprehensive test coverage:

```bash
# Run all tests
make test

# Run with coverage report
make coverage

# Run specific test file
pytest tests/test_routes.py
```

Test coverage is maintained at 95%+ to ensure code quality and reliability.

## Deployment

### Docker

Build and run the application in a container:

```bash
# Build the image
docker build -t accounts-service .

# Run the container
docker run -p 5000:5000 accounts-service
```

### Kubernetes

Deploy to a Kubernetes cluster:

```bash
# Apply Kubernetes manifests
kubectl apply -f deploy/

# Check deployment status
kubectl get pods
kubectl get services
```

### Local Kubernetes Development

For local development with K3D and Tekton:

```bash
# Create local K3D cluster
make cluster

# Install Tekton
make tekton

# Install ClusterTasks
make clustertasks
```

Requirements:
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Visual Studio Code](https://code.visualstudio.com)
- [Remote Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

## CI/CD Pipeline

The project includes automated CI/CD pipelines:

- **GitHub Actions**: Automated testing and building on every push
- **Tekton Pipelines**: Kubernetes-native CI/CD for deployment automation

Pipeline configuration files:
- `.github/workflows/ci-build.yaml` - GitHub Actions workflow
- `tekton/pipeline.yaml` - Tekton pipeline definition
- `tekton/tasks.yaml` - Tekton task definitions

## Troubleshooting

### Activate virtual environment manually
```bash
source ~/venv/bin/activate
```

### Reinstall dependencies
```bash
make install
```

### Check database status
```bash
docker ps
```

### View application logs
```bash
docker logs <container-id>
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Implement your changes
5. Ensure all tests pass (`make test`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

