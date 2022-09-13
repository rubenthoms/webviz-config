from typing import List, Type, Union
from enum import Enum

from dash.development.base_component import Component
from dash import html

import webviz_core_components as wcc

from webviz_config.utils import StrEnum
from webviz_config.webviz_plugin_subclasses import SettingsGroupABC, ViewElementABC


class Kindness(StrEnum):
    FRIENDLY = "friendly"
    UNFRIENDLY = "unfriendly"


class TextViewElementSettingsGroup(SettingsGroupABC):
    class Ids(StrEnum):
        KINDNESS_SELECTOR = "kindness-selector"

    def __init__(self) -> None:
        super().__init__("Kindness")

    def layout(self) -> List[Component]:
        return [
            html.Div(
                children=[
                    wcc.Label("Kindness"),
                    wcc.RadioItems(
                        id=self.register_component_unique_id(
                            TextViewElementSettingsGroup.Ids.KINDNESS_SELECTOR
                        ),
                        options=[
                            {
                                "label": a.value,
                                "value": a.value,
                            }
                            for a in Kindness
                        ],
                        value="friendly",
                    ),
                ]
            )
        ]


class TextViewElement(ViewElementABC):
    class Ids(str, Enum):
        TEXT = "text"
        TEXT_SETTINGS = "text-settings"
        TEXT_SETTINGS_2 = "text-settings-2"

    def __init__(self) -> None:
        super().__init__()

        self.add_settings_group(
            TextViewElementSettingsGroup(), TextViewElement.Ids.TEXT_SETTINGS
        )
        self.add_settings_group(
            TextViewElementSettingsGroup(), TextViewElement.Ids.TEXT_SETTINGS_2
        )

    def inner_layout(self) -> Union[str, Type[Component]]:
        return html.Div(
            id=self.register_component_unique_id(TextViewElement.Ids.TEXT),
            children=[
                html.H1("Hello"),
                """
                This is an example plugin.
                Please have a look how views and settings are working in this new environment =).
                """,
            ],
        )
