# StreamFlex Plugin Development Guide

## Core Concepts

### Plugin Structure
```
plugins/
└── YourPlugin/          # Plugin directory (exact class name)
    ├── plugin.py        # Mandatory: Plugin implementation
    ├── configs/
    │   └── config.toml  # Plugin metadata
    └── requirements.txt # Optional dependencies
```

## Basic Implementation

### 1. Minimal Plugin Template (`plugin.py`)
```python
from plugin import Plugin
import streamlit as st

class BaselinePlugin(Plugin):
    def __init__(self):
        self.file = __file__ # Required if class name is different from directory name of plugin
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
```

### 2. Configuration (`configs/config.toml`)
```toml
name = "Baseline Plugin"
version = "0.0.1"
```

## Widget Management

### `create_widget()` Fundamentals
Persists widget state across sessions using:
- **widget_manager**: Handles state storage
- **widget_name**: Unique identifier (auto-namespaced)
- **default_value**: Initial state
- **serialization**:
  - `value_serializer`: Converts values for storage
  - `value_deserializer`: Restores from stored format

```python
# Abstract example
self.create_widget(
    widget_manager=manager,
    widget_type=StreamlitWidget,
    widget_name="unique_id",
    default_value=initial_state,
    value_serializer=custom_serialize,
    value_deserializer=custom_deserialize
)
```

## Data Flow Patterns

### Cross-Plugin Communication
```python
# Producer
data_manager.set_data("shared_key", analysis_results)

# Consumer
received_data = data_manager.get_data("shared_key", default=None)
```

## Best Practices

1. **State Management**
   - Use `widget_manager` for UI persistence
   - Namespace data keys: `"{plugin}_{data}"`

2. **Error Resilience**
   ```python
   try:
       essential_data = data_manager.get_data("required_key")
   except DataUnavailable:
       self.logger.error("Missing dependencies")
       return
   ```

3. **Dependency Management**
   - Declare plugin-specific requirements
   - Handle missing imports gracefully

---

## Implementation Checklist

- [ ] Config contains `name` and `version`
- [ ] Widgets use `create_widget()` pattern
- [ ] Data keys are properly namespaced
- [ ] Error handling for external data

---

## Execution & Deployment

```bash
# Install plugin dependencies
pip install -r plugins/YourPlugin/requirements.txt

# Launch application
streamlit run app.py
```

---

Key principles:
1. Plugins are self-contained modules
2. State persistence through managed components
3. Explicit data dependencies between plugins