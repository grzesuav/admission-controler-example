import json
import logging

LOGGER = logging.getLogger(__name__)


class Validator:
    @staticmethod
    def validate(payload: dict) -> str:
        uid: str = payload['request']['uid']
        name: str = payload['request']['object']['metadata']['name']
        result: dict = Validator.construct_allowed_response(uid) \
            if name != 'forbidden' \
            else \
            Validator.construct_deny_response(name, uid)
        return json.dumps(result)

    @staticmethod
    def construct_allowed_response(uid: str) -> dict:
        return {
            'apiVersion': 'admission.k8s.io/v1beta1',
            'kind': 'AdmissionReview',
            'response': {
                'uid': uid,
                'allowed': True
            }
        }

    @staticmethod
    def construct_deny_response(name: str, uid: str) -> dict:
        message: str = "Name of the namespace object must be different than'forbidden', but it is:'{}'".format(name)
        return {
            'apiVersion': 'admission.k8s.io/v1beta1',
            'kind': 'AdmissionReview',
            'response': {
                'uid': uid,
                'allowed': False,
                'status': {
                    'message': message,
                    'code': 404
                }
            }
        }
