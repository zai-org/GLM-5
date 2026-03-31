# GLM-5

<div align="center">
<img src=resources/logo.svg width="15%"/>
</div>
<p align="center">
    👋 加入我们的 <a href="resources/WECHAT.md" target="_blank">微信群</a> 或 <a href="https://discord.gg/zFMhpMRFP" target="_blank">Discord</a> 社区。
    <br>
    📖 查看 GLM-5 <a href="https://arxiv.org/abs/2602.15763" target="_blank">技术报告</a>。
    <br>
    📍 前往 <a href="https://docs.z.ai/guides/llm/glm-5">Z.ai API 平台</a> 使用 GLM-5 API 服务。
    <br>
    👉 点击即可体验 <a href="https://chat.z.ai">GLM-5</a>。
</p>

## 简介

GLM-5 正式发布，面向复杂系统工程与长周期 Agent 任务。规模化仍是提升通用人工智能（AGI）智能效率的核心路径。相较于 GLM-4.5，GLM-5 参数规模由 355B（激活 32B）扩展至 744B（激活 40B），预训练数据量从 23T 增长至 28.5T tokens。同时，GLM-5 集成了 DeepSeek Sparse Attention（DSA），在保持长上下文能力的前提下，大幅降低了部署成本。

强化学习旨在让预训练模型实现从「能用」到「好用」的跨越。然而，RL 训练效率低下，在大规模 LLM 上的应用面临挑战。为此，我们开发了 [slime](https://github.com/THUDM/slime)——一套创新的**异步 RL 基础设施**，显著提升了训练吞吐量与效率，支持更细粒度的后训练迭代。依托预训练与后训练的双重突破，GLM-5 在各类学术基准上相较 GLM-4.7 取得了显著进步，在推理、代码与 Agent 任务上跻身全球开源模型顶尖行列，与前沿模型的差距进一步缩小。

![bench](resources/bench.png)

GLM-5 专为复杂系统工程与长周期 Agent 任务而生。在内部评测套件 CC-Bench-V2 上，GLM-5 在前端、后端及长周期任务上均大幅超越 GLM-4.7，与 Claude Opus 4.5 的差距显著缩小。

![realworld_bench](resources/realworld_bench.png)

在衡量长期运营能力的基准 [Vending Bench 2](https://andonlabs.com/evals/vending-bench-2) 上，GLM-5 位居开源模型榜首。Vending Bench 2 要求模型在一年时间跨度内经营一家模拟自动售货机业务，GLM-5 最终账户余额达 4,432 美元，逼近 Claude Opus 4.5，展现出卓越的长期规划与资源管理能力。

![vending_bench](resources/vending_bench.png)

## 下载模型

| 模型      | 下载链接                                                                                                                        | 模型规模  | 精度 |
| --------- | ------------------------------------------------------------------------------------------------------------------------------- | --------- | ---- |
| GLM-5     | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-5)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-5)         | 744B-A40B | BF16 |
| GLM-5-FP8 | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-5-FP8)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-5-FP8) | 744B-A40B | FP8  |

## 本地部署 GLM-5

### 环境准备

vLLM、SGLang 和 xLLM 均支持 GLM-5 本地部署，以下提供简易部署指引。

+ vLLM

    使用 Docker (0.18.0 或者更高版本)：

    ```shell
    docker pull vllm/vllm-openai:v0.18.0
    ```

    随后升级 transformers (5.4.0 或者更高版本)：

    ```shell
    pip install -U transformers
    ```

+ SGLang

    使用 Docker：

    ```bash
    docker pull lmsysorg/sglang:glm5-hopper      # 适用于 Hopper GPU
    docker pull lmsysorg/sglang:glm5-blackwell   # 适用于 Blackwell GPU
    ```

### 部署

+ vLLM

    ```shell
    vllm serve zai-org/GLM-5-FP8 \
         --tensor-parallel-size 8 \
         --gpu-memory-utilization 0.85 \
         --speculative-config.method mtp \
         --speculative-config.num_speculative_tokens 1 \
         --tool-call-parser glm47 \
         --reasoning-parser glm45 \
         --enable-auto-tool-choice \
         --served-model-name glm-5-fp8
    ```

更多细节请查看 [recipes](https://github.com/vllm-project/recipes/blob/main/GLM/GLM5.md)。

+ SGLang

    ```shell
    sglang serve \
        --model-path zai-org/GLM-5-FP8 \
        --tp-size 8 \
        --tool-call-parser glm47  \
        --reasoning-parser glm45 \
        --speculative-algorithm EAGLE \
        --speculative-num-steps 3 \
        --speculative-eagle-topk 1 \
        --speculative-num-draft-tokens 4 \
        --mem-fraction-static 0.85 \
        --served-model-name glm-5-fp8
    ```

更多细节请查看 [sglang cookbook](https://cookbook.sglang.io/autoregressive/GLM/GLM-5)。

+ xLLM 与昇腾 NPU

    请参考[部署指南](https://github.com/zai-org/GLM-5/blob/main/example/ascend.md)。

## 引用

如果 GLM-5 对您的研究有所帮助，欢迎引用我们的技术报告：

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
