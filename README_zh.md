# GLM-5.2 & GLM-5.1 & GLM-5

<div align="center">
<img src=resources/logo.svg width="15%"/>
</div>
<p align="center">
    👋 加入我们的 <a href="resources/WECHAT.md" target="_blank">微信</a> 或 <a href="https://discord.gg/Hc5z9bx5Xw" target="_blank">Discord</a> 社区。
    <br>
    📖 查看 GLM-5.2 <a href="https://z.ai/blog/glm-5.2" target="_blank">技术博客</a> 和 GLM-5 <a href="https://arxiv.org/abs/2602.15763" target="_blank">技术报告</a>。
    <br>
    📍 在 <a href="https://docs.bigmodel.cn/cn/guide/models/text/glm-5.2">API 平台</a> 使用 GLM-5.2 API 服务。
    <br>
    🔜 在 <a href="https://z.ai">z.ai</a> 上体验 GLM-5.2。
</p>

## 简介

### GLM-5.2

GLM-5.2，面向长程任务的最新旗舰模型。相比前代 GLM-5.1，它在长周期任务能力上实现了重大飞跃，并且首次在**稳定的 100 万 token 上下文**上交付这一能力。

GLM-5.2 的新能力包括：
- **稳定的 100 万上下文：** 提供稳定的 100 万 token 上下文，可持续支撑长周期工作
- **支持弹性思考力度的高级编码**：更强的编码能力，并提供多档思考力度（thinking effort），以平衡性能与延迟
- **改进的架构**：我们提出了 [IndexShare](https://arxiv.org/abs/2603.12201)，在每四个稀疏注意力层之间复用同一个索引器，在 100 万上下文长度下将每 token 的 FLOPs 降低 2.9 倍。我们还改进了 GLM-5.2 用于推测解码的 MTP 层，将接受长度提升最多 20%。

![bench_52](resources/bench_52.png)

在标准编码基准测试中，GLM-5.2 是最强的开源模型，相比 GLM-5.1 大幅领先：在 Terminal-Bench 2.1 上为 81.0 对 62.0，在 SWE-bench Pro 上为 62.1 对 58.4。它还大幅缩小了与闭源前沿模型的差距——在 Terminal-Bench 2.1（81.0）上，与 Claude Opus 4.8（85.0）仅相差几分——同时保持领先于 Gemini 3.1 Pro。

更多细节，请查看我们的[博客](https://z.ai/blog/glm-5.2)。

### GLM-5.1

GLM-5.1 是我们面向智能体工程的新一代旗舰模型，代码能力较前代有显著跃升。在 SWE-Bench Pro 上达到业界领先水平，并在 NL2Repo（仓库级代码生成）和 Terminal-Bench 2.0（真实终端任务）上大幅超越 GLM-5。

![bench_51](resources/bench_51.png)

但最具意义的突破，不在于单次表现的上限，而在于持续优化的能力。此前的模型——包括 GLM-5——往往很快就"用尽招数"：凭借熟悉的策略快速取得初始收益后便陷入瓶颈，给再多时间也无济于事。

GLM-5.1 则不同。它天生适合在更长的时间跨度上执行智能体任务。我们发现，面对模糊问题，它展现出更优的判断力，并能在长时间会话中保持高效产出——拆解复杂问题、设计实验、解读结果、精准定位瓶颈。通过反复审视自身推理、动态调整策略，GLM-5.1 能够在数百轮迭代、数千次工具调用中持续优化。运行越久，结果越好。

### GLM-5

我们推出了 GLM-5，旨在解决复杂系统工程和长周期智能体任务。扩展（Scaling）仍然是提升通用人工智能（AGI）智能效率的最重要途径之一。与 GLM-4.5 相比，GLM-5 的参数规模从 355B（激活 32B）扩展到 744B（激活 40B），预训练数据量从 23T 增加到 28.5T tokens。GLM-5 还集成了 DeepSeek 稀疏注意力（DSA），在保持长上下文能力的同时大幅降低了部署成本。

强化学习旨在弥合预训练模型中"能力"与"卓越"之间的差距。然而，由于 RL 训练效率低下，在大规模 LLM 上部署强化学习是一项挑战。为此，我们开发了 [slime](https://github.com/THUDM/slime)，一种全新的**异步 RL 基础设施**，大幅提升了训练吞吐量和效率，使更细粒度的后训练迭代成为可能。凭借预训练和后训练两方面的进步，GLM-5 在广泛的学术基准测试上相比 GLM-4.7 取得了显著提升，并在推理、编程和智能体任务上达到了全球开源模型的最佳性能，缩小了与前沿模型的差距。

![bench](resources/bench.png)

GLM-5 专为复杂系统工程和长周期智能体任务而设计。在我们的内部评估套件 CC-Bench-V2 上，GLM-5 在前端、后端和长周期任务上均显著超越 GLM-4.7，缩小了与 Claude Opus 4.5 的差距。

![realworld_bench](resources/realworld_bench.png)

在 [Vending Bench 2](https://andonlabs.com/evals/vending-bench-2)（一个衡量长期运营能力的基准测试）上，GLM-5 在开源模型中排名第一。Vending Bench 2 要求模型在一年时间跨度内运营一个模拟自动售货机业务；GLM-5 最终以 4,432 美元的账户余额完成测试，接近 Claude Opus 4.5，展现出强大的长期规划和资源管理能力。

![vending_bench](resources/vending_bench.png)

## 下载模型

| 模型        | 下载链接                                                                                                                            | 模型规模   | 精度 |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------|------------|------|
| GLM-5.2     | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-5.2)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-5.2)         | 744B-A40B  | BF16 |
| GLM-5.2-FP8 | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-5.2-FP8)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-5.2-FP8) | 744B-A40B  | FP8  |
| GLM-5.1     | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-5.1)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-5.1)         | 744B-A40B  | BF16 |
| GLM-5.1-FP8 | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-5.1-FP8)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-5.1-FP8) | 744B-A40B  | FP8  |
| GLM-5       | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-5)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-5)             | 744B-A40B  | BF16 |
| GLM-5-FP8   | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-5-FP8)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-5-FP8)     | 744B-A40B  | FP8  |

## 本地部署 GLM-5 系列模型

GLM-5 系列支持使用以下多种框架部署，欢迎尝试：

- [SGLang](https://github.com/sgl-project/sglang) (v0.5.13.post1+) — 参见 [cookbook](https://cookbook.sglang.io/autoregressive/GLM/GLM-5.2)
- [vLLM](https://github.com/vllm-project/vllm) (v0.23.0+) — 参见 [recipes](https://recipes.vllm.ai/zai-org/GLM-5.2)
- [Transformers](https://github.com/huggingface/transformers) (v5.15.0+) — 参见 [transformers docs](https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/glm_moe_dsa.md)
- [KTransformers](https://github.com/kvcache-ai/ktransformers) (v0.5.12+) — 参见 [tutorial](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/kt-kernel/GLM-5.2-Tutorial.md)
- [Unsloth](https://github.com/unslothai/unsloth) (v0.1.47-beta+) — 参见 [guide](https://unsloth.ai/docs/models/glm-5.2)
- 在 `Ascend NPU` 平台上部署时，支持 vLLM-Ascend、xLLM 、SGLang 等推理框架，参见 [这里](example/ascend.md)

GLM-5 支持通过 `reasoning_effort` 参数控制思考力度，可选 `max` 和 `high` 两档。**默认为 `max`** —— 若不设置 `reasoning_effort`（或设置为 `high` 以外的任意值），模型均按 `Max` 运行；如需使用 `High` 档，必须显式传入 `reasoning_effort="high"`。 对于榜单复现等默认场景，请保持 `Max`（无需任何设置）；仅当确实需要 `High` 档时再设置 `reasoning_effort="high"`。如需完全关闭思考，可设置 `enable_thinking=false`。

## 微调 GLM-5 系列模型

GLM-5 系列支持使用以下多种框架进行微调，欢迎尝试：

- [Slime](https://github.com/THUDM/slime) (v0.3.0+), GLM团队使用的强化学习框架。
- [ms-swift](https://github.com/modelscope/ms-swift) (v4.4.0+)，支持 SFT，PPO，GRPO。

## 引用

如果您在研究中发现 GLM-5 系列模型有帮助，请引用我们的技术报告：

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
