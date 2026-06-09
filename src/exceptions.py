class TranscriptionProjectError(Exception):
    """Base exception for the transcription project."""
    pass

class InputDirectoryNotFoundError(TranscriptionProjectError):
    """Raised when the specified input directory does not exist."""
    pass

class NoVideoFilesFoundError(TranscriptionProjectError):
    """Raised when no valid video/audio files are found in the directory."""
    pass

class TranscriptionError(TranscriptionProjectError):
    """Raised when an error occurs during the transcription process."""
    pass

class UnsupportedFormatError(TranscriptionProjectError):
    """Raised when an unsupported output format is requested."""
    pass
