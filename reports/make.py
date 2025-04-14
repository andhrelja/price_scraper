import pandas as pd
import matplotlib.pyplot as plt
import logging

from price_scraper.repository import Product
from price_scraper.repository.io import REPOSITORY_IO_PATH

IO_DIR = REPOSITORY_IO_PATH.parent / "reports"
logger = logging.getLogger("reports.make")

dtypes = dict(
    short_name="string",
    source="string",
    price="float",
    created_at="datetime64[ns]",
    product_type="string",
)


def _plot_price(df, product_type):
    nrows = len(df.short_name.unique())
    fig, ax = plt.subplots(nrows=nrows, figsize=(8, nrows * 2), squeeze=False)
    for i, product_name in enumerate(df.short_name.unique()):
        plt_df = (
            df[df.short_name == product_name]
            .groupby(["created_date", "source"])
            .mean(numeric_only=True)
            .reset_index()
        )
        plt_df = plt_df.pivot(index="created_date", columns="source", values="price")
        plt_df.plot(ax=ax[i][0], title=product_name, rot=30)
        ax[i][0].set_xlabel("Price date")
        # handles, labels = ax[i][0].get_legend_handles_labels()
        # ax[i][0].legend(handles=handles[1:], labels=labels[1:])
    fig.tight_layout()
    plt.savefig(IO_DIR / f"{product_type}.svg", format="svg")


def make():
    records = Product.list()
    df = pd.DataFrame(records, columns=dtypes.keys()).astype(dtypes)
    # df['created_at'] = pd.to_datetime(df['created_at'])
    df["created_date"] = df.created_at.dt.date

    for product_type in df.product_type.unique():
        logger.info(f"Generating report for {product_type}")
        _plot_price(df[df.product_type == product_type], product_type)
        logger.info(f"Report generated for {product_type}")


if __name__ == "__main__":
    make()
