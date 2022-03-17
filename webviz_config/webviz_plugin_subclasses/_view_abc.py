from typing import Optional, Type
import abc

from typing import List
from uuid import uuid4

from dash import html

import webviz_core_components as wcc

from ._view_element_abc import ViewElementABC
from ._settings_group_abc import SettingsGroupABC

from dash import Dash
from dash.development.base_component import Component


class ViewABC(abc.ABC):
    def __init__(self, name: str) -> None:
        super().__init__()

        self._uuid = ""
        self.name = name

        self._view_elements: List[ViewElementABC] = []
        self._settings_groups: List[SettingsGroupABC] = []

    def _set_uuid(self, uuid: str) -> None:
        self._uuid = uuid
        for element in self._view_elements:
            element._set_uuid(f"{uuid}-{element.uuid()}")

        for setting in self._settings_groups:
            setting._set_uuid(f"{uuid}-{setting.uuid()}")

    def uuid(self, element: Optional[str] = None) -> str:
        if element:
            return f"{element}-{self._uuid}"
        return self._uuid

    def view_element_uuid(self, view_id: str, element: Optional[str]) -> str:
        if element:
            return f"{element}-{self._uuid}-{view_id}"
        return f"{self._uuid}-{view_id}"

    def view_element(self, id: str) -> ViewElementABC:
        view_element = next(
            (el for el in self.view_elements() if el.uuid().split("-")[-1] == id), None
        )
        if view_element:
            return view_element

        raise LookupError(
            f"Invalid view element id: '{id}. Available view element ids: {[el.uuid for el in self.view_elements()]}"
        )

    def settings_group(self, id: str) -> SettingsGroupABC:
        settings_group = next(
            (el for el in self.settings_groups() if el.uuid().split("-")[-1] == id),
            None,
        )
        if settings_group:
            return settings_group

        raise LookupError(
            f"Invalid settings group id: '{id}. Available settings group ids: {[el.uuid for el in self.settings_groups()]}"
        )

    def settings_group_uuid(self, settings_id: str, element: Optional[str]) -> str:
        if element:
            return f"{element}-{self._uuid}-{settings_id}"
        return f"{self._uuid}-{settings_id}"

    def add_view_element(
        self, view_element: ViewElementABC, id: Optional[str] = None
    ) -> None:
        uuid = f"{self._uuid}-" if self._uuid != "" else ""
        if id is not None:
            uuid += id
        else:
            uuid += f"element{len(self._view_elements)}"

        view_element._set_uuid(uuid)
        self._view_elements.append(view_element)

    def add_view_elements(self, view_elements: List[ViewElementABC]) -> None:
        for view_element in view_elements:
            self.add_view_element(view_element)

    def add_settings_group(
        self, settings_group: SettingsGroupABC, id: Optional[str] = None
    ) -> None:
        uuid = f"{self._uuid}-" if self._uuid != "" else ""
        if id is not None:
            uuid += id
        else:
            uuid += f"element{len(self._view_elements)}"

        settings_group._set_uuid(uuid)
        self._settings_groups.append(settings_group)

    def add_settings_groups(self, settings_groups: List[SettingsGroupABC]) -> None:
        for settings_group in settings_groups:
            self.add_settings_group(settings_group)

    def _set_all_callbacks(self, app: Dash) -> None:
        for element in self._view_elements:
            element._set_all_callbacks(app)

        for setting in self._settings_groups:
            setting._set_callbacks(app)

        self._set_callbacks(app)

    def view_elements(self) -> List[ViewElementABC]:
        return self._view_elements

    def settings_groups(self) -> List[SettingsGroupABC]:
        return self._settings_groups

    def layout(self) -> Type[Component]:
        return html.Div(
            [
                wcc.WebvizViewElement(id=el.uuid(), children=[el.layout()])
                for el in self.view_elements()
            ]
        )

    def _set_callbacks(self, app: Dash) -> None:
        return
