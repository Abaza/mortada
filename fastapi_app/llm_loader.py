import os

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
    import torch, threading
    _HAVE_TRANSFORMERS = True
except Exception:  # pragma: no cover - optional heavy deps
    _HAVE_TRANSFORMERS = False

MODEL_ID = os.getenv("LLM_MODEL_ID", "tiiuae/Falcon-Arabic-7B-Instruct")

if _HAVE_TRANSFORMERS:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        device_map="auto",
        load_in_4bit=True,
        trust_remote_code=True,
    )


def stream(prompt: str, max_new_tokens: int = int(os.getenv("MAX_NEW_TOKENS", "768"))):
    """Yield tokens from the language model.

    In test environments where transformers or torch are unavailable, this
    function returns a trivial response to avoid heavy downloads.
    """

    if not _HAVE_TRANSFORMERS:
        yield "(mock answer)"
        return

    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)
    streamer = TextIteratorStreamer(tokenizer)
    thread = threading.Thread(
        target=model.generate,
        kwargs=dict(
            input_ids=input_ids,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            streamer=streamer,
            pad_token_id=tokenizer.eos_token_id,
        ),
    )
    thread.start()
    for text in streamer:
        yield text
    thread.join()
