import pytest
import re

def validate_input_zipcode_field_numerical(zipcode):
    pattern = r"^\d{5}$" # regular expression pattern to match a 5-digit number
    assert bool(re.match(pattern, zipcode)) == True

def validate_input_aqsid_field_numerical(aqsid):
    pattern = r"^\d{9}$" # regular expression pattern to match a 9-digit number
    assert bool(re.match(pattern, aqsid)) == True


