import pandas as pd
import matplotlib.pyplot as plt

from price_scraper import Repository
from price_scraper.repository.io import IO_DIR

IO_DIR = IO_DIR.parent / 'reports'

dtypes = dict(
    short_name='string', 
    source='string', 
    price='float',
    created_at='datetime64[ns]')

def make():
    records = Repository.list()
    df = pd.DataFrame(records, columns=dtypes.keys()).astype(dtypes)
    # df['created_at'] = pd.to_datetime(df['created_at'])
    df['created_date'] = df.created_at.dt.date

    fig, ax = plt.subplots(nrows=len(df.short_name.unique()), figsize=(8, 12), squeeze=False)
    for i, product_name in enumerate(df.short_name.unique()):
        plt_df = df[
            df.short_name == product_name
        ].groupby(
            ['created_date', 'source']
        ).mean(numeric_only=True).reset_index()
        plt_df = plt_df.pivot(index='created_date', columns='source', values='price')
        plt_df.plot(ax=ax[i][0], title=product_name)
    plt.savefig(IO_DIR / 'index.svg', format='svg')


if __name__ == '__main__':
    make()