from pathlib import Path
import pickle
from typing import Union, List, Optional
from monopyly.models.deeds.color_group import ColorGroup


DEFAULT_DEED_FILE = Path(__file__).parent / 'deeds.pkl'


def load_deed_file(deed_file: Optional[Union[str, Path]] = None):
    deed_file = deed_file or DEFAULT_DEED_FILE


def load_deeds(deed_file: Optional[Union[str, Path]] = None) -> List:
    """
    Load property deeds from a pickle file.

    Parameters:
        deed_file (Optional[Union[str, Path]]): The path to the pickle file containing the property deeds.

    Returns:
        List: A list of property deeds.
    """
    deed_data = None
    deed_list = []

        
    if not deed_data:
        return deed_list
    
    for deed in deed_data:
        name = deed['name']
