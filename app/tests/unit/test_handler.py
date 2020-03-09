import json
import pytest
import pdb

# Make pytest find the code, someone better at Python can help me make this better :-)
import sys
sys.path.append('/code/app/src')

from src import lambda_function

def event(country_code, slug="/"):
    return {
        "Records": [
            {
                "cf": {
                    "request": {
                        "uri": slug,
                        "headers": {
                            "cloudfront-viewer-country": [
                                {
                                    "key": "CloudFront-Viewer-Country",
                                    "value": country_code
                                }
                            ],
                            "cookie": [
                                {
                                    "key": "cookie",
                                    "value": "somename=put_a_cookie_value_here"
                                }
                            ],
                        }
                    }
                }
            }
        ]
    }

def test_diagnostic(mocker):
    response = lambda_function.lambda_handler(event("US", "/diagnostic"), "")
    assert response['status'] == '200'
