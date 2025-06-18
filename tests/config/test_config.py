import shutil
from pathlib import Path

import pytest

from mooch import Config

default_settings = {
    "settings.name": "MyName",
    "settings.mood": "MyMood",
    "dictionary.key1": "value1",
    "dictionary.key2": "value2",
    "dictionary.subdictionary.key1": "subvalue1",
    "dictionary.subdictionary.key2": "subvalue2",
}

default_settings2 = {
    "settings": {"name": "MyName", "mood": "MyMood", "gui": {"theme": {"ios": "dark"}}},
}


@pytest.fixture
def settings_filepath(tmpdir_factory: pytest.TempdirFactory):
    temp_dir = str(tmpdir_factory.mktemp("temp"))
    filepath = temp_dir + "/settings.toml"
    yield filepath
    shutil.rmtree(temp_dir)


def test_config_initializes_with_default_settings(settings_filepath: str):
    config = Config(settings_filepath, default_settings)
    for k, v in default_settings.items():
        assert config.get(k) == v

    assert config.get("settings.name") == "MyName"
    assert config.get("settings.mood") == "MyMood"
    assert config.get("dictionary.key1") == "value1"
    assert config.get("dictionary") == {
        "key1": "value1",
        "key2": "value2",
        "subdictionary": {"key1": "subvalue1", "key2": "subvalue2"},
    }

    assert config.get("foo") is None


def test_config_sets_default_settings_if_not_present(settings_filepath: str):
    config = Config(settings_filepath, default_settings)
    assert config.get("foo") is None

    default_settings["foo"] = "bar"
    new_config = Config(settings_filepath, default_settings)

    assert new_config.get("foo") == "bar"
    for k, v in default_settings.items():
        assert new_config.get(k) == v


def test_config_get_and_set_methods_success(settings_filepath: str):
    config = Config(settings_filepath, default_settings)

    config.set("string", "string_value")
    config.set("none", None)
    config.set("int", 42)
    config.set("float", 3.14)
    config.set("bool", True)  # noqa: FBT003
    config.set("list", [1, 2, 3])
    config.set("dict", {"key": "value"})
    config.set("nested_dict", {"nested_key": {"sub_key": "sub_value"}})
    config.set("empty_list", [])
    config.set("nested_list", [[1, 2, 3], [4, 5, 6], ["a", "b", "c"]])
    config.set("empty_dict", {})
    config.set("complex", {"list": [1, 2, 3], "dict": {"key": "value"}})
    config.set("complex_nested", {"outer": {"inner": {"key": "value"}}})
    config.set("unicode", "こんにちは")  # Japanese for "Hello"
    config.set("emoji", "😊")  # Smiling face emoji

    assert config.get("string") == "string_value"
    assert config.get("none") is None
    assert config.get("int") == 42
    assert config.get("float") == 3.14
    assert config.get("bool") is True
    assert config.get("list") == [1, 2, 3]
    assert config.get("dict") == {"key": "value"}
    assert config.get("nested_dict") == {"nested_key": {"sub_key": "sub_value"}}
    assert config.get("empty_list") == []
    assert config.get("nested_list") == [[1, 2, 3], [4, 5, 6], ["a", "b", "c"]]
    assert config.get("empty_dict") == {}
    assert config.get("complex") == {"list": [1, 2, 3], "dict": {"key": "value"}}
    assert config.get("complex_nested") == {"outer": {"inner": {"key": "value"}}}
    assert config.get("unicode") == "こんにちは"
    assert config.get("emoji") == "😊"


def test_config_overrides_existing_settings(settings_filepath: str):
    config = Config(settings_filepath, default_settings)

    # Set an initial value
    config.set("name", "InitialName")
    assert config.get("name") == "InitialName"

    # Override the value
    config.set("name", "NewName")
    assert config.get("name") == "NewName"


def test_config_handles_non_existent_keys(settings_filepath: str):
    config = Config(settings_filepath, default_settings)

    assert config.get("non_existent_key") is None


def test_config_handles_empty_settings_file(settings_filepath: str):
    # Create an empty settings file
    with Path.open(settings_filepath, "w") as f:
        f.write("")
    config = Config(settings_filepath, default_settings)
    # Check that default settings are applied
    for k, v in default_settings.items():
        assert config.get(k) == v


def test_config_saves_settings_to_file(settings_filepath: str):
    config = Config(settings_filepath, default_settings)

    # Set some values
    config.set("name", "TestName")
    config.set("mood", "TestMood")

    # Reload the config to check if values are saved
    new_config = Config(settings_filepath, default_settings)
    assert new_config.get("name") == "TestName"
    assert new_config.get("mood") == "TestMood"


def test_config_no_default_settings(settings_filepath: str):
    # Test with no default settings
    config = Config(settings_filepath)

    # Check that no settings are set initially
    assert config.get("name") is None
    assert config.get("mood") is None

    # Set a value and check if it persists
    config.set("name", "NoDefaultName")
    assert config.get("name") == "NoDefaultName"

    # Reload the config to check if the value is saved
    new_config = Config(settings_filepath)
    assert new_config.get("name") == "NoDefaultName"


def test_config_with_getitem_and_setitem(settings_filepath: str):
    config = Config(settings_filepath, default_settings)

    # Test __getitem__
    assert config["settings.name"] == "MyName"
    assert config["settings.mood"] == "MyMood"
    assert config["dictionary.key1"] == "value1"

    # Test __setitem__
    config["settings.name"] = "NewName"
    assert config["settings.name"] == "NewName"

    config["new_key"] = "new_value"
    assert config["new_key"] == "new_value"


def test_config_updates_defaults_with_nested_dict(settings_filepath: str):
    config = Config(settings_filepath, default_settings)
    assert config.get("dictionary.subdictionary.key3") is None
    assert config["dictionary.subdictionary.key3"] is None

    default_settings["dictionary.subdictionary.key3"] = "subvalue3"

    # Access a nested value
    new_config = Config(settings_filepath, default_settings)
    assert new_config.get("dictionary.subdictionary.key3") == "subvalue3"
    assert new_config["dictionary"]["subdictionary"]["key3"] == "subvalue3"


def test_config_initializes_defaults_with_nested_dict(settings_filepath: str):
    config = Config(settings_filepath, default_settings2)
    assert config.get("settings.name") == "MyName"
    assert config.get("settings.mood") == "MyMood"
    assert config["settings"]["name"] == "MyName"
    assert config["settings"]["mood"] == "MyMood"
    assert config["settings"] == {"gui": {"theme": {"ios": "dark"}}, "mood": "MyMood", "name": "MyName"}
    assert config["settings"]["gui"]["theme"] == {"ios": "dark"}
    assert config["settings"]["gui"]["theme"]["ios"] == "dark"
    assert config.get("dictionary") is None
    assert config.get("dictionary.key1") is None
    assert config.get("dictionary.subdictionary") is None
    assert config.get("dictionary.subdictionary.key1") is None
    assert config.get("settings.gui.theme.ios") == "dark"
    assert config.get("settings") == {"gui": {"theme": {"ios": "dark"}}, "mood": "MyMood", "name": "MyName"}


def test_config_sets_default_settings_of_nested_dictionaries_if_not_present(settings_filepath: str):
    config = Config(settings_filepath, default_settings2)
    assert config.get("settings.gui.theme.ios") == "dark"
    assert config.get("settings.gui.theme.android") is None

    config.set("settings.gui.theme.ios", "light")  # change from default dark to light

    new_default_settings = {
        "settings": {"name": "MyName", "mood": "MyMood", "gui": {"theme": {"ios": "dark", "android": "light"}}},
    }

    new_config = Config(settings_filepath, new_default_settings)

    assert new_config.get("settings.gui.theme.ios") == "light"  # verify that this is not overwritten by the default
    assert new_config.get("settings.gui.theme.android") == "light"
