from django.utils.timezone import now
from rest_framework import serializers

from accounts.models import User
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)

    class Meta:
        model = Task
        fields = (
            'id', 'customer', 'worker', 'created_at', 'updated_at', 'closed_at',
            'title', 'description', 'status', 'report', 'customer_id'
        )
        extra_kwargs = {
            'customer': {'read_only': True},
            'worker': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'closed_at': {'read_only': True},
            'status': {'read_only': True},
            'report': {'read_only': True},
        }

    def validate(self, attrs):
        customer_id = attrs.pop('customer_id', None)
        if self.context['request'].user.role == User.Roles.customer:
            attrs['customer'] = self.context['request'].user
        else:
            if customer_id is None:
                raise serializers.ValidationError('You need to select customer')
            else:
                customer = User.objects.filter(id=customer_id, role=User.Roles.customer).first()
                if customer:
                    attrs['customer'] = customer
                else:
                    raise serializers.ValidationError('Customer does not exists')
        return attrs

    def update(self, instance, validated_data):
        if self.instance.status == Task.Statuses.COMPLETED:
            raise serializers.ValidationError('Task already completed')
        return super(TaskSerializer, self).update(instance, validated_data)


class AssignTaskSerializer(serializers.ModelSerializer):
    task_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Task
        fields = (
            'id', 'customer', 'worker', 'created_at', 'updated_at', 'closed_at',
            'title', 'description', 'status', 'report', 'task_id'
        )
        extra_kwargs = {
            'customer': {'read_only': True},
            'worker': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'closed_at': {'read_only': True},
            'status': {'read_only': True},
            'report': {'read_only': True},
            'title': {'read_only': True},
            'description': {'read_only': True},
        }

    def validate(self, attrs):
        task = Task.objects.filter(id=attrs.pop('task_id')).first()
        if task is None:
            raise serializers.ValidationError('Task does not exists')
        if task.worker is not None:
            raise serializers.ValidationError('Task already assigned')
        attrs['worker'] = self.context['request'].user.id
        task.worker = self.context['request'].user
        task.status = task.Statuses.IN_PROGRESS
        task.save(update_fields=['worker', 'status'])
        return attrs


class MarkAsCompletedSerializer(serializers.ModelSerializer):
    task_id = serializers.IntegerField(write_only=True, required=True)
    report = serializers.CharField(max_length=500, required=True, allow_blank=False)

    class Meta:
        model = Task
        fields = (
            'id', 'customer', 'worker', 'created_at', 'updated_at', 'closed_at',
            'title', 'description', 'status', 'report', 'task_id'
        )
        extra_kwargs = {
            'customer': {'read_only': True},
            'worker': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'closed_at': {'read_only': True},
            'status': {'read_only': True},
            'title': {'read_only': True},
            'description': {'read_only': True},
        }

    def validate(self, attrs):
        task = Task.objects.filter(id=attrs.pop('task_id')).first()
        if task is None:
            raise serializers.ValidationError('Task does not exists')
        if task.worker != self.context['request'].user:
            raise serializers.ValidationError('You can not manage other workers tasks')
        attrs['worker'] = self.context['request'].user.id
        task.worker = self.context['request'].user
        task.status = task.Statuses.COMPLETED
        task.report = attrs['report']
        task.closed_at = now()
        task.save(update_fields=['worker', 'status', 'closed_at', 'report'])
        return attrs
