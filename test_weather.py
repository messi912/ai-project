from weather import get_coordinates, get_weather, weather_codes

def test_get_coordinates_valid_city():
    result = get_coordinates("Paris")
    assert result is not None
    latitude, longitude, name, country = result
    assert "Paris" in name
    assert country == "France"
    assert -90 <= latitude <= 90
    assert -180 <= longitude <= 180

def test_get_coordinates_invalid_city():
    result = get_coordinates("xyznotacity123")
    assert result is None

def test_get_weather_returns_data():
    result = get_weather(48.8566, 2.3522)
    assert result is not None
    assert "temperature" in result
    assert "windspeed" in result
    assert "weathercode" in result

def test_weather_codes_has_clear_sky():
    assert 0 in weather_codes
    assert weather_codes[0] == "Clear sky"

def test_weather_codes_has_thunderstorm():
    assert 95 in weather_codes
    assert weather_codes[95] == "Thunderstorm"