"""
Created: May, 2023

@author: tsalemink
"""
from cmlibs.widgets.handlers.sceneselection import SceneSelection
from cmlibs.widgets.definitions import BUTTON_MAP, SelectionMode
from cmlibs.zinc.sceneviewerinput import Sceneviewerinput
from cmlibs.zinc.field import Field


MODE_MAP = {
    "Exclusive": SelectionMode.EXCLUSIVE,
    "Additive": SelectionMode.ADDITIVE,
    "Intersection": SelectionMode.INTERSECTION,
}


TYPE_MAP = {
    "Points": Field.DOMAIN_TYPE_DATAPOINTS,
    "Whole Surfaces": Field.DOMAIN_TYPE_MESH2D,
    "Surface Sections": Field.DOMAIN_TYPE_MESH2D,
}


class CustomSceneSelection(SceneSelection):

    def __init__(self, key_code):
        super().__init__(key_code)
        self._selection_mode = SelectionMode.NONE
        self._primary_selection_mode = SelectionMode.EXCLUSIVE
        self._scene_filter = None

    def set_primary_selection_mode(self, mode):
        self._primary_selection_mode = mode

    def set_scene_filter(self, scene_filter):
        self._scene_filter = scene_filter

    def mouse_press_event(self, event):
        super().mouse_press_event(event)

        if BUTTON_MAP[event.button()] == Sceneviewerinput.BUTTON_TYPE_LEFT:
            self._selection_mode = self._primary_selection_mode

    def mouse_release_event(self, event):
        scene_picker = self._scene_viewer.get_scenepicker()
        scene_picker.setScenefilter(self._scene_filter)
        super().mouse_release_event(event)
