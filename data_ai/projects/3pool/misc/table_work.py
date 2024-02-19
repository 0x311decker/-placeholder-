import pandas as pd

# Load the file
file_path = r"C:\Users\Reilly Decker\Desktop\_3pool_liquidty_data.csv"
data = pd.read_csv(file_path)

# Initialize an empty list to hold the adjusted rows
adjusted_rows = []

# Iterate over each row in the DataFrame
for _, row in data.iterrows():
    event = row['event']
    transaction_hash = row['transactionHash']
    symbols = ['DAI', 'USDC', 'USDT']  # Assuming these are the symbols in order

    # Example for another nested column
    # You can replicate this approach for other nested columns as needed
    fees = eval(row['feesNormalized']) if pd.notna(row['feesNormalized']) else [None, None, None]

    # Check if the event requires splitting
    if event in ['AddLiquidity', 'RemoveLiquidity', 'RemoveLiquidityImbalance']:
        amounts = eval(row['tokenAmountsNormalized']) if pd.notna(row['tokenAmountsNormalized']) else [None, None, None]
        for i, symbol in enumerate(symbols):
            new_row = row.copy()
            new_row['transactionHash'] = f"{transaction_hash}_{i+1}"
            if event == 'AddLiquidity':
                new_row['suppliedTokenSymbol'] = symbol
                new_row['redeemedTokenSymbol'] = None
            else:
                new_row['redeemedTokenSymbol'] = symbol
                new_row['suppliedTokenSymbol'] = None
            new_row['tokenAmountNormalized'] = amounts[i]
            # Assigning the unnested value from the additional nested column
            new_row['feesNormalized'] = fees[i]
            adjusted_rows.append(new_row)
    else:
        new_row = row.copy()
        new_row['transactionHash'] = f"{transaction_hash}_1"
        # It's possible you don't need to adjust these for non-split rows, or you might set them to a default value
        adjusted_rows.append(new_row)

# Create a new DataFrame from the adjusted rows
adjusted_df = pd.DataFrame(adjusted_rows)

# Save the adjusted DataFrame to a new CSV file
adjusted_file_path = r"C:\Users\Reilly Decker\Desktop\_3pool_liquidty_data_v2.csv"
adjusted_df.to_csv(adjusted_file_path, index=False)
