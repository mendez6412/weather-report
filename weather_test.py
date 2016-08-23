from weather import Weather


def test():
    dc = Weather(20002)

    assert dc.zipcode == 20002


def test_fake_lookup():
    dc = Weather(20002)
    dcweather = dc.lookup(test=1)
    
    assert dc.result['current_observation']['display_location']['city'] == 'Durham' 


# def test_real_lookup():
    """ Do not run this all the time """
    # dc = Weather(20002)
    # dcweather = dc.lookup()

    # assert dc.result['current_observation']['display_location']['city'] == 'Washington'

