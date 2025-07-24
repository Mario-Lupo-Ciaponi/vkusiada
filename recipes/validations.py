from typing import Optional
import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class IsYoutubeLinkValidValidator:
    def __init__(self, message: Optional[str]=None) -> None:
        self.message = message or "The YouTube URL is not Valid!"

    def __call__(self, value: str) -> None:
        if value and not re.match(
            r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(?:-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|live\/|v\/)?)([\w\-]+)(\S+)?$",
            value,
        ):
            raise ValidationError(self.message)
