import pandas as pd
import numpy as np
import datetime
import os

def create_time_series_scaffold(num_matches=10, num_days=90, zones=['A', 'B', 'C', 'D']):
    """Creates a date scaffold to serve as the base for the time-series dataset."""
    print("Step 1: Creating the time-series scaffold...")
    scaffold_rows = []
    match_day_zero = datetime.datetime(2025, 10, 26)

    for match_id in range(1, num_matches + 1):
        match_date = match_day_zero + datetime.timedelta(days=match_id * 14)
        for days_before in range(num_days, 0, -1):
            prediction_date = match_date - datetime.timedelta(days=days_before)
            for zone_id in zones:
                scaffold_rows.append({
                    'match_id': match_id,
                    'zone_id': zone_id,
                    'prediction_date': prediction_date.date(),
                    'match_date': match_date.date(),
                    'days_until_match': days_before
                })
    print(f"  Scaffold created with {len(scaffold_rows)} rows.")
    return pd.DataFrame(scaffold_rows)

def calculate_time_dependent_features(scaffold_df, members_df):
    """Calculates time-dependent features like cumulative and rolling releases."""
    print("Step 2: Calculating time-dependent features...")
    
    # Ensure correct data types
    members_df['release_timestamp'] = pd.to_datetime(members_df['release_timestamp'])
    members_df['release_date'] = members_df['release_timestamp'].dt.date
    scaffold_df['prediction_date'] = pd.to_datetime(scaffold_df['prediction_date']).dt.date

    # Calculate daily releases from the raw data
    daily_releases = members_df.groupby(['match_id', 'zone_id', 'release_date']).size().reset_index(name='daily_releases')
    
    # Merge daily releases onto the scaffold
    ts_df = pd.merge(
        scaffold_df,
        daily_releases,
        how='left',
        left_on=['match_id', 'zone_id', 'prediction_date'],
        right_on=['match_id', 'zone_id', 'release_date']
    ).drop(columns=['release_date'])
    
    ts_df['daily_releases'] = ts_df['daily_releases'].fillna(0)
    
    # Calculate cumulative and rolling features
    ts_df = ts_df.sort_values(by=['match_id', 'zone_id', 'prediction_date'])
    ts_df['seats_released_so_far'] = ts_df.groupby(['match_id', 'zone_id'])['daily_releases'].cumsum()
    ts_df['release_velocity_7d'] = ts_df.groupby(['match_id', 'zone_id'])['daily_releases'].transform(lambda x: x.rolling(7, min_periods=1).sum())
    
    print("  Time-dependent features calculated.")
    return ts_df

def generate_static_features(num_matches=10):
    """Generates the static, contextual features for each match."""
    print("Step 3: Generating static features...")
    static_features = []
    for match_id in range(1, num_matches + 1):
        excitement_factor = np.random.uniform(0.1, 1.0)
        
        # Team Momentum
        p_win = 0.1 + 0.7 * excitement_factor
        p_draw = 0.15
        p_loss = 1.0 - p_win - p_draw
        
        static_features.append({
            'match_id': match_id,
            'opponent_position': np.random.randint(1, 21),
            'is_derby': np.random.choice([True, False], p=[0.1, 0.9]),
            'team_position': np.random.randint(1, 5),
            'last_match_lost': np.random.choice([True, False], p=[p_loss, 1 - p_loss]),
            'top_player_injured': np.random.choice([True, False], p=[1 - excitement_factor, excitement_factor]),
        })
    print("  Static features generated.")
    return pd.DataFrame(static_features)

if __name__ == '__main__':
    # --- Configuration ---
    MEMBERS_DATA_FILENAME = 'data/03_synthetic/club_members_app.csv'
    OUTPUT_FILENAME = 'data/03_synthetic/match_data_timeseries.csv'

    try:
        # Load the raw event data
        members_data = pd.read_csv(MEMBERS_DATA_FILENAME)
        
        # --- Build the Time-Series Dataset ---
        # 1. Create the base scaffold (match, zone, date)
        scaffold = create_time_series_scaffold()
        
        # 2. Calculate time-dependent features from raw events
        ts_data = calculate_time_dependent_features(scaffold, members_data)
        
        # 3. Generate static, contextual features for each match
        static_data = generate_static_features()
        
        # 4. Calculate the final target variable (total releases per match/zone)
        print("Step 4: Calculating final target variable...")
        target_data = members_data.groupby(['match_id', 'zone_id'])['released'].sum().reset_index(name='final_released_seats')
        
        # 5. Merge everything together
        print("Step 5: Merging all dataframes...")
        final_df = pd.merge(ts_data, static_data, on='match_id', how='left')
        final_df = pd.merge(final_df, target_data, on=['match_id', 'zone_id'], how='left')
        
        # --- Save to CSV ---
        output_dir = os.path.dirname(OUTPUT_FILENAME)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        final_df.to_csv(OUTPUT_FILENAME, index=False)
        
        print(f"\nSuccessfully generated the time-series dataset.")
        print(f"Total rows: {len(final_df)}")
        print(f"Saved to '{OUTPUT_FILENAME}'")
        print("\n--- Sample of the final data ---")
        pd.set_option('display.max_columns', None)
        print(final_df.tail())

    except FileNotFoundError:
        print(f"ERROR: The file '{MEMBERS_DATA_FILENAME}' was not found.")
        print("Please run the 'make_dataset_members.py' script first to generate it.")