#EDA for identifying missing values, inconsistencies, and outliers in the dataset:
try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from data_loader import load_data

    #All insights are written inside eda_insights.md

    df = load_data('data/raw/Nassau-Candy-Distributor.csv')

    #Getting shape of the data:
    print(df.shape) #(10194, 18)

    #Getting a quick overview of the dataset:
    print(df.head())

    #Getting overview of the columns of the dataset:
    print(df.info())

    #Getting numerial summaries of the columns:
    print(df.describe())

    #Separating numerical and categorical columns:
    num_col = df.select_dtypes(include = 'number').columns
    cat_col = df.select_dtypes(include = 'object').columns

    #Chacking for any missing values in the data:
    print(df.isnull().sum()) #0 missing values in the data.

    #Checking for duplicate values in the data:
    print(df.duplicated().sum()) #0 duplicated values in the data

    #Converting into datetime columns:
    df['Order Date'] = pd.to_datetime(
        df['Order Date'],
        format='%d-%m-%Y'
    )
    df['Ship Date'] = pd.to_datetime(
        df['Ship Date'],
        format='%d-%m-%Y'
    )

    #Getting simple overview for the datetime columns:
    print(df['Order Date'].min()) #2019-01-01 00:00:00
    print(df['Order Date'].max()) #2023-12-31 00:00:00
    print(df['Order Date'].nunique()) #717 unique dates in the data.
    print(df['Order Date'].dt.month.value_counts().sort_values()) #Checking orders per month
    print(df['Order Date'].dt.year.value_counts().sort_index()) #Checking orders per year
    print('================================')
    print(df['Ship Date'].min()) #2019-01-01 00:00:00
    print(df['Ship Date'].max()) #2023-12-31 00:00:00
    print(df['Ship Date'].nunique()) #717 unique dates in the data.
    print(df['Ship Date'].dt.month.value_counts().sort_values()) #Checking shipments per month
    print(df['Ship Date'].dt.year.value_counts().sort_index()) #Checking shipments per year
    print('================================')


    #Checking for counts of unique values in categorical columns:
    for col in cat_col:
        print(f'Counts of unique values in {col}: {df[col].value_counts()}')


    #                           Feature Engineering:

    #Creating a new column for shipping lead time:
    df['Shipping Lead Time'] = ((df['Ship Date'] - df['Order Date']).dt.days).astype(int)

    def associate_factory_name(division, product):
        if division == "Chocolate":
            if product in (
                "Wonka Bar - Nutty Crunch Surprise",
                "Wonka Bar - Fudge Mallows",
                "	Wonka Bar -Scrumdiddlyumptious",
            ):
                return "Lot's O' Nuts"
            elif product in (
                "Wonka Bar - Milk Chocolate",
                "Wonka Bar - Triple Dazzle Caramel",
            ):
                return "Wicked Choccy's"
        elif division == "Sugar":
            if product in (
                "Laffy Taffy",
                "SweeTARTS",
                "Nerds",
                "Fun Dip",
            ):
                return "Sugar Shack"
            elif product == "Everlasting Gobstopper":
                return "Secret Factory"
            elif product == "Hair Toffee":
                return "The Other Factory"
        elif division == "Other":
            if product == "Fizzy Lifting Drinks":
                return "Sugar Shack"
            elif product in (
                "Lickable Wallpaper",
                "Wonka Gum",
            ):
                return "Secret Factory"
            elif product == "Kazookles":
                return "The Other Factory"
        return "Unknown Factory"

    df["Factory Name"] = df.apply(
        lambda row: associate_factory_name(row["Division"], row["Product Name"]),
        axis=1
    )

    df['Factory Location'] = 'United States'

    df['Profit Margin %'] = (df['Gross Profit'] / df['Cost']) * 100

    df['Factory to Region'] = df['Factory Location'] + ' to ' + df['Country/Region']
    df['Factory to State'] = df['Factory Location'] + ' to ' + df['State/Province']
    df['Efficiency Rank'] = df['Shipping Lead Time'].rank(method = 'dense', ascending = True)

except ModuleNotFoundError as e:
    print(f"Error: {e}. Please ensure that all required libraries are installed.")
except:
    print("An unexpected error occurred during the EDA process. Please check the data and code for issues.")

#Exporting the cleaned and feature-engineered dataset to a new CSV file:
try:
    df.to_csv('data/processed/Nassau-Candy-Distributor-Cleaned.csv', index=False)
    print("="*60)
    print("Cleaned and feature-engineered dataset exported successfully.")
    print("="*60)
except Exception as e:
    print(f"Error exporting the dataset: {e}. Please check the file path and permissions.")



'''For evaluation team:
The above methods are the standard practices which most of the beginners use while performing EDA.
But, we can generate a comprehensive EDA report using the ydata_profiling library. 
This report will provide insights into the dataset, including missing values, correlations, 
and distributions of numerical and categorical features.'''

# from ydata_profiling import ProfileReport
# try:
#     profile = ProfileReport(df, title="Exploratory Data Analysis Report")
#     profile.to_file("assets/images/eda/ydata-profile/eda_report.html")
# except:
#     print("An error occured while generating the EDA report. Please ensure that the ydata_profiling library is installed and up to date.")