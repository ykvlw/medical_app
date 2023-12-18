from pathlib import Path


class PathHelper:
    @classmethod
    def package_dir(cls) -> Path:
        return Path(__file__).absolute().parent.parent.parent

    @classmethod
    def relative_path(cls, *args: str) -> str:
        return str(Path(cls.package_dir() / Path(*args)))
