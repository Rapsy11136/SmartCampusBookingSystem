class Booking:

    def __init__(
        self,
        booking_id=None,
        lecturer_id=None,
        resource_id=None,
        booking_date="",
        start_time="",
        end_time="",
        purpose="",
        status="Pending"
    ):
        self.booking_id = booking_id
        self.lecturer_id = lecturer_id
        self.resource_id = resource_id
        self.booking_date = booking_date
        self.start_time = start_time
        self.end_time = end_time
        self.purpose = purpose
        self.status = status