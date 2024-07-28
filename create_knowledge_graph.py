from biocypher import BioCypher
from project_planning.adapters.github_adapter import GitHubAdapter
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)


def main():
    bc = BioCypher()

    adapter = GitHubAdapter()

    # bc.add_nodes(adapter.get_nodes())
    # bc.add_edges(adapter.get_edges())

    # dfs = bc.to_df()

    # for name, df in dfs.items():
    #     print(name)
    #     print(df.head())

    bc.write_nodes(adapter.get_nodes())
    bc.write_edges(adapter.get_edges())
    bc.write_schema_info(as_node=True)
    bc.write_import_call()
    bc.summary()


if __name__ == "__main__":
    main()
