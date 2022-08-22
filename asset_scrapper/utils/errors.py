class DatabaseError(Exception):
    """
    Generic DB error class that can be filled out later
    """
    def __init__(self, message) -> None:
        
        super().__init__(message)

