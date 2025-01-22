import ell


@ell.tool()
def get_weather(location: str) -> str:
    # Implementation to fetch weather
    return f"The weather in {location} is sunny."
