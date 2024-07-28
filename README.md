# GitHub Project Planning

This repo implements a BioCypher pipeline that grabs all issues on a GitHub
Projects board that simulates a collaborative team (available
[here](https://github.com/orgs/biocypher/projects/6/views/1)).  The pipeline
builds a knowledge graph of issues, categories, assigned team members, and
annotations on the issues, and then provides access to an LLM assistant that
summarises tasks performed in the previous iteration of the project for the
group and each individual. Further, the web app provides a planning tab that
analyses tasks in next iterations of the project and provides suggestions for
task prioritisation and collaboration, again for the group and each individual.

## Usage

> [!IMPORTANT]
> The knowledge graph build stage requires a GitHub token to access the GitHub
> API, `BIOCYPHER_GITHUB_PROJECT_TOKEN`, in the environment. If you don't have
> access to this token, the KG build will fail. You can see an online version
> of the app [here](https://project.biochatter.org).

The `docker-compose.yml` file contains the necessary services to run the
pipeline. To start the pipeline, run:

```bash
git clone https://github.com/biocypher/project-planning.git
cd project-planning
docker-compose up -d
```

The pipeline will `build`, `import`, and `deploy` the knowledge graph, and then
start the `app` service. The KG is available at `http://localhost:7474` and the
app is available at `http://localhost:8051`.

This standard pipeline runs a non-password-protected Neo4j instance. To run a
password-protected instance (with ports open to the web), run:

```bash
docker-compose -f docker-compose-password.yml up -d
```

Authentification settings are configured in the `docker-compose-password.yml`
