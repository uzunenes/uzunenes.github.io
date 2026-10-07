---
layout: post
title: "TRL v1.14.2 fixes prompt-completion training for Gemma 4 12B/26B/31B"
date: 2026-10-07
description: "With thinking off, the Gemma 4 12B/26B/31B chat template made TRL put the SFT loss on the wrong tokens and drop short answers; short DPO pairs compared nothing. Reported as huggingface/trl#7449, fixed by the maintainers in #7463, released in v1.14.2. What remains, and a two-line template patch."
tags: [trl, gemma, fine-tuning, chat-templates]
---

On 2026-10-06 Hugging Face released TRL v1.14.2. It fixes a bug I reported a week earlier: with the chat template of Gemma 4 12B, 26B-A4B and 31B, prompt-completion training put the loss on the wrong tokens and dropped short answers without an error. It affects SFT, DPO and KTO on TRL 1.14.1 and earlier when thinking is off, the default. The fix is by Quentin Gallouédec, reviewed by Albert Villanova. If you trained one of these models this way and saw the warning "Mismatch between tokenized prompt and the start of tokenized prompt+completion", upgrade and train again.

## Issue

TRL tokenizes a prompt-completion row twice: the prompt alone with `add_generation_prompt=True`, and prompt plus completion as a full conversation. Before the fix it assumed the first is a prefix of the second and set `completion_mask = [0] * len(prompt_ids) + [1] * rest`.

Gemma 4 12B-it, 26B-A4B-it and 31B-it share one chat template. When thinking is off, the generation prompt ends with an empty thought block, four tokens: `<|channel>thought\n<channel|>`. The full conversation render does not contain it. So the prompt is not a prefix, and the mask started four tokens too late. With `enable_thinking=True` the prompt is a prefix of the full render, 22 of 22 tokens, and nothing is lost. Gemma 4 E2B and E4B use a different template and are not affected.

This concerns prompt-completion data only; a dataset with a single `messages` column takes a different code path.

## Impact

I ran TRL 1.14.1 (transformers 5.19.0) with the tiny Gemma 4 test tokenizer and the official 12B template on `trl-internal-testing/zen`, 17 rows. SFT kept 9 of 17. Completions of four tokens or fewer were fully masked and dropped; the rest trained on the tail of the answer. Three rows before and after (`raw` is the dataset row, `proc` its index after preprocessing):

```text
# TRL 1.14.1
raw[ 0] 'What is better than ugly?': DROPPED (no processed row contains this prompt)
raw[ 7]->proc[ 1] loss tokens=12: " aren't special enough to break the rules.<turn|>\n"
raw[11]->proc[ 4] loss tokens= 5: ' to guess.<turn|>\n'

# TRL v1.14.2
raw[ 0]->proc[ 0] loss tokens= 4: 'Beautiful.<turn|>\n'
raw[ 7]->proc[ 7] loss tokens=16: "No, special cases aren't special enough to break the rules.<turn|>\n"
raw[11]->proc[11] loss tokens= 9: 'Refuse the temptation to guess.<turn|>\n'
```

The training sequence itself, `input_ids`, was already the full render; only the mask was wrong. DPO failed differently: the chosen and rejected ids of the short rows were empty or a newline, so the pair compared nothing.

```text
raw[ 0]->proc[ 0] chosen_ids='' rejected_ids='\n'
raw[ 1]->proc[ 1] chosen_ids='' rejected_ids=''
raw[12]->proc[12] chosen_ids=' only one.<turn|>\n' rejected_ids='.<turn|>\n'
```

KTO lost the first tokens of every completion the same way. No error was raised. The only signal was a generic warning, once per row, 17 times on this dataset: "Mismatch between tokenized prompt and the start of tokenized prompt+completion. This may be due to unexpected tokenizer behavior, whitespace issues, or special token handling. ..."

Olmo 3 has the same problem with its `<think>` prefill, three tokens: 10 of 17 rows kept, `'.<|endoftext|>'` trained where the answer was `'Practicality.<|endoftext|>'`. DeepSeek-R1-Distill, Nemotron 3 and Qwen3.5-Think diverge too; Qwen3, Qwen2.5 and Gemma 3 do not in the base case.

## Fix

I opened issue #7449 on 2026-09-29 and PR #7458 on 2026-09-30. My patch kept the inference prompt ids and appended the rest. The same day Quentin opened #7463 with a simpler approach. It keeps the full chat-template render and moves the prompt/completion boundary to where the tokenized prompt and the tokenized prompt+completion diverge; the difference is which side each PR keeps exact. Quentin, in a comment on the PR: "I prefer keeping the sequence a real template render, with less code. A context that differs from inference is a template bug anyway, so there is no 'right' way to handle it." #7458 was closed in favor of #7463 on 2026-10-01. #7463 merged on 2026-10-06 with a new `common_prefix_length` in `trl/data_utils.py`, covering SFT, DPO, KTO and the experimental TPO trainer.

After the fix all 17 rows are kept and the loss covers the whole assistant turn. DPO and KTO completions are whole turns too. The old warning is replaced by one `warning_once` per process. It names the excluded tokens and says "The model is trained on a context that differs from the one it sees at inference." It also fires for plain-text data when BPE merges tokens across the boundary (`'Hello '` + `'world'`).

## What remains

The fix moves the boundary; it does not put the thought block back. The PR description says so: "Without a patched training template, TRL can't make the training context match inference for them, but it can stop mis-masking the completion." With the stock template and thinking off, the training sequence ends with `model\nIt is blue.<turn|>\n`, while every inference prompt with thinking off ends with `model\n<|channel>thought\n<channel|>`. For DPO, KTO and TPO the prompt ids are also cut to the common prefix. On 1.14.1 their context was already the inference prompt and only the completion was broken; now the sequence is the full render, so for these templates the training context moved away from inference. The PR description documents this trade-off.

To make them match, add two lines to the official template: completed model turns also render the empty block when thinking is off. The `elif` branch and the line under it are new; the rest is context:

{% raw %}
```jinja
    {%- if thinking_text and thinking_gate -%}
        {{- '<|channel>thought\n' + thinking_text + '\n<channel|>' -}}
    {%- elif role == 'model' and not enable_thinking and loop.index0 > ns_turn.last_user_idx -%}
        {{- '<|channel>thought\n<channel|>' -}}
    {%- endif -%}
```
{% endraw %}

The patched file is [gemma-4-12B-it.training.jinja](/assets/gemma-4-12B-it.training.jinja). Pass it with `SFTConfig(chat_template_path="gemma-4-12B-it.training.jinja")`. The prompt is a prefix again, 19 of 19 tokens, there is no warning, and `input_ids` end with `\n<channel|>It is blue.<turn|>\n`. I measured this with SFTTrainer on single-turn rows only, for completion-only training: `assistant_only_loss=True` raises a ValueError with every Gemma 4 template I tried, because TRL has no training template with generation markers for it.

## Check it yourself

[verify_gemma4_prompt_prefix.py](/assets/verify_gemma4_prompt_prefix.py) needs `transformers` and `jinja2`, no torch. It renders a prompt both ways with the tiny test tokenizer and prints where they diverge:

```text
[official 12B template ]
  generation prompt ends with : 'model\n<|channel>thought\n<channel|>'
  common prefix               : 15/19 prompt tokens
  left out of training        : '<|channel>thought\n<channel|>'
  trained completion          : 'It is blue.<turn|>\n'
[official 12B template {'enable_thinking': True}]
  generation prompt ends with : '?<turn|>\n<|turn>model\n'
  common prefix               : 22/22 prompt tokens
  left out of training        : ''
  trained completion          : 'It is blue.<turn|>\n'
[patched 12B template ]
  generation prompt ends with : 'model\n<|channel>thought\n<channel|>'
  common prefix               : 19/19 prompt tokens
  left out of training        : ''
  trained completion          : 'It is blue.<turn|>\n'
```

`--trainer` also runs SFTTrainer on both templates; that mode needs `trl`, `torch` and `datasets`.

## Acknowledgments

I reported the bug and proposed a fix. The merged fix is Quentin Gallouédec's, reviewed by Albert Villanova.

## References

- [Issue #7449](https://github.com/huggingface/trl/issues/7449)
- [PR #7458](https://github.com/huggingface/trl/pull/7458), mine, closed
- [PR #7463](https://github.com/huggingface/trl/pull/7463), merged, 8 files, +172/-53
- [TRL v1.14.2](https://github.com/huggingface/trl/releases/tag/v1.14.2)
- [TRL SFT docs](https://huggingface.co/docs/trl/sft_trainer)
- [Gemma 4 12B chat template](https://huggingface.co/google/gemma-4-12B-it/blob/main/chat_template.jinja)
- [verify_gemma4_prompt_prefix.py](/assets/verify_gemma4_prompt_prefix.py), [gemma-4-12B-it.training.jinja](/assets/gemma-4-12B-it.training.jinja)
