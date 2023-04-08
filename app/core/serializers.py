from rest_framework import serializers

from app.core.models import Questions, Stats


class QuestionsSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Question Model
    """
    class Meta:
        model = Questions
        fields = ['id', 'question', 'iq_index', 'created_date', 'answers', ]


class StatsSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Stats Model
    """
    class Meta:
        model = Stats
        fields = ['id', 'name', 'age', 'iq_score', 'created_date', 'session_id', ]
