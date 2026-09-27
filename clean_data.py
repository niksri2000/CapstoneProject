import pandas as pd
import numpy as np
import os

def clean_data():
    # Ensure we look in the correct directory (/content/ is the default in Colab)
    input_path = 'pharmeasy_orders_raw.csv'
    if not os.path.exists(input_path) and os.path.exists('/content/pharmeasy_orders_raw.csv'):
        input_path = '/content/pharmeasy_orders_raw.csv'
        
    # Load the raw dataset
    df = pd.read_csv(input_path)
    initial_count = len(df)
    
    # 1. Remove exact duplicate rows (all 8 columns identical)
    df_no_dups = df.drop_duplicates()
    removed_duplicates = initial_count - len(df_no_dups)
    print(f"Removed {removed_duplicates} exact duplicate rows.")
    
    # Use a copy to avoid SettingWithCopy warnings
    df_clean = df_no_dups.copy()
    
    # 2. Normalize the region column: strip leading/trailing whitespace and title-case it
    df_clean['region'] = df_clean['region'].astype(str).str.strip().str.title()
    
    # 3. Impute missing category using product -> category lookup table
    # Build lookup from rows where category is not missing/empty
    valid_cat_df = df_clean[df_clean['category'].notna() & (df_clean['category'] != "") & (df_clean['category'] != "nan")]
    prod_cat_map = dict(zip(valid_cat_df['product'], valid_cat_df['category']))
    
    # Fill missing or empty category values
    df_clean['category'] = df_clean['category'].fillna('')
    df_clean.loc[df_clean['category'] == '', 'category'] = df_clean['product'].map(prod_cat_map)
    
    # 4. Impute missing profit_inr using mean profit margin across each category
    # Cast to numeric to ensure math correctness
    df_clean['sales_inr'] = pd.to_numeric(df_clean['sales_inr'])
    df_clean['profit_inr'] = pd.to_numeric(df_clean['profit_inr'], errors='coerce')
    
    # Calculate profit margin for non-missing profit rows
    df_clean['profit_margin'] = df_clean['profit_inr'] / df_clean['sales_inr']
    
    # Compute category-wise mean profit margin
    category_margins = df_clean.groupby('category')['profit_margin'].mean().to_dict()
    
    # Fill missing profit_inr
    missing_profit_mask = df_clean['profit_inr'].isna()
    for idx, row in df_clean[missing_profit_mask].iterrows():
        cat = row['category']
        mean_margin = category_margins[cat]
        imputed_profit = round(row['sales_inr'] * mean_margin, 2)
        df_clean.at[idx, 'profit_inr'] = imputed_profit
        
    # Drop the temporary profit_margin column
    df_clean = df_clean.drop(columns=['profit_margin'])
    
    # Save the result as orders_clean.csv
    output_path = '/content/orders_clean.csv' if os.path.exists('/content') else 'orders_clean.csv'
    df_clean.to_csv(output_path, index=False)
    print(f"Cleaned dataset saved to {output_path} with {len(df_clean)} rows (originally {initial_count} rows).")
    return df_clean

# Run the cleaning function
cleaned_df = clean_data()

# Schema Validation
def validate_schema(df, required_columns):
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        return {
            "status": "blocked_schema",
            "row_count": len(df),
            "missing_columns": missing_cols
        }
    else:
        return {
            "status": "validated",
            "row_count": len(df),
            "missing_columns": []
        }

required_cols = ["order_id", "order_date", "region", "category", "product", "quantity", "sales_inr", "profit_inr"]

# 1. Run against the cleaned dataset
print("--- Validating Cleaned Dataset ---")
validation_result = validate_schema(cleaned_df, required_cols)
print(validation_result)

# 2. Run against a deliberately broken copy
print("\n--- Validating Deliberately Broken Dataset (Dropped 'profit_inr') ---")
broken_df = cleaned_df.drop(columns=["profit_inr"])
broken_result = validate_schema(broken_df, required_cols)
print(broken_result)