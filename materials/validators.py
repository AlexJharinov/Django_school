from rest_framework import serializers


def validate_youtube_url(value: str):
    """
    Проверяет, что ссылка ведёт только на YouTube.
    """
    allowed_domains = ["youtube.com"]
    if not any(domain in value for domain in allowed_domains):
        raise serializers.ValidationError(
            "Разрешены только ссылки на YouTube (youtube.com)."
        )
    return value
