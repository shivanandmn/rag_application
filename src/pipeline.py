from llama_index import PromptTemplate
import json
from src.data.ingestion import indexing_from_directory
from llama_index.postprocessor import SentenceTransformerRerank
from llama_index.query_engine import RetrieverQueryEngine


class QAPipeline:
    def __init__(self, config_path) -> None:
        with open(config_path, "r") as f:
            config = json.load(f)
        index, service_context = indexing_from_directory(config["data_ingestion"])
        reranker = SentenceTransformerRerank(
            top_n=config["top_n_to_llm"], model=config["rerank_model_repo_name"]
        )
        # as you are an assistant for Indian Employes and has knowledge about the Indian code of Wages.
        template = """
        
        If the query is about greeting please ignore the context, directly greet and ignore the next words.
        Given context as {context_str} answer the question {query_str} as if you are have knowledge about the Indian code of Wages.
        """
        qa_prompt_template = PromptTemplate(template)
        query_retriever = index.as_retriever(
            similarity_top_k=config["similarity_top_k"],
        )
        self.query_engine = RetrieverQueryEngine.from_args(
            retriever=query_retriever,
            node_postprocessors=[reranker],
            service_context=service_context,
            text_qa_template=qa_prompt_template,
            response_mode="refine",
        )

    def answer(self, query_str: str):
        import json

        print(
            json.dumps(
                self.query_engine.get_prompts()[
                    "response_synthesizer:text_qa_template"
                ].__dict__,
                indent=2,
            )
        )
        response = self.query_engine.query(query_str)
        return response.response.strip()


if __name__ == "__main__":
    pipeline = QAPipeline("config/simple.json")
    res = pipeline.answer(
        "What are the employers responsibility on full and final settlement after the employees resignation in state?"
    )
    print(res)
    breakpoint()
