from plugin import Plugin
import streamlit as st

class BaselinePlugin(Plugin):
    def __init__(self):
        self.file = __file__
        super().__init__()
    def run(self, data_manager, widget_manager):
        # Persistent widget example
        value = self.create_widget(
            widget_manager=widget_manager,
            widget_type=st.slider,
            widget_name="baseline_control",
            default_value=30,
            args=("Control Range:", 0, 100)
        )
        
        # Cross-plugin communication
        data_manager.set_data("baseline_output", value * 2)