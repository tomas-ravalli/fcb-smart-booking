import pandas as pd
import numpy as np
import datetime
import random
import os

def generate_club_members_data(
    num_matches=10,
    num_days=90,
    zones=['A', 'B', 'C', 'D'],
    seats_per_zone=5000,
    avg_release_rate=0.40
):
    """
    Generates a synthetic dataset of seat releases from a club members app.

    Args:
        num_matches (int): The number of unique matches to generate data for.
        num_days (int): The time-series window (in days) before each match.
        zones (list): A list of seating zone identifiers.
        seats_per_zone (int): The total number of seats available in each zone.
        avg_release_rate (float): The average percentage of seats that will be released.

    Returns:
        pandas.DataFrame: A DataFrame containing the synthetic seat release data.
    """
    print("Starting dataset generation...")
    all_releases = []
    
    # Generate a base pool of member and seat IDs to sample from
    total_seats = seats_per_zone * len(zones)
    member_ids = range(100001, 100001 + total_seats)
    seat_ids_by_zone = {
        zone: range(
            (i * seats_per_zone) + 1, ((i + 1) * seats_per_zone) + 1
        ) for i, zone in enumerate(zones)
    }

    # Set the match day as a fixed future date for reproducibility
    match_day_zero = datetime.datetime(2025, 10, 26)

    for match_id in range(1, num_matches + 1):
        print(f"  Generating data for match_id: {match_id}...")
        match_date = match_day_zero + datetime.timedelta(days=match_id * 14) # Stagger matches

        for zone_id in zones:
            # 1. Determine total seats to be released for this match/zone
            # Introduce some randomness around the average release rate
            release_rate_for_match = np.random.normal(avg_release_rate, 0.05)
            n_releases = int(seats_per_zone * release_rate_for_match)

            # 2. Sample unique seats and members for these releases
            released_seat_ids = random.sample(seat_ids_by_zone[zone_id], n_releases)
            releasing_member_ids = random.sample(member_ids, n_releases)

            # 3. Generate release timestamps with a strong bias towards match day
            # We use a beta distribution with alpha=1, beta=5 to skew releases closer to day 0
            # This creates the realistic "last-minute" release pattern.
            days_before_match = np.random.beta(a=1, b=5, size=n_releases) * num_days
            
            for i in range(n_releases):
                # Calculate the exact release timestamp
                delta_seconds = days_before_match[i] * 24 * 60 * 60
                release_time = match_date - datetime.timedelta(seconds=delta_seconds)
                
                all_releases.append({
                    'match_id': match_id,
                    'seat_id': released_seat_ids[i],
                    'zone_id': zone_id,
                    'member_id': releasing_member_ids[i],
                    'release_timestamp': release_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'released': 1
                })

    print("Generation complete. Creating DataFrame...")
    df = pd.DataFrame(all_releases)
    
    # Sort the data logically
    df['release_timestamp'] = pd.to_datetime(df['release_timestamp'])
    df = df.sort_values(by=['match_id', 'release_timestamp']).reset_index(drop=True)
    
    return df

if __name__ == '__main__':
    # --- Configuration ---
    OUTPUT_FILENAME = 'data/03_synthetic/club_members_app.csv'

    # --- Execution ---
    synthetic_data = generate_club_members_data()
    
    # --- Save to CSV ---
    # Ensure the output directory exists
    output_dir = os.path.dirname(OUTPUT_FILENAME)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    synthetic_data.to_csv(OUTPUT_FILENAME, index=False)
    print(f"\nSuccessfully generated synthetic data.")
    print(f"Total rows: {len(synthetic_data)}")
    print(f"Saved to '{OUTPUT_FILENAME}'")
    print("\n--- Sample of the data ---")
    print(synthetic_data.head())
    print("\n--- Data summary ---")
    print(synthetic_data.info())