import pickle
import pandas as pd
from pathlib import Path
from typing import Union, Optional, List


DEFAULT_CSV_FILEPATH = Path(__file__).parent / "properties.csv"
DEFAULT_PKL_FILEPATH = DEFAULT_CSV_FILEPATH.parent / 'deeds.pkl'


def download_csv(local_file_path: Optional[Union[Path, str]]) -> Path:
    """
    Download the CSV file from the web and save it to the local file system.

    Parameters:
        local_file_path (Optional[Union[Path, str]]):
            The local file path where the CSV file should be saved. If not specified, the default path is used.
    """
    import requests

    url = "https://raw.githubusercontent.com/veekun/pokedex/master/pokedex/data/csv/pokemon.csv"
    local_file_path = local_file_path or DEFAULT_CSV_FILEPATH

    if not isinstance(local_file_path, (Path, str)):
        raise TypeError("local_file_path must be a string or Path object.")

    if not isinstance(local_file_path, Path):
        local_file_path = Path(local_file_path).expanduser().resolve().absolute()

    response = requests.get(url)
    response.raise_for_status()

    with open(local_file_path, 'wb') as file:
        file.write(response.content)

    return local_file_path



def load_csv_data(csv_file: Union[str, Path] = None) -> pd.DataFrame:
    """
    Load a CSV file into a pandas `DataFrame` object.

    Parameters:
        csv_file (Optional[Union[str, Path]]):
            The path to the CSV file to load. +If not specified, the default CSV file is used.
    """
    csv_file = csv_file or DEFAULT_CSV_FILEPATH

    if not isinstance(csv_file, (Path, str)):
        raise TypeError("csv_file must be a string or Path object.")

    if not isinstance(csv_file, Path):
        csv_file = Path(csv_file).expanduser().resolve().absolute()

    if not csv_file.is_file() or not csv_file.exists():
        raise FileNotFoundError(f"File not found: {csv_file}")

    return pd.read_csv(csv_file)


def save_csv_to_pickle(csv_file: Optional[Union[str, Path]] = None, pickle_file: Optional[Union[str, Path]] = None):
    """
    Save a CSV file to a pickle data file.
    """
    csv_file    = csv_file or DEFAULT_CSV_FILEPATH
    pickle_file = pickle_file or DEFAULT_PKL_FILEPATH

    df = load_csv_data(csv_file)

    return save_data_to_pickle(df, pickle_file)




def save_data_to_pickle(data: Union[pd.DataFrame, List[dict]], pickle_file: Optional[Union[str, Path]] = None) -> Path:
    pickle_file = pickle_file or DEFAULT_PKL_FILEPATH

    if not isinstance(pickle_file, (Path, str)):
        raise TypeError("pickle_file must be a string or Path object.")

    if not isinstance(pickle_file, Path):
        pickle_file = Path(pickle_file).expanduser().resolve().absolute()

    if not isinstance(data, (pd.DataFrame, list)):
        raise TypeError("data must be a pandas DataFrame or a list of dictionaries.")

    if isinstance(data, pd.DataFrame):
        data.to_pickle(pickle_file)
    else:
        with open(pickle_file, 'wb') as file:
            pickle.dump(data, file)

    return pickle_file