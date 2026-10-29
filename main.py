import pandas as pd
import matplotlib.pyplot as plt
import os
import logging

# Setup basic error logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def load_data(file_path):
    """Loads the dataset with error handling."""
    try:
        df = pd.read_csv(file_path)
        logging.info("Data loaded successfully.")
        return df
    except FileNotFoundError:
        logging.error(f"File '{file_path}' not found. Ensure it is in the 'data/' directory.")
        return None
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return None

def clean_data(df):
    """Cleans and prepares data for analysis."""
    try:
        df['Date'] = pd.to_datetime(df['Date'])
        # Drop any missing rows for clean visualization
        df.dropna(inplace=True)
        # Create a Year-Month column for trend analysis
        df['Month'] = df['Date'].dt.to_period('M')
        logging.info("Data cleaned successfully.")
        return df
    except Exception as e:
        logging.error(f"Error cleaning data: {e}")
        return None

def create_visualizations(df, output_dir="visualizations"):
    """Generates and saves the required charts."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # 1. Bar Chart: Sales by Product
        product_sales = df.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False)
        plt.figure(figsize=(10, 6))
        product_sales.plot(kind='bar', color='#4A90E2')
        plt.title('Total Sales by Product Category', fontsize=14, fontweight='bold')
        plt.xlabel('Product', fontsize=12)
        plt.ylabel('Total Sales ($)', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/product_sales_bar.png")
        plt.close()

        # 2. Line Chart: Monthly Revenue Trend
        monthly_sales = df.groupby('Month')['Total_Sales'].sum()
        plt.figure(figsize=(10, 6))
        monthly_sales.plot(kind='line', marker='o', color='#E24A4A', linewidth=2)
        plt.title('Monthly Sales Trend (Jan-Apr 2024)', fontsize=14, fontweight='bold')
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Total Sales ($)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/monthly_sales_line.png")
        plt.close()

        # 3. Pie Chart: Sales Distribution by Region
        region_sales = df.groupby('Region')['Total_Sales'].sum()
        plt.figure(figsize=(8, 8))
        colors = ['#FFD700', '#98FB98', '#FFB6C1', '#87CEFA']
        region_sales.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=colors)
        plt.title('Sales Distribution by Region', fontsize=14, fontweight='bold')
        plt.ylabel('') 
        plt.tight_layout()
        plt.savefig(f"{output_dir}/region_sales_pie.png")
        plt.close()

        logging.info("Visualizations saved to the 'visualizations/' folder.")
    except Exception as e:
        logging.error(f"Error generating visualizations: {e}")

def main():
    print("Starting Data Analysis Pipeline...")
    project_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(project_dir, 'sales_data (1).csv')

    if not os.path.exists(data_file):
        data_file = os.path.join(project_dir, 'data', 'sales_data (1).csv')

    df = load_data(data_file)
    
    if df is not None:
        df = clean_data(df)
        
        if df is not None:
            create_visualizations(df)
            
            # Print basic terminal insights
            print("\n--- Basic Analysis Summary ---")
            print(f"Total Revenue: ${df['Total_Sales'].sum():,.2f}")
            print(f"Top Selling Product: {df.groupby('Product')['Total_Sales'].sum().idxmax()}")
            print(f"Top Performing Region: {df.groupby('Region')['Total_Sales'].sum().idxmax()}")
            print("------------------------------")
            print("Pipeline completed successfully.")

if __name__ == "__main__":
    main()