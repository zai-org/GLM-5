# Using Ascend NPU to Deploy GLM-5

- SGLang: https://github.com/sgl-project/sglang/blob/main/docs/platforms/ascend_npu_glm5_examples.md
- vLLM-Ascend: https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.html
- xLLM: https://github.com/jd-opensource/xllm/blob/preview/glm-5/docs/zh/getting_started/quick_start_GLM5.md

## Environment Preparation

### Model Weight

- ==GLM-5.0==(BF16 version): [Download model weight](https://www.modelscope.cn/models/ZhipuAI/GLM-5).
- ==GLM-5.0-w4a8==(Quantized version without mtp): [Download model weight](https://modelers.cn/models/Eco-Tech/GLM-5-w4a8).
- You can use [msmodelslim](https://gitcode.com/Ascend/msmodelslim) to quantify the model naively.

It is recommended to download the model weight to the shared directory of multiple nodes, such as ==/root/.cache/==

### Installation
### SGLang

The dependencies required for the NPU runtime environment have been integrated into a Docker image and uploaded to the quay.io platform. You can directly pull it.

```
#Atlas 800 A3
swr.cn-southwest-2.myhuaweicloud.com/base_image/dockerhub/lmsysorg/sglang:cann8.5.0-a3-glm5

#start container
docker run -itd --shm-size=16g --privileged=true --name ${NAME} \
--privileged=true --net=host \
-v /var/queue_schedule:/var/queue_schedule \
-v /etc/ascend_install.info:/etc/ascend_install.info \
-v /usr/local/sbin:/usr/local/sbin \
-v /usr/local/Ascend/driver:/usr/local/Ascend/driver \
-v /usr/local/Ascend/firmware:/usr/local/Ascend/firmware \
--device=/dev/davinci0:/dev/davinci0  \
--device=/dev/davinci1:/dev/davinci1  \
--device=/dev/davinci2:/dev/davinci2  \
--device=/dev/davinci3:/dev/davinci3  \
--device=/dev/davinci4:/dev/davinci4  \
--device=/dev/davinci5:/dev/davinci5  \
--device=/dev/davinci6:/dev/davinci6  \
--device=/dev/davinci7:/dev/davinci7  \
--device=/dev/davinci8:/dev/davinci8  \
--device=/dev/davinci9:/dev/davinci9  \
--device=/dev/davinci10:/dev/davinci10  \
--device=/dev/davinci11:/dev/davinci11  \
--device=/dev/davinci12:/dev/davinci12  \
--device=/dev/davinci13:/dev/davinci13  \
--device=/dev/davinci14:/dev/davinci14  \
--device=/dev/davinci15:/dev/davinci15  \
--device=/dev/davinci_manager:/dev/davinci_manager \
--device=/dev/hisi_hdc:/dev/hisi_hdc \
--entrypoint=bash \
quay.io/ascend/sglang:${TAG}

```

### vLLM
vLLM and vLLM-ascend only support GLM-5 on our main branches. you can use our official docker images and upgrade vllm and vllm-ascend for inference.

Refer to [supported features](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/support_matrix/supported_models.html)to get the model's supported feature matrix.

Refer to [feature guide](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/support_matrix/supported_features.html) to get the feature's configuration.

```
# Update --device according to your device (Atlas A3:/dev/davinci[0-15]).
# Update the vllm-ascend image according to your environment.
# Note you should download the weight to /root/.cache in advance.
# Update the vllm-ascend image, alm5-a3 can be replaced by: glm5;glm5-openeuler;glm5-a3-openeuler
export IMAGE=m.daocloud.io/quay.io/ascend/vllm-ascend:glm5-a3
export NAME=vllm-ascend

# Run the container using the defined variables
# Note: If you are running bridge network with docker, please expose available ports for multiple nodes communication in advance
docker run --rm \
--name $NAME \
--net=host \
--shm-size=1g \
--device /dev/davinci0 \
--device /dev/davinci1 \
--device /dev/davinci2 \
--device /dev/davinci3 \
--device /dev/davinci4 \
--device /dev/davinci5 \
--device /dev/davinci6 \
--device /dev/davinci7 \
--device /dev/davinci_manager \
--device /dev/devmm_svm \
--device /dev/hisi_hdc \
-v /usr/local/dcmi:/usr/local/dcmi \
-v /usr/local/Ascend/driver/tools/hccn_tool:/usr/local/Ascend/driver/tools/hccn_tool \
-v /usr/local/bin/npu-smi:/usr/local/bin/npu-smi \
-v /usr/local/Ascend/driver/lib64/:/usr/local/Ascend/driver/lib64/ \
-v /usr/local/Ascend/driver/version.info:/usr/local/Ascend/driver/version.info \
-v /etc/ascend_install.info:/etc/ascend_install.info \
-v /root/.cache:/root/.cache \
-it $IMAGE bash

```

In addition, if you don't want to use the docker image as above, you can also build all from source:

- Install ==vllm-ascend== from source, refer to [installation](https://docs.vllm.ai/projects/ascend/en/latest/installation.html).

To inference ==GLM-5==, you should upgrade vllm、vllm-ascend、transformers to main branches:

```
# upgrade vllm
git clone https://github.com/vllm-project/vllm.git
cd vllm
git checkout 978a37c82387ce4a40aaadddcdbaf4a06fc4d590
VLLM_TARGET_DEVICE=empty pip install -v .

# upgrade vllm-ascend
git clone https://github.com/vllm-project/vllm-ascend.git
cd vllm-ascend
git checkout ff3a50d011dcbea08f87ebed69ff1bf156dbb01e
git submodule update --init --recursive
pip install -v .

# reinstall transformers
pip install git+https://github.com/huggingface/transformers.git

```

If you want to deploy multi-node environment, you need to set up environment on each node.

### xLLM

First, pull the image we provide:

```
# A2 x86
docker pull quay.io/jd_xllm/xllm-ai:xllm-dev-hb-rc2-x86
# A2 arm
docker pull quay.io/jd_xllm/xllm-ai:xllm-dev-hb-rc2-arm
# A3 arm
docker pull quay.io/jd_xllm/xllm-ai:xllm-dev-hc-rc2-arm

```

Then create the corresponding container:

```
sudo docker run -it --ipc=host -u 0 --privileged --name mydocker --network=host \
 -v /var/queue_schedule:/var/queue_schedule \
 -v /usr/local/Ascend/driver:/usr/local/Ascend/driver \
 -v /usr/local/Ascend/add-ons/:/usr/local/Ascend/add-ons/ \
 -v /usr/local/sbin/npu-smi:/usr/local/sbin/npu-smi \
 -v /var/log/npu/conf/slog/slog.conf:/var/log/npu/conf/slog/slog.conf \
 -v /var/log/npu/slog/:/var/log/npu/slog \
 -v ~/.ssh:/root/.ssh  \
 -v /var/log/npu/profiling/:/var/log/npu/profiling \
 -v /var/log/npu/dump/:/var/log/npu/dump \
 -v /runtime/:/runtime/ -v /etc/hccn.conf:/etc/hccn.conf \
 -v /export/home:/export/home \
 -v /home/:/home/  \
 -w /export/home \
 quay.io/jd_xllm/xllm-ai:xllm-dev-hb-rc2-x86

```

Pull Source Code and Build

Clone the official repository and submodule dependencies:

```
git clone https://github.com/jd-opensource/xllm
cd xllm
git checkout preview/glm-5
git submodule init
git submodule update

```

Install dependencies:

```
pip install --upgrade pre-commit
yum install numactl

```

Run the build command. The executable ==build/xllm/core/server/xllm== is generated under ==build/==:

```
python setup.py build --device a3

```

## Deployment

### SGLang

### Single-node Deployment

**A2 series**

Not test yet.

**A3 series**

- Quantized model ==glm5_w4a8== can be deployed on 1 Atlas 800 A3 (128G × 8) .

Run the following script to execute online inference.

```
# high performance cpu
echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
sysctl -w vm.swappiness=0
sysctl -w kernel.numa_balancing=0
sysctl -w kernel.sched_migration_cost_ns=50000
# bind cpu
export SGLANG_SET_CPU_AFFINITY=1

unset https_proxy
unset http_proxy
unset HTTPS_PROXY
unset HTTP_PROXY
unset ASCEND_LAUNCH_BLOCKING
# can
source /usr/local/Ascend/ascend-toolkit/set_env.sh
source /usr/local/Ascend/nnal/atb/set_env.sh
export PYTORCH_NPU_ALLOC_CONF=expandable_segments:True
export STREAMS_PER_DEVICE=32
export SGLANG_DISAGGREGATION_BOOTSTRAP_TIMEOUT=600
export SGLANG_ENABLE_SPEC_V2=1
export SGLANG_ENABLE_OVERLAP_PLAN_STREAM=1
export SGLANG_NPU_USE_MULTI_STREAM=1
export HCCL_BUFFSIZE=1000
export HCCL_OP_EXPANSION_MODE=AIV

python3 -m sglang.launch_server \
        --model-path $MODEL_PATH \
        --attention-backend ascend \
        --device npu \
        --tp-size 16 --nnodes 1 --node-rank 0 \
        --chunked-prefill-size 16384 --max-prefill-tokens 280000 \
        --trust-remote-code \
        --host 127.0.0.1 \
        --mem-fraction-static 0.7 \
        --port 8000 \
        --served-model-name glm-5 \
        --cuda-graph-bs 16 \
        --quantization modelslim \
        --moe-a2a-backend deepep --deepep-mode auto

```

### Multi-node Deployment

- ==GLM-5-bf16==: require at least 2 Atlas 800 A3 (128G × 8).

**A3 series**

Modify the IP of 2 nodes, then run the same scripts on two nodes.

**node 0/1**

```
echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
sysctl -w vm.swappiness=0
sysctl -w kernel.numa_balancing=0
sysctl -w kernel.sched_migration_cost_ns=50000
# bind cpu
export SGLANG_SET_CPU_AFFINITY=1

unset https_proxy
unset http_proxy
unset HTTPS_PROXY
unset HTTP_PROXY
unset ASCEND_LAUNCH_BLOCKING
# can
source /usr/local/Ascend/ascend-toolkit/set_env.sh
source /usr/local/Ascend/nnal/atb/set_env.sh
export PYTORCH_NPU_ALLOC_CONF=expandable_segments:True
export STREAMS_PER_DEVICE=32
export SGLANG_DISAGGREGATION_BOOTSTRAP_TIMEOUT=600
export SGLANG_ENABLE_SPEC_V2=1
export SGLANG_ENABLE_OVERLAP_PLAN_STREAM=1
export SGLANG_NPU_USE_MULTI_STREAM=1
export HCCL_BUFFSIZE=1000
export HCCL_OP_EXPANSION_MODE=AIV

# Run command ifconfig on two nodes, find out which inet addr has same IP with your node IP. That is your public interface, which should be added here
export HCCL_SOCKET_IFNAME=enp48s3u1u1
export GLOO_SOCKET_IFNAME=enp48s3u1u1


P_IP=('your ip1' 'your ip2')
P_MASTER="${P_IP[0]}:your port"
export SGLANG_DISAGGREGATION_BOOTSTRAP_TIMEOUT=600

export SGLANG_ENABLE_SPEC_V2=1
export SGLANG_ENABLE_OVERLAP_PLAN_STREAM=1

LOCAL_HOST1=`hostname -I|awk -F " " '{print$1}'`
LOCAL_HOST2=`hostname -I|awk -F " " '{print$2}'`
for i in "${!P_IP[@]}";
do
    if [[ "$LOCAL_HOST1"  "${P_IP[$i]}" || "$LOCAL_HOST2"  "${P_IP[$i]}" ]];
    then
        echo "${P_IP[$i]}"
        python3 -m sglang.launch_server \
        --model-path $MODEL_PATH \
        --attention-backend ascend \
        --device npu \
        --tp-size 32 --nnodes 2 --node-rank $i --dist-init-addr $P_MASTER \
        --chunked-prefill-size 16384 --max-prefill-tokens 131072 \
        --trust-remote-code \
        --host 127.0.0.1 \
        --mem-fraction-static 0.8\
        --port 8000 \
        --served-model-name glm-5 \
        --cuda-graph-max-bs 16 \
        --disable-radix-cache
        NODE_RANK=$i
        break
    fi
done


```

### Prefill-Decode Disaggregation

Not test yet.

### vLLM

### Single-node Deployment

**A2 series**

Not test yet.

**A3 series**

- Quantized model ==glm-5-w4a8== can be deployed on 1 Atlas 800 A3 (128G × 8) .

Run the following script to execute online inference.

```
export HCCL_OP_EXPANSION_MODE="AIV"
export OMP_PROC_BIND=false
export OMP_NUM_THREADS=10
export VLLM_USE_V1=1
export HCCL_BUFFSIZE=200
export PYTORCH_NPU_ALLOC_CONF=expandable_segments:True
export VLLM_ASCEND_BALANCE_SCHEDULING=1

vllm serve /root/.cache/modelscope/hub/models/vllm-ascend/GLM5-w4a8 \
--host 0.0.0.0 \
--port 8077 \
--data-parallel-size 1 \
--tensor-parallel-size 16 \
--enable-expert-parallel \
--seed 1024 \
--served-model-name glm-5 \
--max-num-seqs 8 \
--max-model-len 66600 \
--max-num-batched-tokens 4096 \
--trust-remote-code \
--gpu-memory-utilization 0.95 \
--quantization ascend \
--enable-chunked-prefill \
--enable-prefix-caching \
--async-scheduling \
--additional-config '{"multistream_overlap_shared_expert":true}' \
--compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY"}' \
--speculative-config '{"num_speculative_tokens": 3, "method": "deepseek_mtp"}'

```

**Notice:**
The parameters are explained as follows:

- For single-node deployment, we recommend using ==dp1tp16== and turn off expert parallel in low-latency scenarios.
- ==--async-scheduling== Asynchronous scheduling is a technique used to optimize inference efficiency. It allows non-blocking task scheduling to improve concurrency and throughput, especially when processing large-scale models.

### Multi-node Deployment

**A2 series**

Not test yet.

**A3 series**

- ==glm-5-bf16==: require at least 2 Atlas 800 A3 (128G × 8).

Run the following scripts on two nodes respectively.

**node 0**

```
# this obtained through ifconfig
# nic_name is the network interface name corresponding to local_ip of the current node
nic_name="xxx"
local_ip="xxx"

# The value of node0_ip must be consistent with the value of local_ip set in node0 (master node)
node0_ip="xxxx"

export HCCL_OP_EXPANSION_MODE="AIV"

export HCCL_IF_IP=$local_ip
export GLOO_SOCKET_IFNAME=$nic_name
export TP_SOCKET_IFNAME=$nic_name
export HCCL_SOCKET_IFNAME=$nic_name
export OMP_PROC_BIND=false
export OMP_NUM_THREADS=10
export VLLM_USE_V1=1
export HCCL_BUFFSIZE=200
export PYTORCH_NPU_ALLOC_CONF=expandable_segments:True

vllm serve /root/.cache/modelscope/hub/models/vllm-ascend/GLM5-bf16 \
--host 0.0.0.0 \
--port 8077 \
--data-parallel-size 2 \
--data-parallel-size-local 1 \
--data-parallel-address $node0_ip \
--data-parallel-rpc-port 12890 \
--tensor-parallel-size 16 \
--quantization ascend \
--seed 1024 \
--served-model-name glm-5 \
--enable-expert-parallel \
--max-num-seqs 16 \
--max-model-len 8192 \
--max-num-batched-tokens 4096 \
--trust-remote-code \
--no-enable-prefix-caching \
--gpu-memory-utilization 0.95 \
--compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY"}' \
--speculative-config '{"num_speculative_tokens": 3, "method": "deepseek_mtp"}'

```

**node 1**

```
# this obtained through ifconfig
# nic_name is the network interface name corresponding to local_ip of the current node
nic_name="xxx"
local_ip="xxx"

# The value of node0_ip must be consistent with the value of local_ip set in node0 (master node)
node0_ip="xxxx"

export HCCL_OP_EXPANSION_MODE="AIV"

export HCCL_IF_IP=$local_ip
export GLOO_SOCKET_IFNAME=$nic_name
export TP_SOCKET_IFNAME=$nic_name
export HCCL_SOCKET_IFNAME=$nic_name
export OMP_PROC_BIND=false
export OMP_NUM_THREADS=10
export VLLM_USE_V1=1
export HCCL_BUFFSIZE=200
export PYTORCH_NPU_ALLOC_CONF=expandable_segments:True

vllm serve /root/.cache/modelscope/hub/models/vllm-ascend/GLM5-bf16 \
--host 0.0.0.0 \
--port 8077 \
--headless \
--data-parallel-size 2 \
--data-parallel-size-local 1 \
--data-parallel-start-rank 1 \
--data-parallel-address $node0_ip \
--data-parallel-rpc-port 12890 \
--tensor-parallel-size 16 \
--quantization ascend \
--seed 1024 \
--served-model-name glm-5 \
--enable-expert-parallel \
--max-num-seqs 16 \
--max-model-len 8192 \
--max-num-batched-tokens 4096 \
--trust-remote-code \
--no-enable-prefix-caching \
--gpu-memory-utilization 0.95 \
--compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY"}' \
--speculative-config '{"num_speculative_tokens": 3, "method": "deepseek_mtp"}'

```

### Prefill-Decode Disaggregation

Not test yet.

### xLLM

### Single-node Deployment

**A2 series**

Not test yet.

**A3 series**

- Quantized model ==glm-5-w8a8== can be deployed on 1 Atlas 800 A3 (128G × 8) .

### GLM-5 Weight Quantization

```
#Install msmodelslim
git clone https://gitcode.com/shenxiaolong/msmodelslim.git
cd msmodelslim
bash install.sh

```

### Modify tokenizer_config.json

```
  "extra_special_tokens"
    Change to "additional_special_tokens"

  "tokenizer_class": "TokenizersBackend"
    Change to "tokenizer_class": "PreTrainedTokenizer"

```

### Quantize GLM-5-BF16 Weights to W8A8

```
### Preprocess MTP-related weights
python example/GLM5/extract_mtp.py --model-dir ${model_path}

# Specify the transformers version
pip install transformers==4.48.2

# Run quantization (generate quantized weights)
msmodelslim quant  --model_path ${model_path}  --save_path ${save_path}  --model_type DeepSeek-V3.2  --quant_type w8a8  --trust_remote_code True

# Copy the chat_template file
cp ${model_path}/chat_template.jinja ${save_path}

# Export quantized MTP weights (for xllm inference)
python example/GLM5/export_mtp.py --input-dir  ${int8_save_path} --output-dir  ${mtp_save_path}

```

Run the following script to execute online inference.

```
export LD_PRELOAD=/usr/lib64/libjemalloc.so.2:$LD_PRELOAD
rm -rf /root/ascend/log/
rm -rf core.*
export PYTORCH_NPU_ALLOC_CONF=expandable_segments:True
export NPU_MEMORY_FRACTION=0.96
export ATB_WORKSPACE_MEM_ALLOC_ALG_TYPE=3
export ATB_WORKSPACE_MEM_ALLOC_GLOBAL=1

export OMP_NUM_THREADS=12
export ALLOW_INTERNAL_FORMAT=1

export ATB_LAYER_INTERNAL_TENSOR_REUSE=1
export ATB_LLM_ENABLE_AUTO_TRANSPOSE=0
export ATB_CONVERT_NCHW_TO_AND=1
export ATB_LAUNCH_KERNEL_WITH_TILING=1
export ATB_OPERATION_EXECUTE_ASYNC=2
export ATB_CONTEXT_WORKSPACE_SIZE=0
export INF_NAN_MODE_ENABLE=1
export HCCL_EXEC_TIMEOUT=300
export HCCL_CONNECT_TIMEOUT=300
export HCCL_OP_EXPANSION_MODE="AIV"
export HCCL_IF_BASE_PORT=2864

BATCH_SIZE=256
# Maximum inference batch size
XLLM_PATH="./myxllm/xllm/build/xllm/core/server/xllm"
# Inference entry executable path (build artifact from the previous step)
MODEL_PATH=/export/home/models/GLM-5-w8a8/
# Model path (INT-quantized GLM-5 in this example)
DRAFT_MODEL_PATH=/export/home/models/GLM-5-MTP/
# MTP weights exported from GLM-5 (see tutorial below)

MASTER_NODE_ADDR="11.87.49.110:10015"
LOCAL_HOST="11.87.49.110"
# Service Port
START_PORT=18994
START_DEVICE=0
LOG_DIR="logs"
NNODES=16

for (( i=0; i<$NNODES; i ))
do
  PORT=$((START_PORT + i))
  DEVICE=$((START_DEVICE + i))
  LOG_FILE="$LOG_DIR/node_$i.log"
  nohup numactl -C $((DEVICE*40))-$((DEVICE*40+39)) $XLLM_PATH \
    --model $MODEL_PATH \
    --port $PORT \
    --devices="npu:$DEVICE" \
    --master_node_addr=$MASTER_NODE_ADDR \
    --nnodes=$NNODES \
    --node_rank=$i \
    --max_memory_utilization=0.85 \
    --max_tokens_per_batch=8192 \
    --max_seqs_per_batch=64 \
    --block_size=128 \
    --enable_prefix_cache=false \
    --enable_chunked_prefill=true \
    --communication_backend="hccl" \
    --enable_schedule_overlap=true \
    --enable_graph=true \
    --enable_graph_no_padding=true \
    --enable_mla=true \
    --draft_model=$DRAFT_MODEL_PATH \
    --draft_devices="npu:$DEVICE" \
    --num_speculative_tokens=1 \
    --ep_size=16 \
    --dp_size=1 \
    > $LOG_FILE 2>&1 &
done

```

**++Notice:++**++ ++
++The parameters are explained as follows:++

```
#numactl -C $((i*12))-$((i*12+11))
#                           CPU affinity pinning (check affinity with: npu-smi info -t topo)
#--max_memory_utilization   Maximum memory usage ratio per card
#--max_tokens_per_batch     Maximum tokens per batch (mainly limits prefill)
#--max_seqs_per_batch       Maximum requests per batch (mainly limits decode)
#--communication_backend    Communication backend; `hccl` is recommended
#--enable_schedule_overlap  Enable asynchronous scheduling
#--enable_prefix_cache      Enable prefix cache
#--enable_chunked_prefill   Enable chunked prefill
#--enable_graph             Enable ACL graph
#--draft_model              MTP weights path
#--draft_devices            MTP inference device(s) (same as the main model)
#--num_speculative_tokens   MTP speculative token count

```

++If logs show "Brpc Server Started", the service has started successfully.++

### ++Multi-node Deployment++

**++A2 series++**

++Not test yet.++

**++A3 series++**

++Run the following scripts on two nodes respectively.++

**++node 0++**

```
MASTER_NODE_ADDR="11.87.49.110:19990"
LOCAL_HOST="11.87.49.110"
START_PORT=15890
START_DEVICE=0
LOG_DIR="logs"
NNODES=32
LOCAL_NODES=16
export HCCL_IF_BASE_PORT=48439
unset HCCL_OP_EXPANSION_MODE

for (( i=0; i<$LOCAL_NODES; i ))do
  PORT=$((START_PORT + i))
  DEVICE=$((START_DEVICE + i))  LOG_FILE="$LOG_DIR/node_$i.log"
  nohup numactl -C $((DEVICE*40))-$((DEVICE*40+39)) $XLLM_PATH \    --model $MODEL_PATH \
    --host $LOCAL_HOST \
    --port $PORT \
    --devices="npu:$DEVICE" \
    --master_node_addr=$MASTER_NODE_ADDR \
    --nnodes=$NNODES \
    --node_rank=$i \
    --max_memory_utilization=0.85 \
    --max_tokens_per_batch=64000 \
    --max_seqs_per_batch=32 \
    --block_size=128 \
    --enable_prefix_cache=false \
    --enable_chunked_prefill=false \
    --communication_backend="hccl" \
    --enable_schedule_overlap=true \
    --enable_graph=true \
    --enable_graph_no_padding=true \
    --enable_mla=true \
    --ep_size=16 \
    --dp_size=1 \
    --rank_tablefile=/yourPath/ranktable.json \
    > $LOG_FILE 2>&1 &
done

```

**node 1**

```
MASTER_NODE_ADDR="11.87.49.110:19990"
LOCAL_HOST="11.87.49.111"
START_PORT=15890
START_DEVICE=0
LOG_DIR="logs"
NNODES=32
LOCAL_NODES=16
export HCCL_IF_BASE_PORT=48439
unset HCCL_OP_EXPANSION_MODE

for (( i=0; i<$LOCAL_NODES; i ))do
  PORT=$((START_PORT + i))
  DEVICE=$((START_DEVICE + i))  LOG_FILE="$LOG_DIR/node_$i.log"
  nohup numactl -C $((DEVICE*40))-$((DEVICE*40+39)) $XLLM_PATH \    --model $MODEL_PATH \
    --host $LOCAL_HOST \
    --port $PORT \
    --devices="npu:$DEVICE" \
    --master_node_addr=$MASTER_NODE_ADDR \
    --nnodes=$NNODES \
    --node_rank=$((i + LOCAL_NODES)) \
    --max_memory_utilization=0.85 \
    --max_tokens_per_batch=64000 \
    --max_seqs_per_batch=32 \
    --block_size=128 \
    --enable_prefix_cache=false \
    --enable_chunked_prefill=false \
    --communication_backend="hccl" \
    --enable_schedule_overlap=true \
    --enable_graph=true \
    --enable_graph_no_padding=true \
    --enable_mla=true \
    --ep_size=16 \
    --dp_size=1 \
    --rank_tablefile=/yourPath/ranktable.json \
    > $LOG_FILE 2>&1 &
done

```

++ranktable configuration guide: [https://www.hiascend.com/document/detail/zh/canncommercial/83RC1/hccl/hcclug/hcclug_000014.html](https://www.hiascend.com/document/detail/zh/canncommercial/83RC1/hccl/hcclug/hcclug_000014.html)++

### ++Prefill-Decode Disaggregation++

### ++etcd\xllm-service Installation++

++==xllm== supports Dependencies deployment. This needs to be used together with another open-source project, [xllm service](https://github.com/jd-opensource/xllm-service).++

### ++xLLM Service Dependencies++

++First, clone and install ==xllm service==, similar to installing/building ==xllm==:++

```
git clone https://github.com/jd-opensource/xllm-service
cd xllm_service
git submodule init
git submodule update

```

### ++Install etcd++

++==xllm_service== depends on [etcd](https://github.com/etcd-io/etcd). Install it via the official [installation script](https://github.com/etcd-io/etcd/releases). The default install path in that script is ==/tmp/etcd-download-test/etcd==. You can either modify the path in the script or move it manually afterward:++

```
mv /tmp/etcd-download-test/etcd /path/to/your/etcd

```

### ++Build xLLM Service++

++Apply the patch first:++

```
sh prepare.sh

```

++Then build:++

```
mkdir -p build
cd build
cmake ..
make -j 8
cd ..

```

++!!! warning "Possible errors" ++
++You may encounter installation errors for ==boost-locale== and ==boost-interprocess==: ==vcpkg-src/packages/boost-locale_x64-linux/include: No such file or directory==, ==/vcpkg-src/packages/boost-interprocess_x64-linux/include: No such file or directory== ++
++Reinstall these packages with ==vcpkg==: ++
++==bash /path/to/vcpkg remove boost-locale boost-interprocess /path/to/vcpkg install boost-locale:x64-linux /path/to/vcpkg install boost-interprocess:x64-linux ==++

### ++Run in Dependencies Mode++

++Start etcd:++

```
./etcd-download-test/etcd --listen-peer-urls 'http://localhost:2390'  --listen-client-urls 'http://localhost:2389' --advertise-client-urls  'http://localhost:2391'

```

++For cross-machine deployment, etcd can be configured as follows:++

```
/tmp/etcd-download-test/etcd --listen-peer-urls 'http://0.0.0.0:3390' --listen-client-urls 'http://0.0.0.0:3389' --advertise-client-urls 'http://11.87.191.82:3389'

```

++Start xllm service:++

```
ENABLE_DECODE_RESPONSE_TO_SERVICE=true ./xllm_master_serving --etcd_addr="127.0.0.1:12389" --http_server_port 28888 --rpc_server_port 28889 --tokenizer_path=/export/home/models/GLM-5-W8A8/

```

++For cross-machine deployment, start xllm service with:++

```
ENABLE_DECODE_RESPONSE_TO_SERVICE=true ../xllm-service/build/xllm_service/xllm_master_serving --etcd_addr="11.87.191.82:3389" --http_server_port 38888 --rpc_server_port 38889 --tokenizer_path=/export/home/models/GLM-5-W8A8/

```

- ++Start Prefill instances++

```
  BATCH_SIZE=256
  # Maximum inference batch size
  XLLM_PATH="./myxllm/xllm/build/xllm/core/server/xllm"
  # Inference entry executable path (build artifact from the previous step)
  MODEL_PATH=/export/home/models/GLM-5-w8a8/
  # Model path (INT-quantized GLM-5 in this example)
  DRAFT_MODEL_PATH=/export/home/models/GLM-5-MTP/

  MASTER_NODE_ADDR="11.87.49.110:10015"
  LOCAL_HOST="11.87.49.110"
  # Service Port
  START_PORT=18994
  START_DEVICE=0
  LOG_DIR="logs"
  NNODES=16

  for (( i=0; i<$NNODES; i ))
  do
    PORT=$((START_PORT + i))
    DEVICE=$((START_DEVICE + i))
    LOG_FILE="$LOG_DIR/node_$i.log"
    nohup numactl -C $((i*40))-$((i*40+39)) $XLLM_PATH \
      --model $MODEL_PATH  -model_id glmmoe \
      --host $LOCAL_HOST \
      --port $PORT \
      --devices="npu:$DEVICE" \
      --master_node_addr=$MASTER_NODE_ADDR \
      --nnodes=$NNODES \
      --node_rank=$i \
      --max_memory_utilization=0.86 \
      --max_tokens_per_batch=5000 \
      --max_seqs_per_batch=$BATCH_SIZE \
      --communication_backend=hccl \
      --enable_schedule_overlap=true \
      --enable_prefix_cache=false \
      --enable_chunked_prefill=false \
      --enable_graph=true \
      --draft_model $DRAFT_MODEL_PATH \
      --draft_devices="npu:$DEVICE" \
      --num_speculative_tokens 1 \
      --enable_disagg_pd=true \
      --instance_role=PREFILL \
      --etcd_addr=$LOCAL_HOST:3389 \
      --transfer_listen_port=$((36100 + i)) \
      --disagg_pd_port=8877 \
      > $LOG_FILE 2>&1 &
  done

  #--etcd_addr=$LOCAL_HOST:3389  Refer to etcd `advertise-client-urls` settings
  #--instance_role=DECODE     PD setting, DECODE\PREFILL

```

- Start Decode instances

```
BATCH_SIZE=256
# Maximum inference batch size
XLLM_PATH="./myxllm/xllm/build/xllm/core/server/xllm"
# Inference entry executable path (build artifact from the previous step)
MODEL_PATH=/export/home/models/GLM-5-w8a8/
# Model path (INT-quantized GLM-5 in this example)
DRAFT_MODEL_PATH=/export/home/models/GLM-5-MTP/

MASTER_NODE_ADDR="11.87.49.110:10015"
LOCAL_HOST="11.87.49.110"
# Service Port
START_PORT=18994
START_DEVICE=0
LOG_DIR="logs"
NNODES=16

for (( i=0; i<$NNODES; i++ ))
do
PORT=$((START_PORT + i))
DEVICE=$((START_DEVICE + i))
LOG_FILE="$LOG_DIR/node_$i.log"
nohup numactl -C $((i*40))-$((i*40+39)) $XLLM_PATH \
    --model $MODEL_PATH  -model_id glmmoe \
    --host $LOCAL_HOST \
    --port $PORT \
    --devices="npu:$DEVICE" \
    --master_node_addr=$MASTER_NODE_ADDR \
    --nnodes=$NNODES \
    --node_rank=$i \
    --max_memory_utilization=0.86 \
    --max_tokens_per_batch=5000 \
    --max_seqs_per_batch=$BATCH_SIZE \
    --communication_backend=hccl \
    --enable_schedule_overlap=true \
    --enable_prefix_cache=false \
    --enable_chunked_prefill=false \
    --enable_graph=true \
    --draft_model $DRAFT_MODEL_PATH \
    --draft_devices="npu:$DEVICE" \
    --num_speculative_tokens 1 \
    --enable_disagg_pd=true \
    --instance_role=DECODE \
    --etcd_addr=$LOCAL_HOST:3389 \
    --transfer_listen_port=$((36100 + i)) \
    --disagg_pd_port=8877 \
    > $LOG_FILE 2>&1 &
done

#--etcd_addr=$LOCAL_HOST:3389  Refer to etcd `advertise-client-urls` settings
#--instance_role=DECODE     PD setting, DECODE\PREFILL

```

Notes:

- PD separation requires reading ==/etc/hccn.conf==; ensure the host file is mounted into the container.

- ==etcd_addr== must match the ==etcd_addr== used by ==xllm_service==.
- The test command is similar to the one above. For ==curl http://localhost:{PORT}/v1/chat/completions ...==, use the xLLM service ==http_server_port== as ==PORT==.

- When deploying multiple P or Q instances across machines (for example, two P instances), add ==--rank_tablefile== to enable communication.

## Accuracy Evaluation

Here are two accuracy evaluation methods.

### Using AISBench

1. Refer to [Using AISBench](../developer_guide/evaluation/using_ais_bench.md) for details.

2. After execution, you can get the result.

### Using Language Model Evaluation Harness

Not test yet.

## Performance

### Using AISBench

Refer to [Using AISBench for performance evaluation](../developer_guide/evaluation/using_ais_bench.md#execute-performance-evaluation) for details.

### Using vLLM Benchmark

Refer to [vllm benchmark](https://docs.vllm.ai/en/latest/contributing/benchmarks.html) for more details.

### Using vLLM Benchmark

Refer to [vllm benchmark](https://docs.vllm.ai/en/latest/contributing/benchmarks.html) for more details.
