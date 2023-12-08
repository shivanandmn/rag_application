from llama_index.llms import HuggingFaceLLM
from typing import Any
from llama_index.llms.base import (
    CompletionResponse,
    llm_completion_callback,
)
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch


class CustomHuggingFaceLLM(HuggingFaceLLM):
    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        """Completion endpoint."""
        full_prompt = prompt
        is_formatted = kwargs.pop("formatted", False)
        if not is_formatted:
            if self.query_wrapper_prompt:
                full_prompt = self.query_wrapper_prompt.format(query_str=prompt)
            if self.system_prompt:
                full_prompt = f"{self.system_prompt} {full_prompt}"

        inputs = self._tokenizer(full_prompt, return_tensors="pt")
        inputs = inputs.to(self._model.device)

        # remove keys from the tokenizer if needed, to avoid HF errors
        for key in self.tokenizer_outputs_to_remove:
            if key in inputs:
                inputs.pop(key, None)

        tokens = self._model.generate(
            **inputs,
            max_new_tokens=self.max_new_tokens,
            stopping_criteria=self._stopping_criteria,
            **self.generate_kwargs,
        )
        # completion_tokens = tokens[0][inputs["input_ids"].size(1) :]
        completion = self._tokenizer.decode(tokens[0], skip_special_tokens=True)

        return CompletionResponse(text=completion, raw={"model_output": tokens})


def google_flan_t5_large(**kwargs):
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")
    hug_llm = CustomHuggingFaceLLM(
        model=model,
        tokenizer=tokenizer,
        generate_kwargs={"pad_token_id": tokenizer.eos_token_id},
        **kwargs,
    )
    return hug_llm


def mistralai_7b_instruct(**kwargs):
    # model_id = "TheBloke/Llama-2-7b-Chat-AWQ"
    model_id = "mistralai/Mistral-7B-Instruct-v0.1"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        load_in_4bit=True,
        quantization_config=BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
        ),
        device_map="auto",
        # use_flash_attention_2=True,
    )
    hug_llm = HuggingFaceLLM(
        model=model,
        tokenizer=tokenizer,
        generate_kwargs={"pad_token_id": tokenizer.eos_token_id},
        **kwargs,
    )
    return hug_llm


MODELS = {
    "mistralai/Mistral-7B-Instruct-v0.1": mistralai_7b_instruct,
    "google/flan-t5-large": google_flan_t5_large,
}
