# import torch

# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
# from langchain_huggingface import HuggingFacePipeline

# from config.settings import (
#     LLM_MODEL_NAME,
#     MAX_NEW_TOKENS,
#     TEMPERATURE
# )


# def load_llm():
#     print("Loading LLM:", LLM_MODEL_NAME)

#     tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME)

#     if torch.cuda.is_available():
#         print("CUDA available. Loading model on GPU.")

#         model = AutoModelForCausalLM.from_pretrained(
#             LLM_MODEL_NAME,
#             torch_dtype=torch.float16,
#             device_map="auto"
#         )

#     else:
#         print("CUDA not available. Loading model on CPU. This may be slow.")

#         model = AutoModelForCausalLM.from_pretrained(
#             LLM_MODEL_NAME,
#             torch_dtype=torch.float32
#         )

    

#     generation_pipeline = pipeline(
#         task="text-generation",
#         model=model,
#         tokenizer=tokenizer,
#         max_new_tokens=MAX_NEW_TOKENS,
#         temperature=TEMPERATURE,
#         do_sample=True,
#         return_full_text=False
#     )

#     llm = HuggingFacePipeline(
#         pipeline=generation_pipeline
#     )

#     return llm






import torch

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline

from config.settings import (
    LLM_MODEL_NAME,
    MAX_NEW_TOKENS,
    TEMPERATURE
)


def load_llm():
    print("Loading LLM:", LLM_MODEL_NAME)

    tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME)

    if torch.cuda.is_available():
        print("CUDA available. Loading model on GPU.")

        model = AutoModelForCausalLM.from_pretrained(
            LLM_MODEL_NAME,
            torch_dtype=torch.float16,
            device_map="auto"
        )

    else:
        print("CUDA not available. Loading model on CPU. This may be slow.")

        model = AutoModelForCausalLM.from_pretrained(
            LLM_MODEL_NAME,
            torch_dtype=torch.float32
        )

    generation_pipeline = pipeline(
        task="text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=MAX_NEW_TOKENS,
        # temperature=TEMPERATURE,
        do_sample=False,
        return_full_text=False
    )

    llm = HuggingFacePipeline(
        pipeline=generation_pipeline
    )

    return llm















# import torch

# from transformers import (
#     AutoTokenizer,
#     AutoModelForCausalLM,
#     pipeline
# )

# from langchain_huggingface import HuggingFacePipeline

# from config.settings import (
#     LLM_MODEL_NAME,
#     MAX_NEW_TOKENS
# )


# def load_llm():
#     print("Loading LLM:", LLM_MODEL_NAME)

#     tokenizer = AutoTokenizer.from_pretrained(
#         LLM_MODEL_NAME,
#         trust_remote_code=True
#     )

#     if tokenizer.pad_token is None:
#         tokenizer.pad_token = tokenizer.eos_token

#     if torch.cuda.is_available():
#         print("CUDA available. Loading model on GPU.")

#         model = AutoModelForCausalLM.from_pretrained(
#             LLM_MODEL_NAME,
#             dtype=torch.float16,
#             device_map="auto",
#             trust_remote_code=True
#         )

#     else:
#         print("CUDA not available. Loading model on CPU. This may be slow.")

#         model = AutoModelForCausalLM.from_pretrained(
#             LLM_MODEL_NAME,
#             dtype=torch.float32,
#             trust_remote_code=True
#         )

#     # Set generation settings directly on the model config
#     model.generation_config.max_new_tokens = MAX_NEW_TOKENS
#     model.generation_config.do_sample = False
#     model.generation_config.temperature = None
#     model.generation_config.top_p = None
#     model.generation_config.repetition_penalty = 1.15
#     model.generation_config.no_repeat_ngram_size = 4
#     model.generation_config.pad_token_id = tokenizer.pad_token_id
#     model.generation_config.eos_token_id = tokenizer.eos_token_id

#     generation_pipeline = pipeline(
#         task="text-generation",
#         model=model,
#         tokenizer=tokenizer,
#         return_full_text=False,
#         clean_up_tokenization_spaces=False
#     )

#     llm = HuggingFacePipeline(
#         pipeline=generation_pipeline
#     )

#     return llm