from .plc_core import PlcCore


class PlcMeasurements:
    record_counter: int = 0

    @staticmethod
    def read_wells(self):
        # Load in wells from db

        # Create empty list of alarm db objects

        # Configure list of tags to read based on wells from db

        # Read list of tags

        # Cycle through tags looking for alarms; if found, add alarm to list of alarm db objects

        # Add all alarm db objects to db

        # Send alarm email

        # Check if we need to add well measurements to db
        # If true: save to db and reset record_counter
        # If false: increment record_counter
        pass
