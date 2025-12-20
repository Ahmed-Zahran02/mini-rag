from pathlib import Path


class TemplateParser:
    def __init__(self, language: str = "en", default_language: str = "en"):
        self.language = language.lower()
        self.default_language = default_language.lower()
        self.set_language(self.language)

    def set_language(self, language: str):
        language = language
        language_path = Path(__file__).parent / "locales" / language
        if language_path.exists():
            self.language = language
        else:
            self.language = self.default_language

    def get_template(self, group: str, key: str, vars: dict):
        if not group or not key:
            raise ValueError("Group and key must be provided")
        template_path = (
            Path(__file__).parent / "locales" / self.language / f"{group}.py"
        )
        if not template_path.exists():
            raise FileNotFoundError(
                f"Template file not found for group '{group}' in language '{self.language}'"
            )
        module = __import__(
            f"mini_rag.src.stores.llm.templates.locales.{self.language}.{group}",
            fromlist=[group],
        )
        if not module:
            raise ImportError(
                f"Module not found for group '{group}' in language '{self.language}'"
            )

        key_module = getattr(module, key)
        if not key_module:
            raise AttributeError(
                f"Key '{key}' not found in module '{group}' in language '{self.language}'"
            )

        return key_module.substitute(**vars)
