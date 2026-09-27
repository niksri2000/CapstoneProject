Data Quality Report
This report maps each of the data cleaning steps implemented in clean_data() to the specific data-quality dimension it addresses:

1. Removing Exact Duplicate Rows
Dimension Addressed: Uniqueness
Description: Removing duplicate entries ensures that each transaction is represented exactly once in the dataset, preventing double-counting and maintaining the statistical integrity of downstream aggregations.
2. Normalizing the Region Column
Dimension Addressed: Consistency (and Validity)
Description: Stripping whitespace and applying title-case formatting collapses messy variants (such as hyderabad, HYDERABAD , and Hyderabad) into canonical values. This establishes consistent grouping keys and ensures that every region matches the standard naming convention stored in regions_master.csv.
3. Imputing Missing Categories via Product-to-Category Mapping
Dimension Addressed: Completeness (and Accuracy)
Description: Missing values are populated deterministically using an exact 1:1 lookup table built from complete records. This restores missing categorical data without introducing arbitrary bias or dropping valuable rows.
4. Imputing Missing Profit Values via Mean Margin Imputation
Dimension Addressed: Completeness (and Accuracy)
Description: Replacing missing numerical values (profit_inr) with a calculated estimate ( sales_inr×category_mean_margin ) preserves the size of the dataset while maintaining reasonable category-level margin profiles for financial calculations.
