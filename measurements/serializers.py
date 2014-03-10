from rest_framework import serializers
from measurements.models import Measurement


class MeasurementSerializer(serializers.HyperlinkedModelSerializer):

    measurements = serializers.HyperlinkedIdentityField(view_name='measurements', format='html')

    # owner = serializers.Field(source='owner.username')
    # highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Measurement
        fields = ['time']