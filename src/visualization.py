try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from data_loader import load_data

    df = load_data('data/processed/Nassau-Candy-Distributor-Cleaned.csv')

    #Separating numerical and categorical columns:
    num_col = df.select_dtypes(include = 'number').columns
    cat_col = df.select_dtypes(include = 'object').columns

    #                     Univariate analysis:
    # Checking for outliers in the numerical columns using boxplots:
    for col in num_col:
        plt.figure(figsize=(10, 5))
        sns.boxplot(x=df[col])
        plt.title(f'Boxplot for {col}')
        plt.savefig(f'assets/images/eda/univariate/boxplot_{col}.png',
                    dpi = 300,
                    format = 'png',
                    bbox_inches = 'tight',
                    facecolor = 'white',
                    edgecolor = 'black'
                    )  # Saving the boxplot as an image to the desired path.
        plt.close()  # Closing the figure to free up memory.

    #                     Bivariate analysis:
    #Checking for correlation between numerical columns:
    sns.heatmap(df.corr(numeric_only = True), annot=True, cmap='coolwarm')
    plt.title('Correlation Heatmap')
    plt.savefig('assets/images/eda/bivariate/correlation_heatmap.png',
                dpi = 300,
                format = 'png',
                bbox_inches = 'tight',
                facecolor = 'white',
                edgecolor = 'black'
                )
    plt.close()  

    #                      Multivariate analysis:
    # Pivot Table to calculate average shipping lead time per lane
    route_matrix = df.pivot_table(
        values='Shipping Lead Time', 
        index='Factory Location', 
        columns='Country/Region', 
        aggfunc='mean'
    )
    sns.heatmap(route_matrix, annot=True, cmap='coolwarm', fmt=".1f")
    plt.title("Average Shipping Lead Time by Route Logistics")
    plt.savefig("assets/images/eda/multivariate/shipping_bottlenecks.png", 
                dpi = 300,
                bbox_inches='tight',
                facecolor='white',
                edgecolor='black'
                )

except ModuleNotFoundError as e:
    print(f"Error: {e}. Please ensure that all required libraries are installed.")
except Exception as e:
    print(f"An unexpected error occurred during the visualization process: {e}. Please check the data and code for issues.")