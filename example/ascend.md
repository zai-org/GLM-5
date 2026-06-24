# Using Ascend NPU to Deploy GLM-5.2

Currently, the Ascend platform already supports the deployment of GLM-5.2. Efficient Inference Optimization for the GLM-5.2 Model on the Ascend Platform focuses on the following key techniques:

1. **MoE Mega-Fusion Operator** – Expert routing, weighted computation, and result reduction are fused into a single unified operator, eliminating redundant reads and writes of intermediate tensors and significantly boosting computational efficiency.
2. **Communication–Computation Fusion** – By decomposing AllReduce into ReduceScatter and AllGather primitives and tightly coupling them with matrix computations in a pipeline, communication latency is effectively hidden.
3. **Attention Preprocessing and Multi-Token Prediction Optimization** – An attention preprocessing fusion operator is adopted, combined with accelerated Multi-Token Prediction (MTP), to improve single-step generation efficiency.
4. **High-Concurrency Scheduling with Prefill Delay** – In high-concurrency mixed-load scenarios, a prefill delay scheduling mechanism is introduced to smooth computation peaks and reduce resource contention between the Prefill and Decode phases.
5. **Intelligent Caching and Index Optimization** – IndexCache is used to cache high-frequency expert paths and static routing tables, and methods such as Chunked Prefill and sparse index retrieval are employed to optimize long-context inference performance.
6. **PD Separation and Prefix Caching** – By separating the Prefill and Decode stages and applying prefix caching, decode latency jitter is suppressed and throughput stability of online services is improved.
7. **Quantization Scheme** – A hybrid W8A8 quantization strategy is adopted. Through QuaRot preprocessing, Flex SmoothQuant smoothing, and SSZ weight quantization, expert weights are efficiently compressed while maintaining accuracy on critical paths.

# vLLM

This [vLLM-Ascend](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.2.html) document demonstrates how to deploy GLM-5.2 on vLLM using the vLLM-Ascend plugin. It shows the main verification steps of the model, including supported features, feature configuration, environment preparation, single-node and multi-node deployment, Prefill-Decode disaggregation, accuracy and performance evaluation.

# SGLang

This [sgLang](https://github.com/sgl-project/sglang/blob/main/docs_new/docs/hardware-platforms/ascend-npus/ascend_npu_glm5.2_examples.mdx) document demonstrates how to deploy GLM-5.2 on sglang. It shows the main verification steps of the model, including supported features, feature configuration, environment preparation, single-node and multi-node deployment, accuracy and performance evaluation.

# xLLM

This [xLLM](https://github.com/jd-opensource/xllm/blob/preview/glm-5.2/docs/zh/getting_started/quick_start_GLM5.md) document demonstrates how to deploy GLM-5.2 on xLLM. It shows the main verification steps of the model, including supported features, feature configuration, environment preparation, single-node and multi-node deployment, Prefill-Decode disaggregation, accuracy and performance evaluation.
