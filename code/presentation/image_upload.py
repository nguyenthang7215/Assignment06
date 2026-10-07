from pathlib import Path


class ImageUpload:
    """Collect a local image path; ImageService handles decoding."""

    def collect(self, image_path: Path) -> Path:
        return Path(image_path)
