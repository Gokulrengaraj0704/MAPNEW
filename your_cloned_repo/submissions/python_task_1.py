def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here

    # Create a pivot table with 'id_1' as index, 'id_2' as columns
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    # Set the diagonal values to 0
    for idx in car_matrix.index:
        car_matrix.at[idx, idx] = 0


    return car_matrix


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here

     # Create a new column 'car_type' based on the values of the 'car' column
    df['car_type'] = pd.cut(df['car'], bins=[0, 15, 25, 100], labels=['low', 'medium', 'high'])

    # Calculate the count of occurrences for each car type category
    type_counts = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    type_counts = dict(sorted(type_counts.items()))

    return type_counts


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    # Calculate the mean value of the 'bus' column
    bus_mean = df['bus'].mean()

    # Identify indices where the 'bus' values are greater than twice the mean value
    bus_indexes = df.index[df['bus'] > 2 * bus_mean].tolist()

    # Sort the indices in ascending order
    bus_indexes.sort()

    return bus_indexes
    


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    # Group by 'route' and calculate the mean of the 'truck' column for each route
    route_means = df.groupby('route')['truck'].mean()

    # Filter routes where the average of 'truck' column is greater than 7
    selected_routes = route_means[route_means > 7].index.tolist()
    selected_routes.sort()

    return selected_routes


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    # Copy the input matrix to avoid modifying the original DataFrame
    modified_matrix = matrix.copy()

    # Apply the multiplication logic based on the specified conditions
    modified_matrix = modified_matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Round the values to 1 decimal place
    modified_matrix = modified_matrix.round(1)

    return modified_matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series

    """
    # Write your logic here
    # Combine 'startDay' and 'startTime' columns and convert to datetime
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], format='%A %H:%M:%S', errors='coerce')

    # Combine 'endDay' and 'endTime' columns and convert to datetime
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], format='%A %H:%M:%S', errors='coerce')

    # Calculate the time difference for each (id, id_2) pair
    df['time_difference'] = df['end_timestamp'] - df['start_timestamp']

    # Check if each pair has incorrect timestamps
    incorrect_timestamps = df.groupby(['id', 'id_2'])['time_difference'].agg(
        lambda x: not (all(x.dt.total_seconds().between(0, 24 * 3600)) and all(day.days == 0 for day in x))
    )

    return incorrect_timestamps




