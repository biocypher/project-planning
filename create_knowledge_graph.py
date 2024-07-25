from biocypher import BioCypher
from scheduling.adapters.github_adapter import GitHubAdapter
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)


def main():
    bc = BioCypher()

    adapter = GitHubAdapter()

    bc.add_nodes(adapter.get_nodes())
    bc.add_edges(adapter.get_edges())

    dfs = bc.to_df()

    for name, df in dfs.items():
        print(name)
        print(df.head())


if __name__ == "__main__":
    main()
