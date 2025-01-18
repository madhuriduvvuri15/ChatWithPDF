from langchain.llms import LlamaCpp # type: ignore
from langchain.callbacks.manager import CallbackManager # type: ignore
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler # type: ignore

model_path = 'C:/Users/Madhuri Personal/Documents/ML/ChatwithPDF/llama-2-7b-chat.Q4_K_M.gguf'

class Loadllm:
    @staticmethod
    def load_llm():
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        # Prepare the LLM

        llm = LlamaCpp(
            model_path=model_path,
            n_gpu_layers=40,
            n_batch=512, # Batch size to use during inference. A batch is a collection of input samples processed together in a single forward pass
            n_ctx=2048, #  MOdel considers preceding 2048 tokens as context when generating predictions for the next token.
            f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
            callback_manager=callback_manager,
            verbose=True,
        )

        return llm