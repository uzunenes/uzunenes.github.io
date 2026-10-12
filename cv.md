---
layout: page
title: CV
permalink: /cv/
---

**Senior Software Architect** · Istanbul, Türkiye · Open to relocation worldwide

[Download PDF](/assets/enes-uzun-cv.pdf) · updated 12 Oct 2026

## Summary

Senior software architect at Ford Otosan (Ford Motor Company joint venture) with 8 years of production ML work. I work on the company's on-prem AI platform: the GPU cluster, the LLM serving that 250 developers and their coding agents use (about 25,000 requests a day on two H200s, 93% of prompt tokens served from the prefix cache), and the internal chatbot for 15,000 employees. Before that I built real-time computer vision systems in C/C++ that run in four car plants, analysing 250+ camera streams in real time. My recent open-source work is bug reports and root-cause analysis for self-hosted LLMs in SGLang, Hugging Face TRL and jcode.

## Experience

### Senior Software Architect
*Ford Otosan (Ford Motor Company joint venture), Istanbul. Senior Software Engineer from Dec 2022 to Aug 2026.* · Aug 2026 – Present

- Designed and built the company's LLM gateway. It decides per request whether the data may leave the company: confidential code and documents go to open models on our own GPUs, the rest to Azure OpenAI. Access goes through Entra ID (OAuth2/OIDC).
- Run the inference service for 250 developers and their coding agents on two H200 GPUs (SGLang with speculative decoding): about 25,000 requests a day with ~96K-token prompts, 2.4B prompt tokens a day of which 93% are served from the prefix cache, and p95 time to first token under 1 s. Code never leaves the network and there are no per-token API costs.
- Run the Kubernetes GPU cluster across three sites in two countries (5 servers, 16 GPUs: 2× H200, 4× A100, 6× L40S, 4× V100) with Prometheus and Grafana monitoring. It hosts the internal chatbot (15,000 users), the coding models, LLM fine-tuning and the production vision models.
- Turned MobileAI, our vision system in four plants, into a no-code platform where line engineers collect data, label and train models themselves. New models go live only after engineering review and are monitored for drift.
- Lead technical direction for a team of 9. The team's work received 2 global Ford and 2 local Koç Group innovation awards.

### Software Engineer, Network & Systems
*Ford Otosan, Gölcük plant* · May 2019 – Dec 2022

- Built Gözcü, a no-code platform for real-time accident detection on CCTV, deployable to a new camera in one click.
- Wrote its inference backend in C/C++ (GStreamer, OpenCV, YOLO): 250+ concurrent RTSP streams, under 200 ms end-to-end latency.
- Gözcü and MobileAI are part of the Ford Otosan plant named a World Economic Forum Global Lighthouse in 2026.

### Software Engineer
*Evstek Information Technologies, Istanbul* · Jun 2018 – May 2019

- Developed the image-analysis software of KE-BOT, a robotic system for FUE hair transplantation (C++, OpenCV).

## Open source

### Hugging Face TRL
*[Issue #7449](https://github.com/huggingface/trl/issues/7449); fix merged as [PR #7463](https://github.com/huggingface/trl/pull/7463)* · Sep – Oct 2026

- Found and root-caused a bug where prompt-completion training (SFT, DPO, KTO) on Gemma 4 12B/26B/31B put the loss on the wrong tokens and silently dropped short answers. Opened the issue and a patch; the maintainers merged a closely related fix that credits me as co-author, released in v1.14.2 ([write-up](https://uzunenes.com/2026/10/07/trl-v1-14-2-gemma-4-prompt-completion-fix.html)).

### SGLang
*[Issue #36333](https://github.com/sgl-project/sglang/issues/36333): production reports* · Sep – Oct 2026

- Reported a production failure on v0.5.17 (DeepSeek-V4-Flash, 2× H200): after a streaming client disconnected, an orphan request flooded the logs, the detokenizer stopped responding and Kubernetes restarted the server. After the upstream fix, confirmed on v0.5.20 with about 28 hours and 45,000 production requests and controlled disconnect tests that it no longer occurs.

### jcode, an agentic coding CLI in Rust
*3 bugs reported and root-caused, all fixed upstream* · Aug 2026

- Agents on self-hosted models (vLLM, SGLang, Ollama) stalled after context compaction. Traced it to custom providers being routed through the OpenRouter runtime, which dropped orphaned tool outputs ([#908](https://github.com/1jehuang/jcode/issues/908)).
- Models without a declared `input` list were treated as image-capable, causing an unrecoverable HTTP 400 loop. Isolated it with an A/B matrix; the text-only default I proposed was adopted ([#847](https://github.com/1jehuang/jcode/issues/847)).

### Ultralytics YOLO
*[PR #20553](https://github.com/ultralytics/ultralytics/pull/20553), merged in release 8.3.131* · May 2025

- Co-authored, with three others, the official YOLO11 example for Triton Inference Server in C++: gRPC client, FP16 preprocessing, NMS, CMake build.

### Own projects
github.com/uzunenes

- [triton-server-hpa](https://github.com/uzunenes/triton-server-hpa): scales Triton on Kubernetes by GPU utilisation (DCGM metrics, Prometheus adapter, HPA), with GPU time-slicing so it runs on one GPU.
- [k8s-ai-stack](https://github.com/uzunenes/k8s-ai-stack): self-hosted LLM stack on Kubernetes with vLLM, Ollama and OpenWebUI (OAuth2), plus throughput benchmarks.
- [puci](https://github.com/uzunenes/puci): small AI coding-agent harness in C17; about 100 kB per session, runs 1,000 agents on one `poll()` loop for evaluation.

## Skills

- **Inference:** vLLM, SGLang, Triton Inference Server, TensorRT, OpenAI-compatible APIs
- **Platform:** Kubernetes, OpenShift, Docker, ArgoCD, NVIDIA DCGM, Prometheus, Grafana, MLflow, GitHub Actions, Azure DevOps, Linux (strace, perf); gRPC, MQTT, RTSP
- **Languages:** Python, C, Bash (expert); C++, Go
- **ML and vision:** PyTorch, YOLO, RT-DETR, OpenCV, GStreamer
- **Spoken:** Turkish (native), English (professional)

## Publications and talks

- *Autoencoder-based video anomaly detection.* 2nd International Conference of Engineering Sciences (ICES), Dec 2023.
- Image analysis for the KE-BOT hair transplantation robot. IEEE Xplore, document [8719213](https://ieeexplore.ieee.org/document/8719213).
- *Multi-site Kubernetes for on-prem GPU workloads.* Talk at KCD Istanbul 2026 (Kubernetes Community Days, CNCF), Jul 2026.

## Awards

### Global Manufacturing Technical Excellence Award
*Ford Motor Company* · Apr 2025

- For robotic vision in global manufacturing.

### President's Health & Safety Award
*Ford Motor Company* · Jun 2023

- For combining AI, computer vision and collaborative robots on the line. Signed by CEO Jim Farley.

## Education

### M.Sc. Electronics Engineering
*Gebze Technical University* · 2019 – Jan 2027 (expected)

- Coursework completed 2019–2022; thesis started in 2026, graduation expected January 2027.

### B.Sc. Electronics and Telecommunication Engineering
*Kocaeli University* · 2013 – 2018
