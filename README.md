# devops-capstone-project

Customer Accounts RESTful microservice for DevOps Capstone: simple API to manage user accounts, suitable for CI/CD and deployment exercises.

[CI Build](https://github.com/1DeliDolu/devops-capstone-project/actions/workflows/ci-build.yaml/badge.svg?branch=main)(https://github.com/1DeliDolu/devops-capstone-project/actions/workflows/ci-build.yaml)

## Status

The project is complete. All CD pipeline changes were applied in `tekton/pipeline.yaml` and deployment manifests are located under `deploy/`.

Report: [Build an Automated CD DevOps Pipeline Using Tekton and OpenShift.pdf](Build%20an%20Automated%20CD%20DevOps%20Pipeline%20Using%20Tekton%20and%20OpenShift.pdf)

If you want any other updates to the README, tell me and I'll apply them.

## Quickstart

Clone the repository:

```
git clone https://github.com/1DeliDolu/devops-capstone-project.git
cd devops-capstone-project
```

Prerequisites:

- Python 3.9+
- pip
- Docker (for building images)
- OpenShift CLI (`oc`) if you plan to run the `deploy` task locally

Run locally (development):

```
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Start with gunicorn (bind to 0.0.0.0:8080):
gunicorn "service:app" -b 0.0.0.0:8080
```

Run tests:

```
pip install -r requirements.txt
pytest -q
```

CI / CD notes:

- Tekton pipeline configuration is in `tekton/pipeline.yaml` and uses ClusterTasks `buildah` and `openshift-client` to build and deploy the image.
- Manifests for deployment are under the `deploy/` directory. The pipeline replaces `IMAGE_NAME_HERE` in `deploy/deployment.yaml` with the built image tag.

If you want, I can commit and push these README changes for you.

## Submission Evidence

This repository includes the files and placeholders used for the final submission. Add the required screenshots and output files to the repository (or provide public URLs) and they will be referenced here.

- README (this file): README.md (public URL: https://github.com/1DeliDolu/devops-capstone-project/blob/main/README.md)
- CI workflow output: `ci-workflow-done` (terminal output file)
- CI workflow config: `.github/workflows/ci-build.yaml` or `ci-build.yaml` in repo
- Tekton pipeline config: `tekton/pipeline.yaml`
- Deployment manifests: `deploy/deployment.yaml` and files under `deploy/`
- Dockerfile: `Dockerfile` (root)
- Kubernetes outputs: `kube-app-output`, `kube-images`, `kube-deploy-accounts` (if generated)
- Tekton logs: `pipelinerun.txt` (save pipeline run logs here)
- Screenshots (place under `screenshots/`):
  - `planning-userstories-done.png`
  - `planning-productbacklog-done.png`
  - `planning-labels-done.png`
  - `planning-kanban-done.png`
  - `rest-techdebt-done.png`
  - `read-accounts.png`
  - `list-accounts.png`
  - `update-accounts.png`
  - `delete-accounts.png`
  - `sprint2-plan.png`
  - `ci-kanban-done.png`
  - `security-kanban-done.png`
  - `sprint3-plan.png`
  - `kube-docker-done.png`
  - `kube-kubernetes-done.png`
  - `cd-pipeline-done.png`

Notes:

- If you want, I can commit and push any evidence files you add to the `screenshots/` directory and generate the final public URLs.
- Tell me which submission option you will use (AI-graded or Peer-graded) and I can prepare a zip or a checklist file with the required files.
