<template>
  <div class="container">
    <!-- 头部导航保持原样 -->
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

    <div class="aside-main-container">
      <div class="aside-intro">
        <div class="intro-card">
          <h2 class="intro-title">病例分析功能</h2>

          <div class="feature-item">
            <div class="feature-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path
                  d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15h-2v-6h2v6zm3 0h-2v-8h2v8zm3 0h-2v-4h2v4z"
                />
              </svg>
            </div>
            <div class="feature-content">
              <h3>智能识别</h3>
              <p>拍摄或上传医疗文档，自动识别文字内容</p>
            </div>
          </div>

          <div class="feature-item">
            <div class="feature-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path
                  d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"
                />
              </svg>
            </div>
            <div class="feature-content">
              <h3>医学分析</h3>
              <p>基于专业医学模型解析病情，提供诊疗建议</p>
            </div>
          </div>

          <div class="feature-item">
            <div class="feature-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path
                  d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-7 12h-2v-2h2v2zm0-4h-2V6h2v4z"
                />
              </svg>
            </div>
            <div class="feature-content">
              <h3>结果解读</h3>
              <p>清晰展示诊疗结果，帮助理解医疗建议</p>
            </div>
          </div>

          <div class="usage-tips">
            <div class="tip-header">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path
                  d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"
                />
              </svg>
              <span>使用提示</span>
            </div>
            <ul>
              <li>确保文档对齐虚线框</li>
              <li>尽量保持文档平整无褶皱</li>
              <li>包含关键医疗信息：症状、病史、检查结果</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="main-picture">
        <!-- 图片预览区域 -->
        <div class="picture-preview">
          <img
            class="preview-image"
            v-if="capturedImage"
            :src="capturedImage"
            alt="拍摄结果"
          />
          <div v-else class="upload-placeholder">待上传</div>
        </div>

        <!-- 识别结果区域 -->
        <div class="textarea" placeholder="识别结果将显示在这里">
          {{ resultText }}
        </div>
        <div class="cap_buttons">
          <button class="caputure-button" @click="toggleCamera">
            {{ isCameraOpen ? "拍照" : "开启摄像头" }}
          </button>

          <button class="analysis-button" @click="sendForAnalysis">
            分析诊疗结果
          </button>
        </div>
        <div v-show="isCameraOpen" class="camera-modal">
          <div class="modal-mask" @click.self="closeCamera"></div>

          <div class="modal-content">
            <video ref="videoElement" autoplay playsinline></video>
            <div class="focus-frame"></div>
            <canvas ref="canvasElement" style="display: none"></canvas>

            <div class="modal-controls">
              <button @click="closeCamera" class="modal-close-btn">关闭</button>
              <button @click="capturePhoto" class="modal-capture-btn">
                拍摄
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="main-response">
        <div class="diagnosis-title">诊疗结果</div>
        <pre class="diagnosis-content">{{ diagnosisResult }}</pre>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      isCameraOpen: false,
      capturedImage: null, // 新增图片预览
      resultText: "",
      mediaStream: null,

      diagnosisResult: "", // 新增诊疗结果
    };
  },
  methods: {
    async toggleCamera() {
      if (this.isCameraOpen) return;

      try {
        this.mediaStream = await navigator.mediaDevices.getUserMedia({
          video: { width: 1280, height: 720 },
        });
        this.$refs.videoElement.srcObject = this.mediaStream;
        this.isCameraOpen = true;
      } catch (error) {
        console.error("摄像头访问失败:", error);
        alert("无法访问摄像头，请确保已授予权限");
      }
    },

    closeCamera() {
      if (this.mediaStream) {
        this.mediaStream.getTracks().forEach((track) => track.stop());
        this.mediaStream = null;
      }
      this.isCameraOpen = false;
    },

    async capturePhoto() {
      const video = this.$refs.videoElement;
      const canvas = this.$refs.canvasElement;

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0);

      // 显示拍摄预览
      this.capturedImage = canvas.toDataURL("image/jpeg");

      // 上传逻辑保持不变
      canvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append("image", blob, "photo.jpg");

        try {
          const response = await axios.post(
            "http://localhost:8000/picture",
            formData,
            { headers: { "Content-Type": "multipart/form-data" } }
          );
          this.resultText = response.data.text;
          console.log(123213);
          console.log(this.resultText);
        } catch (error) {
          console.error("识别失败:", error);
          alert("OCR处理失败");
        }
      }, "image/jpeg");

      this.closeCamera();
    },
    async sendForAnalysis() {
      if (!this.resultText) {
        alert("请先识别图片内容");
        return;
      }

      try {
        const response = await fetch(
          `http://localhost:8000/analysis/${this.resultText}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        if (!response.ok) {
          throw new Error(`请求失败: ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        this.diagnosisResult = ""; // 清空之前的结果

        let isReading = true;
        while (isReading) {
          const { done, value } = await reader.read();
          if (done) {
            isReading = false;
            break;
          }

          const chunk = decoder.decode(value, { stream: true });
          // 处理流式数据
          const lines = chunk.split("\n\n").filter((line) => line.trim());
          for (const line of lines) {
            if (line.startsWith("data: ")) {
              const dataStr = line.replace("data: ", "");
              try {
                const data = JSON.parse(dataStr);
                this.diagnosisResult += data.content;
              } catch (e) {
                console.error("解析JSON失败:", e);
              }
            }
          }
        }
      } catch (error) {
        console.error("分析请求失败:", error);
        alert("分析失败，请检查控制台");
      }
    },
  },
  beforeUnmount() {
    this.closeCamera();
  },
};
</script>
<style scoped>
.container {
  height: 100vh;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  display: grid;
  grid-template-rows: 1fr 15fr;
  font-family: "Segoe UI", system-ui, sans-serif;
}
/* 导航栏 */
.head {
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

.aside-main-container {
  display: grid;
  grid-template-columns: 1fr 2fr 2fr;
  overflow: hidden;
  padding: 1.5rem; /*内边距*/
  gap: 1.5rem;
}

.aside-intro {
  background: linear-gradient(135deg, #f0f7ff 0%, #e6f0ff 100%);
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 82, 204, 0.08);
  padding: 0.5rem;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  border: 1px solid #d0e0ff;
}

.intro-card {
  background: rgba(255, 255, 255, 0.85);
  border-radius: 12px;
  padding: 0.5rem;
  box-shadow: 0 4px 12px rgba(0, 41, 102, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(208, 224, 255, 0.5);
}

.intro-title {
  color: #0052cc;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid rgba(0, 82, 204, 0.15);
  text-align: center;
  font-weight: 600;
  letter-spacing: -0.5px;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 1.25rem;
  padding: 0.75rem;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.feature-item:hover {
  background: rgba(240, 247, 255, 0.6);
  transform: translateY(-2px);
}

.feature-icon {
  background: linear-gradient(135deg, #4dabf7 0%, #1971c2 100%);
  width: 42px;
  height: 42px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  flex-shrink: 0;
  box-shadow: 0 4px 8px rgba(25, 113, 194, 0.2);
}

.feature-icon svg {
  width: 24px;
  height: 24px;
  fill: white;
}

.feature-content h3 {
  color: #1971c2;
  margin-bottom: 0.25rem;
  font-weight: 600;
  font-size: 1.1rem;
}

.feature-content p {
  color: #495057;
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0;
}

.usage-tips {
  background: #fff8e6;
  border-radius: 10px;
  padding: 1rem;
  margin-top: 1.5rem;
  border-left: 4px solid #ffc107;
}

.tip-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
}

.tip-header svg {
  width: 20px;
  height: 20px;
  fill: #e67700;
  margin-right: 0.5rem;
}

.tip-header span {
  color: #e67700;
  font-weight: 600;
  font-size: 1.05rem;
}

.usage-tips ul {
  margin: 0;
  padding-left: 1.5rem;
}

.usage-tips li {
  color: #5c3c00;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  line-height: 1.5;
}

.usage-tips li:last-child {
  margin-bottom: 0;
}

/* 调整整体布局比例 */
.aside-main-container {
  grid-template-columns: 1.1fr 2fr 2fr;
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .aside-main-container {
    grid-template-columns: 1.2fr 2fr 2fr;
  }
}

.main-picture {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;

  gap: 1rem;
}

.picture-preview {
  height: 55%;
  border: 2px dashed #cbd5e1;
  border-radius: 8px;
  text-align: center;
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  background: #f8fafc;
  transition: border-color 0.3s ease;
}

.picture-preview:hover {
  border-color: #3b82f6;
}

.upload-placeholder {
  color: #94a3b8;
  font-size: 0.875rem;
}

.textarea {
  height: 40%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-family: monospace;
  resize: vertical;
  transition: border-color 0.3s ease;
}

.textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}
.cap_buttons {
  height: 5%;
  gap: 2rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
}
.caputure-button,
.analysis-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  align-items: center;
}

.caputure-button {
  background: #3b82f6;
  color: white;
}

.caputure-button:hover {
  background: #2563eb;
  transform: translateY(-1px);
}

.analysis-button {
  background: #10b981;
  color: white;
}

.analysis-button:hover {
  background: #059669;
  transform: translateY(-1px);
}

.camera-modal {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-mask {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
}

.modal-content {
  position: relative;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  max-width: 90vw;
}

.modal-content video {
  width: 640px;
  max-width: 100%;
  height: auto;
  display: block;
}
/* 添加对准框样式 */
.focus-frame {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40%;
  height: 80%;
  border: 2px dashed rgba(255, 255, 255, 0.8);
  box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.3);
  pointer-events: none;
  z-index: 10;
}
.modal-controls {
  padding: 1rem;
  background: #f8fafc;
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.modal-close-btn,
.modal-capture-btn {
  padding: 0.5rem 1.25rem;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.modal-close-btn {
  background: #ef4444;
  color: white;
}

.modal-close-btn:hover {
  background: #dc2626;
}

.modal-capture-btn {
  background: #22c55e;
  color: white;
}

.modal-capture-btn:hover {
  background: #16a34a;
}

.main-response {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.diagnosis-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.diagnosis-content {
  height: 80%;
  white-space: pre-wrap;
  background: #f8fafc;
  padding: 1rem;
  border-radius: 8px;
  overflow-y: auto;
  font-family: monospace;
  color: #334155;
  border: 1px solid #e2e8f0;
  line-height: 1.6;
}

.preview-image {
  width: 100%;
  height: 100%;
  border-radius: 8px;
  object-fit: contain;
}
</style>