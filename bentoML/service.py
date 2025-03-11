from __future__ import annotations
import bentoml
import modules.nlp_model as nlp_model

EXAMPLE_INPUT = "これはサンプルです"

my_image = bentoml.images.PythonImage(python_version="3.12") \
        .python_packages("torch", "transformers")

@bentoml.service(
    image=my_image,
    resources={"cpu": "2"},
    traffic={"timeout": 30},
)
class SampleService:
    
    @bentoml.api
    def hello(self) -> str:
        return "Hello, World!"
    
    @bentoml.api
    def tokenize(self, text: str = EXAMPLE_INPUT) -> list:
        return nlp_model.tokenize_text(text)
    
    @bentoml.api
    def embedding(self, text: str = EXAMPLE_INPUT) -> list:
        return nlp_model.get_embeddings(text).tolist()
