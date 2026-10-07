"""Check the claims of the TRL docs note on Gemma 4 and prompt-completion SFT.

Needs `pip install transformers jinja2`. No torch, no GPU.

1. Downloads the official google/gemma-4-12B-it chat template (same file as 26B-A4B-it and 31B-it).
2. Renders a prompt with the generation prompt vs. the prompt followed by the completion, tokenizes both
   with the tiny Gemma 4 test tokenizer, and prints where they diverge and what is left out.
3. Does the same with `enable_thinking=True` (prompt is a prefix, nothing left out).
4. Builds the remedy: the same template plus two lines that also render the empty thought block in
   completed model turns, and shows the prompt is a prefix again.

Optional: `python verify_gemma4_prompt_prefix.py --trainer` also runs SFTTrainer with `chat_template_path`
on the stock and the patched template (needs `pip install trl torch datasets`, CPU is fine).
"""

import sys
import urllib.request

from transformers import AutoTokenizer

TEMPLATE_URL = "https://huggingface.co/google/gemma-4-12B-it/resolve/main/chat_template.jinja"
TOKENIZER = "trl-internal-testing/tiny-Gemma4ForConditionalGeneration"

PROMPT = [{"role": "user", "content": "What color is the sky?"}]
COMPLETION = [{"role": "assistant", "content": "It is blue."}]


def common_prefix_length(ids, other_ids):
    # Same as trl.data_utils.common_prefix_length (added in TRL #7463).
    length = 0
    for token, other_token in zip(ids, other_ids):
        if token != other_token:
            break
        length += 1
    return length


def patch(template):
    # Also render the empty thought block in completed model turns when thinking is off, so the
    # full conversation renders the same prefix as the generation prompt.
    needle = (
        "    {%- if thinking_text and thinking_gate -%}\n"
        "        {{- '<|channel>thought\\n' + thinking_text + '\\n<channel|>' -}}\n"
        "    {%- endif -%}\n"
    )
    assert template.count(needle) == 1, "template layout changed, patch by hand"
    return template.replace(
        needle,
        "    {%- if thinking_text and thinking_gate -%}\n"
        "        {{- '<|channel>thought\\n' + thinking_text + '\\n<channel|>' -}}\n"
        "    {%- elif role == 'model' and not enable_thinking and loop.index0 > ns_turn.last_user_idx -%}\n"
        "        {{- '<|channel>thought\\n<channel|>' -}}\n"
        "    {%- endif -%}\n",
    )


def show(tok, name, template, **kwargs):
    prompt_ids = tok.apply_chat_template(
        PROMPT, chat_template=template, add_generation_prompt=True, tokenize=True, return_dict=True, **kwargs
    )["input_ids"]
    full_ids = tok.apply_chat_template(
        PROMPT + COMPLETION, chat_template=template, tokenize=True, return_dict=True, **kwargs
    )["input_ids"]
    n = common_prefix_length(prompt_ids, full_ids)
    print(f"[{name} {kwargs or ''}]")
    print(f"  generation prompt ends with : {tok.decode(prompt_ids[-6:])!r}")
    print(f"  common prefix               : {n}/{len(prompt_ids)} prompt tokens")
    print(f"  left out of training        : {tok.decode(prompt_ids[n:])!r}")
    print(f"  trained completion          : {tok.decode(full_ids[n:])!r}")


def main():
    official = urllib.request.urlopen(TEMPLATE_URL).read().decode("utf-8")
    patched = patch(official)
    tok = AutoTokenizer.from_pretrained(TOKENIZER)

    show(tok, "official 12B template", official)
    show(tok, "official 12B template", official, enable_thinking=True)
    show(tok, "patched 12B template", patched)

    if "--trainer" in sys.argv:
        import logging, io, tempfile
        from datasets import Dataset
        from trl import SFTConfig, SFTTrainer

        with open("gemma-4-12B-it.jinja", "w", encoding="utf-8") as f:
            f.write(official)
        with open("gemma-4-12B-it.training.jinja", "w", encoding="utf-8") as f:
            f.write(patched)
        ds = Dataset.from_list([{"prompt": PROMPT, "completion": COMPLETION}] * 4)
        for path in ["gemma-4-12B-it.jinja", "gemma-4-12B-it.training.jinja"]:
            buf = io.StringIO()
            handler = logging.StreamHandler(buf)
            logging.getLogger("trl.trainer.sft_trainer").addHandler(handler)
            with tempfile.TemporaryDirectory() as out:
                trainer = SFTTrainer(
                    model=TOKENIZER,
                    args=SFTConfig(output_dir=out, report_to="none", use_cpu=True, chat_template_path=path),
                    train_dataset=ds,
                )
                ex = trainer.train_dataset[0]
                labels = [t for t in ex["labels"] if t != -100]
                print(f"[SFTTrainer, chat_template_path={path}]")
                print(f"  input_ids tail : {tok.decode(ex['input_ids'][-8:])!r}")
                print(f"  trained labels : {tok.decode(labels)!r}")
                print(f"  warning emitted: {'not a prefix' in buf.getvalue()}")
            logging.getLogger("trl.trainer.sft_trainer").removeHandler(handler)


if __name__ == "__main__":
    main()
