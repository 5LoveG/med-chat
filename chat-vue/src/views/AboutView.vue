<template>
  <div class="container">
    <div class="head">
      <div class="nav-buttons">
        <router-link to="/chat" class="nav-button" active-class="active"
          >智能问诊</router-link
        >
        <router-link to="/picture" class="nav-button" active-class="active"
          >病例分析</router-link
        >
        <router-link to="/about" class="nav-button" active-class="active"
          >科室导航</router-link
        >
      </div>
    </div>

    <div class="content">
      <div class="grid-container">
        <!-- 科室卡片 -->
        <div class="department-card" v-for="dept in departments" :key="dept.id">
          <div class="card-header">
            <h3>{{ dept.name }}</h3>
            <span
              class="status-indicator"
              :style="statusColor(dept.waitTime)"
            ></span>
          </div>
          <div class="card-body">
            <div class="info-row">
              <span>当前排队</span>
              <span class="number-badge">{{ dept.currentNumber }}</span>
            </div>
            <div class="info-row">
              <span>预计等待</span>
              <span class="time-badge">{{ dept.waitTime }}分钟</span>
            </div>
          </div>
        </div>
      </div>
      <div class="instruction">
        <div class="step">
          <div class="step-icon">1</div>
          <div class="step-text">在输入框输入您要去的科室名称</div>
        </div>
        <div class="step">
          <div class="step-icon">2</div>
          <div class="step-text">点击发送按钮获取导航路线</div>
        </div>
        <div class="step">
          <div class="step-icon">3</div>
          <div class="step-text">查看下方导航路线指引</div>
        </div>
        <div class="step">
          <div class="step-icon">4</div>
          <div class="step-text">
            可追问详细路线："怎么走？" "附近有什么标志？"
          </div>
        </div>
      </div>
      <!-- 下方留空区域 -->
      <div class="bottom-space">
        <div ref="chatContainer" class="response-container">
          <pre class="response-text">{{ responseText }}</pre>
        </div>
        <div class="input-container">
          <input
            v-model="inputMessage"
            @keyup.enter="sendMessage"
            placeholder="输入目的地科室..."
            class="message-input"
          />
          <button @click="sendMessage" class="send-button">
            <span>发送</span>
            <svg class="send-icon" viewBox="0 0 24 24">
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
            </svg>
          </button>
          <button class="record" @click="toggleRecording">
            {{ isRecording ? "停止录音" : "语音输入" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      departments: [
        { id: 1, name: "心血管内科", currentNumber: 15, waitTime: 75 },
        { id: 2, name: "神经外科", currentNumber: 8, waitTime: 40 },
        { id: 3, name: "儿科门诊", currentNumber: 22, waitTime: 110 },
        { id: 4, name: "急诊科", currentNumber: 5, waitTime: 25 },
        { id: 5, name: "骨科", currentNumber: 12, waitTime: 60 },
        { id: 6, name: "眼科", currentNumber: 18, waitTime: 90 },
        { id: 7, name: "消化内科", currentNumber: 9, waitTime: 45 },
        { id: 8, name: "皮肤科", currentNumber: 6, waitTime: 30 },
        { id: 9, name: "妇产科", currentNumber: 14, waitTime: 70 },
        { id: 10, name: "耳鼻喉科", currentNumber: 10, waitTime: 50 },
      ],
      inputMessage: "",
      responseText: "", // 新增响应内容存储

      isRecording: false,
      mediaRecorder: null,
      audioChunks: [],
      error: null,
    };
  },
  methods: {
    statusColor(time) {
      if (time <= 30) return "background: #4CAF50";
      if (time <= 50) return "background: #FFC107";
      return "background: #F44336";
    },
    async sendMessage() {
      const inputMessage = this.inputMessage;

      if (!inputMessage.trim()) return;
      this.inputMessage = "";

      try {
        const response = await fetch(
          `http://localhost:8000/road/${inputMessage}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        this.responseText = "";
        let isReading = true;
        while (isReading) {
          const { done, value } = await reader.read();
          if (done) {
            isReading = false;
            break;
          }

          const chunk = decoder.decode(value);
          const lines = chunk.split("\n\n").filter((line) => line.trim());

          for (const line of lines) {
            if (line.startsWith("data: ")) {
              const dataStr = line.replace("data: ", "");
              try {
                const data = JSON.parse(dataStr);
                this.responseText += data.content;
              } catch (e) {
                console.error("解析JSON失败:", e);
              }
            }
          }
          this.scrollToBottom();
        }
      } catch (err) {
        console.error("发送失败:", err);
        this.history[this.history.length - 1].content += "\n(请求失败)";
      }
      this.scrollToBottom();
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.chatContainer;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    },
    async startRecording() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });
        this.mediaRecorder = new MediaRecorder(stream);

        this.mediaRecorder.ondataavailable = (e) => {
          this.audioChunks.push(e.data);
        };

        this.mediaRecorder.onstop = async () => {
          const audioBlob = new Blob(this.audioChunks, { type: "audio/wav" });
          const formData = new FormData();
          formData.append("file", audioBlob, "recording.wav");

          try {
            const response = await axios.post(
              "http://localhost:8000/audio",
              formData,
              { headers: { "Content-Type": "multipart/form-data" } }
            );

            if (response.data.text) {
              this.inputMessage = response.data.text;
            }
          } catch (err) {
            this.error =
              "识别失败：" + (err.response?.data?.error || err.message);
            console.error("上传失败:", err);
          }

          this.audioChunks = [];
          stream.getTracks().forEach((track) => track.stop());
        };

        this.mediaRecorder.start();
        this.isRecording = true;
      } catch (err) {
        this.error = "需要麦克风权限才能录音";
        console.error("录音错误:", err);
      }
    },
    toggleRecording() {
      if (!this.isRecording) {
        this.startRecording();
      } else {
        this.mediaRecorder.stop();
        this.isRecording = false;
      }
    },
  },
};
</script>

<style scoped>
.container {
  height: 100vh;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  display: flex;
  flex-direction: column;
  font-family: "Segoe UI", system-ui, sans-serif;
}
/* 导航栏 */
.head {
  height: 6.4%;
  padding: 0 2rem; /*内边距 上下 左右*/
  background: rgba(255, 255, 255, 0.95);
  border-bottom: 1px solid #e4e7ed; /*元素底部添加细边框*/
}
.nav-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  width: 12%;
  gap: 15px;
}

.nav-button {
  padding: 1rem 0;
  color: #606266;
  text-decoration: none; /*消除连接下划线*/
  font-weight: 700; /*文本字体粗细*/
  transition: all 0.3s ease;
  position: relative; /*使元素遵循常规文档流 允许通过偏移属性进行微调*/
  text-align: center; /*文本居中*/
  font-size: 0.85rem; /* 修改这个值即可调整文字大小 */
}

.nav-button:hover {
  color: #409eff;
}

.nav-button.active {
  color: #409eff;
  font-weight: 600;
}

.nav-button.active::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: #409eff;
  border-radius: 2px;
}
.content {
  height: 93.6%;
  display: flex;
  flex-direction: column;
  padding: 1rem;
}

.grid-container {
  background-color: #f7f7f7;
  flex: 5;
  display: grid;
  grid-template-columns: repeat(5, 1fr); /* 改为5列布局 */
  gap: 1rem;
  margin-bottom: 1rem;
}

.department-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.department-card:hover {
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.1rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0.8rem 0;
  color: #666;
}

.number-badge {
  background: #e8f4ff;
  color: #2196f3;
  padding: 4px 12px;
  border-radius: 20px;
  font-weight: 600;
}

.time-badge {
  color: #666;
  font-weight: 500;
}
.instruction {
  flex: 0.5;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  background: rgba(232, 241, 244, 0.95);
  border-radius: 12px;
  padding: 0.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.step {
  display: flex;
}

.step-icon {
  width: 30px;
  height: 30px;
  background: #409eff;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.9rem;
  margin-right: 1rem;
  flex-shrink: 0;
}

.step-text {
  color: #2c3e50;
  font-size: 0.95rem;
  line-height: 1.8;
}

.bottom-space {
  flex: 4.5;
  background: rgba(221, 237, 255, 0.9);
  border-radius: 12px;
  margin-top: 1rem;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.response-container {
  flex: 1;
  background: white;
  border-radius: 8px;
  padding: 1rem;
  overflow-y: auto;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
}

.response-text {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
  font-family: monospace;
  color: #333;
  line-height: 1.6;
}

.input-container {
  display: flex;
  gap: 0.5rem;
  height: 48px;
}

.message-input {
  flex: 1;
  border: 2px solid #e0e0e0;
  border-radius: 24px;
  padding: 0 1.5rem;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.message-input:focus {
  outline: none;
  border-color: #409eff;
  box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.1);
}

.send-button {
  background: #409eff;
  color: white;
  border: none;
  border-radius: 24px;
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.send-button:hover {
  background: #66b1ff;
  transform: translateY(-1px);
}

.send-button:active {
  transform: translateY(0);
}

.send-icon {
  width: 20px;
  height: 20px;
  fill: currentColor;
}
</style> 