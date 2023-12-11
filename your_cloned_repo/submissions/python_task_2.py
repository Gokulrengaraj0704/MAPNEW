def calculate_df(df)->pd.DataFrame():
    
    # Write your logic here
# Create a dictionary to store the distance matrix
  df = {}

  # Iterate over the DataFrame and populate the distance matrix
  for row in df.iterrows():
    start_id, end_id, distance = row[1]

    # Add the distance from the start ID to the end ID to the distance matrix
    if start_id not in df:
      df[start_id] = {}

    df[start_id][end_id] = distance

    # Add the distance from the end ID to the start ID to the distance matrix,
    # unless it is already present
    if end_id not in df[start_id]:
      df[start_id][end_id] = distance

    # Convert the distance matrix to a DataFrame
    df_df = pd.DataFrame(df)

    # Set the diagonal values of the distance matrix to 0
    df_df.values[np.diag_indices(len(df_df))] = 0

    # Return the distance matrix DataFrame
    return df_df



def unroll_df(df)->pd.DataFrame():

    # Write your logic here
    # Initialize lists to store unrolled data
    id_start_list = []
    id_end_list = []
    distance_list = []

    # Iterate over the entire DataFrame
    for i in range(len(df.index)):
        for j in range(i + 1, len(df.columns)):
            id_start = df.index[i]
            id_end = df.columns[j]
            dist_value = df.at[id_start, id_end]  # Use a different variable name

            # Append data to the lists
            id_start_list.append(id_start)
            id_end_list.append(id_end)
            distance_list.append(dist_value)

    # Create a DataFrame from the lists
    unrolled_df = pd.DataFrame({
        'id_start': id_start_list,
        'id_end': id_end_list,
        'distance': distance_list
    })

    return unrolled_df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():

    # Write your logic here
    for col in df.columns:
        if 'id_start' in col:
            id_start_col = col
            break
    else:
        raise ValueError("'id_start' column not found in the DataFrame.")

    # Filter DataFrame based on the reference value in the dynamically found 'id_start' column
    reference_df = df[df[id_start_col] == reference_value]

    # Check if the reference value exists in the DataFrame
    if reference_df.empty:
        raise ValueError(f"Reference value {reference_value} not found in the '{id_start_col}' column.")

    # Calculate the average distance for the reference value
    average_distance = reference_df['distance'].mean()

    # Calculate the lower and upper bounds for the 10% threshold
    lower_bound = average_distance - (average_distance * 0.1)
    upper_bound = average_distance + (average_distance * 0.1)

    # Filter DataFrame for values within the 10% threshold
    within_threshold_df = df[(df['distance'] >= lower_bound) & (df['distance'] <= upper_bound)]

    # Get the sorted list of values from the dynamically found 'id_start' column
    sorted_ids_within_threshold = within_threshold_df[id_start_col].unique().tolist()
    sorted_ids_within_threshold.sort()

    return sorted_ids_within_threshold


def calculate_toll_rate(df)->pd.DataFrame():
  
    # Wrie your logic here
    # Define rate coefficients for each vehicle type
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    # Find the column representing distance dynamically
    distance_column = None
    for col in df.columns:
        if 'distance' in col.lower():
            distance_column = col
            break

    # Check if a distance column is found
    if distance_column is None:
        raise KeyError("No column representing distance found in the DataFrame.")

    # Create columns for each vehicle type in the DataFrame
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df[distance_column] * rate_coefficient

    return df



def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
# Define time ranges and discount factors for weekdays and weekends
    weekday_time_ranges = [(time(0, 0, 0), time(10, 0, 0)), (time(10, 0, 0), time(18, 0, 0)), (time(18, 0, 0), time(23, 59, 59))]
    weekend_time_ranges = [(time(0, 0, 0), time(23, 59, 59))]
    weekday_discount_factors = [0.8, 1.2, 0.8]
    weekend_discount_factor = 0.7

    # Create columns for start_day, start_time, end_day, and end_time
    df['start_day'] = np.nan
    df['start_time'] = np.nan
    df['end_day'] = np.nan
    df['end_time'] = np.nan

    # Iterate over each unique (id_start, id_end) pair
    for _, group in df.groupby(['id_start', 'id_end']):
        id_start, id_end = _
        for day in range(7):
            start_date = datetime(2023, 1, 1) + timedelta(days=day)
            end_date = start_date + timedelta(days=1)

            # Set the time-based toll rates for weekdays
            if day < 5:  # Weekdays (Monday - Friday)
                for start_time, end_time in weekday_time_ranges:
                    df.loc[
                        (df['id_start'] == id_start) &
                        (df['id_end'] == id_end) &
                        (df['start_day'].isnull()) &
                        (df['end_day'].isnull()) &
                        (df['start_time'].isnull()) &
                        (df['end_time'].isnull()) &
                        (df['time'] >= datetime.combine(start_date, start_time)) &
                        (df['time'] < datetime.combine(end_date, end_time)),
                        ['start_day', 'start_time', 'end_day', 'end_time']
                    ] = [start_date.strftime('%A'), start_time, end_date.strftime('%A'), end_time]

                    # Apply discount factor to vehicle columns
                    for vehicle_type in ['moto', 'car', 'rv', 'bus', 'truck']:
                        df.loc[
                            (df['id_start'] == id_start) &
                            (df['id_end'] == id_end) &
                            (df['start_day'] == start_date.strftime('%A')) &
                            (df['end_day'] == end_date.strftime('%A')) &
                            (df['start_time'] == start_time) &
                            (df['end_time'] == end_time),
                            vehicle_type
                        ] *= weekday_discount_factors[weekday_time_ranges.index((start_time, end_time))]
    return df
