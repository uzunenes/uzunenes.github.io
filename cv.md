---
layout: page
title: CV
permalink: /cv/
---

**Senior Software Architect** · Istanbul, Türkiye · Open to relocation worldwide

[Download PDF](/assets/enes-uzun-cv.pdf) · updated 29 Sep 2026

## Summary

Senior software architect at Ford Otosan (Ford Motor Company joint venture), working on AI infrastructure, with 8 years of production ML work. I run the on-prem GPU cluster and LLM serving stack used by 15,000 employees and 250 developers. Before that I built real-time computer vision systems in C/C++ that run in four car plants. My recent open-source work is on the reliability of coding agents with self-hosted models.

## Experience

### Senior Software Architect
*Ford Otosan (Ford Motor Company joint venture), Istanbul. Senior Software Engineer from Dec 2022 to Aug 2026.* · Aug 2026 – Present

- Designed and built the company's LLM gateway. It decides per request whether the data may leave the company: confidential code and documents go to open models on our own GPUs, the rest to Azure OpenAI. Access goes through Entra ID (OAuth2/OIDC).
- Deployed vLLM on on-prem GPUs behind OpenAI-compatible endpoints, so 250 developers use Copilot CLI with internal models (600+ agent requests a day) without code leaving the network or per-token API costs.
- Run the multi-site Kubernetes GPU cluster (5 servers; 2× H200, 4× A100, 4× L40S, 4× V100) with Prometheus and Grafana monitoring. It hosts the internal chatbot (15,000 users), the coding models and the production vision models.
- Turned MobileAI, our vision system in four plants, into a no-code platform where line engineers collect data, label and train models themselves. New models go live only after engineering review and are monitored for drift.
- Lead technical direction for a team of 9. The team's work received 2 global Ford and 2 local Koç Group innovation awards.

### Software Engineer, Network & Systems
*Ford Otosan, Gölcük plant* · May 2019 – Dec 2022

- Built Gözcü, a no-code platform for real-time accident detection on CCTV, deployable to a new camera in one click.
- Wrote its inference backend in C/C++ (GStreamer, OpenCV, YOLO): 250+ concurrent RTSP streams, under 200 ms end-to-end latency.
- Gözcü received Ford's President's Health & Safety Award in 2023. Gözcü and MobileAI are part of the Ford Otosan plant named a World Economic Forum Global Lighthouse in 2026.

### Software Engineer
*Evstek Information Technologies, Istanbul* · Jun 2018 – May 2019

- Developed the image-analysis software of KE-BOT, a robotic system for FUE hair transplantation (C++, OpenCV). The work was published at IEEE.

## Open source

### jcode, an agentic coding CLI in Rust
*3 bugs reported and root-caused, all fixed upstream* · Aug 2026

- Agents on self-hosted models (vLLM, SGLang, Ollama) stalled after context compaction. Traced it to custom providers being routed through the OpenRouter runtime, which dropped orphaned tool outputs ([#908](https://github.com/1jehuang/jcode/issues/908)).
- Models without a declared `input` list were treated as image-capable, causing an unrecoverable HTTP 400 loop. Isolated it with an A/B matrix; the text-only default I proposed was adopted ([#847](https://github.com/1jehuang/jcode/issues/847)).
- Shifted symbols were lost on Turkish Q keyboards in the VS Code terminal. Identified the missing Kitty `REPORT_ALTERNATE_KEYS` flag ([#870](https://github.com/1jehuang/jcode/issues/870)).

### Ultralytics YOLO
*[PR #20553](https://github.com/ultralytics/ultralytics/pull/20553), merged in release 8.3.131* · May 2025

- Co-authored, with three others, the official YOLO11 example for Triton Inference Server in C++: gRPC client, FP16 preprocessing, NMS, CMake build.

### Own projects
github.com/uzunenes

- [triton-server-hpa](https://github.com/uzunenes/triton-server-hpa): scales Triton on Kubernetes by GPU utilisation (DCGM metrics, Prometheus adapter, HPA), with GPU time-slicing so it runs on one GPU.
- [k8s-ai-stack](https://github.com/uzunenes/k8s-ai-stack): self-hosted LLM stack on Kubernetes with vLLM, Ollama and OpenWebUI (OAuth2), plus throughput benchmarks.
- [puci](https://github.com/uzunenes/puci): small AI coding-agent harness in C17; about 100 kB per session, runs 1,000 agents on one `poll()` loop for evaluation.
- [piciem](https://github.com/uzunenes/piciem), [librtsplink](https://github.com/uzunenes/librtsplink), [libmqttlink](https://github.com/uzunenes/libmqttlink): image processing in plain C (DFT/FFT, convolution), RTSP and MQTT client libraries.

## Skills

- **Inference:** vLLM, SGLang, Triton Inference Server, TensorRT, OpenAI-compatible APIs
- **Platform:** Kubernetes, OpenShift, Docker, ArgoCD, NVIDIA DCGM, Prometheus, Grafana, MLflow, GitHub Actions, Azure DevOps
- **Languages:** Python, C, Bash (expert); C++, Go; Rust (reading and debugging)
- **ML and vision:** PyTorch, YOLO, RT-DETR, OpenCV, GStreamer
- **Systems:** Linux, strace, perf; TCP/UDP, gRPC, MQTT, RTSP
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

### M.Sc. Electronics Engineering, coursework completed
*Gebze Technical University* · 2019 – 2023

- Research on unsupervised video anomaly detection with autoencoders (ICES 2023 paper above).

### B.Sc. Electronics and Telecommunication Engineering
*Kocaeli University* · 2013 – 2018

- Thesis: real-time lane departure warning on an embedded platform.

## Courses

Fast and Efficient LLM Inference with vLLM (DeepLearning.AI, 2026); Accelerate Your Model (Google DeepMind on DataCamp, 2026); Executive Leadership (Koç University, 2025); Certified Scrum Team Member (Scrum Inc., 2022).
