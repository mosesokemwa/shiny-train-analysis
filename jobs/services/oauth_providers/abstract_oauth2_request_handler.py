import abc
import requests
import json
from rest_framework import exceptions
class Oauth2RequestHandlerInterface(abc.ABC):

    @abc.abstractmethod
    def get_access_token(self,code):
        pass

    @abc.abstractmethod
    def refresh_token(self, token):
        pass


class AbstractOauth2RequestHandler(Oauth2RequestHandlerInterface):

    def __init__(self, *args, **kwargs):
        self.CLIENT_ID=None
        self.CLIENT_SECRET=None
        self.CLIENT_ENDPOINT=None
        self.CLIENT_REDIRECT_URI=None

    def get_access_token(self, code):
        raise NotImplementedError("Not implemented")

    def refresh_token(self, token):
        raise NotImplementedError("Not implemented")

    def make_request(self, method, url, options, response_type="json"):
        func={"post":requests.post,"get":requests.get}
        res=func[method](url,**options)
        print(res.status_code)
        if res.status_code == 200:
            if response_type=="json":
                try:
                    data = res.json()
                    return data
                except json.decoder.JSONDecodeError:
                    raise exceptions.APIException("Unable to decode json response")
                except Exception as e:
                    message = str(e)
                    print(message)
                    raise exceptions.APIException("Server error: %s"%message)
            else:
                raise exceptions.APIException("Unsupported response_type")
        else:
            raise exceptions.AuthenticationFailed("Request unsuccessfull, code: %s"%str(res.status_code))

