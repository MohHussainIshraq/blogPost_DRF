from rest_framework import serializers

from post.models import Post


class PostSerializer(serializers.ModelSerializer):
    publisher = serializers.ReadOnlyField(source='publisher.username')

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('id', 'date_added', 'is_public', 'publisher')
        extra_kwargs = {'image': {'required': False}}
