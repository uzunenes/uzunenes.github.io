---
layout: page
title: Enes Uzun
---

<section class="hero">
  <h1>Enes Uzun</h1>
  <p class="role">Senior Software Architect · Ford Otosan · Istanbul</p>
  <p>I run Ford Otosan's on-prem AI platform: GPU clusters, LLM serving for developers' coding agents and an internal chatbot. I write here about inference, GPUs and coding agents.</p>
  <div class="links">
    <a class="btn primary" href="/cv/">CV</a>
    <a class="btn" href="/assets/enes-uzun-cv.pdf">PDF</a>
    <a class="btn" href="https://github.com/uzunenes">GitHub</a>
    <a class="btn" href="https://www.linkedin.com/in/uzunenes">LinkedIn</a>
    <a class="btn" href="mailto:me@uzunenes.com">me@uzunenes.com</a>
  </div>
</section>

<div class="stats">
  <div class="stat"><b>250</b><span>developers served</span></div>
  <div class="stat"><b>25K</b><span>requests a day on 2× H200</span></div>
  <div class="stat"><b>93%</b><span>prompt tokens from prefix cache</span></div>
  <div class="stat"><b>&lt; 1 s</b><span>p95 time to first token</span></div>
</div>

<h2 class="section-title">Selected work</h2>
<div class="cards">
  <a class="card" href="https://github.com/uzunenes/triton-server-hpa">
    <h3>triton-server-hpa</h3>
    <p>Autoscale NVIDIA Triton on Kubernetes by GPU utilisation: DCGM, Prometheus adapter, HPA, GPU time-slicing.</p>
    <span class="tag">Python · Kubernetes</span>
  </a>
  <a class="card" href="https://github.com/uzunenes/k8s-ai-stack">
    <h3>k8s-ai-stack</h3>
    <p>Self-hosted LLM stack on Kubernetes with vLLM, Ollama and OpenWebUI behind OAuth2.</p>
    <span class="tag">Go · vLLM</span>
  </a>
  <a class="card" href="https://github.com/ultralytics/ultralytics/pull/20553">
    <h3>Ultralytics YOLO11 + Triton</h3>
    <p>Co-authored the official C++ example for Triton Inference Server; merged in release 8.3.131.</p>
    <span class="tag">C++ · merged</span>
  </a>
  <a class="card" href="/2026/10/07/trl-v1-14-2-gemma-4-prompt-completion-fix.html">
    <h3>TRL Gemma 4 bug</h3>
    <p>Root-caused wrong loss masking in prompt-completion training. Fixed upstream in v1.14.2.</p>
    <span class="tag">Hugging Face TRL</span>
  </a>
</div>

<h2 class="section-title">Writing</h2>
<ul class="post-list">
  {% for post in site.posts limit:5 %}
  <li>
    <span class="date">{{ post.date | date: "%-d %b %Y" }}</span><br>
    <a href="{{ post.url }}">{{ post.title }}</a>
  </li>
  {% endfor %}
</ul>
