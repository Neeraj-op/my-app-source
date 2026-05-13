# My Flask Application

A simple Flask web application for learning CI/CD with Jenkins and ArgoCD.

## Features

- Simple REST API endpoints
- Automated unit tests
- Docker containerization
- Health check endpoint for Kubernetes

## Endpoints

- \`GET /\` - Returns a greeting message
- \`GET /health\` - Health check endpoint (used by Kubernetes probes)

## Local Development

### Prerequisites

- Python 3.11+
- pip

### Installation

\`\`\`bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
\`\`\`

### Running the Application

\`\`\`bash
python app.py
\`\`\`

App will be available at: http://localhost:5000

### Running Tests

\`\`\`bash
pip install pytest
pytest test_app.py -v
\`\`\`

## Docker

### Build Docker Image

\`\`\`bash
docker build -t my-app:1.0.0 .
\`\`\`

### Run Docker Container

\`\`\`bash
docker run -p 5000:5000 my-app:1.0.0
\`\`\`

## CI/CD

This repository is set up with:
- Jenkins for Continuous Integration
- Docker Hub for image registry
- ArgoCD for Continuous Deployment

Changes pushed to this repo trigger the Jenkins pipeline automatically