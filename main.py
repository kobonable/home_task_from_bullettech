import pandas as pd
from ohlc_generator import generate_ohlc_data_by_date, save_ohlc_data_to_file
from ohlc_metrics_enrichment import agg_to_5min, agg_to_30min, agg_to_1day, add_moving_average, add_moving_median


def main():
    print("Starting OHLC Data Generation and Aggregation Script")
    print("\n[Step 1/4] Generating 1-minute simulated OHLC data...")
    original_df = generate_ohlc_data_by_date()
    print(f"Successfully generated {len(original_df)} 1-minute OHLC bars.")

    print("[Step 2/4] Saving 1-minute OHLC data to 'ohlc_original_data.csv'...")
    save_ohlc_data_to_file(original_df, 'result_data/ohlc_original_data.csv')
    print("1-minute OHLC data saved.")

    print("\n[Step 3/4] Processing 5-minute aggregated data...")
    df_5min = original_df.copy()
    df_5min = agg_to_5min(df_5min)
    print(f"Aggregated data to {len(df_5min)} 5-minute bars.")
    df_5min = add_moving_average(df_5min, window_size_minutes=30, bar_interval_minutes=5)
    df_5min = add_moving_median(df_5min, window_size_minutes=30, bar_interval_minutes=5)
    print("Added 30-minute moving average and median to 5-minute bars.")
    save_ohlc_data_to_file(df_5min, 'result_data/ohlc_5min_data.csv')
    print("5-minute OHLC data saved to 'ohlc_5min_data.csv'.")

    print("\n[Step 3/4] Processing 30-minute aggregated data...")
    df_30min = original_df.copy()
    df_30min = agg_to_30min(df_30min)
    print(f"Aggregated data to {len(df_30min)} 30-minute bars.")
    df_30min = add_moving_average(df_30min, window_size_minutes=30, bar_interval_minutes=30)
    df_30min = add_moving_median(df_30min, window_size_minutes=30, bar_interval_minutes=30)
    print("Added 30-minute moving average and median to 30-minute bars.")
    save_ohlc_data_to_file(df_30min, 'result_data/ohlc_30min_data.csv')
    print("30-minute OHLC data saved to 'ohlc_30min_data.csv'.")

    print("\n[Step 4/4] Processing 1-day aggregated data...")
    df_1day = original_df.copy()
    df_1day = agg_to_1day(df_1day)
    print(f"Aggregated data to {len(df_1day)} 1-day bars.")

    save_ohlc_data_to_file(df_1day, 'result_data/ohlc_1day_data.csv')
    print("1-day OHLC data saved to 'ohlc_1day_data.csv'.")

    print("\nScript execution completed successfully!")

if __name__ == "__main__":
    main()