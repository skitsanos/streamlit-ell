# ELL Integration with Streamlit Demo

A demonstration application showcasing how to integrate ELL with Streamlit to create an interactive chat interface. This
app demonstrates explicitly ELL's tool calling capabilities and session management in a Streamlit environment.

> `ell` is a lightweight prompt engineering library treating prompts as functions. Documentation can be
> found [here](https://docs.ell.so/).

## Key Demonstration Points

- **ELL Integration**: Shows how to initialize and use ELL within a Streamlit application
- **Tool Calling**: Demonstrates ELL's tool calling functionality using a weather service example
- **Streamlit State Management**: Examples of managing ELL chat state with Streamlit's session state
- **Complex Function Handling**: Shows how to use ELL's `@complex` decorator with Streamlit's dynamic state

## Technical Highlights

```python
@ell.complex(model=lambda: st.session_state.model or DEFAULT_MODEL, 
             tools=[weather.get_weather], 
             temperature=0.0)
def execute_with_tools(message_history: List[Message]):
    return message_history
```

This example demonstrates:

- Dynamic model selection using Streamlit's session state
- Tool registration with ELL
- Message history management

## Prerequisites

- Python 3.9+
- OpenAI API key
- Required packages:
  ```
  streamlit
  openai
  ell
  ```

## Installation

1. Clone this repository:

```bash
git clone https://github.com/skitsanos/streamlit-ell.git
cd streamlit-ell
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Running the Demo

1. Start the application:

```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided URL (typically http://localhost:8501)

## Demo Features

### ELL Tool Integration

- Weather information tool demonstration
- Example of how to structure and register tools with ELL
- Tool execution flow in a Streamlit environment

### State Management

- ELL chat history preservation using Streamlit session state
- Model selection state management
- Message threading with tool calls

### UI Components

- Model selector in sidebar
- Chat interface with message history
- Tool response display

## Project Structure

```
.
├── app.py              # Main demonstration file
├── tools/
│   └── weather.py      # Example tool integration
├── logdir/             # ELL logging directory
└── requirements.txt    # Project dependencies
```

## Learning Points

1. How to initialize ELL in a Streamlit application
2. Managing tool calls with ELL and Streamlit
3. Handling chat state and history
4. Error handling in ELL tool calls
5. Integrating external services (weather API example)

## Contributing

Feel free to submit issues and pull requests with additional examples or improvements to the demonstration.

## License

MIT

## Support

For questions about:

- ELL integration: https://docs.ell.so/
- Streamlit usage: https://streamlit.io/