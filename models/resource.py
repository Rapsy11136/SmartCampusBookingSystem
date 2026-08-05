class Resource:

    def __init__(
            self,
            resource_id=None,
            campus_id=None,
            name="",
            resource_type="",
            status="Available"
    ):
        self.resource_id = resource_id
        self.campus_id = campus_id
        self.name = name
        self.resource_type = resource_type
        self.status = status