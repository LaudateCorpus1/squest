from service_catalog.api.serializers.dynamic_survey_serializer import DynamicSurveySerializer


class AcceptRequestSerializer(DynamicSurveySerializer):
    def __init__(self, *args, **kwargs):
        self.target_request = kwargs.pop('target_request')
        self.user = kwargs.pop('user')
        self.read_only_form = kwargs.get('read_only_form', False)
        kwargs['fill_in_survey'] = self.target_request.operation.job_template.survey
        super(AcceptRequestSerializer, self).__init__(*args, **kwargs)
        if self.read_only_form:
            self._set_initial_and_default(self.target_request.fill_in_survey)
            self._set_initial_and_default(self.target_request.admin_fill_in_survey)

    def save(self, **kwargs):
        if not self.read_only_form:
            user_provided_survey_fields = dict()
            for field_key, value in self.validated_data.items():
                # tower doesnt allow empty value for choices fields
                if value != '':
                    user_provided_survey_fields[field_key] = str(value)
            # update the request
            self.target_request.set_fill_in_survey(user_provided_survey_fields)
            self.target_request.accept()
            self.target_request.save()
            # reset the instance state if it was failed (in case of resetting the state)
            self.target_request.instance.reset_to_last_stable_state()
            self.target_request.instance.save()
            return self.target_request
