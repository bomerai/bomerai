"""
This module demonstrates how to use the DictWrapper with Django JSON fields.
"""

from typing import Dict, Any, Optional

from django.db import models
from draft_building_designs.utils.dict_wrapper import DictWrapper, TypedDictWrapper


# Example 1: Basic usage with DictWrapper
class BuildingComponent(models.Model):
    name = models.CharField(max_length=255)
    component_data = models.JSONField(default=dict)

    def get_component_data(self) -> DictWrapper:
        """
        Get the component data as a DictWrapper.

        Returns:
            A DictWrapper instance for the component data
        """
        return DictWrapper(self.component_data)


# Example 2: Using TypedDictWrapper for type hints
class ColumnData(TypedDictWrapper["ColumnData"]):
    """
    A typed wrapper for column component data.

    This class provides type hints for the column component data.
    """

    height: str
    width: str
    length: str
    longitudinal_reinforcement: str
    transverse_reinforcement: str


class ColumnComponent(models.Model):
    name = models.CharField(max_length=255)
    component_data = models.JSONField(default=dict)

    def get_component_data(self) -> ColumnData:
        """
        Get the component data as a ColumnData instance.

        Returns:
            A ColumnData instance for the component data
        """
        return ColumnData(self.component_data)


# Example 3: Using the wrapper in a service
def process_column_component(column: ColumnComponent) -> None:
    """
    Process a column component using the typed wrapper.

    Args:
        column: The column component to process
    """
    data = column.get_component_data()

    # Access attributes with type hints
    height = data.height  # Type hint: str
    width = data.width  # Type hint: str

    # Access nested dictionaries
    if isinstance(data.longitudinal_reinforcement, dict):
        reinforcement = DictWrapper(data.longitudinal_reinforcement)
        diameter = reinforcement.get("diameter", "10mm")

    # Convert back to dictionary if needed
    data_dict = data.to_dict()


# Example 4: Using the wrapper with the existing code
def get_column_component_data(component_data: Dict[str, Any]) -> ColumnData:
    """
    Get the column component data as a ColumnData instance.

    Args:
        component_data: The component data dictionary

    Returns:
        A ColumnData instance for the component data
    """
    return ColumnData(component_data)


# Example usage
if __name__ == "__main__":
    # Example 1: Basic usage
    component = BuildingComponent(name="Column A1", component_data={"foo": "bar"})
    data = component.get_component_data()
    print(data.foo)  # Output: bar

    # Example 2: Typed usage
    column = ColumnComponent(
        name="Column B1",
        component_data={
            "height": "3.0m",
            "width": "0.3m",
            "length": "0.3m",
            "longitudinal_reinforcement": "4T16",
            "transverse_reinforcement": "T8@150",
        },
    )
    column_data = column.get_component_data()
    print(column_data.height)  # Output: 3.0m
    print(column_data.width)  # Output: 0.3m
