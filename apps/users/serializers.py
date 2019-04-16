from rest_framework import serializers, exceptions
from rest_framework_jwt.settings import api_settings
from users.models import CustomUser
from users.utils import validate_email, get_additional_info


class UserSignupSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'phone',
            'token',
        ]
        write_only_fields = ('password',)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        email = validated_data.get('email', None)
        first_name = validated_data.get('first_name', None)
        last_name = validated_data.get('last_name', None)
        is_email_valid = True

        if email:
            is_email_valid = validate_email(email)
            additional_user_info = get_additional_info(email)

            if not first_name:
                first_name = additional_user_info['person']['name']['givenName']
            if not last_name:
                last_name = additional_user_info['person']['name']['familyName']

        if is_email_valid:
            instance = self.Meta.model(**validated_data)
            if password is not None:
                instance.set_password(password)
            if first_name:
                instance.first_name = first_name
            if last_name:
                instance.last_name = last_name
            instance.save()
            return instance

        raise exceptions.ValidationError(
            detail=f'Email {email} is invalid'
        )
