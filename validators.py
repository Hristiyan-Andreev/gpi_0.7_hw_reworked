from PyInquirer import Validator, ValidationError
import ipaddress as ip
import regex as re


class AvDurValidator(Validator):
    def validate(self, document):
        try:
            float(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number (float or int)',
                cursor_position=len(document.text)
                )

class IpValidator(Validator):
    def validate(self, document):        
        try:
            ip.ip_address(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a valid IP address',
                cursor_position=len(document.text))  # Move cursor to end
