# Every Tueday at noon, calculate the schedule for the next week and update the
# GitHub project accordingly.

from biocypher import BioCypher
from scheduling.adapters.adapter import (
    GitHubAdapter,
    GitHubAdapterNodeType,
    GitHubAdapterEdgeType,
    GitHubAdapterIssueField,
)
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view as swv

pd.set_option("display.max_columns", None)


def main():
    bc = BioCypher()

    node_types = [
        GitHubAdapterNodeType.ISSUE,
    ]

    node_fields = [
        GitHubAdapterIssueField.NUMBER,
        GitHubAdapterIssueField.TITLE,
        GitHubAdapterIssueField.BODY,
    ]

    edge_types = [
        GitHubAdapterEdgeType.PART_OF,
    ]

    adapter = GitHubAdapter(
        node_types=node_types,
        node_fields=node_fields,
        edge_types=edge_types,
    )

    bc.add_nodes(adapter.get_nodes())
    bc.add_edges(adapter.get_edges())

    dfs = bc.to_df()

    for name, df in dfs.items():
        print(name)
        print(df.head())


if __name__ == "__main__":
    main()
