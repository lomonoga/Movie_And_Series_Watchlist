from help_functions.database_functions import check_connect_database


def test_connection_database():
    result = check_connect_database()
    assert isinstance(result, bool)

def test_filling_configuration():
    from conf import Config
    # If Config was imported - Passed
    assert True
