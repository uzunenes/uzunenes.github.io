---
layout: page
title: About
permalink: /about/
---

I'm a senior software architect at Ford Otosan, the Ford Motor Company joint venture in Türkiye. I work on the infrastructure that runs AI models inside the company.

### What I work on now

I run our on-prem GPU cluster and the LLM serving stack on top of it. The internal chatbot has 15,000 users, and 250 developers use self-hosted coding models through vLLM, around 600 agent requests a day, without their code leaving the network. In front of the models sits a gateway I designed: for each request it decides whether the data may go to Azure OpenAI or has to stay on our own GPUs.

The cluster spans several sites and mixes H200, A100, L40S and V100 GPUs under one Kubernetes setup. I spoke about how we run it at KCD Istanbul 2026.

### Before LLMs

I spent five years on real-time computer vision in C and C++. Gözcü, an accident-detection system for the production line, handles more than 250 camera streams at under 200 ms. MobileAI lets line engineers collect data, label it and train their own quality models in four plants, with engineering review before anything goes live. Gözcü won Ford's President's Health & Safety Award in 2023, and both systems are part of the plant named a World Economic Forum Global Lighthouse in 2026.

### Open source

- Co-authored the official [YOLO11 example for Triton Inference Server in C++](https://github.com/ultralytics/ultralytics/pull/20553) in Ultralytics.
- Reported and root-caused three bugs in the [jcode](https://github.com/1jehuang/jcode/issues/908) coding agent while running it on self-hosted vLLM and SGLang. All were fixed upstream.
- Maintain [triton-server-hpa](https://github.com/uzunenes/triton-server-hpa) (GPU-based autoscaling for Triton) and [k8s-ai-stack](https://github.com/uzunenes/k8s-ai-stack) (a self-hosted LLM stack on Kubernetes).

### Contact

[me@uzunenes.com](mailto:me@uzunenes.com), [LinkedIn](https://www.linkedin.com/in/uzunenes), [GitHub](https://github.com/uzunenes).
