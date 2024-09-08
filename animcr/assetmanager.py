from pathlib import Path
from astropy.io import fits


class AssetManager:
    ASSETS_PATH = Path(__file__).parent / "assets"

    @classmethod
    def get_image(cls, image_path: str):
        path = cls.ASSETS_PATH / image_path

        if not path.exists():
            raise ValueError(f"Image {image_path} does not exist")

        if path.suffix == ".fits":
            return fits.getdata(path)

        raise ValueError(f"Unsupported image format: {path.suffix}")
