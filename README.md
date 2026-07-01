# GLM-5.2 & GLM-5.1 & GLM-5

[![Listed on TakoAPI](https://takoapi.com/api/badge/zai-org-glm-5)](https://takoapi.com/agents/zai-org-glm-5)

<div align="center">
<img src=resources/logo.svg width="15%"/>
</div>
<p align="center">
    👋 Join our <a href="resources/WECHAT.md" target="_blank">Wechat</a> or <a href="https://discord.gg/Hc5z9bx5Xw" target="_blank">Discord</a> community.
    <br>
    📖 Check out the GLM-5.2 <a href="https://z.ai/blog/glm-5.2" target="_blank">blog</a> and GLM-5 <a href="https://arxiv.org/abs/2602.15763" target="_blank">Technical report</a>.
    <br>
    📍 Use GLM-5.2 API services on <a href="https://docs.z.ai/guides/llm/glm-5.2">Z.ai API Platform. </a>
    <br>
    🔜 Try GLM-5.2 at <a href="https://z.ai">z.ai</a>.
</p>

## Introduction

### GLM-5.2

GLM-5.2, our latest flagship model for long-horizon tasks. It marks a substantial leap in long-horizon task capability over its predecessor GLM-5.1 and, for the first time, delivers that capability on a **solid 1M-token context**. 

GLM-5.2's new capabilities include:
- **Solid 1M Context:** A solid 1M-token context that stably sustains long-horizon work
- **Advanced Coding with Flexible Effort**: Stronger coding capabilities with multiple thinking effort levels to balance performance and latency
- **Improved Architecture**: We propose [IndexShare](https://arxiv.org/abs/2603.12201), which reuses the same indexer across every four sparse attention layers, reducing per-token FLOPs by 2.9× at a 1M context length. We also improve GLM-5.2’s MTP layer for speculative decoding, increasing the acceptance length by up to 20%

![bench_52](resources/bench_52.png)

On standard coding benchmarks, GLM-5.2 is the strongest open-source model, improving on GLM-5.1 by a wide margin: 81.0 vs. 62.0 on Terminal-Bench 2.1 and 62.1 vs. 58.4 on SWE-bench Pro. It also closes much of the gap to the closed-source frontier — on Terminal-Bench 2.1 (81.0) it lands within a few points of Claude Opus 4.8 (85.0) — while staying ahead of Gemini 3.1 Pro.

For more detail, check our [blog](https://z.ai/blog/glm-5.2).

### GLM-5.1

GLM-5.1 is our next-generation flagship model for agentic engineering, with significantly stronger coding capabilities than its predecessor. It achieves state-of-the-art performance on SWE-Bench Pro and leads GLM-5 by a wide margin on NL2Repo (repo generation) and Terminal-Bench 2.0 (real-world terminal tasks).

![bench_51](resources/bench_51.png)

But the most meaningful leap goes beyond first-pass performance. Previous models—including GLM-5—tend to exhaust their repertoire early: they apply familiar techniques for quick initial gains, then plateau. Giving them more time doesn't help.

GLM-5.1, by contrast, is built to stay effective on agentic tasks over much longer horizons. We've found that the model handles ambiguous problems with better judgment and stays productive over longer sessions. It breaks complex problems down, runs experiments, reads results, and identifies blockers with real precision. By revisiting its reasoning and revising its strategy through repeated iteration, GLM-5.1 sustains optimization over hundreds of rounds and thousands of tool calls. The longer it runs, the better the result.

### GLM-5

We are launching GLM-5, targeting complex systems engineering and long-horizon agentic tasks. Scaling is still one of the most important ways to improve the intelligence efficiency of Artificial General Intelligence (AGI). Compared to GLM-4.5, GLM-5 scales from 355B parameters (32B active) to 744B parameters (40B active), and increases pre-training data from 23T to 28.5T tokens. GLM-5 also integrates DeepSeek Sparse Attention (DSA), largely reducing deployment cost while preserving long-context capacity.

Reinforcement learning aims to bridge the gap between competence and excellence in pre-trained models. However, deploying it at scale for LLMs is a challenge due to the RL training inefficiency. To this end, we developed [slime](https://github.com/THUDM/slime), a novel **asynchronous RL infrastructure** that substantially improves training throughput and efficiency, enabling more fine-grained post-training iterations. With advances in both pre-training and post-training, GLM-5 delivers significant improvement compared to GLM-4.7 across a wide range of academic benchmarks and achieves best-in-class performance among all open-source models in the world on reasoning, coding, and agentic tasks,  closing the gap with frontier models.

![bench](resources/bench.png)

GLM-5 is purpose-built for complex systems engineering and long-horizon agentic tasks. On our internal evaluation suite CC-Bench-V2, GLM-5 significantly outperforms GLM-4.7 across frontend, backend, and long-horizon tasks, narrowing the gap to Claude Opus 4.5.

![realworld_bench](resources/realworld_bench.png)

On [Vending Bench 2](https://andonlabs.com/evals/vending-bench-2), a benchmark that measures long-term operational capability, GLM-5 ranks \#1 among open-source models. Vending Bench 2 requires the model to run a simulated vending machine business over a one-year horizon; GLM-5 finishes with a final account balance of $4,432, approaching Claude Opus 4.5 and demonstrating strong long-term planning and resource management.

![vending_bench](resources/vending_bench.png)

## Download Model

| Model       | Download Links                                                                                                                      | Model Size | Precision |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------|------------|-----------|
| GLM-5.2     | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-5.2)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-5.2)         | 744B-A40B  | BF16      |
| GLM-5.2-FP8 | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-5.2-FP8)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-5.2-FP8) | 744B-A40B  | FP8       |
| GLM-5.1     | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-5.1)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-5.1)         | 744B-A40B  | BF16      |
| GLM-5.1-FP8 | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-5.1-FP8)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-5.1-FP8) | 744B-A40B  | FP8       |
| GLM-5       | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-5)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-5)             | 744B-A40B  | BF16      |
| GLM-5-FP8   | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-5-FP8)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-5-FP8)     | 744B-A40B  | FP8       |

## Serve GLM-5 Series Locally

GLM-5.2 supports deployment with the following frameworks. Feel free to try them out:

- [SGLang](https://github.com/sgl-project/sglang) (v0.5.13.post1+) — see [cookbook](https://cookbook.sglang.io/autoregressive/GLM/GLM-5.2)
- [vLLM](https://github.com/vllm-project/vllm) (v0.23.0+) — see [recipes](https://recipes.vllm.ai/zai-org/GLM-5.2)
- [Transformers](https://github.com/huggingface/transformers) (v0.5.12+) — see [transformers docs](https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/glm_moe_dsa.md)
- [KTransformers](https://github.com/kvcache-ai/ktransformers) (v0.5.12+) — see [tutorial](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/kt-kernel/GLM-5.2-Tutorial.md)
- [Unsloth](https://github.com/unslothai/unsloth) (v0.1.47-beta+) — see [guide](https://unsloth.ai/docs/models/glm-5.2)
- For deployment on the `Ascend NPU` platform, inference frameworks such as vLLM-Ascend, xLLM and SGLang are supported — see [here](example/ascend.md).

GLM-5 supports controlling the thinking budget through the `reasoning_effort` parameter, which accepts two levels: `max` and `high`. **`max` is the default** — if `reasoning_effort` is left unset (or set to any value other than `high`), the model runs at `Max`. To use the `High` level, you must explicitly pass `reasoning_effort="high"`. For default scenarios such as benchmark/leaderboard reproduction, keep `Max` (no setting required); only set `reasoning_effort="high"` when you specifically want the `High` level. Thinking can be turned off entirely by setting `enable_thinking=false`.

## Citation

If you find GLM-5 series model useful in your research, please cite our technical report:

```bibtex
@misc{glm5team2026glm5vibecodingagentic,
      title={GLM-5: from Vibe Coding to Agentic Engineering},
      author={GLM-5-Team and : and Aohan Zeng and Xin Lv and Zhenyu Hou and Zhengxiao Du and Qinkai Zheng and Bin Chen and Da Yin and Chendi Ge and Chenghua Huang and Chengxing Xie and Chenzheng Zhu and Congfeng Yin and Cunxiang Wang and Gengzheng Pan and Hao Zeng and Haoke Zhang and Haoran Wang and Huilong Chen and Jiajie Zhang and Jian Jiao and Jiaqi Guo and Jingsen Wang and Jingzhao Du and Jinzhu Wu and Kedong Wang and Lei Li and Lin Fan and Lucen Zhong and Mingdao Liu and Mingming Zhao and Pengfan Du and Qian Dong and Rui Lu and Shuang-Li and Shulin Cao and Song Liu and Ting Jiang and Xiaodong Chen and Xiaohan Zhang and Xuancheng Huang and Xuezhen Dong and Yabo Xu and Yao Wei and Yifan An and Yilin Niu and Yitong Zhu and Yuanhao Wen and Yukuo Cen and Yushi Bai and Zhongpei Qiao and Zihan Wang and Zikang Wang and Zilin Zhu and Ziqiang Liu and Zixuan Li and Bojie Wang and Bosi Wen and Can Huang and Changpeng Cai and Chao Yu and Chen Li and Chengwei Hu and Chenhui Zhang and Dan Zhang and Daoyan Lin and Dayong Yang and Di Wang and Ding Ai and Erle Zhu and Fangzhou Yi and Feiyu Chen and Guohong Wen and Hailong Sun and Haisha Zhao and Haiyi Hu and Hanchen Zhang and Hanrui Liu and Hanyu Zhang and Hao Peng and Hao Tai and Haobo Zhang and He Liu and Hongwei Wang and Hongxi Yan and Hongyu Ge and Huan Liu and Huanpeng Chu and Jia'ni Zhao and Jiachen Wang and Jiajing Zhao and Jiamin Ren and Jiapeng Wang and Jiaxin Zhang and Jiayi Gui and Jiayue Zhao and Jijie Li and Jing An and Jing Li and Jingwei Yuan and Jinhua Du and Jinxin Liu and Junkai Zhi and Junwen Duan and Kaiyue Zhou and Kangjian Wei and Ke Wang and Keyun Luo and Laiqiang Zhang and Leigang Sha and Liang Xu and Lindong Wu and Lintao Ding and Lu Chen and Minghao Li and Nianyi Lin and Pan Ta and Qiang Zou and Rongjun Song and Ruiqi Yang and Shangqing Tu and Shangtong Yang and Shaoxiang Wu and Shengyan Zhang and Shijie Li and Shuang Li and Shuyi Fan and Wei Qin and Wei Tian and Weining Zhang and Wenbo Yu and Wenjie Liang and Xiang Kuang and Xiangmeng Cheng and Xiangyang Li and Xiaoquan Yan and Xiaowei Hu and Xiaoying Ling and Xing Fan and Xingye Xia and Xinyuan Zhang and Xinze Zhang and Xirui Pan and Xu Zou and Xunkai Zhang and Yadi Liu and Yandong Wu and Yanfu Li and Yidong Wang and Yifan Zhu and Yijun Tan and Yilin Zhou and Yiming Pan and Ying Zhang and Yinpei Su and Yipeng Geng and Yong Yan and Yonglin Tan and Yuean Bi and Yuhan Shen and Yuhao Yang and Yujiang Li and Yunan Liu and Yunqing Wang and Yuntao Li and Yurong Wu and Yutao Zhang and Yuxi Duan and Yuxuan Zhang and Zezhen Liu and Zhengtao Jiang and Zhenhe Yan and Zheyu Zhang and Zhixiang Wei and Zhuo Chen and Zhuoer Feng and Zijun Yao and Ziwei Chai and Ziyuan Wang and Zuzhou Zhang and Bin Xu and Minlie Huang and Hongning Wang and Juanzi Li and Yuxiao Dong and Jie Tang},
      year={2026},
      eprint={2602.15763},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2602.15763},
}
```
