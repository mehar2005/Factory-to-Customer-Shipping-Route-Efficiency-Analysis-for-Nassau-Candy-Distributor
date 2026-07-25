try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from data_loader import load_data

    df = load_data('data/processed/Nassau-Candy-Distributor-Cleaned.csv')

    print(df.groupby('Factory to Region')['Factory Name'].value_counts())
    print(df.groupby('Factory to State')['Factory Name'].value_counts())
    print(df.groupby('Factory to Region')['Shipping Lead Time'].mean())
    print(df.groupby('Factory to Region')['Shipping Lead Time'].max())
    print(df.groupby('Factory to Region')['Shipping Lead Time'].min())

    print(df['Factory Name'].value_counts())
    print(df['Product Name'].value_counts())
    print(df['Division'].value_counts())
    print(df['Profit Margin %'].value_counts())
    print(df.info())
    print(df.pivot_table(
        index = 'Factory to State',
        values = 'Shipping Lead Time',
        aggfunc = 'count'
    ).sort_values(by = 'Shipping Lead Time', ascending = True).head(10))

    print(df.pivot_table(
        index = 'Factory to State',
        values = 'Shipping Lead Time',
        aggfunc = 'count'
    ).sort_values(by = 'Shipping Lead Time', ascending = False).head(10))

    print(df[df['Shipping Lead Time'] > df['Shipping Lead Time'].mean()]['State/Province'].value_counts())
    print(df[(df['Shipping Lead Time'] > df['Shipping Lead Time'].mean()) & (df['Units'] > df['Units'].mean())]['State/Province'].value_counts())
    print(df.groupby('Ship Mode')['Shipping Lead Time'].mean())
    print(df.groupby('Ship Mode')['Cost'].mean())

except ModuleNotFoundError as e:
    print(f"Error: {e}. Please ensure that all required libraries are installed.")
except:
    print("An unexpected error occurred during the EDA process. Please check the data and code for issues.")
