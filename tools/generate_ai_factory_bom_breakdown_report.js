const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const PROJECT_ID = "ai_factory_industry_scurve_timeslice_20260302";
const OUT_DIR = path.join(ROOT, "research", "qa_projects", PROJECT_ID);
const OUT_FILE = path.join(OUT_DIR, "professional_report.html");

const sources = [
  src("SRC-NVDA-FY26-Q4", "NVIDIA FY2026 Q4 results", "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/", "NVIDIA 把客户需求表述为 AI factories，并披露 Q4 FY26 Data Center revenue $62.3B。"),
  src("SRC-AVGO-FY25-Q4", "Broadcom FY2025 Q4 results", "https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-fourth-quarter-and-fiscal-year-2025", "Broadcom 披露 AI semiconductor revenue 高增长，覆盖 custom AI accelerators 与 Ethernet AI switches。"),
  src("SRC-TSM-Q4-2025", "TSMC Q4 2025 results", "https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm", "TSMC 披露 advanced technologies revenue share、gross margin 与 2026 capex 指引。"),
  src("SRC-MU-FY26-Q1-PREPARED", "Micron FY2026 Q1 prepared remarks", "https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9", "Micron 给出 HBM TAM 与 2026 HBM supply 价量协议线索。"),
  src("SRC-SKHYNIX-FY25", "SK hynix FY2025 results", "https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html", "SK hynix 披露 AI memory 与 HBM 驱动的高收入和高 operating margin。"),
  src("SRC-SAMSUNG-FY25", "Samsung Q4 and FY2025 results", "https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results", "Samsung 披露 HBM、server DDR5、enterprise SSD 等 high-value AI products。"),
  src("SRC-SA-GB200-BOM-2024", "SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM", "https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component", "SemiAnalysis 用 GB200/rack-scale 架构拆解 AI server、rack、液冷和网络 BOM。"),
  src("SRC-SA-COWOS-HBM-2023", "SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain", "https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share", "SemiAnalysis 把 CoWoS 与 HBM 放在 AI accelerator 供给约束中分析。"),
  src("SRC-SA-OPTICAL-2024", "SemiAnalysis NVL72 / 800G / 1.6T networking", "https://newsletter.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband", "SemiAnalysis 把 rack-scale 架构与 NVLink、InfiniBand、800G、1.6T 光网络需求连接起来。"),
  src("SRC-LC-AI-OPTICS-202501", "LightCounting Optics for AI Clusters", "https://www.lightcounting.com/newsletter/en/january-2025-optics-for-ai-clusters-319", "LightCounting 拆解 AI cluster optical transceiver、LPO、CPO 等需求。"),
  src("SRC-DO-AI-NETWORKS-20250715", "Dell'Oro Ethernet AI Backend Network Forecast", "https://www.prnewswire.com/news-releases/ethernet-is-winning-the-war-against-infiniband-in-ai-back-end-networks-according-to-delloro-group-302501890.html", "Dell'Oro 讨论 AI back-end network 与 Ethernet/InfiniBand 路线。"),
  src("SRC-VRT-Q4-2025", "Vertiv Q4 2025 results", "https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/", "Vertiv 披露 AI infrastructure demand 对 orders/backlog 的拉动。"),
  src("SRC-DO-LIQUID-COOLING-20260108", "Dell'Oro Data Center Liquid Cooling Forecast", "https://www.prnewswire.com/news-releases/data-center-liquid-cooling-market-to-approach-7-billion-by-2029-as-ai-deployments-accelerate-according-to-delloro-group-302655848.html", "Dell'Oro 拆解 liquid cooling 市场与 direct liquid cooling adoption。"),
  src("SRC-DELL-FY26-Q4", "Dell FY2026 Q4 results", "https://investors.delltechnologies.com/node/19176/pdf", "Dell 披露 AI-optimized server orders、shipments 和 backlog。"),
  src("SRC-SMCI-FY26-Q2", "Supermicro FY2026 Q2 results", "https://ir.supermicro.com/news/news-details/2026/Super-Micro-Computer-Inc.-Reports-Second-Quarter-Fiscal-2026-Financial-Results/default.aspx", "Supermicro 是 AI server/rack 交付链条上的系统商样本。"),
  src("SRC-MSFT-FY26-Q2", "Microsoft FY2026 Q2 results", "https://www.microsoft.com/en-us/investor/earnings/fy-2026-q2/press-release-webcast", "Microsoft cloud revenue 与 commercial RPO 用于验证下游需求。"),
  src("SRC-GOOGL-Q4-2025", "Alphabet Q4 2025 results", "https://s206.q4cdn.com/479360582/files/doc_news/2026/Feb/04/attachments/2025q4-alphabet-earnings-release.pdf", "Alphabet capex 与 Google Cloud revenue 用于验证 AI factory 下游预算。"),
  src("SRC-AMZN-Q4-2025", "Amazon Q4 2025 results", "https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Fourth-Quarter-Results/default.aspx", "Amazon AWS 与 PPE purchases 用于验证客户侧基础设施投入。"),
  src("SRC-META-Q3-2025", "Meta Q3 2025 results", "https://investor.atmeta.com/investor-news/press-release-details/2025/Meta-Reports-Third-Quarter-2025-Results/default.aspx", "Meta capex guidance 用于验证下游 AI infrastructure 投入。"),
  src("SRC-ORCL-FY26-Q2", "Oracle FY2026 Q2 results", "https://investor.oracle.com/investor-news/news-details/2025/Oracle-Announces-Fiscal-Year-2026-Second-Quarter-Financial-Results/default.aspx", "Oracle cloud RPO 用于验证 AI infrastructure 订单需求。"),
];

const sourceById = Object.fromEntries(sources.map((item) => [item.id, item]));

const bomNodes = [
  {
    layer: "需求层",
    node: "云厂商 / AI labs / 企业与主权 AI",
    role: "定义 AI factory 要服务的工作负载，并支付 capex、租约或采购订单。",
    receives: "终端 AI 应用需求、模型训练与推理任务、企业数据和合规要求。",
    produces: "capex 预算、长期订单、RPO/backlog、利用率、云收入、AI ROI 反馈。",
    suppliesTo: "GPU/ASIC 平台、服务器系统商、数据中心基础设施商、网络与内存供应链。",
    companies: "Microsoft、Amazon、Alphabet、Meta、Oracle、AI labs、企业/主权 AI 项目",
    metrics: "capex、cloud revenue、RPO/backlog、FCF、AI 服务收入、算力利用率。",
    sources: ["SRC-MSFT-FY26-Q2", "SRC-GOOGL-Q4-2025", "SRC-AMZN-Q4-2025", "SRC-META-Q3-2025", "SRC-ORCL-FY26-Q2"],
  },
  {
    layer: "核心算力层",
    node: "GPU / AI Accelerator / Custom ASIC",
    role: "把 AI 工作负载转成可采购、可部署、可扩展的算力平台。",
    receives: "客户 capex、模型训练/推理需求、性能功耗目标、机柜规格。",
    produces: "GPU、AI ASIC、加速卡、参考架构、平台软件、集群互联标准。",
    suppliesTo: "服务器系统商、云厂商、AI labs、HBM/封装/网络供应链。",
    companies: "NVIDIA、Broadcom custom ASIC、AMD、云厂自研 ASIC",
    metrics: "Data Center revenue、AI semiconductor revenue、供给排期、gross margin、客户导入。",
    sources: ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4", "SRC-SA-GB200-BOM-2024"],
  },
  {
    layer: "制造封装层",
    node: "先进制程 / CoWoS 类先进封装 / 基板",
    role: "把 GPU/ASIC 设计制造出来，并把逻辑芯片与 HBM 组合成高带宽封装。",
    receives: "芯片设计、wafer 订单、先进封装需求、HBM 集成规格。",
    produces: "先进制程晶圆、先进封装产能、良率、交付周期。",
    suppliesTo: "GPU/ASIC 平台方、HBM 供应链、服务器系统商。",
    companies: "TSMC、先进封装生态、ABF/基板、设备与材料供应商",
    metrics: "advanced technologies revenue share、capex、advanced packaging capacity、gross margin、良率。",
    sources: ["SRC-TSM-Q4-2025", "SRC-SA-COWOS-HBM-2023"],
  },
  {
    layer: "内存存储层",
    node: "HBM / Server DRAM / Enterprise SSD",
    role: "给 AI 加速器和服务器提供带宽、容量和数据吞吐，是训练/推理效率的关键 BOM。",
    receives: "GPU/ASIC 规格、客户认证、价量协议、服务器平台需求。",
    produces: "HBM3E/HBM4、server DDR5、enterprise SSD、memory stack。",
    suppliesTo: "GPU/ASIC 平台、AI server、云数据中心。",
    companies: "SK hynix、Micron、Samsung",
    metrics: "HBM TAM、HBM ASP、客户资格、HBM bit shipment、operating margin、memory mix。",
    sources: ["SRC-MU-FY26-Q1-PREPARED", "SRC-SKHYNIX-FY25", "SRC-SAMSUNG-FY25"],
  },
  {
    layer: "板卡与机内连接层",
    node: "Retimer / AEC / CXL-PCIe / 电源管理 / 板级组件",
    role: "让 GPU、CPU、内存、网卡、存储在服务器和机柜内部稳定高速连接。",
    receives: "rack-scale 带宽、延迟、功耗和信号完整性要求。",
    produces: "retimer、AEC、PCIe/CXL 连接芯片、板级电源和信号完整性方案。",
    suppliesTo: "AI server、rack-scale 系统、OEM/ODM。",
    companies: "Astera Labs、Credo、Marvell、Broadcom、板级组件供应商",
    metrics: "design win、revenue growth、gross margin、客户集中度、平台认证。",
    sources: ["SRC-SA-GB200-BOM-2024", "SRC-SA-OPTICAL-2024"],
  },
  {
    layer: "集群网络层",
    node: "Switch / NIC / Optical Transceiver / PAM4 DSP / InfiniBand-Ethernet",
    role: "把单机、机柜和集群连成可训练大模型、可服务推理流量的网络。",
    receives: "GPU 集群规模、东西向流量、低延迟和高带宽需求。",
    produces: "交换机、NIC、光模块、PAM4 DSP、800G/1.6T 连接、网络操作系统。",
    suppliesTo: "云厂商 AI 集群、服务器/rack 系统、数据中心网络。",
    companies: "NVIDIA networking、Arista、Broadcom、Marvell、Credo、光模块供应链",
    metrics: "800G/1.6T 出货、switch revenue、optical demand、客户导入、ASP。",
    sources: ["SRC-SA-OPTICAL-2024", "SRC-LC-AI-OPTICS-202501", "SRC-DO-AI-NETWORKS-20250715"],
  },
  {
    layer: "系统交付层",
    node: "AI Server / Rack / Cluster Integration",
    role: "把 GPU、CPU、内存、网络、电源、散热和软件预集成为可上线系统。",
    receives: "GPU/ASIC allocation、内存、网卡、交换机、电力液冷部件、客户配置。",
    produces: "AI server、rack-scale system、cluster integration、部署与服务。",
    suppliesTo: "云厂商、AI labs、企业和主权 AI 项目。",
    companies: "Dell、Supermicro、HPE、ODM/OEM",
    metrics: "AI server orders、shipments、backlog、gross margin、inventory、cash conversion。",
    sources: ["SRC-DELL-FY26-Q4", "SRC-SMCI-FY26-Q2", "SRC-SA-GB200-BOM-2024"],
  },
  {
    layer: "数据中心物理基础设施层",
    node: "Power / UPS / PDU / Liquid Cooling / Thermal / Facility",
    role: "让高功率机柜真的接上电、散掉热、稳定运行，是 AI factory 落地的物理条件。",
    receives: "高功率 rack density、热负载、电力容量、项目建设周期、现场运维要求。",
    produces: "UPS、配电、PDU、CDU、direct-to-chip liquid cooling、热管理、现场工程服务。",
    suppliesTo: "数据中心运营方、云厂商、AI factory 项目和系统集成商。",
    companies: "Vertiv、Schneider、Eaton、液冷与数据中心工程供应商",
    metrics: "orders、backlog、project margin、delivery cycle、cash conversion、液冷 attach rate。",
    sources: ["SRC-VRT-Q4-2025", "SRC-DO-LIQUID-COOLING-20260108", "SRC-SA-GB200-BOM-2024"],
  },
  {
    layer: "运营与软件层",
    node: "Cluster Operations / Scheduling / Observability / AI Cloud Service",
    role: "把硬件集群变成可售卖、可计费、可调度、可监控的算力服务。",
    receives: "已经上线的 GPU/ASIC 集群、客户任务、SLA、模型和数据管线。",
    produces: "算力服务、调度、计费、利用率优化、故障运维、客户 ROI 数据。",
    suppliesTo: "AI 应用、企业客户、模型公司、内部业务部门。",
    companies: "云厂商、AI cloud、MLOps/observability 生态",
    metrics: "利用率、云收入、gross margin、客户续约、AI ROI、推理单位成本。",
    sources: ["SRC-MSFT-FY26-Q2", "SRC-GOOGL-Q4-2025", "SRC-ORCL-FY26-Q2"],
  },
];

const flows = [
  ["1", "需求出现", "云厂商、AI labs、企业和主权 AI 需要训练、推理、agent 与专用算力。"],
  ["2", "需求变订单", "下游把需求变成 capex、长期订单、RPO、服务器 backlog 和交付排期。"],
  ["3", "平台定规格", "GPU/ASIC 平台决定算力形态，并把需求传导到 HBM、封装、网络和机柜。"],
  ["4", "BOM 被放大", "单芯片需求扩展为 GPU/ASIC、HBM、网络、服务器、液冷、电力等一整套 BOM。"],
  ["5", "系统被交付", "系统商和数据中心基础设施商把部件组合成可上线的 rack/cluster/facility。"],
  ["6", "运营再验证", "利用率、云收入、FCF、AI ROI 决定下一轮 capex 是否继续。"],
];

function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  fs.writeFileSync(OUT_FILE, renderHtml(), "utf8");
  console.log(OUT_FILE);
}

function renderHtml() {
  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Factory 产业 BOM 拆解</title>
  <style>${css()}</style>
</head>
<body>
  <header class="hero">
    <p class="eyebrow">Step 1 · BOM Map</p>
    <h1>AI Factory 产业 BOM 拆解</h1>
    <p class="subtitle">先不做 QA、不做评分、不做投资结论。只回答一个问题：AI factory 这个产业到底由哪些环节构成，每个环节从谁那里接收什么，自己生产什么，再交付给谁。</p>
  </header>
  <nav>
    <a href="#plain">一句话</a>
    <a href="#flow">价值流</a>
    <a href="#bom">BOM 与供需</a>
    <a href="#table">总表</a>
    <a href="#sources">来源</a>
  </nav>
  <main>
    <section id="plain" class="section">
      <h2>一句话看懂</h2>
      <div class="summary-card">
        <p><b>AI factory 不是一块 GPU，也不是一个数据中心。</b>它是一套把 AI 需求持续转成可上线算力的工业系统：下游客户提出模型训练、推理和企业 AI 需求；GPU/ASIC 平台定义算力规格；先进制造、HBM、网络、电力、液冷和系统集成共同组成 BOM；最后由云收入、利用率和 ROI 决定是否继续扩容。</p>
      </div>
    </section>

    <section id="flow" class="section">
      <h2>需求如何变成 BOM</h2>
      <div class="flow-grid">${flows.map(renderFlow).join("")}</div>
    </section>

    <section id="bom" class="section">
      <h2>按 BOM 拆解产业构成与供需斜率</h2>
      <p class="section-lead">每个节点都用同一张表回答：当前 BOM 的需求是否会被 S 曲线放大拉动、供给能否跟上、谁控制供给、是否已经财务兑现、市场是否已定价、反证是什么。单位用量弹性并入第一问。</p>
      <div class="bom-stack">${bomNodes.map(renderNode).join("")}</div>
    </section>

    <section id="table" class="section">
      <h2>BOM 总表</h2>
      <div class="table-scroll">
        <table>
          <thead><tr><th>层级</th><th>BOM 节点</th><th>接受什么</th><th>生产什么</th><th>提供给谁</th><th>代表公司</th><th>验证指标</th></tr></thead>
          <tbody>${bomNodes.map((node) => `<tr><td>${e(node.layer)}</td><td>${e(node.node)}</td><td>${e(node.receives)}</td><td>${e(node.produces)}</td><td>${e(node.suppliesTo)}</td><td>${e(node.companies)}</td><td>${e(node.metrics)}</td></tr>`).join("")}</tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <h2>这张 BOM 图怎么用</h2>
      <div class="use-grid">
        <article><span>先看需求</span><p>如果云厂 capex、RPO、利用率和 AI ROI 不成立，后面所有 BOM 都只是短期库存波动。</p></article>
        <article><span>再看规格传导</span><p>GPU/ASIC 平台一旦提高功耗、带宽、内存和网络要求，会把需求放大到 HBM、封装、光网络、液冷和电力。</p></article>
        <article><span>最后看交付闭环</span><p>服务器、rack、数据中心基础设施把 BOM 变成上线算力；只有上线后的收入和 ROI 能开启下一轮扩容。</p></article>
      </div>
    </section>

    <section id="sources" class="section">
      <h2>来源索引</h2>
      <details class="sources" open>
        <summary>查看来源</summary>
        <div class="source-grid">${sources.map((item) => `<a href="${e(item.url)}" target="_blank" rel="noopener"><b>${e(item.id)}</b><span>${e(item.title)}</span><small>${e(item.note)}</small></a>`).join("")}</div>
      </details>
    </section>
  </main>
</body>
</html>`;
}

function renderFlow(row) {
  return `<article class="flow-card"><span>${e(row[0])}</span><h3>${e(row[1])}</h3><p>${e(row[2])}</p></article>`;
}

function renderNode(node, index) {
  const analysisRows = analysisForNode(node.node);
  return `<details class="bom-node" ${index < 4 ? "open" : ""}>
    <summary><span>${String(index + 1).padStart(2, "0")}</span><div><h3>${e(node.node)}</h3><p>${e(node.layer)} · ${e(node.role)}</p></div><b>展开</b></summary>
    <div class="node-body">
      <div class="node-grid">
        <article><span>接受什么</span><p>${e(node.receives)}</p></article>
        <article><span>自己生产什么</span><p>${e(node.produces)}</p></article>
        <article><span>提供给谁</span><p>${e(node.suppliesTo)}</p></article>
        <article><span>代表公司</span><p>${e(node.companies)}</p></article>
        <article><span>验证指标</span><p>${e(node.metrics)}</p></article>
        <article><span>这一层的作用</span><p>${e(node.role)}</p></article>
      </div>
      <div class="node-conclusion"><b>当前供需判断</b><p>${e(nodeVerdict(node.node))}</p></div>
      <div class="analysis-wrap">
        <table class="analysis-table">
          <thead><tr><th>问题</th><th>AI factory 产业里的回答</th><th>证据</th></tr></thead>
          <tbody>${analysisRows.map((row) => `<tr><td><b>${e(row.question)}</b><small>${e(row.prompt)}</small></td><td>${e(row.answer)}</td><td>${row.sources.map(chip).join("")}</td></tr>`).join("")}</tbody>
        </table>
      </div>
      <div class="source-row">${node.sources.map(chip).join("")}</div>
    </div>
  </details>`;
}

function analysisForNode(nodeName) {
  const sharedDemandRefute = "最主要反证是客户 capex 下修、AI ROI 不达预期、RPO/backlog 不转收入，或数据中心电力约束使扩容节奏后移。";
  const rows = {
    "云厂商 / AI labs / 企业与主权 AI": [
      a("需求是否会大幅增长？", "它和 AI S 曲线的传导关系", "模型训练、推理、agent、企业 AI 和主权 AI 都需要持续算力，云厂商先用 capex、RPO/backlog 和数据中心建设锁定未来供给。Microsoft、Alphabet、Amazon、Meta、Oracle 的材料说明需求已经进入预算、合同和基础设施投入口径。", ["SRC-MSFT-FY26-Q2", "SRC-GOOGL-Q4-2025", "SRC-AMZN-Q4-2025", "SRC-META-Q3-2025", "SRC-ORCL-FY26-Q2"]),
      a("单位用量是否会提升？", "每台服务器/每个机柜/每个 GPU 是否用更多", "下游不是直接决定单机 BOM 的工程规格，但它决定集群规模和服务等级：训练和推理规模越大，需要的 GPU/ASIC、HBM、网络、电力和冷却总量越多。单位用量提升最终体现在高功率机柜、更多网络端口、更大内存带宽和更高数据中心 capex。", ["SRC-GOOGL-Q4-2025", "SRC-SA-GB200-BOM-2024"]),
      a("供给能否跟上？", "产能、良率、认证、设备、材料、周期", "下游供给不是单一商品，约束来自 GPU allocation、HBM、先进封装、数据中心建设、电力接入、液冷和系统交付周期。客户愿意投钱不代表产能能同步上线。", ["SRC-SA-COWOS-HBM-2023", "SRC-VRT-Q4-2025", "SRC-DELL-FY26-Q4"]),
      a("谁控制供给？", "具体公司和份额", "需求侧由 hyperscaler 和大型 AI labs 控制预算与订单节奏；供给侧被 NVIDIA/ASIC 平台、TSMC、HBM 厂商、系统商和数据中心基础设施供应商共同约束。这里没有单一份额表，应该看各客户 capex 与 RPO/backlog 的绝对规模。", ["SRC-MSFT-FY26-Q2", "SRC-GOOGL-Q4-2025", "SRC-ORCL-FY26-Q2"]),
      a("是否已经财务兑现？", "收入、毛利、订单、backlog、指引", "已经部分兑现：云收入、RPO、PPE/capex 和数据中心订单都在财报里出现。但这些是需求兑现，不等于所有上游公司都能保留利润。", ["SRC-MSFT-FY26-Q2", "SRC-AMZN-Q4-2025", "SRC-ORCL-FY26-Q2"]),
      a("市场是否已定价？", "估值、预期、盈利上修空间", "市场对大型云厂商 AI capex 已高度关注；本节点更适合作为全链条需求验证，而不是直接寻找最便宜标的。需要补云厂商 AI capex ROI、FCF 压力和 AI 收入贡献。", ["SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025"]),
      a("反证是什么？", "价格下跌、capex 下修、供给释放、客户延迟", sharedDemandRefute, ["SRC-AMZN-Q4-2025", "SRC-META-Q3-2025"]),
    ],
    "GPU / AI Accelerator / Custom ASIC": [
      a("需求是否会大幅增长？", "它和 AI S 曲线的传导关系", "AI factory 的第一层实物需求是加速器。模型规模、推理请求和 agent 工作负载增加，会先拉动 GPU/ASIC 采购；NVIDIA 数据中心收入和 Broadcom AI semiconductor 指引说明需求已财务化。", ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4"]),
      a("单位用量是否会提升？", "每台服务器/每个机柜/每个 GPU 是否用更多", "单位用量提升体现在从单卡/单服务器走向 rack-scale：更多 GPU/ASIC、更高功耗、更强互联、更大 HBM 容量和更多网络端口。GB200/rack-scale 架构说明平台升级会放大整机 BOM。", ["SRC-SA-GB200-BOM-2024"]),
      a("供给能否跟上？", "产能、良率、认证、设备、材料、周期", "供给受先进制程、先进封装、HBM、板卡/系统集成和客户认证共同限制。即便芯片设计完成，交付仍受 TSMC、HBM 和系统产能制约。", ["SRC-SA-COWOS-HBM-2023", "SRC-TSM-Q4-2025", "SRC-MU-FY26-Q1-PREPARED"]),
      a("谁控制供给？", "具体公司和份额", "NVIDIA 控制通用 GPU 平台和软件/互联生态，Broadcom/云厂 custom ASIC 是第二路线。现有 source pack 没有可直接使用的全球 AI accelerator 份额表；可用代理是 NVIDIA 数据中心收入远高于其他单项 AI semiconductor 披露。", ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4"]),
      a("是否已经财务兑现？", "收入、毛利、订单、backlog、指引", "兑现最充分：NVIDIA Data Center revenue 达 $62.3B；Broadcom Q1 FY26 AI semiconductor revenue expected $8.2B。", ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4"]),
      a("市场是否已定价？", "估值、预期、盈利上修空间", "高度可能已部分定价，尤其是 NVIDIA。这个节点胜率高，但赔率要看未来盈利上修能否继续超过市场隐含预期；不能只因供不应求就直接认为仍便宜。", ["SRC-NVDA-FY26-Q4"]),
      a("反证是什么？", "价格下跌、capex 下修、供给释放、客户延迟", "云厂 capex 放缓、ASIC 分流超预期、GPU 毛利下行、客户订单延迟、先进封装/HBM 供给缓解导致交期缩短。", ["SRC-AVGO-FY25-Q4", "SRC-GOOGL-Q4-2025"]),
    ],
    "先进制程 / CoWoS 类先进封装 / 基板": [
      a("需求是否会大幅增长？", "它和 AI S 曲线的传导关系", "GPU/ASIC 放量必须经过先进制程和先进封装。AI accelerator 越复杂，越依赖高端晶圆制造、CoWoS 类封装和基板。", ["SRC-TSM-Q4-2025", "SRC-SA-COWOS-HBM-2023"]),
      a("单位用量是否会提升？", "每台服务器/每个机柜/每个 GPU 是否用更多", "单位用量不是简单 wafer 数量，而是每颗加速器对先进节点、封装面积、HBM 集成和基板复杂度的要求提升。rack-scale 架构越复杂，制造/封装约束越重要。", ["SRC-SA-GB200-BOM-2024", "SRC-SA-COWOS-HBM-2023"]),
      a("供给能否跟上？", "产能、良率、认证、设备、材料、周期", "先进节点和先进封装扩产周期长，受设备、良率、工程经验、客户认证和 capex 制约。TSMC 的高 capex 既说明需求强，也说明供给扩张不容易。", ["SRC-TSM-Q4-2025"]),
      a("谁控制供给？", "具体公司和份额", "核心控制者是 TSMC 及其先进封装生态；当前 source pack 可直接用 TSMC advanced technologies 占 wafer revenue 77% 和 gross margin 62.3% 作为高端制造价值捕获证据，但不能替代全球份额表。", ["SRC-TSM-Q4-2025"]),
      a("是否已经财务兑现？", "收入、毛利、订单、backlog、指引", "已兑现：TSMC Q4 2025 revenue、gross margin、advanced technologies share 和 2026 capex 指引都说明先进制造处于强需求状态。", ["SRC-TSM-Q4-2025"]),
      a("市场是否已定价？", "估值、预期、盈利上修空间", "大概率已有较高预期。该节点卡点强但公司成熟度高，赔率取决于 advanced packaging 是否继续短缺、capex 回报是否保持、地缘风险是否被折价。", ["SRC-TSM-Q4-2025"]),
      a("反证是什么？", "价格下跌、capex 下修、供给释放、客户延迟", "先进封装产能释放快于需求、客户转单或自建替代、capex 回报下降、毛利率下行、地缘风险上升。", ["SRC-TSM-Q4-2025"]),
    ],
    "HBM / Server DRAM / Enterprise SSD": [
      a("需求是否会大幅增长？", "它和 AI S 曲线的传导关系", "AI accelerator 需要高带宽内存喂数据。GPU/ASIC 数量增加、模型上下文变长、推理并发提升，都会提高 HBM、server DRAM 和高端 SSD 的需求。", ["SRC-MU-FY26-Q1-PREPARED", "SRC-SKHYNIX-FY25"]),
      a("单位用量是否会提升？", "每台服务器/每个机柜/每个 GPU 是否用更多", "是。每代平台提高 HBM 容量、带宽和堆叠层数；服务器也需要更多 DRAM 与高速存储承接训练/推理数据流。TrendForce 和 Micron 的材料支持 HBM 单位价值和 TAM 扩张。", ["SRC-MU-FY26-Q1-PREPARED"]),
      a("供给能否跟上？", "产能、良率、认证、设备、材料、周期", "HBM 扩产受 DRAM wafer、堆叠封装、良率、客户资格认证和提前价量协议限制。Micron 提到 2026 HBM supply 已完成 price and volume agreements，本身就是供需紧张信号。", ["SRC-MU-FY26-Q1-PREPARED", "SRC-SA-COWOS-HBM-2023"]),
      a("谁控制供给？", "具体公司和份额", "主要是 SK hynix、Micron、Samsung。SK hynix 当前 HBM 领导力更强；Micron 是高弹性追赶者；Samsung 规模大但 HBM 领导力仍需验证。source pack 没有同口径 HBM 份额表，下一步需补按代际和客户的份额。", ["SRC-SKHYNIX-FY25", "SRC-MU-FY26-Q1-PREPARED", "SRC-SAMSUNG-FY25"]),
      a("是否已经财务兑现？", "收入、毛利、订单、backlog、指引", "已经明显兑现：SK hynix FY25 operating margin 49%；Micron 披露 record revenue/margin expansion 与 HBM TAM；Samsung Memory record revenue/profit，且 high-value AI products 包含 HBM、server DDR5、enterprise SSD。", ["SRC-SKHYNIX-FY25", "SRC-MU-FY26-Q1-PREPARED", "SRC-SAMSUNG-FY25"]),
      a("市场是否已定价？", "估值、预期、盈利上修空间", "存储稀缺已经被市场注意到，但不同公司定价程度不同。该节点仍有研究价值，因为 HBM 供需、ASP、资格认证和盈利弹性可能继续改变利润预期。需要补估值分位和盈利上修速度。", ["SRC-MU-FY26-Q1-PREPARED", "SRC-SKHYNIX-FY25"]),
      a("反证是什么？", "价格下跌、capex 下修、供给释放、客户延迟", "HBM ASP 下跌、客户资格不及预期、扩产快于需求、DRAM/NAND 周期反转、GPU/ASIC 需求放缓。", ["SRC-MU-FY26-Q1-PREPARED"]),
    ],
    "Retimer / AEC / CXL-PCIe / 电源管理 / 板级组件": [
      a("需求是否会大幅增长？", "它和 AI S 曲线的传导关系", "rack-scale AI server 内部的数据流和信号完整性要求更高，GPU、CPU、内存、网卡和存储之间需要更多高速连接芯片和线缆。", ["SRC-SA-GB200-BOM-2024", "SRC-SA-OPTICAL-2024"]),
      a("单位用量是否会提升？", "每台服务器/每个机柜/每个 GPU 是否用更多", "是。机柜级架构把连接从板内扩展到机柜内，retimer、AEC、PCIe/CXL、电源管理和高速信号组件的 attach rate 会随系统复杂度提升。", ["SRC-SA-GB200-BOM-2024"]),
      a("供给能否跟上？", "产能、良率、认证、设备、材料、周期", "供给约束主要不是总产能，而是客户设计导入、平台认证、低功耗/低延迟指标、信号完整性和批量可靠性。", ["SRC-SA-OPTICAL-2024"]),
      a("谁控制供给？", "具体公司和份额", "Astera、Credo、Marvell、Broadcom 等控制关键子环节，但每家公司暴露的子品类不同。当前 source pack 对板级组件份额不足，需要补 retimer/AEC/CXL/PMIC 分项份额和客户导入。", ["SRC-SA-GB200-BOM-2024"]),
      a("是否已经财务兑现？", "收入、毛利、订单、backlog、指引", "已在部分连接公司收入中兑现，但当前 BOM-only source pack 对 ALAB/CRDO/MRVL 财务源未在本页展开；下一步应补公司财报逐项解析。", ["SRC-SA-OPTICAL-2024"]),
      a("市场是否已定价？", "估值、预期、盈利上修空间", "这类小节点往往弹性大、估值也容易提前透支。需要用客户集中、design win、gross margin 和出货节奏判断是否仍有赔率。", ["SRC-SA-GB200-BOM-2024"]),
      a("反证是什么？", "价格下跌、capex 下修、供给释放、客户延迟", "平台自研替代、客户设计切换、价格快速下行、主要客户延迟 ramp、组件 attach rate 不及预期。", ["SRC-SA-OPTICAL-2024"]),
    ],
    "Switch / NIC / Optical Transceiver / PAM4 DSP / InfiniBand-Ethernet": [
      a("需求是否会大幅增长？", "它和 AI S 曲线的传导关系", "AI cluster 规模越大，东西向流量越大，需要更高速、更低延迟的网络。训练集群和推理集群都会提高 switch、NIC、光模块、PAM4 DSP、800G/1.6T 需求。", ["SRC-SA-OPTICAL-2024", "SRC-LC-AI-OPTICS-202501", "SRC-DO-AI-NETWORKS-20250715"]),
      a("单位用量是否会提升？", "每台服务器/每个机柜/每个 GPU 是否用更多", "是。rack-scale 和 cluster-scale 架构会提升每 GPU 或每机柜网络端口、光模块和 DSP 的用量；速度从 800G 向 1.6T 迁移也提高价值量。", ["SRC-SA-OPTICAL-2024", "SRC-LC-AI-OPTICS-202501"]),
      a("供给能否跟上？", "产能、良率、认证、设备、材料、周期", "约束来自高速光器件、DSP、交换芯片、网络软件、客户认证和部署经验。高速迭代还会带来良率和可靠性压力。", ["SRC-LC-AI-OPTICS-202501"]),
      a("谁控制供给？", "具体公司和份额", "控制者分散：NVIDIA networking、Arista、Broadcom、Marvell、Credo、光模块供应链分别控制不同环节。当前 source pack 有路线和市场预测，但缺同口径份额表。", ["SRC-DO-AI-NETWORKS-20250715", "SRC-SA-OPTICAL-2024"]),
      a("是否已经财务兑现？", "收入、毛利、订单、backlog、指引", "行业侧已看到需求预测，部分公司财报可验证，但本页未展开公司财务。需要补 Arista/Broadcom/Marvell/Credo/光模块公司收入、毛利和订单。", ["SRC-DO-AI-NETWORKS-20250715", "SRC-LC-AI-OPTICS-202501"]),
      a("市场是否已定价？", "估值、预期、盈利上修空间", "市场已关注 AI networking，但各子环节定价不同。真正机会可能来自还未被认为是核心瓶颈、但单位用量和客户导入快速提升的细分组件。", ["SRC-SA-OPTICAL-2024"]),
      a("反证是什么？", "价格下跌、capex 下修、供给释放、客户延迟", "以太网/InfiniBand 路线变化、CPO/LPO/AEC 替代、光模块 ASP 快速下行、客户自研或平台内化、AI capex 放缓。", ["SRC-DO-AI-NETWORKS-20250715"]),
    ],
    "AI Server / Rack / Cluster Integration": [
      a("需求是否会大幅增长？", "它和 AI S 曲线的传导关系", "GPU/ASIC、HBM、网络和电力冷却最终必须组合成服务器、机柜和集群才能上线。AI factory 扩张会直接拉动系统交付。", ["SRC-DELL-FY26-Q4", "SRC-SA-GB200-BOM-2024"]),
      a("单位用量是否会提升？", "每台服务器/每个机柜/每个 GPU 是否用更多", "单位复杂度提升：AI server 从单机走向 rack-scale，单系统包含更多 GPU、网络、电源、冷却和集成服务。", ["SRC-SA-GB200-BOM-2024"]),
      a("供给能否跟上？", "产能、良率、认证、设备、材料、周期", "供给受 GPU allocation、供应链协调、整机工程、客户定制、液冷/电力配套和交付周期约束。", ["SRC-DELL-FY26-Q4", "SRC-SA-GB200-BOM-2024"]),
      a("谁控制供给？", "具体公司和份额", "Dell、Supermicro、HPE、ODM/OEM 是主要系统交付者。该节点玩家较多，客户议价力较强；因此它是需求验证节点，不天然是高利润瓶颈。", ["SRC-DELL-FY26-Q4", "SRC-SMCI-FY26-Q2"]),
      a("是否已经财务兑现？", "收入、毛利、订单、backlog、指引", "已经兑现到订单和 backlog：Dell 披露 AI-optimized server orders、shipments 和 backlog；Supermicro 也有 AI server exposure，但需要更严格看毛利、库存和执行风险。", ["SRC-DELL-FY26-Q4", "SRC-SMCI-FY26-Q2"]),
      a("市场是否已定价？", "估值、预期、盈利上修空间", "订单弹性容易被市场快速定价，但利润质量可能被高估。关键不是 backlog 多大，而是 backlog 是否转成毛利和现金流。", ["SRC-DELL-FY26-Q4"]),
      a("反证是什么？", "价格下跌、capex 下修、供给释放、客户延迟", "订单取消、GPU allocation 变化、毛利率下降、库存/应收上升、客户延迟部署、治理或执行问题。", ["SRC-SMCI-FY26-Q2", "SRC-DELL-FY26-Q4"]),
    ],
    "Power / UPS / PDU / Liquid Cooling / Thermal / Facility": [
      a("需求是否会大幅增长？", "它和 AI S 曲线的传导关系", "GPU/ASIC 和 rack-scale 系统功耗提升后，数据中心必须新增电力、UPS、PDU、液冷和热管理能力，否则算力不能上线。", ["SRC-VRT-Q4-2025", "SRC-SA-GB200-BOM-2024", "SRC-DO-LIQUID-COOLING-20260108"]),
      a("单位用量是否会提升？", "每台服务器/每个机柜/每个 GPU 是否用更多", "是。高功率机柜提高每 rack 的电力和散热需求，直接抬升 UPS、配电、液冷 CDU、管路、现场工程和服务价值量。", ["SRC-SA-GB200-BOM-2024", "SRC-DO-LIQUID-COOLING-20260108"]),
      a("供给能否跟上？", "产能、良率、认证、设备、材料、周期", "这里的约束不是芯片良率，而是工程交付、项目周期、电力接入、现场可靠性、液冷方案认证和供应链交付能力。", ["SRC-VRT-Q4-2025", "SRC-DO-LIQUID-COOLING-20260108"]),
      a("谁控制供给？", "具体公司和份额", "Vertiv、Schneider、Eaton 和数据中心工程/液冷供应商控制关键供给。当前 source pack 以 Vertiv orders/backlog 和 Dell'Oro 液冷预测为主，缺分项份额。", ["SRC-VRT-Q4-2025", "SRC-DO-LIQUID-COOLING-20260108"]),
      a("是否已经财务兑现？", "收入、毛利、订单、backlog、指引", "兑现很直接：Vertiv organic orders +252% YoY、backlog $15.0B。这个节点是 AI factory 物理瓶颈财务化最清楚的环节之一。", ["SRC-VRT-Q4-2025"]),
      a("市场是否已定价？", "估值、预期、盈利上修空间", "市场已开始识别电力/液冷，但相对 GPU 平台可能仍更容易出现预期差。下一步需要看 backlog 质量、项目毛利、现金转化和估值隐含增长。", ["SRC-VRT-Q4-2025"]),
      a("反证是什么？", "价格下跌、capex 下修、供给释放、客户延迟", "客户 capex 下修、电力接入延迟、项目毛利低于预期、backlog 取消或转收入慢、液冷渗透率低于预期。", ["SRC-VRT-Q4-2025", "SRC-DO-LIQUID-COOLING-20260108"]),
    ],
    "Cluster Operations / Scheduling / Observability / AI Cloud Service": [
      a("需求是否会大幅增长？", "它和 AI S 曲线的传导关系", "硬件上线后必须被调度、计费、监控和优化，才能变成可售卖算力服务。推理和企业 AI 扩散会提高运营层价值。", ["SRC-MSFT-FY26-Q2", "SRC-GOOGL-Q4-2025", "SRC-ORCL-FY26-Q2"]),
      a("单位用量是否会提升？", "每台服务器/每个机柜/每个 GPU 是否用更多", "单位硬件对应的软件和运营需求会提升：集群规模越大，调度、故障监控、能耗优化、成本归因和利用率管理越重要。", ["SRC-MSFT-FY26-Q2"]),
      a("供给能否跟上？", "产能、良率、认证、设备、材料、周期", "供给瓶颈主要是工程能力、云平台软件、客户 SLA、数据安全和运维经验，而不是传统制造产能。", ["SRC-GOOGL-Q4-2025"]),
      a("谁控制供给？", "具体公司和份额", "云厂商和 AI cloud 控制主要运营平台；第三方 MLOps/observability 生态可参与，但价值捕获需要另行验证。本页 source pack 不足以给份额。", ["SRC-MSFT-FY26-Q2", "SRC-ORCL-FY26-Q2"]),
      a("是否已经财务兑现？", "收入、毛利、订单、backlog、指引", "云收入和 RPO 已有验证，但还不能直接拆出 AI factory 运营软件利润。这个节点目前更适合验证 AI ROI，而不是直接下投资结论。", ["SRC-MSFT-FY26-Q2", "SRC-GOOGL-Q4-2025", "SRC-ORCL-FY26-Q2"]),
      a("市场是否已定价？", "估值、预期、盈利上修空间", "大型云厂商已被市场广泛跟踪；真正难点是区分 AI capex 带来的云收入增量和折旧/FCF 压力。", ["SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025"]),
      a("反证是什么？", "价格下跌、capex 下修、供给释放、客户延迟", "利用率不足、AI 服务价格下行、客户 ROI 不佳、折旧压力压低 FCF、RPO 不转收入。", ["SRC-AMZN-Q4-2025", "SRC-ORCL-FY26-Q2"]),
    ],
  };
  return (rows[nodeName] || [])
    .filter((row) => row.question !== "单位用量是否会提升？")
    .map((row) => {
      if (row.question !== "需求是否会大幅增长？") return row;
      return {
        ...row,
        question: "当前 BOM 的需求是否会被 S 曲线放大拉动？",
        prompt: "需求增长和单位用量弹性",
      };
    });
}

function nodeVerdict(nodeName) {
  const verdicts = {
    "云厂商 / AI labs / 企业与主权 AI": "需求验证层。它决定 S 曲线是否继续，但不是单一瓶颈资产；核心看 capex、RPO、云收入、FCF 和 AI ROI 是否同时成立。",
    "GPU / AI Accelerator / Custom ASIC": "当前最强平台层，需求和财务兑现最充分；但也最可能已被市场高预期定价，下一步重点是判断 ASIC 分流和隐含估值。",
    "先进制程 / CoWoS 类先进封装 / 基板": "硬供给层。制程和封装决定 AI accelerator 交付斜率；卡点强，但成熟龙头赔率要看 capex 回报和稀缺持续性。",
    "HBM / Server DRAM / Enterprise SSD": "最像从 GPU 约束迁移出来的下一层卡点。需求随平台升级放大，供给受资格、良率和扩产周期限制，财务兑现已经明显。",
    "Retimer / AEC / CXL-PCIe / 电源管理 / 板级组件": "高弹性但更细碎的连接/板级节点。真正机会取决于客户 design-in、attach rate 和平台替代风险。",
    "Switch / NIC / Optical Transceiver / PAM4 DSP / InfiniBand-Ethernet": "集群规模扩张的网络层。单位用量提升明确，但路线变化和 ASP 下行会影响利润质量。",
    "AI Server / Rack / Cluster Integration": "需求落地层。订单和 backlog 能验证 S 曲线，但玩家较多、客户议价强，必须用毛利和现金流过滤。",
    "Power / UPS / PDU / Liquid Cooling / Thermal / Facility": "物理落地层。高功率机柜倒逼电力和液冷，财务兑现清楚，是当前最值得继续深挖的非芯片卡点之一。",
    "Cluster Operations / Scheduling / Observability / AI Cloud Service": "运营验证层。它决定硬件投资能否产生 ROI，但本页证据不足以拆出独立利润池。",
  };
  return verdicts[nodeName] || "";
}

function a(question, prompt, answer, sources) {
  return { question, prompt, answer, sources };
}

function chip(id) {
  const item = sourceById[id];
  if (!item) return "";
  return `<a class="chip" href="${e(item.url)}" target="_blank" rel="noopener">${e(id)}</a>`;
}

function src(id, title, url, note) {
  return { id, title, url, note };
}

function e(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]));
}

function css() {
  return `
:root{--bg:#f6f7f9;--ink:#16181d;--muted:#667085;--line:#dce3ed;--panel:#fff;--blue:#0878d9;--green:#1d9a6c;--shadow:0 16px 45px rgba(32,44,68,.09)}
*{box-sizing:border-box}body{margin:0;background:linear-gradient(180deg,#fbfcff 0,#f2f5f9 45%,#f6f7f9 100%);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",sans-serif;line-height:1.68}a{color:var(--blue);text-decoration:none}a:hover{text-decoration:underline}
.hero{max-width:1180px;margin:0 auto;padding:48px clamp(20px,4vw,36px) 34px}.eyebrow{margin:0 0 10px;color:var(--blue);font-size:12px;font-weight:900;letter-spacing:.08em;text-transform:uppercase}h1{max-width:900px;margin:0;font-size:clamp(38px,5vw,72px);line-height:1.02;letter-spacing:0}.subtitle{max-width:760px;margin:18px 0 0;color:#475467;font-size:19px}
nav{position:sticky;top:0;z-index:3;display:flex;gap:10px;flex-wrap:wrap;justify-content:center;padding:12px;background:rgba(246,247,249,.82);backdrop-filter:blur(16px);border-block:1px solid rgba(220,227,237,.78)}nav a{padding:8px 12px;border:1px solid rgba(8,120,217,.16);border-radius:999px;background:#fff;color:#2c5474;font-size:13px}
.section{max-width:1180px;margin:0 auto;padding:34px clamp(20px,4vw,36px)}h2{margin:0 0 16px;font-size:clamp(28px,3vw,42px);letter-spacing:0}.section-lead{max-width:820px;margin:-6px 0 18px;color:#526173;font-size:16px}.summary-card,.bom-node,.flow-card,.use-grid article,.sources{border:1px solid var(--line);border-radius:22px;background:rgba(255,255,255,.92);box-shadow:var(--shadow)}.summary-card{padding:24px}.summary-card p{margin:0;font-size:20px;color:#26364f}.flow-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.flow-card{padding:18px;min-height:166px}.flow-card span{display:inline-flex;width:32px;height:32px;align-items:center;justify-content:center;border-radius:999px;background:#eaf4ff;color:var(--blue);font-weight:900}.flow-card h3{margin:12px 0 6px;font-size:19px}.flow-card p{margin:0;color:#4b5d73}.bom-stack{display:grid;gap:12px}.bom-node{overflow:hidden}.bom-node>summary{list-style:none;display:grid;grid-template-columns:auto 1fr auto;gap:14px;align-items:center;padding:18px 20px;cursor:pointer}.bom-node>summary::-webkit-details-marker{display:none}.bom-node[open]>summary{border-bottom:1px solid var(--line)}.bom-node summary>span{width:40px;height:40px;border-radius:999px;display:inline-flex;align-items:center;justify-content:center;background:#eef7ff;color:var(--blue);font-weight:900}.bom-node h3{margin:0;font-size:22px}.bom-node summary p{margin:2px 0 0;color:var(--muted);font-size:14px}.bom-node summary b{color:var(--blue);font-size:13px}.node-body{padding:18px 20px}.node-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.node-grid article{border:1px solid #e8eef6;border-radius:16px;background:#fbfcff;padding:14px}.node-grid span{display:block;margin-bottom:6px;color:var(--blue);font-size:12px;font-weight:900}.node-grid p{margin:0;color:#344054}.node-conclusion{margin:14px 0;border:1px solid rgba(8,120,217,.18);border-radius:16px;background:#f7fbff;padding:14px}.node-conclusion b{display:block;color:#123958;margin-bottom:4px}.node-conclusion p{margin:0;color:#344054}.analysis-wrap{max-width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;margin-top:14px}.analysis-table{width:100%;min-width:1050px;border-collapse:separate;border-spacing:0;border:1px solid #dfe8f4;border-radius:18px;overflow:hidden;background:#fff}.analysis-table th,.analysis-table td{padding:12px 14px;text-align:left;vertical-align:top;border-bottom:1px solid #eef2f7;font-size:13px}.analysis-table th{background:#f5f8fc;color:#475467;font-size:12px;font-weight:900}.analysis-table td:first-child{width:220px;color:#1f344d}.analysis-table td:first-child small{display:block;color:#8090a3;font-weight:500;line-height:1.45;margin-top:4px}.analysis-table td:nth-child(2){min-width:560px;color:#344054}.analysis-table td:nth-child(3){width:230px}.source-row{display:flex;flex-wrap:wrap;gap:6px;margin-top:14px}.chip{display:inline-flex;border:1px solid rgba(8,120,217,.2);border-radius:999px;background:#eef7ff;color:var(--blue);font-size:11px;padding:4px 9px}.table-scroll{max-width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch}.table-scroll table{width:100%;min-width:1080px;border-collapse:separate;border-spacing:0;border:1px solid var(--line);border-radius:20px;overflow:hidden;background:#fff;box-shadow:var(--shadow)}th,td{padding:12px 14px;text-align:left;vertical-align:top;border-bottom:1px solid #edf1f6;font-size:13px}th{background:#f5f8fc;color:#475467;font-size:12px;font-weight:900}.use-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.use-grid article{padding:18px}.use-grid span{display:block;color:var(--blue);font-weight:900;margin-bottom:8px}.use-grid p{margin:0;color:#344054}.sources{padding:16px}.sources summary{cursor:pointer;font-weight:900;color:#26364f}.source-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:14px}.source-grid a{display:block;border:1px solid #e8eef6;border-radius:16px;background:#fbfcff;padding:12px}.source-grid b{display:block;color:var(--blue);font-size:12px}.source-grid span{display:block;color:#24364d;font-weight:800}.source-grid small{display:block;color:var(--muted);margin-top:4px}
@media(max-width:860px){.flow-grid,.node-grid,.use-grid,.source-grid{grid-template-columns:1fr}.bom-node>summary{grid-template-columns:auto 1fr}.bom-node summary b{display:none}}
`;
}

main();
