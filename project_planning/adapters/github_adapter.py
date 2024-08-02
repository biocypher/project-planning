import requests
import json
import os
from enum import Enum, auto
from itertools import chain
from biocypher._logger import logger

logger.debug(f"Loading module {__name__}.")


class GitHubAdapterNodeType(Enum):
    """
    Define types of nodes the adapter can provide.
    """

    PERSON = "person"
    PROJECT = "project"
    ITERATION = "iteration"


class GitHubAdapterProjectField(Enum):
    """
    Define possible fields the adapter can provide.
    """

    TITLE = "title"
    DESCRIPTION = "description"
    LABELS = "labels"
    STATUS = "status"
    SIZE = "size"
    PRIORITY = "priority"
    ITERATION = "iteration"
    ASSIGNEES = "assignees"
    ISSUE = "issue"


class GitHubAdapterEdgeType(Enum):
    """
    Enum for the edge types of the adapter.
    """

    LEADS = "leads"
    PART_OF = "part of"


class GitHubAdapter:
    """
    Example BioCypher adapter. Generates nodes and edges for creating a
    knowledge graph.

    Args:
        node_types: List of node types to include in the result.
        node_fields: List of node fields to include in the result.
        edge_types: List of edge types to include in the result.
        edge_fields: List of edge fields to include in the result.
    """

    def __init__(
        self,
        node_types: str = None,
        node_fields: str = None,
        edge_types: str = None,
        edge_fields: str = None,
    ):
        self._set_types_and_fields(node_types, node_fields, edge_types, edge_fields)

        self._nodes = []
        self._edges = []

        self._setup_api()
        self._download_data()
        self._process_nodes()
        self._process_edges()

    def get_nodes(self) -> list:
        """
        Returns a list of node tuples for node types specified in the
        adapter constructor.

        Returns:
            List of nodes.
        """

        return self._nodes

    def get_edges(self):
        """
        Returns a list of edge tuples for edge types specified in the
        adapter constructor.
        """

        return self._edges

    def _get_token(self):
        token = os.getenv("BIOCYPHER_GITHUB_PROJECT_TOKEN")
        if not token:
            if not token:
                raise ValueError(
                    "No GitHub API key found. Please set the "
                    "BIOCYPHER_GITHUB_PROJECT_TOKEN environment variable."
                )

        return token

    def _setup_api(self):
        """
        Set up the GitHub API.
        """

        # Set the API endpoint and headers
        self.url = "https://api.github.com/graphql"
        self.headers = {"Authorization": f"Bearer {self._get_token()}"}

    def _download_data(self):
        """
        Download data from the GitHub project page using the API.
        """

        # Get the project ID
        self._id = self._get_project_id(self.url, self.headers)

        # Get the project fields
        self._fields = self._get_project_fields(self.url, self.headers, self._id)

        # Get the project items
        self._items = self._get_project_items(self.url, self.headers, self._id)

    def mutate_column(self, item_id: str, new_column: str):
        """
        Move a card to a new column.
        """

        # find the id of the status field and the column
        for field in self._fields:
            if field.get("name") == "Status":
                field_id = field.get("id")
                for option in field.get("options"):
                    if option.get("name") == new_column:
                        field_value = option.get("id")

        query = """
          mutation {
            updateProjectV2ItemFieldValue (input: {fieldId: "%s", itemId: "%s", projectId: "%s", value: {singleSelectOptionId: "%s"} }) {
              clientMutationId
            }
          }
        """ % (
            field_id,
            item_id,
            self._id,
            field_value,
        )

        # Set the request data as a dictionary
        data = {"query": query}

        # Send the API request
        response = requests.post(self.url, headers=self.headers, json=data)

        # Parse the response JSON
        response_json = json.loads(response.text)

        # Extract the data from the response JSON
        data = response_json.get("data")

    def mutate_timeslot(self, item_id: str, new_timeslot: str):
        """
        Update the timeslot value of a card.
        """

        field_value = None

        # find the id of the status field and the column
        for field in self._fields:
            if field.get("name") == "Timeslot":
                field_id = field.get("id")
                for option in field.get("options"):
                    if option.get("name") == new_timeslot:
                        field_value = option.get("id")

        if not field_value:
            logger.warning(f"Could not find {new_timeslot} in field options.")
            return

        query = """
          mutation {
            updateProjectV2ItemFieldValue (input: {fieldId: "%s", itemId: "%s", projectId: "%s", value: {singleSelectOptionId: "%s"} }) {
              clientMutationId
            }
          }
        """ % (
            field_id,
            item_id,
            self._id,
            field_value,
        )

        # Set the request data as a dictionary
        data = {"query": query}

        # Send the API request
        response = requests.post(self.url, headers=self.headers, json=data)

        # Parse the response JSON
        response_json = json.loads(response.text)

        # Extract the data from the response JSON
        data = response_json.get("data")

    def mutate_duration(self, item_id: str, new_duration: str):
        """
        Update the duration of an event (card).
        """

        # find the id of the status field and the column
        for field in self._fields:
            if field.get("name") == "Duration":
                field_id = field.get("id")
                for option in field.get("options"):
                    if option.get("name") == new_duration:
                        field_value = option.get("id")

        query = """
          mutation {
            updateProjectV2ItemFieldValue (input: {fieldId: "%s", itemId: "%s", projectId: "%s", value: {singleSelectOptionId: "%s"} }) {
              clientMutationId
            }
          }
        """ % (
            field_id,
            item_id,
            self._id,
            field_value,
        )

        # Set the request data as a dictionary
        data = {"query": query}

        # Send the API request
        response = requests.post(self.url, headers=self.headers, json=data)

        # Parse the response JSON
        response_json = json.loads(response.text)

        # Extract the data from the response JSON
        data = response_json.get("data")

    def _get_project_id(self, url: str, headers: dict) -> str:
        query = """
                query{
                    organization(login: "biocypher"){
                        projectV2(number: 6) {
                            id
                        }
                    }
                }
                """

        # Send the API request
        response = requests.post(url, headers=headers, json={"query": query})

        if response.status_code == 200:
            response_data = response.json()
            # Check for errors in the response data
            if "errors" in response_data:
                print("Errors in the response:", response_data["errors"])
            else:
                project_id = response_data["data"]["organization"]["projectV2"]["id"]
                return project_id
        else:
            print("Failed to fetch project ID, status code:", response.status_code)

    def _get_project_fields(self, url: str, headers: dict, id_: str) -> dict:
        query = (
            """
                query{
                    node(id: "%s") {
                        ... on ProjectV2 {
                            fields(first: 20) {
                                nodes {
                                    ... on ProjectV2Field {
                                        id
                                        name
                                    }
                                    ... on ProjectV2SingleSelectField {
                                        id
                                        name
                                        options {
                                            id
                                            name
                                        }
                                    }
                                    ... on ProjectV2IterationField {
                                      id
                                      name
                                      configuration {
                                        iterations {
                                          startDate
                                          id
                                        }
                                      }
                                    }
                                }
                            }
                        }
                    }
                }
                """
            % id_
        )

        # Set the request data as a dictionary
        data = {"query": query}

        # Send the API request
        response = requests.post(url, headers=headers, json=data)

        # Parse the response JSON
        response_json = json.loads(response.text)

        # Extract the data from the response JSON
        data = response_json.get("data")
        return data.get("node").get("fields").get("nodes")

    def _get_project_items(self, url: str, headers: dict, id_: str) -> dict:
        nodes = []

        query = (
            """
                query{
                  node(id: "%s") {
                    ... on ProjectV2 {
                      items(first: 20) {
                        nodes {
                          id
                          fieldValues(first: 100) {
                            nodes {
                              ... on ProjectV2ItemFieldTextValue {
                                text
                                field {
                                  ... on ProjectV2FieldCommon {
                                    name
                                  }
                                }
                              }
                              ... on ProjectV2ItemFieldIterationValue {
                                title
                                iterationId
                              }
                              ... on ProjectV2ItemFieldDateValue {
                                date
                                field {
                                  ... on ProjectV2FieldCommon {
                                    name
                                  }
                                }
                              }
                              ... on ProjectV2ItemFieldSingleSelectValue {
                                name
                                field {
                                  ... on ProjectV2FieldCommon {
                                    name
                                  }
                                }
                              }
                            }
                          }
                          content {
                            ... on Issue {
                              title
                              body
                              number
                              labels(first: 10) {
                                edges {
                                  node {
                                    name
                                  }
                                }
                              }
                              assignees(first: 10) {
                                nodes {
                                  login
                                }
                              }
                            }
                          }
                        }
                        pageInfo {
                          endCursor
                          hasNextPage
                        }
                      }
                    }
                  }
                }
                """
            % id_
        )

        # Set the request data as a dictionary
        data = {"query": query}

        # Send the API request
        response = requests.post(url, headers=headers, json=data)

        # Parse the response JSON
        response_json = json.loads(response.text)

        nodes.extend(response_json.get("data").get("node").get("items").get("nodes"))

        # Extract the data from the response JSON
        pageInfo = response_json.get("data").get("node").get("items").get("pageInfo")

        while pageInfo.get("hasNextPage"):
            next_query = """
                            query{
                              node(id: "%s") {
                                ... on ProjectV2 {
                                  items(first: 20, after: "%s") {
                                    nodes {
                                      id
                                      fieldValues(first: 100) {
                                        nodes {
                                          ... on ProjectV2ItemFieldTextValue {
                                            text
                                            field {
                                              ... on ProjectV2FieldCommon {
                                                name
                                              }
                                            }
                                          }
                                          ... on ProjectV2ItemFieldIterationValue {
                                            title
                                            iterationId
                                          }
                                          ... on ProjectV2ItemFieldDateValue {
                                            date
                                            field {
                                              ... on ProjectV2FieldCommon {
                                                name
                                              }
                                            }
                                          }
                                          ... on ProjectV2ItemFieldSingleSelectValue {
                                            name
                                            field {
                                              ... on ProjectV2FieldCommon {
                                                name
                                              }
                                            }
                                          }
                                        }
                                      }
                                      content {
                                        ... on Issue {
                                          title
                                          body
                                          number
                                          labels(first: 10) {
                                            edges {
                                              node {
                                                name
                                              }
                                            }
                                          assignees(first: 10) {
                                            nodes {
                                              login
                                            }
                                          }
                                        }
                                      }
                                    }
                                    pageInfo {
                                      endCursor
                                      hasNextPage
                                    }
                                  }
                                }
                              }
                            }
                            """ % (
                id_,
                pageInfo.get("endCursor"),
            )

            # Set the request data as a dictionary
            data = {"query": next_query}

            # Send the API request
            response = requests.post(url, headers=headers, json=data)

            # Parse the response JSON
            response_json = json.loads(response.text)

            nodes.extend(
                response_json.get("data").get("node").get("items").get("nodes")
            )

            # Extract the data from the response JSON
            pageInfo = (
                response_json.get("data").get("node").get("items").get("pageInfo")
            )

        node_dict = {}

        for node in nodes:
            if not node["content"].get("number"):
                continue

            issue_number = node["content"]["number"]
            node_dict[issue_number] = node

        return node_dict

    def _process_nodes(self):
        """
        Returns a list of node tuples for node types specified in the
        adapter constructor.
        """

        logger.info("Generating nodes.")

        # Fields
        for field in self._fields:
            if not field:
                continue
            if field["name"] not in [
                "Status",
                "Size",
                "Priority",
            ]:
                continue

            for option in field["options"]:
                name = option["name"].lower()
                type = field["name"].lower()

                self._nodes.append((name, type, {}))

        # Individual cards
        for key, value in self._items.items():
            # add fields to item
            fields = [
                field
                for field in value.get("fieldValues", {}).get("nodes", [])
                if field
            ]

            for field in fields:
                if field.get("iterationId"):
                    field_type = "Iteration"
                    value["Iteration"] = field["title"]
                    value["Iteration ID"] = field["iterationId"]
                else:
                    field_type = field["field"]["name"]
                    value[field_type] = field.get("text") or field.get("name")

            # add labels to item
            labels = [
                label["node"]["name"]
                for label in value.get("content", {}).get("labels", {}).get("edges", [])
            ]

            value["labels"] = labels

            # add assignees to item
            assignees = [
                assignee["login"]
                for assignee in value.get("content", {})
                .get("assignees", {})
                .get("nodes", [])
            ]

            value["Assignees"] = assignees

            # if issue, add IssueNumber
            if value.get("content").get("number"):
                value["IssueNumber"] = "project-planning" + str(
                    value.get("content").get("number")
                )

            # add back to _items
            self._items[key] = value

            title = value.get("Title")

            if not title:
                logger.warning(f"Item {value['id']} has no title.")
                continue

            description = value.get("content").get("body", "")

            label = self._get_label()

            self._nodes.append(
                (
                    value["id"],
                    label,
                    {
                        "title": title,
                        "description": description,
                        "labels": labels,
                        "status": value.get("Status"),
                        "size": value.get("Size"),
                        "priority": value.get("Priority"),
                        "iteration": value.get("Iteration"),
                        "assignees": value.get("Assignees"),
                        "issue_number": value.get("IssueNumber"),
                    },
                )
            )

            # Create Iteration node
            if value.get("Iteration"):
                iteration_id = value.get("Iteration ID")
                if iteration_id not in [node[0] for node in self._nodes]:
                    self._nodes.append(
                        (
                            iteration_id,
                            "iteration",
                            {
                                "title": value.get("Iteration"),
                            },
                        )
                    )

            # Create edges from item to iteration
            if value.get("Iteration"):
                self._edges.append(
                    (
                        None,
                        value["id"],
                        value.get("Iteration ID"),
                        "part of",
                        {},
                    )
                )

            # Retrieve all comments for the issue
            comments = self._get_comments(value.get("IssueNumber"))

            if comments:
                source_id = value["id"]
                recency = 0
                for comment in comments:
                    # add each author / body as an individual node and connect to the project node
                    comment_id = comment.get("id")
                    text = (
                        comment.get("author").get("login") + ": " + comment.get("body")
                    )
                    self._nodes.append(
                        (
                            comment_id,
                            "comment",
                            {"text": text},
                        )
                    )
                    self._edges.append(
                        (
                            None,
                            source_id,
                            comment_id,
                            "has comment",
                            {"recency": recency},
                        )
                    )
                    recency += 1

        # Edges to fields
        for key, value in self._items.items():
            for assignee in value.get("Assignees", []):
                # check if assignee is in the first element of the list of tuples that is self._nodes
                if assignee not in [node[0] for node in self._nodes]:
                    self._nodes.append((assignee, "person", {"name": assignee}))

                self._edges.append((None, assignee, value["id"], "leads", {}))

    def _get_comments(self, issue_number, k: int = 10):
        """
        Get all comments for a given issue, up to k most recent.

        Args:
            issue_number: The issue number to get comments for.
            k: The number of most recent comments to get.
        """
        try:
            number = int(issue_number.split("project-planning")[1])
        except (IndexError, ValueError):
            logger.warning(f"Could not extract number from {issue_number}.")
            return

        query = """
          query {
            repository(owner: "biocypher", name: "project-planning") {
              issue(number: %s) {
                comments(last: %s) {
                  nodes {
                    author {
                      login
                    }
                    id
                    body
                  }
                }
              }
            }
          }
        """ % (
            number,
            k,
        )

        # Set the request data as a dictionary
        data = {"query": query}

        # Send the API request
        response = requests.post(self.url, headers=self.headers, json=data)

        # Parse the response JSON
        response_json = json.loads(response.text)

        # Extract the data from the response JSON
        data = (
            response_json.get("data")
            .get("repository")
            .get("issue")
            .get("comments")
            .get("nodes")
        )

        return data

    def _get_label(self):
        """
        Get the label for the node. Just returns project for now.
        """

        return "project"

    def _process_edges(self):
        """
        Returns a list of edge tuples for edge types specified in the
        adapter constructor.
        """

        logger.info("Generating edges.")

        for value in self._items.values():
            continue
            uses = self._extract_uses(value["content"]["body"])

            parent = "i" + str(value["content"]["number"])

            for use in uses:
                if not use:
                    continue

                part = use.replace("#", "i")

                self._edges.append((None, part, parent, "part of", {}))

                # also connect pipelines to the adapter's data type
                if value.get("Component Type") == "Pipeline":
                    if not self._items.get(part):
                        logger.warning(f"Could not find {part} in items.")
                        continue

                    data_type = self._items.get(part).get("Data Type")

                    if not data_type:
                        continue

                    self._edges.append((None, parent, data_type.lower(), "uses", {}))

    def _extract_uses(self, body) -> list:
        """
        Extract the uses from the body of the item.
        """

        if not body:
            return []

        lines = body.split("\n")

        for line in lines:
            if line.startswith("Uses:"):
                uses = line.split(": ")[1]

                return uses.split(" ")

        return []

    def get_node_count(self):
        """
        Returns the number of nodes generated by the adapter.
        """
        return len(self.get_nodes())

    def _set_types_and_fields(self, node_types, node_fields, edge_types, edge_fields):
        if node_types:
            self.node_types = node_types
        else:
            self.node_types = [type for type in GitHubAdapterNodeType]

        if node_fields:
            self.node_fields = node_fields
        else:
            self.node_fields = [
                field
                for field in chain(
                    GitHubAdapterProjectField,
                )
            ]

        if edge_types:
            self.edge_types = edge_types
        else:
            self.edge_types = [type for type in GitHubAdapterEdgeType]

        if edge_fields:
            self.edge_fields = edge_fields
        else:
            self.edge_fields = [field for field in chain()]
