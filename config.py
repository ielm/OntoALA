from knowledge.lexicon import Lexicon
from knowledge.ontology import Ontology
from ontomem.memory import MemoryManager

import os
import yaml


class OntoALAConfig:
    @classmethod
    def from_file(cls, filename: str) -> "OntoALAConfig":
        """Generate OntoALAConfig from a file"""
        with open(filename, "r") as config_file:
            config_dict = yaml.load(config_file, Loader=yaml.FullLoader)
            return OntoALAConfig(
                knowledge_file=config_dict["knowledge-file"],
            )

    def __init__(self, knowledge_file: str = None):
        self.knowledge_file = self.parameter_environment_or_default(
            knowledge_file, "KNOWLEDGE-FILE", "knowledge/build/knowledge.om"
        )

    @staticmethod
    def parameter_environment_or_default(parameter, env_var: str, default):
        """Returns the environment parameter if defined else returns the default value"""
        if parameter is not None:
            return parameter
        if env_var in os.environ:
            return os.environ[env_var]
        return default

    def load_knowledge(self):
        """Load knowledge into memory from a knowledge file"""
        MemoryManager.load_memory(self.knowledge_file)

    @staticmethod
    def ontology() -> Ontology:
        """Generates a new Ontology object from the available knowledge"""
        return Ontology()

    @staticmethod
    def lexicon() -> Lexicon:
        """Generates a new Lexicon object from the available knowledge"""
        return Lexicon()

    def to_dict(self) -> dict:
        return {
            "knowledge-file": self.knowledge_file,
        }
