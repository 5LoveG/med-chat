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

    <div class="aside-main-container">
      <div class="aside">
        <!-- 新对话 -->

        <button class="new-conv" type="primary" @click="createNewSession">
          新对话
        </button>

        <!-- 会话记录列表 -->
        <div class="session-list">
          <div
            v-for="session in chatSessions"
            :key="session.id"
            class="session-item"
            :class="{ 'active-session': session.id === currentSessionId }"
            @click="switchSession(session.id)"
          >
            <span class="session-title">{{ session.title }}</span>
            <button
              type="text"
              class="delete-btn"
              @click.stop="deleteSession(session.id)"
            >
              删除
            </button>
          </div>
        </div>
        <div class="rag">
          <div class="rag-header">
            <h2>功能选择</h2>
            <button
              class="help-btn"
              @click="toggleHelp"
              :class="{ active: showHelp }"
            >
              ?
            </button>

            <!-- 帮助列表 -->
            <transition name="fade">
              <div class="help-list" v-if="showHelp">
                <div class="help-item">
                  <span class="label">专科门诊：</span>
                  <span class="value">选用专科医生</span>
                </div>
                <div class="help-item">
                  <span class="label">智能问药：</span>
                  <span class="value">解读药品使用</span>
                </div>
                <div class="help-item">
                  <span class="label">医保咨询：</span>
                  <span class="value">详解医保信息</span>
                </div>
              </div>
            </transition>
          </div>
          <button
            class="rag-button"
            :class="{ active: currentRagId === 1 }"
            @click="chooseRag(1)"
          >
            综合门诊
          </button>

          <button
            class="rag-button"
            @click="showSpecialty = !showSpecialty"
            :class="{ active: currentRagId === 2 }"
          >
            专科门诊
            <div class="specialty-menu" v-show="showSpecialty">
              <div class="menu-header">请选择科室</div>
              <div class="menu-list">
                <button
                  class="menu-item"
                  v-for="item in specialtyList"
                  :key="item"
                  @click="choosedepartments(item)"
                >
                  {{ item }}
                </button>
              </div>
            </div>
          </button>

          <button
            class="rag-button"
            :class="{ active: currentRagId === 3 }"
            @click="chooseRag(3)"
          >
            智能问药
          </button>

          <button
            class="rag-button"
            :class="{ active: currentRagId === 4 }"
            @click="chooseRag(4)"
          >
            医保咨询
          </button>
        </div>
      </div>

      <div class="main">
        <div ref="chatContainer" class="chat">
          <div
            v-for="(msg, index) in history"
            :key="index"
            class="message-item"
            :class="{
              'user-message': msg.role === 'user',
              'assistant-message': msg.role === 'assistant',
            }"
          >
            <svg
              t="1746539494512"
              v-if="msg.role === 'assistant'"
              class="assistant-icon"
              viewBox="0 0 1024 1024"
              version="1.1"
              xmlns="http://www.w3.org/2000/svg"
              p-id="85587"
              width="32"
              height="32"
            >
              <path
                d="M0.361412 507.120941a506.096941 506.096941 0 1 0 1012.133647 0 506.096941 506.096941 0 0 0-1012.133647 0z"
                fill="#77caf5"
                p-id="85588"
                data-spm-anchor-id="a313x.search_index.0.i51.3b523a81y1baZG"
                class="selected"
              ></path>
              <path
                d="M1012.615529 507.120941l-339.124705-339.124706-264.07153 253.168941-93.967059 71.077648 92.280471 92.220235-21.564235-6.866824 117.579294 117.579294 226.966588 265.758118a506.277647 506.277647 0 0 0 281.901176-453.812706z"
                fill="#77caf5"
                p-id="85589"
                data-spm-anchor-id="a313x.search_index.0.i50.3b523a81y1baZG"
                class="selected"
              ></path>
              <path
                d="M328.884706 458.390588v225.039059l167.574588-10.962823V447.488z"
                fill="#935635"
                p-id="85590"
              ></path>
              <path
                d="M664.033882 436.525176l-167.574588 10.962824v224.978824l167.574588-10.962824z"
                fill="#804000"
                p-id="85591"
              ></path>
              <path
                d="M551.815529 632.711529V577.656471H452.668235v54.994823c0 4.397176-3.614118 7.890824-7.890823 7.890824H376.410353v189.861647h251.904v-189.861647H559.947294a7.951059 7.951059 0 0 1-8.131765-7.890824z"
                fill="#FED8B2"
                p-id="85592"
              ></path>
              <path
                d="M628.193882 640.602353H559.826824a7.951059 7.951059 0 0 1-7.830589-7.890824V577.656471h-48.790588v252.747294h125.108706l-0.120471-189.861647z"
                fill="#EABE96"
                p-id="85593"
              ></path>
              <path
                d="M302.019765 462.486588a39.634824 39.634824 0 1 0 79.269647 0 39.634824 39.634824 0 0 0-79.269647 0z"
                fill="#FED8B2"
                p-id="85594"
              ></path>
              <path
                d="M623.314824 462.486588a39.634824 39.634824 0 1 0 79.269647 0 39.634824 39.634824 0 0 0-79.269647 0z"
                fill="#EABE96"
                p-id="85595"
              ></path>
              <path
                d="M506.759529 627.531294h-8.914823a149.624471 149.624471 0 0 1-149.624471-149.684706V341.293176a149.624471 149.624471 0 0 1 149.624471-149.62447h8.914823a149.624471 149.624471 0 0 1 149.684706 149.62447v136.553412a149.744941 149.744941 0 0 1-149.684706 149.684706z"
                fill="#F4E3C3"
                p-id="85596"
              ></path>
              <path
                d="M506.759529 191.668706h-3.614117v435.862588h3.614117a149.624471 149.624471 0 0 0 149.684706-149.684706V341.293176a149.805176 149.805176 0 0 0-149.684706-149.62447z"
                fill="#FED8B2"
                p-id="85597"
              ></path>
              <path
                d="M501.519059 180.705882h-9.697883a162.996706 162.996706 0 0 0-163.117176 162.394353v228.592941h24.395294V402.974118c72.402824-7.348706 143.540706-21.564235 205.884235-52.766118 22.467765 25.780706 48.368941 48.790588 77.101177 67.463529V571.632941h27.828706V343.100235A162.153412 162.153412 0 0 0 501.519059 180.705882z"
                fill="#B97850"
                p-id="85598"
              ></path>
              <path
                d="M634.578824 249.976471A162.153412 162.153412 0 0 0 501.458824 180.705882H496.338824v194.680471a433.694118 433.694118 0 0 0 62.765176-25.178353c22.467765 25.780706 48.368941 48.790588 77.040941 67.463529V571.632941h27.888941V343.100235c0-34.635294-10.962824-66.861176-29.515294-93.184z"
                fill="#935635"
                p-id="85599"
              ></path>
              <path
                d="M414.298353 444.897882a15.36 15.36 0 1 0 30.72 0 15.36 15.36 0 0 0-30.72 0z"
                fill="#59595B"
                p-id="85600"
              ></path>
              <path
                d="M559.525647 444.897882a15.36 15.36 0 1 0 30.72 0 15.36 15.36 0 0 0-30.72 0z"
                fill="#272525"
                p-id="85601"
              ></path>
              <path
                d="M502.241882 571.151059a50.416941 50.416941 0 0 1-50.356706-50.356706 8.432941 8.432941 0 1 1 16.926118 0 33.310118 33.310118 0 1 0 66.620235 0 8.432941 8.432941 0 1 1 16.986353 0 50.055529 50.055529 0 0 1-50.176 50.356706z"
                fill="#FD8469"
                p-id="85602"
              ></path>
              <path
                d="M552.598588 520.794353a8.432941 8.432941 0 1 0-16.865882 0c0 18.070588-14.456471 32.828235-32.527059 33.129412v17.106823a50.296471 50.296471 0 0 0 49.392941-50.236235z"
                fill="#FC6F58"
                p-id="85603"
              ></path>
              <path
                d="M639.036235 640.602353H586.089412a83.968 83.968 0 0 1-167.81553 0h-52.766117a115.049412 115.049412 0 0 0-115.049412 115.049412v187.934117a503.567059 503.567059 0 0 0 256 69.51153c89.931294 0 174.381176-23.491765 247.567059-64.632471v-192.752941c0-63.488-51.621647-115.109647-115.049412-115.109647z"
                fill="#FFFFFF"
                p-id="85604"
              ></path>
              <path
                d="M639.036235 640.602353H586.089412c0 46.08-37.165176 83.486118-83.124706 83.907765v288.527058c1.144471 0 2.288941 0.180706 3.373176 0.180706 89.931294 0 174.441412-23.491765 247.567059-64.63247v-192.873412a115.049412 115.049412 0 0 0-114.928941-115.109647z"
                fill="#E6F3FF"
                p-id="85605"
              ></path>
              <path
                d="M506.458353 825.705412v187.51247c9.577412 0 19.154824-0.361412 28.672-0.903529l83.787294-185.584941-44.272941-27.467294 44.272941-36.020706v-124.867765h-56.259765l-56.199529 187.331765z"
                fill="#CFDBE6"
                p-id="85606"
              ></path>
              <path
                d="M450.319059 638.373647h-56.259765v124.867765l44.272941 36.020706-44.272941 27.467294 83.787294 185.524706c9.517176 0.602353 18.974118 0.963765 28.672 0.963764v-187.51247l-56.199529-187.331765z"
                fill="#E6F3FF"
                p-id="85607"
              ></path>
              <path
                d="M332.619294 167.936h340.87153v167.032471H332.498824z"
                fill="#FFFFFF"
                p-id="85608"
              ></path>
              <path
                d="M503.024941 167.936h170.465883v167.032471H502.964706z"
                fill="#D0D1D3"
                p-id="85609"
              ></path>
              <path
                d="M553.622588 234.556235h-33.671529v-33.611294h-33.731765v33.611294h-33.671529v33.792h33.671529v33.67153h33.731765v-33.67153h33.731765z"
                fill="#FC6F58"
                p-id="85610"
              ></path>
              <path
                d="M520.011294 234.556235v-33.611294H502.964706v101.074824h16.926118v-33.67153h33.731764v-33.731764z"
                fill="#F1543F"
                p-id="85611"
              ></path>
              <path
                d="M629.217882 916.058353a39.152941 39.152941 0 1 0 78.305883 0 39.152941 39.152941 0 0 0-78.305883 0z"
                fill="#A3CFFF"
                p-id="85612"
              ></path>
              <path
                d="M678.550588 867.749647v-223.533176a10.300235 10.300235 0 0 0-10.24-10.24 10.300235 10.300235 0 0 0-10.300235 10.24v223.472941a49.513412 49.513412 0 0 0 10.24 97.822117 49.513412 49.513412 0 1 0 10.24-97.822117h0.060235z m-10.179764 77.221647a28.912941 28.912941 0 0 1 0-57.825882 28.912941 28.912941 0 0 1 0 57.825882zM365.025882 774.445176V645.12a10.300235 10.300235 0 0 0-10.24-10.24 10.300235 10.300235 0 0 0-10.300235 10.24v129.325176a58.006588 58.006588 0 0 0-47.706353 57.042824v107.821176c0 5.662118 4.638118 10.300235 10.300235 10.300236h20.781177c5.662118 0 10.24-4.638118 10.24-10.24a10.300235 10.300235 0 0 0-10.24-10.300236H317.44v-97.701647a37.526588 37.526588 0 0 1 74.992941 0v97.701647H377.675294a10.300235 10.300235 0 0 0-10.24 10.24c0 5.662118 4.577882 10.300235 10.24 10.300236h24.877177c5.601882 0 10.24-4.638118 10.24-10.24v-107.881412a58.066824 58.066824 0 0 0-47.766589-57.042824z"
                fill="#5CA4F3"
                p-id="85613"
              ></path>
            </svg>

            <svg
              v-if="msg.role === 'user'"
              class="user-icon"
              t="1746538363305"
              viewBox="0 0 1024 1024"
              version="1.1"
              xmlns="http://www.w3.org/2000/svg"
              p-id="53491"
              data-spm-anchor-id="a313x.search_index.0.i28.3b523a81y1baZG"
              width="48"
              height="48"
            >
              <path
                d="M511.8194 511.8194m-377.453262 0a377.453263 377.453263 0 1 0 754.906525 0 377.453263 377.453263 0 1 0-754.906525 0Z"
                fill="#1296db"
                p-id="53492"
                data-spm-anchor-id="a313x.search_index.0.i27.3b523a81y1baZG"
                class="selected"
              ></path>
              <path
                d="M359.393298 494.120635s28.895944 114.500176 136.172134 135.088536c0 0 103.302998 13.725573 152.787302-135.088536 49.484303-149.175309-66.099471-214.91358-144.479718-173.375661 0 0-206.244797-24.561552-144.479718 173.375661z"
                fill="#FFD6BD"
                p-id="53493"
              ></path>
              <path
                d="M511.8194 888.911464c110.888183 0 210.579189-47.678307 279.568254-123.891358-61.042681-96.079012-187.101235-96.079012-187.101234-96.079013h-155.676896s-142.312522 0-197.576014 114.861376c67.544268 65.377072 159.650088 105.108995 260.78589 105.108995z"
                fill="#6BD7C7"
                p-id="53494"
              ></path>
              <path
                d="M463.057496 615.122399l0.361199 93.189418h96.801411v-113.05538z"
                fill="#FCD3BE"
                p-id="53495"
              ></path>
              <path
                d="M354.697707 495.926631s-25.283951-92.828219-16.615167-134.727336c0 0 4.334392-47.678307 29.257143-73.323457l-16.253969-3.973192s11.919577-16.615168 62.487478-42.982717c0 0 27.812346-24.561552 117.389771-13.364373 0 0 31.063139 0.722399 63.932275 19.143562 0 0-14.447972-32.146737-21.310758-37.925926 0 0-5.779189-13.364374 38.648324 28.895944 0 0 19.865961 32.146737 21.310759 36.481129s10.835979-3.250794 31.063139 5.05679c0 0 22.033157 17.337566 24.922751 23.116755 2.889594 5.779189-24.561552-9.752381-24.561552-9.752381s24.200353 45.511111 17.337566 109.443386c0 0-15.892769 65.738272-32.869135 92.828219 0 0 1.805996-37.203527-3.973193-56.34709 0 0-19.865961-33.591534-36.119929-45.149912 0 0-3.973192-1.444797-3.973192 6.140388 0 0 4.695591 26.728748 9.029982 31.063139 0 0 5.417989 4.334392-26.006349-9.752381 0 0-48.039506-27.089947-62.126279-47.317107 0 0-8.307584-2.889594-5.417989 3.250793 0 0 15.53157 32.146737 20.949559 35.036332 0 0-48.761905 2.528395-67.905468-7.223986 0 0-36.842328-10.835979-49.484303-28.534744 0 0-3.973192-2.889594-3.973192 1.444797 0 0 13.003175 29.257143 25.28395 33.591534 0 0-27.089947-2.167196-43.705114-15.17037l-15.53157-20.58836s-2.889594-1.444797-3.973192 2.889594c0 0-23.477954 40.81552-26.367549 77.657849 0 0-0.722399 32.507937-0.361199 35.75873 0.361199 2.889594 0.361199 9.029982-1.083598 4.334391z"
                fill="#431B01"
                p-id="53496"
              ></path>
              <path
                d="M520.849383 701.44903l-57.791887-61.40388-50.567902 32.507936 75.851852 86.687831z"
                fill="#FFFFFF"
                p-id="53497"
              ></path>
              <path
                d="M504.595414 703.255026l57.791888-61.40388 54.179894 28.895944-75.851852 86.687831z"
                fill="#FFFFFF"
                p-id="53498"
              ></path>
            </svg>

            <div class="message-bubble">
              <div class="message-content">{{ msg.content }}</div>
            </div>
          </div>
        </div>

        <!-- 输入区域 -->
        <div class="input">
          <input
            class="text"
            v-model="inputMessage"
            placeholder="输入消息..."
            @keyup.enter="sendMessage"
          />
          <button class="submit-btn" @click="sendMessage">提交</button>

          <button class="record" @click="toggleRecording">
            {{ isRecording ? "停止录音" : "语音交互" }}
          </button>
        </div>
      </div>

      <div class="right-aside">
        <h2 class="knowledge-title">🏥 医点小知识</h2>

        <div class="knowledge-card card-glow">
          <div class="card-icon">💡</div>
          <h3>急救黄金四分钟</h3>
          <p>
            心脏骤停后4分钟内实施心肺复苏，存活率可达50%，每延迟1分钟存活率下降7-10%。
          </p>
        </div>

        <div class="knowledge-card card-glow">
          <div class="card-icon">🌡️</div>
          <h3>正确测量体温</h3>
          <p>
            腋温测量应夹紧5分钟，正常范围36.0-37.0℃。电子体温计测量时听到提示音后应再保持1分钟。
          </p>
        </div>

        <div class="knowledge-card card-glow">
          <div class="card-icon">💊</div>
          <h3>服药时间指南</h3>
          <p>
            空腹：餐前1小时<br />
            餐前：30分钟<br />
            餐后：30分钟后<br />
            睡前：睡前15-30分钟
          </p>
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
      inputMessage: "", //输入框信息
      chatSessions: [], // 所有聊天会话
      currentSessionId: null, // 当前选中的会话ID
      history: [], //当前会话历史记录
      currentRagId: 1,
      //whisper
      isRecording: false,
      mediaRecorder: null,
      audioChunks: [],
      error: null,

      //功能选择
      showHelp: false,

      //专科门诊
      showSpecialty: false,
      specialtyList: [
        "心血管内科",
        "呼吸内科",
        "消化内科",
        "神经外科",
        "骨科",
        "泌尿外科",
        "妇产科",
        "儿科",
        "眼科",
        "耳鼻喉科",
        "皮肤科",
        "精神心理科",
        "肿瘤科",
        "内分泌科",
        "风湿免疫科",
        "康复医学科",
        "中医科",
        "急诊科",
      ],
    };
  },

  mounted() {
    this.getSessions();
    this.chooseRag(1);
  },
  methods: {
    // llm -------------------------------------------------------------
    async getSessions() {
      try {
        const response = await axios.get("http://localhost:8000/sessions");
        this.chatSessions = response.data;
      } catch (err) {
        console.log("failed to get sessions");
      }
    },
    async chooseRag(RagId) {
      try {
        const response = await axios.post(`http://localhost:8000/rag/${RagId}`);
        this.currentRagId = response.data;
        console.log("success to change rag");
      } catch (err) {
        console.log("failed to change rag");
      }
    },
    async choosedepartments(department) {
      try {
        const response = await axios.post(
          `http://localhost:8000/chooseDepartment/${department}`
        );
        this.currentRagId = 2;
        console.log(response.data);
        console.log("success to change rag!");
      } catch (err) {
        console.log("failed to change rag");
      }
    },
    async createNewSession() {
      try {
        const response = await axios.get("http://localhost:8000/new");
        const newSession = response.data;
        this.chatSessions.unshift(newSession);
        this.currentSessionId = newSession.id;
        await this.switchSession(this.currentSessionId);
      } catch (err) {
        console.log("failed to create new session");
      }
    },

    async switchSession(sessionId) {
      try {
        const response = await axios.get(
          `http://localhost:8000/history/${sessionId}`
        );
        this.history = response.data.history;
        this.currentSessionId = sessionId;
        this.scrollToBottom();
      } catch (err) {
        console.log("failed to switch Session");
      }
      const selectedSession = this.chatSessions.find((s) => s.id === sessionId);
      if (selectedSession) {
        // 从原位置移除该会话
        this.chatSessions = this.chatSessions.filter((s) => s.id !== sessionId);
        // 将该会话放到列表第一项
        this.chatSessions.unshift(selectedSession);
      }
    },

    async deleteSession(sessionId) {
      try {
        const response = await axios.delete(
          `http://localhost:8000/delete/${sessionId}`
        );
        console.log(response.data);
      } catch (err) {
        console.log("failed to delete sessions");
      }
      this.chatSessions = this.chatSessions.filter((s) => s.id !== sessionId);
      // 如果删除的是当前会话，自动选择第一个会话
      if (sessionId === this.currentSessionId) {
        this.currentSessionId =
          this.chatSessions.length > 0 ? this.chatSessions[0].id : null;
      }
    },

    //功能选择
    async toggleHelp() {
      this.showHelp = !this.showHelp;
    },

    async sendMessage() {
      const inputMessage = this.inputMessage;
      this.inputMessage = "";
      if (!inputMessage.trim()) return;

      if (!this.currentSessionId) {
        await this.createNewSession();
      }

      // 添加用户消息
      this.history.push({
        role: "user",
        content: inputMessage,
      });
      this.scrollToBottom();
      // 添加临时assistant消息
      const assistantMessage = {
        role: "assistant",
        content: "",
        isStreaming: true,
      };
      this.history.push(assistantMessage);

      try {
        const response = await fetch("http://localhost:8000/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: inputMessage,
            session_id: this.currentSessionId,
          }),
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

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
              const data = JSON.parse(line.replace("data: ", ""));
              const lastMsg = this.history[this.history.length - 1];
              lastMsg.content += data.content;
            }
          }
          this.scrollToBottom();
        }

        // 标记流结束
        delete this.history[this.history.length - 1].isStreaming;
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

    //whisper -------------------------------------------------------------
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
<style>
html,
body {
  height: 100vh;
  margin: 0; /*外边距*/
  font-family: "Segoe UI", system-ui, -apple-system, sans-serif; /*字体*/
}

.container {
  height: 100%;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  display: grid;
  grid-template-rows: 1fr 15fr;
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
  /*指示条*/
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px; /*指示条高度*/
  background: #409eff;
  border-radius: 2px;
}

/* 边栏和主聊天容器 */
.aside-main-container {
  display: flex;
  flex-direction: row;
  overflow: hidden;
}

/* 左边栏 */
.aside {
  width: 15%;
  background: rgba(255, 255, 255, 0.95);
  border-right: 1px solid #e4e7ed;
  display: grid;
  grid-template-rows: 1fr 10fr 5fr;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 1);
}

.new-conv {
  margin: 1rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #409eff, #66b1ff);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: transform 0.2s ease;
}

.new-conv:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.3);
}

.session-list {
  overflow-y: auto;
  padding: 0.5rem;
}

.session-item {
  background-color: #f3f6f8;
  padding: 0.75rem 1rem;
  margin: 4px 0;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: all 0.2s ease;
  position: relative;
}

.session-item:hover {
  background: rgba(42, 79, 116, 0.1);
}

.session-item:hover .delete-btn {
  opacity: 1;
}

.active-session {
  background: rgba(64, 158, 255, 0.15) !important;
  font-weight: 500;
  color: #409eff;
}

.session-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 0.95rem;
}

.delete-btn {
  opacity: 0;
  border: none;
  background: none;
  color: #f56c6c;
  padding: 4px;
  margin-left: 8px;
  cursor: pointer;
  transition: opacity 0.2s ease;
}
.rag {
  display: flex;
  flex-direction: column;
}
/* 功能选择头部 */
.rag-header {
  position: relative;
  display: flex;
  align-items: center;
  gap: 80px;
}

.rag-header h2 {
  font-size: 1.2rem;
  color: #2c3e50;
  padding: 0.5rem 1.5rem;
  position: relative;
  border-left: 4px solid #409eff;
  border-radius: 0 8px 8px 0;
  box-shadow: 2px 2px 8px rgba(64, 158, 255, 0.05);
}

/* 帮助按钮 */
.help-btn {
  width: 28px;
  height: 28px;
  border: 2px solid #409eff;
  border-radius: 50%;
  background: white;
  color: #409eff;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.help-btn:hover {
  background: #409eff;
  color: white;
}

.help-btn.active {
  background: #409eff;
  color: white;
}

/* 帮助列表 */
.help-list {
  position: absolute;
  right: 0;
  top: 100%;
  width: 240px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 1rem;
  z-index: 1000;
  margin-top: 8px;
}

.help-item {
  display: flex;
  padding: 10px 15px;
  border-bottom: 1px solid #eee;
}

.help-item:last-child {
  border-bottom: none;
}

.label {
  color: #409eff;
  font-weight: 500;
  min-width: 72px;
}

.value {
  color: #666;
  flex: 1;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
.rag-button {
  width: 90%;
  padding: 10px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: #f8f9fa;
  color: #333;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 3%;
  margin-left: 5%;
}

.rag-button:hover {
  background: #e9ecef;
  transform: translateY(-2px);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
}

.rag-button.active {
  background: #409eff;
  border-color: #409eff;
  color: white;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

/*专科门诊*/
.specialty-menu {
  position: absolute;
  left: calc(100% + 10px); /*位于父元素右侧*/
  top: -500px; /*位于父元素下方*/
  width: 200px;
  height: 600px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  z-index: 1000;
  display: grid;
  grid-template-rows: 1fr 10fr;
}

.menu-header {
  padding: 12px 16px;
  background: #f8f9fa;
  font-weight: 500;
  color: #2c3e50;
  border-radius: 12px 12px 0 0;
  border-bottom: 1px solid #ebeef5;
}

.menu-list {
  overflow-y: auto;
  padding: 0.5rem;
}

.menu-item {
  width: 100%;
  background-color: #f8f9fa;
  padding: 0.75rem 1rem;
  margin: 4px 0;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: all 0.2s ease;
  position: relative;
  border: 2px solid #d5e5f7; /*边框*/
}

.menu-item:hover {
  background: #f5f7fa;
  color: #409eff;
}

.menu-item:hover::after {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: #409eff;
  border-radius: 0 3px 3px 0;
}

/* 滚动条美化 */
.menu-list::-webkit-scrollbar {
  width: 6px;
}

.menu-list::-webkit-scrollbar-track {
  background: rgba(64, 158, 255, 0.1);
}

.menu-list::-webkit-scrollbar-thumb {
  background: rgba(64, 158, 255, 0.4);
  border-radius: 4px;
}

/* 主聊天区域 */
.main {
  width: 70%;

  display: flex;
  flex-direction: column;
  background: rgba(245, 247, 250, 0.95);
}
.right-aside {
  width: 15%;
  display: flex;
  flex-direction: column;
  background: rgba(21, 91, 197, 0.95);
}
.chat {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}
.message-content {
  min-height: 1em; /* 保持消息框高度 */
  white-space: pre-wrap; /* 保留换行 */
}

.message-item {
  display: flex;
  max-width: 80%;
}

.user-message {
  align-self: flex-end;
  order: 0;
}

.user-icon {
  order: 1;
}
.assistant-icon {
  position: relative;
  left: -4px;
  top: 8px;
  width: 32px;
  height: 32px;
  flex-shrink: 0;
}
.assistant-message {
  justify-content: flex-start;
}

.message-bubble {
  padding: 1rem 1.25rem;
  border-radius: 12px;
  line-height: 1.5;
  font-size: 0.95rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  position: relative;
  word-break: break-word;
  white-space: pre-wrap;
}

.user-message .message-bubble {
  background: #409eff;
  color: white;
  border-radius: 12px 12px 0 12px;
}

.assistant-message .message-bubble {
  background: white;
  color: #303133;
  border-radius: 12px 12px 12px 0;
  border: 1px solid #ebeef5;
}

/* 输入区域 */
.input {
  padding: 1.5rem;
  background: white;
  box-shadow: 0 -2px 12px rgba(0, 0, 0, 0.05);
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.text {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

.text:focus {
  outline: none;
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.submit-btn,
.record,
button[type="button"] {
  padding: 0.75rem 1.25rem;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.submit-btn:hover,
.record:hover,
button[type="button"]:hover {
  background: #70abe6;
  transform: translateY(-1px);
}

button[type="button"] {
  background: #67c23a;
}

button[type="button"]:hover {
  background: #85ce61;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
}

::-webkit-scrollbar-thumb {
  background: rgba(144, 147, 153, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(144, 147, 153, 0.5);
}

/* 右边栏 */
.right-aside {
  width: 15%;
  background: rgba(255, 255, 255, 0.98);
  border-left: 1px solid #e4e7ed;
  padding: 0.4rem;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.05);
}

.knowledge-title {
  color: #2c3e50;
  font-size: 1.2rem;
  text-align: center;
  padding-bottom: 1rem;
  border-bottom: 2px solid #409eff;
  margin: 0 0 0.2rem 0;
  position: relative;
}

.knowledge-card {
  background: linear-gradient(145deg, #f8f9fa, #ffffff);
  border-radius: 12px;
  padding: 1.2rem;
  margin-bottom: 0.5rem; /* 辅助微调 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  border: 1px solid rgba(64, 158, 255, 0.15);
}

.knowledge-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(64, 158, 255, 0.15);
}

.card-glow:hover::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 12px;
  box-shadow: 0 0 15px rgba(64, 158, 255, 0.2);
}

.card-icon {
  font-size: 2rem;
  text-align: center;
  margin-bottom: 0.8rem;
}

.knowledge-card h3 {
  color: #34495e;
  font-size: 1.1rem;
  margin: 0 0 0.8rem 0;
  padding-bottom: 0.4rem;
  border-bottom: 1px dashed #dcdfe6;
}

.knowledge-card p {
  color: #7f8c8d;
  font-size: 0.9rem;
  line-height: 1.6;
  margin: 0;
}

.knowledge-card:nth-child(odd) {
  background: linear-gradient(145deg, #f5fbff, #ffffff);
}

@media (max-width: 768px) {
  .right-aside {
    display: none;
  }
}
</style>