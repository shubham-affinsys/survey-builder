class Serializer:
    def __init__(self, data=None, instance=None):
        """
        Initialize with data for deserialization or an instance for serialization.
        """
        self.data = data
        self.instance = instance
        self._validated_data = None

    def validate(self, data):
        """
        Hook for custom validation logic.
        """
        return data

    def is_valid(self):
        """
        Validate incoming data and store the validated result.
        """
        try:
            self._validated_data = self.validate(self.data)
            return True
        except Exception as e:
            self.errors = str(e)
            return False

    @property
    def validated_data(self):
        """
        Return the validated data.
        """
        if not self._validated_data:
            raise ValueError("Call `.is_valid()` before accessing `validated_data`.")
        return self._validated_data

    def serialize(self):
        """
        Convert instance data into JSON-compatible format.
        """
        raise NotImplementedError("Define `serialize` method to specify how data is serialized.")

    def create(self, validated_data):
        """
        Create a new instance with the validated data.
        """
        raise NotImplementedError("Define `create` method to specify instance creation logic.")

    def update(self, instance, validated_data):
        """
        Update an existing instance with validated data.
        """
        raise NotImplementedError("Define `update` method to specify instance update logic.")


from collections import OrderedDict


class ModelSerializer(Serializer):
    def __init__(self, instance=None, data=None, fields=None, exclude=None):
        """
        Automatically infer fields based on the model.
        """
        super().__init__(data=data, instance=instance)
        self.fields = fields
        self.exclude = exclude or []
        self.model = self.Meta.model  # Use Meta to specify the model class
        self._validated_data = None

    def serialize(self):
        """
        Automatically serialize fields based on the model.
        """
        if not self.instance:
            return None

        result = OrderedDict()
        for field in self._get_fields():
            result[field] = getattr(self.instance, field, None)
        return result

    def _get_fields(self):
        """
        Infer fields from the model, applying inclusion/exclusion logic.
        """
        model_fields = [field.name for field in self.Meta.model.__table__.columns]
        if self.fields:
            return [field for field in model_fields if field in self.fields]
        return [field for field in model_fields if field not in self.exclude]

    def create(self, validated_data):
        """
        Create a new instance using the validated data.
        """
        return self.model(**validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing instance using the validated data.
        """
        for key, value in validated_data.items():
            setattr(instance, key, value)
        return instance

    class Meta:
        model = None  # You must define a model in subclasses

