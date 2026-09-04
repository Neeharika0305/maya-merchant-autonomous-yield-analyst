import { useState } from "react";
import {
  Activity,
  AlertTriangle,
  ArrowRight,
  Brain,
  CheckCircle2,
  ChevronRight,
  CircleDollarSign,
  FlaskConical,
  Gauge,
  Lightbulb,
  Lock,
  Play,
  RotateCcw,
  ShieldCheck,
  Sparkles,
  Target,
  TrendingUp,
  Users,
  XCircle,
  Zap,
} from "lucide-react";

const API_URL = "https://maya-api-j3kn.onrender.com/api/maya/run";

function formatCurrency(value) {
  const number = Number(value);
  if (!Number.isFinite(number)) return "₹0";

  return `₹${Math.round(number).toLocaleString("en-IN")}`;
}

function formatNumber(value) {
  const number = Number(value);
  if (!Number.isFinite(number)) return "0";

  return Math.round(number).toLocaleString("en-IN");
}

function formatPercent(value, digits = 1) {
  const number = Number(value);

  if (!Number.isFinite(number)) return "0.0%";

  return `${(number * 100).toFixed(digits)}%`;
}

function formatPoints(value, digits = 1) {
  const number = Number(value);

  if (!Number.isFinite(number)) return "0.0pp";

  return `${(number * 100).toFixed(digits)}pp`;
}

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const runMaya = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`MAYA API returned ${response.status}`);
      }

      const data = await response.json();

      setResult(data);
    } catch (err) {
      console.error(err);

      setError(
        "MAYA could not connect to the backend. Make sure FastAPI is running on port 5000."
      );
    } finally {
      setLoading(false);
    }
  };

  const resetDemo = () => {
    setResult(null);
    setError("");
  };

  /*
   * -----------------------------
   * SAFE DATA EXTRACTION
   * -----------------------------
   */

  const opportunity = result?.opportunity || {};
  const financial = result?.financial || {};
  const experiment = result?.experiment || {};
  const firstExperiment = result?.first_experiment || {};
  const recovery = result?.recovery_experiment || {};
  const diagnosis = result?.failure_diagnosis || {};
  const hypotheses = result?.challenged_hypotheses || [];
  const selected = result?.selected_hypothesis || {};
  const aiPipeline = result?.ai_pipeline || {};
  const aiRecommendation = aiPipeline?.recommendation || {};
  const guardrailValidation =
    aiPipeline?.validation || result?.guardrails || {};

  const aiSegment =
    aiRecommendation?.strongest_segment ||
    experiment?.ai_selected_segment ||
    "Repeat Buyer";

  const aiProduct =
    aiRecommendation?.strongest_product_signal ||
    "Smart Watch (P002)";

  const aiDiscount =
    Number(aiRecommendation?.discount) ||
    Number(experiment?.discount) ||
    8;

  const aiBudget =
    Number(aiRecommendation?.budget) ||
    Number(experiment?.budget) ||
    8000;

  const aiAudience =
    Number(aiRecommendation?.audience_size) ||
    Number(experiment?.eligible_customers) ||
    1013;

  const aiConfidence =
    Number(aiRecommendation?.confidence) ||
    Number(selected?.updated_confidence) * 100 ||
    88;

  const treatmentConversion =
    Number(firstExperiment?.treatment_conversion) || 0;

  const conversionLift =
    Number(firstExperiment?.conversion_lift) || 0;

  const recoveryTreatmentConversion =
    Number(recovery?.treatment_conversion) || 0;

  const recoveryConversionLift =
    Number(recovery?.conversion_lift) || 0;

  const incrementalRevenue =
    Number(financial?.incremental_revenue) || 0;

  const expectedRoi =
    Number(financial?.expected_roi) ||
    Number(experiment?.expected_roi) ||
    0;

  const finalStatus =
    result?.final_status ||
    (recovery?.success ? "RECOVERED" : "FAILED");

  const guardrailsApproved =
    guardrailValidation?.approved ??
    result?.guardrails?.approved ??
    true;

  const aiAvailable = aiPipeline?.ai_status === "AVAILABLE";

  const aiMode =
    aiPipeline?.fallback_mode ||
    aiPipeline?.decision === "FALLBACK"
      ? "DETERMINISTIC FALLBACK"
      : aiAvailable
        ? "GEMINI"
        : "MAYA ENGINE";

  const statusRecovered = finalStatus === "RECOVERED";

  /*
   * -----------------------------
   * COMPONENTS
   * -----------------------------
   */

  const MetricCard = ({
    icon: Icon,
    label,
    value,
    subtext,
    highlight = false,
  }) => (
    <div className={`metric-card ${highlight ? "metric-highlight" : ""}`}>
      <div className="metric-icon">
        <Icon size={20} />
      </div>

      <div className="metric-content">
        <div className="metric-label">{label}</div>
        <div className="metric-value">{value}</div>

        {subtext && <div className="metric-subtext">{subtext}</div>}
      </div>
    </div>
  );

  const SectionHeader = ({ icon: Icon, title, subtitle }) => (
    <div className="section-header">
      <div className="section-title-row">
        <div className="section-icon">
          <Icon size={18} />
        </div>

        <div>
          <h2>{title}</h2>
          {subtitle && <p>{subtitle}</p>}
        </div>
      </div>
    </div>
  );

  const Pill = ({ children, type = "default" }) => (
    <span className={`pill pill-${type}`}>{children}</span>
  );

  const TimelineStep = ({
    number,
    icon: Icon,
    title,
    status,
    description,
    children,
    active = false,
    failed = false,
    success = false,
  }) => (
    <div className="timeline-row">
      <div
        className={`timeline-marker ${
          active ? "timeline-active" : ""
        } ${failed ? "timeline-failed" : ""} ${
          success ? "timeline-success" : ""
        }`}
      >
        {success ? (
          <CheckCircle2 size={18} />
        ) : failed ? (
          <XCircle size={18} />
        ) : (
          <Icon size={18} />
        )}
      </div>

      <div className="timeline-card">
        <div className="timeline-card-top">
          <div>
            <div className="timeline-step">
              STEP {String(number).padStart(2, "0")}
            </div>

            <h3>{title}</h3>
          </div>

          {status && (
            <Pill
              type={
                success
                  ? "success"
                  : failed
                    ? "danger"
                    : active
                      ? "active"
                      : "default"
              }
            >
              {status}
            </Pill>
          )}
        </div>

        {description && (
          <p className="timeline-description">{description}</p>
        )}

        {children && <div className="timeline-data">{children}</div>}
      </div>
    </div>
  );

  /*
   * -----------------------------
   * RENDER
   * -----------------------------
   */

  return (
    <div className="app-shell">
      <style>{`
        * {
          box-sizing: border-box;
        }

        body {
          margin: 0;
          font-family:
            Inter,
            ui-sans-serif,
            system-ui,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
          background: #070b12;
          color: #f3f6fb;
        }

        button {
          font-family: inherit;
        }

        .app-shell {
          min-height: 100vh;
          background:
            radial-gradient(
              circle at 80% 0%,
              rgba(99, 102, 241, 0.12),
              transparent 30%
            ),
            radial-gradient(
              circle at 0% 30%,
              rgba(14, 165, 233, 0.08),
              transparent 30%
            ),
            #070b12;
        }

        .topbar {
          height: 72px;
          border-bottom: 1px solid rgba(255,255,255,0.08);
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0 34px;
          background: rgba(7,11,18,0.88);
          backdrop-filter: blur(16px);
          position: sticky;
          top: 0;
          z-index: 10;
        }

        .brand {
          display: flex;
          align-items: center;
          gap: 13px;
        }

        .brand-logo {
          width: 38px;
          height: 38px;
          border-radius: 11px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: linear-gradient(135deg,#7c3aed,#2563eb);
          box-shadow: 0 0 30px rgba(99,102,241,0.25);
        }

        .brand-name {
          font-size: 20px;
          font-weight: 800;
          letter-spacing: -0.5px;
        }

        .brand-subtitle {
          font-size: 11px;
          color: #7e8a9e;
          margin-top: 2px;
          letter-spacing: 0.4px;
        }

        .topbar-right {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .system-status {
          display: flex;
          align-items: center;
          gap: 7px;
          color: #aeb9c9;
          font-size: 12px;
          padding: 8px 12px;
          border: 1px solid rgba(255,255,255,0.07);
          border-radius: 9px;
          background: rgba(255,255,255,0.025);
        }

        .status-dot {
          width: 7px;
          height: 7px;
          border-radius: 50%;
          background: #22c55e;
          box-shadow: 0 0 10px rgba(34,197,94,0.6);
        }

        .main {
          max-width: 1450px;
          margin: 0 auto;
          padding: 34px;
        }

        .hero {
          display: grid;
          grid-template-columns: 1fr auto;
          gap: 30px;
          align-items: center;
          margin-bottom: 30px;
        }

        .eyebrow {
          color: #8b9bb2;
          font-size: 12px;
          text-transform: uppercase;
          letter-spacing: 1.8px;
          font-weight: 700;
          margin-bottom: 10px;
        }

        .hero h1 {
          font-size: clamp(32px, 5vw, 58px);
          line-height: 1;
          margin: 0;
          letter-spacing: -2.8px;
        }

        .hero h1 span {
          background: linear-gradient(90deg,#a78bfa,#60a5fa);
          -webkit-background-clip: text;
          color: transparent;
        }

        .hero-description {
          max-width: 730px;
          color: #8995a8;
          line-height: 1.65;
          font-size: 15px;
          margin: 17px 0 0;
        }

        .hero-actions {
          display: flex;
          flex-direction: column;
          align-items: flex-end;
          gap: 10px;
        }

        .run-button {
          border: 0;
          color: white;
          background: linear-gradient(135deg,#7c3aed,#2563eb);
          padding: 15px 23px;
          border-radius: 12px;
          font-size: 14px;
          font-weight: 750;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 9px;
          box-shadow: 0 10px 35px rgba(79,70,229,0.25);
          transition: 0.2s ease;
        }

        .run-button:hover {
          transform: translateY(-1px);
          box-shadow: 0 14px 40px rgba(79,70,229,0.35);
        }

        .run-button:disabled {
          opacity: 0.65;
          cursor: wait;
          transform: none;
        }

        .reset-button {
          border: 1px solid rgba(255,255,255,0.1);
          color: #9ca8ba;
          background: transparent;
          padding: 9px 13px;
          border-radius: 9px;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 7px;
          font-size: 12px;
        }

        .error-box {
          display: flex;
          align-items: center;
          gap: 12px;
          border: 1px solid rgba(239,68,68,0.25);
          background: rgba(239,68,68,0.07);
          color: #fca5a5;
          padding: 14px 16px;
          border-radius: 11px;
          margin-bottom: 22px;
          font-size: 13px;
        }

        .metrics-grid {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 13px;
          margin-bottom: 32px;
        }

        .metric-card {
          min-height: 125px;
          border: 1px solid rgba(255,255,255,0.07);
          border-radius: 15px;
          background: rgba(255,255,255,0.025);
          padding: 20px;
          display: flex;
          gap: 15px;
        }

        .metric-highlight {
          border-color: rgba(99,102,241,0.28);
          background: linear-gradient(
            135deg,
            rgba(99,102,241,0.10),
            rgba(255,255,255,0.025)
          );
        }

        .metric-icon {
          width: 38px;
          height: 38px;
          border-radius: 10px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: rgba(124,58,237,0.12);
          color: #a78bfa;
          flex-shrink: 0;
        }

        .metric-label {
          font-size: 10px;
          letter-spacing: 1.1px;
          color: #78859a;
          font-weight: 750;
          text-transform: uppercase;
        }

        .metric-value {
          font-size: 27px;
          font-weight: 800;
          letter-spacing: -1px;
          margin-top: 6px;
        }

        .metric-subtext {
          color: #687589;
          font-size: 11px;
          margin-top: 5px;
        }

        .content-grid {
          display: grid;
          grid-template-columns: minmax(0, 1.45fr) minmax(320px, 0.75fr);
          gap: 18px;
        }

        .panel {
          border: 1px solid rgba(255,255,255,0.07);
          border-radius: 16px;
          background: rgba(255,255,255,0.025);
          overflow: hidden;
        }

        .panel + .panel {
          margin-top: 18px;
        }

        .section-header {
          padding: 21px 22px;
          border-bottom: 1px solid rgba(255,255,255,0.06);
        }

        .section-title-row {
          display: flex;
          gap: 12px;
          align-items: center;
        }

        .section-icon {
          width: 34px;
          height: 34px;
          border-radius: 9px;
          background: rgba(124,58,237,0.12);
          color: #a78bfa;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .section-header h2 {
          font-size: 14px;
          margin: 0;
          font-weight: 800;
        }

        .section-header p {
          color: #687589;
          font-size: 11px;
          margin: 4px 0 0;
        }

        .panel-body {
          padding: 21px;
        }

        .opportunity-card {
          border: 1px solid rgba(99,102,241,0.18);
          background: rgba(99,102,241,0.055);
          border-radius: 13px;
          padding: 19px;
        }

        .opportunity-top {
          display: flex;
          justify-content: space-between;
          gap: 15px;
          align-items: flex-start;
        }

        .opportunity-title {
          font-size: 18px;
          font-weight: 800;
          letter-spacing: -0.4px;
          margin: 0 0 7px;
        }

        .opportunity-text {
          color: #8995a8;
          font-size: 13px;
          line-height: 1.55;
          margin: 0;
        }

        .pill {
          display: inline-flex;
          align-items: center;
          white-space: nowrap;
          border-radius: 999px;
          padding: 5px 9px;
          font-size: 9px;
          font-weight: 800;
          letter-spacing: 0.7px;
          text-transform: uppercase;
          border: 1px solid rgba(255,255,255,0.09);
          color: #aeb9c9;
          background: rgba(255,255,255,0.035);
        }

        .pill-success {
          color: #86efac;
          border-color: rgba(34,197,94,0.2);
          background: rgba(34,197,94,0.08);
        }

        .pill-danger {
          color: #fca5a5;
          border-color: rgba(239,68,68,0.2);
          background: rgba(239,68,68,0.08);
        }

        .pill-active {
          color: #93c5fd;
          border-color: rgba(59,130,246,0.2);
          background: rgba(59,130,246,0.08);
        }

        .opportunity-stats {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 9px;
          margin-top: 18px;
        }

        .mini-stat {
          padding: 12px;
          border-radius: 10px;
          background: rgba(0,0,0,0.16);
        }

        .mini-stat-label {
          color: #687589;
          font-size: 9px;
          text-transform: uppercase;
          letter-spacing: 0.7px;
        }

        .mini-stat-value {
          font-size: 16px;
          font-weight: 750;
          margin-top: 4px;
        }

        .hypothesis-list {
          display: flex;
          flex-direction: column;
          gap: 9px;
        }

        .hypothesis {
          display: grid;
          grid-template-columns: 34px 1fr auto;
          align-items: center;
          gap: 11px;
          padding: 13px;
          border: 1px solid rgba(255,255,255,0.06);
          border-radius: 10px;
          background: rgba(255,255,255,0.018);
        }

        .hypothesis-selected {
          border-color: rgba(124,58,237,0.28);
          background: rgba(124,58,237,0.07);
        }

        .hypothesis-rank {
          width: 30px;
          height: 30px;
          border-radius: 8px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: rgba(255,255,255,0.05);
          color: #98a5b8;
          font-weight: 800;
          font-size: 12px;
        }

        .hypothesis-name {
          font-size: 13px;
          font-weight: 750;
        }

        .hypothesis-score {
          color: #a78bfa;
          font-size: 12px;
          font-weight: 800;
        }

        .ai-card {
          background:
            linear-gradient(
              145deg,
              rgba(124,58,237,0.11),
              rgba(37,99,235,0.055)
            );
          border: 1px solid rgba(124,58,237,0.20);
          border-radius: 13px;
          padding: 18px;
        }

        .ai-card-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 17px;
        }

        .ai-title {
          display: flex;
          align-items: center;
          gap: 9px;
          font-size: 13px;
          font-weight: 800;
        }

        .ai-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 10px;
        }

        .ai-field {
          padding: 12px;
          background: rgba(0,0,0,0.16);
          border-radius: 9px;
        }

        .ai-field-label {
          color: #69768a;
          font-size: 9px;
          text-transform: uppercase;
          letter-spacing: 0.7px;
          margin-bottom: 5px;
        }

        .ai-field-value {
          color: #dce3ed;
          font-size: 12px;
          font-weight: 700;
          line-height: 1.35;
        }

        .ai-confidence {
          margin-top: 12px;
          padding: 13px;
          border-radius: 10px;
          background: rgba(0,0,0,0.16);
        }

        .confidence-row {
          display: flex;
          justify-content: space-between;
          font-size: 11px;
          color: #8490a3;
          margin-bottom: 8px;
        }

        .confidence-row strong {
          color: #c4b5fd;
        }

        .progress {
          height: 5px;
          border-radius: 99px;
          background: rgba(255,255,255,0.07);
          overflow: hidden;
        }

        .progress-fill {
          height: 100%;
          border-radius: inherit;
          background: linear-gradient(90deg,#7c3aed,#3b82f6);
        }

        .experiment-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 10px;
        }

        .experiment-field {
          padding: 13px;
          border: 1px solid rgba(255,255,255,0.06);
          border-radius: 10px;
        }

        .experiment-field-label {
          color: #687589;
          font-size: 9px;
          text-transform: uppercase;
          letter-spacing: 0.7px;
        }

        .experiment-field-value {
          margin-top: 6px;
          font-size: 13px;
          font-weight: 750;
        }

        .guardrail-list {
          display: flex;
          flex-direction: column;
          gap: 9px;
        }

        .guardrail {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 12px 13px;
          border-radius: 10px;
          background: rgba(255,255,255,0.02);
          border: 1px solid rgba(255,255,255,0.06);
        }

        .guardrail-left {
          display: flex;
          align-items: center;
          gap: 9px;
          color: #aeb9c9;
          font-size: 12px;
        }

        .guardrail-right {
          color: #86efac;
          font-size: 11px;
          font-weight: 750;
        }

        .financial-box {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 10px;
        }

        .financial-main {
          padding: 17px;
          border-radius: 11px;
          background: rgba(34,197,94,0.06);
          border: 1px solid rgba(34,197,94,0.13);
        }

        .financial-main .label {
          color: #6f8477;
          font-size: 9px;
          text-transform: uppercase;
          letter-spacing: 0.7px;
        }

        .financial-main .value {
          margin-top: 6px;
          font-size: 23px;
          font-weight: 800;
          color: #bbf7d0;
        }

        .timeline {
          position: relative;
          padding: 21px;
        }

        .timeline-row {
          position: relative;
          display: grid;
          grid-template-columns: 40px 1fr;
          gap: 13px;
        }

        .timeline-row:not(:last-child)::after {
          content: "";
          position: absolute;
          width: 1px;
          background: rgba(255,255,255,0.08);
          left: 19px;
          top: 40px;
          bottom: -15px;
        }

        .timeline-marker {
          width: 40px;
          height: 40px;
          border-radius: 11px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: rgba(255,255,255,0.045);
          color: #8d99ac;
          border: 1px solid rgba(255,255,255,0.07);
          z-index: 1;
        }

        .timeline-active {
          color: #a78bfa;
          border-color: rgba(124,58,237,0.25);
          background: rgba(124,58,237,0.10);
        }

        .timeline-failed {
          color: #f87171;
          border-color: rgba(239,68,68,0.22);
          background: rgba(239,68,68,0.08);
        }

        .timeline-success {
          color: #4ade80;
          border-color: rgba(34,197,94,0.22);
          background: rgba(34,197,94,0.08);
        }

        .timeline-card {
          margin-bottom: 16px;
          padding: 16px;
          border: 1px solid rgba(255,255,255,0.06);
          border-radius: 12px;
          background: rgba(255,255,255,0.018);
        }

        .timeline-card-top {
          display: flex;
          justify-content: space-between;
          gap: 15px;
          align-items: flex-start;
        }

        .timeline-step {
          color: #687589;
          font-size: 9px;
          font-weight: 800;
          letter-spacing: 1px;
        }

        .timeline-card h3 {
          font-size: 14px;
          margin: 4px 0 0;
        }

        .timeline-description {
          color: #7f8b9e;
          font-size: 12px;
          line-height: 1.55;
          margin: 9px 0 0;
        }

        .timeline-data {
          display: flex;
          gap: 9px;
          flex-wrap: wrap;
          margin-top: 12px;
        }

        .data-chip {
          border-radius: 8px;
          background: rgba(0,0,0,0.18);
          padding: 8px 10px;
          color: #aeb9c9;
          font-size: 10px;
        }

        .data-chip strong {
          color: #f0f3f8;
          font-size: 11px;
        }

        .status-banner {
          margin-top: 18px;
          padding: 18px;
          border-radius: 13px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 15px;
          border: 1px solid rgba(34,197,94,0.20);
          background: rgba(34,197,94,0.07);
        }

        .status-banner-left {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .status-banner-icon {
          width: 38px;
          height: 38px;
          border-radius: 10px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: rgba(34,197,94,0.11);
          color: #4ade80;
        }

        .status-banner h3 {
          margin: 0;
          font-size: 14px;
        }

        .status-banner p {
          margin: 4px 0 0;
          color: #779080;
          font-size: 11px;
        }

        .status-large {
          color: #86efac;
          font-weight: 850;
          font-size: 13px;
          letter-spacing: 0.8px;
        }

        .empty-state {
          min-height: 400px;
          display: flex;
          align-items: center;
          justify-content: center;
          text-align: center;
          padding: 50px 30px;
        }

        .empty-icon {
          width: 65px;
          height: 65px;
          border-radius: 18px;
          margin: 0 auto 18px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: rgba(124,58,237,0.10);
          color: #a78bfa;
        }

        .empty-state h2 {
          margin: 0;
          font-size: 21px;
        }

        .empty-state p {
          max-width: 500px;
          color: #748196;
          font-size: 13px;
          line-height: 1.6;
          margin: 10px auto 0;
        }

        .spinner {
          animation: spin 0.9s linear infinite;
        }

        @keyframes spin {
          to {
            transform: rotate(360deg);
          }
        }

        @media (max-width: 1050px) {
          .metrics-grid {
            grid-template-columns: repeat(2, 1fr);
          }

          .content-grid {
            grid-template-columns: 1fr;
          }

          .hero {
            grid-template-columns: 1fr;
          }

          .hero-actions {
            align-items: flex-start;
          }
        }

        @media (max-width: 650px) {
          .topbar {
            padding: 0 16px;
          }

          .main {
            padding: 20px 14px;
          }

          .metrics-grid {
            grid-template-columns: 1fr;
          }

          .opportunity-stats,
          .ai-grid,
          .experiment-grid,
          .financial-box {
            grid-template-columns: 1fr;
          }

          .hero h1 {
            font-size: 38px;
          }
        }
      `}</style>

      {/* HEADER */}

      <header className="topbar">
        <div className="brand">
          <div className="brand-logo">
            <Brain size={21} />
          </div>

          <div>
            <div className="brand-name">MAYA</div>
            <div className="brand-subtitle">
              MERCHANT AUTONOMOUS YIELD ANALYST
            </div>
          </div>
        </div>

        <div className="topbar-right">
          <div className="system-status">
            <span className="status-dot" />
            Autonomous Engine Online
          </div>
        </div>
      </header>

      <main className="main">
        {/* HERO */}

        <section className="hero">
          <div>
            <div className="eyebrow">
              AI Growth & Agentic Commerce
            </div>

            <h1>
              Let AI discover.
              <br />
              <span>Test. Prove. Adapt.</span>
            </h1>

            <p className="hero-description">
              MAYA continuously searches merchant data for hidden growth
              opportunities, challenges its own assumptions, designs
              financially safe experiments, and adapts when experiments fail.
            </p>
          </div>

          <div className="hero-actions">
            <button
              className="run-button"
              onClick={runMaya}
              disabled={loading}
            >
              {loading ? (
                <>
                  <Activity size={18} className="spinner" />
                  MAYA IS THINKING...
                </>
              ) : (
                <>
                  <Play size={18} />
                  RUN MAYA
                </>
              )}
            </button>

            {result && (
              <button className="reset-button" onClick={resetDemo}>
                <RotateCcw size={13} />
                Reset Demo
              </button>
            )}
          </div>
        </section>

        {/* ERROR */}

        {error && (
          <div className="error-box">
            <AlertTriangle size={18} />
            <span>{error}</span>
          </div>
        )}

        {/* EMPTY STATE */}

        {!result && !loading && (
          <div className="panel">
            <div className="empty-state">
              <div>
                <div className="empty-icon">
                  <Sparkles size={29} />
                </div>

                <h2>MAYA is ready.</h2>

                <p>
                  Run the autonomous growth engine to discover a merchant
                  opportunity, challenge the strongest hypothesis, design a
                  guarded experiment, simulate failure, and recover.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* LOADING */}

        {loading && (
          <div className="panel">
            <div className="empty-state">
              <div>
                <div className="empty-icon">
                  <Activity size={29} className="spinner" />
                </div>

                <h2>MAYA is executing the loop.</h2>

                <p>
                  Discovering opportunities → challenging hypotheses →
                  validating economics → testing → adapting.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* RESULTS */}

        {result && !loading && (
          <>
            {/* TOP METRICS */}

            <div className="metrics-grid">
              <MetricCard
                icon={CircleDollarSign}
                label="Incremental Revenue"
                value={formatCurrency(incrementalRevenue)}
                subtext="Expected experiment impact"
                highlight
              />

              <MetricCard
                icon={Brain}
                label="MAYA Confidence"
                value={`${Math.round(aiConfidence)}%`}
                subtext={aiMode}
              />

              <MetricCard
                icon={TrendingUp}
                label="Expected ROI"
                value={`${expectedRoi.toFixed(2)}×`}
                subtext="Revenue / experiment cost"
                highlight
              />

              <MetricCard
                icon={Gauge}
                label="Final Status"
                value={finalStatus}
                subtext={
                  statusRecovered
                    ? "Failure recovered"
                    : "Execution completed"
                }
              />
            </div>

            <div className="content-grid">
              {/* LEFT */}

              <div>
                {/* DISCOVERY */}

                <div className="panel">
                  <SectionHeader
                    icon={Lightbulb}
                    title="Opportunity Discovery"
                    subtitle="MAYA scans verified merchant behavior for non-obvious growth signals."
                  />

                  <div className="panel-body">
                    <div className="opportunity-card">
                      <div className="opportunity-top">
                        <div>
                          <h3 className="opportunity-title">
                            {opportunity.title ||
                              "Earbud → USB-C Cable Cross-Sell Opportunity"}
                          </h3>

                          <p className="opportunity-text">
                            {opportunity.description ||
                              "MAYA identified a cross-sell relationship between high-volume products."}
                          </p>
                        </div>

                        <Pill type="success">
                          {opportunity.status || "DISCOVERED"}
                        </Pill>
                      </div>

                      <div className="opportunity-stats">
                        <div className="mini-stat">
                          <div className="mini-stat-label">
                            Earbud Buyers
                          </div>
                          <div className="mini-stat-value">
                            {formatNumber(
                              opportunity.earbud_buyers || 2848
                            )}
                          </div>
                        </div>

                        <div className="mini-stat">
                          <div className="mini-stat-label">
                            Affinity
                          </div>
                          <div className="mini-stat-value">
                            {Number(
                              opportunity.overall_affinity || 41.78
                            ).toFixed(1)}
                            %
                          </div>
                        </div>

                        <div className="mini-stat">
                          <div className="mini-stat-label">
                            Repeat Buyer
                          </div>
                          <div className="mini-stat-value">
                            {Number(
                              opportunity.repeat_buyer_affinity || 53.96
                            ).toFixed(1)}
                            %
                          </div>
                        </div>

                        <div className="mini-stat">
                          <div className="mini-stat-label">
                            Confidence
                          </div>
                          <div className="mini-stat-value">
                            {Number(
                              opportunity.confidence || 82
                            ).toFixed(0)}
                            %
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* CHALLENGE */}

                <div className="panel">
                  <SectionHeader
                    icon={Target}
                    title="Hypothesis Challenge"
                    subtitle="MAYA does not blindly accept the first explanation."
                  />

                  <div className="panel-body">
                    <div className="hypothesis-list">
                      {hypotheses.length > 0 ? (
                        hypotheses.map((hypothesis, index) => {
                          const isSelected =
                            index === 0 ||
                            hypothesis === selected;

                          const score =
                            Number(
                              hypothesis.challenge_score ??
                                hypothesis.updated_confidence ??
                                hypothesis.score ??
                                0
                            );

                          return (
                            <div
                              key={index}
                              className={`hypothesis ${
                                isSelected
                                  ? "hypothesis-selected"
                                  : ""
                              }`}
                            >
                              <div className="hypothesis-rank">
                                {index + 1}
                              </div>

                              <div>
                                <div className="hypothesis-name">
                                  {hypothesis.name ||
                                    hypothesis.hypothesis ||
                                    `Hypothesis ${index + 1}`}
                                </div>

                                {hypothesis.reasoning && (
                                  <div
                                    style={{
                                      color: "#6f7c90",
                                      fontSize: "10px",
                                      marginTop: "3px",
                                    }}
                                  >
                                    {hypothesis.reasoning}
                                  </div>
                                )}
                              </div>

                              <div className="hypothesis-score">
                                {score <= 1
                                  ? `${(score * 100).toFixed(0)}%`
                                  : `${score.toFixed(0)}%`}
                              </div>
                            </div>
                          );
                        })
                      ) : (
                        <div className="hypothesis">
                          <div className="hypothesis-rank">1</div>
                          <div>
                            <div className="hypothesis-name">
                              High-Intent Segment
                            </div>
                          </div>
                          <div className="hypothesis-score">
                            88%
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                {/* AI DECISION */}

                <div className="panel">
                  <SectionHeader
                    icon={Brain}
                    title="MAYA Decision"
                    subtitle="Controlled AI recommendation with deterministic safety fallback."
                  />

                  <div className="panel-body">
                    <div className="ai-card">
                      <div className="ai-card-header">
                        <div className="ai-title">
                          <Sparkles size={16} />
                          Autonomous Growth Decision
                        </div>

                        <Pill
                          type={
                            guardrailsApproved
                              ? "success"
                              : "danger"
                          }
                        >
                          {guardrailsApproved
                            ? "APPROVED"
                            : "REJECTED"}
                        </Pill>
                      </div>

                      <div className="ai-grid">
                        <div className="ai-field">
                          <div className="ai-field-label">
                            Target Segment
                          </div>
                          <div className="ai-field-value">
                            {aiSegment}
                          </div>
                        </div>

                        <div className="ai-field">
                          <div className="ai-field-label">
                            Product Signal
                          </div>
                          <div className="ai-field-value">
                            {aiProduct}
                          </div>
                        </div>

                        <div className="ai-field">
                          <div className="ai-field-label">
                            Incentive
                          </div>
                          <div className="ai-field-value">
                            {aiDiscount}% discount
                          </div>
                        </div>

                        <div className="ai-field">
                          <div className="ai-field-label">
                            Experiment Budget
                          </div>
                          <div className="ai-field-value">
                            {formatCurrency(aiBudget)}
                          </div>
                        </div>

                        <div className="ai-field">
                          <div className="ai-field-label">
                            Audience
                          </div>
                          <div className="ai-field-value">
                            {formatNumber(aiAudience)} customers
                          </div>
                        </div>

                        <div className="ai-field">
                          <div className="ai-field-label">
                            Decision Mode
                          </div>
                          <div className="ai-field-value">
                            {aiMode}
                          </div>
                        </div>
                      </div>

                      <div className="ai-confidence">
                        <div className="confidence-row">
                          <span>MAYA confidence</span>
                          <strong>
                            {Math.round(aiConfidence)}%
                          </strong>
                        </div>

                        <div className="progress">
                          <div
                            className="progress-fill"
                            style={{
                              width: `${Math.min(
                                100,
                                Math.max(0, aiConfidence)
                              )}%`,
                            }}
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* EXPERIMENT */}

                <div className="panel">
                  <SectionHeader
                    icon={FlaskConical}
                    title="Experiment Design"
                    subtitle="The recommendation becomes a bounded, measurable experiment."
                  />

                  <div className="panel-body">
                    <div className="experiment-grid">
                      <div className="experiment-field">
                        <div className="experiment-field-label">
                          Experiment
                        </div>

                        <div className="experiment-field-value">
                          {experiment.experiment_name ||
                            "AI-Selected Repeat Buyer Cross-Sell Experiment"}
                        </div>
                      </div>

                      <div className="experiment-field">
                        <div className="experiment-field-label">
                          Target
                        </div>

                        <div className="experiment-field-value">
                          {experiment.target || aiSegment}
                        </div>
                      </div>

                      <div className="experiment-field">
                        <div className="experiment-field-label">
                          Audience
                        </div>

                        <div className="experiment-field-value">
                          {formatNumber(
                            experiment.eligible_customers ||
                              aiAudience
                          )}
                        </div>
                      </div>

                      <div className="experiment-field">
                        <div className="experiment-field-label">
                          Offer
                        </div>

                        <div className="experiment-field-value">
                          {experiment.offer ||
                            `${aiDiscount}% targeted incentive`}
                        </div>
                      </div>

                      <div className="experiment-field">
                        <div className="experiment-field-label">
                          Duration
                        </div>

                        <div className="experiment-field-value">
                          {experiment.duration_days || 7} days
                        </div>
                      </div>

                      <div className="experiment-field">
                        <div className="experiment-field-label">
                          Success Metric
                        </div>

                        <div className="experiment-field-value">
                          {experiment.success_metric ||
                            "Treatment conversion lift"}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* FINANCIAL */}

                <div className="panel">
                  <SectionHeader
                    icon={CircleDollarSign}
                    title="Economic Validation"
                    subtitle="MAYA evaluates whether the experiment is worth running."
                  />

                  <div className="panel-body">
                    <div className="financial-box">
                      <div className="financial-main">
                        <div className="label">
                          Incremental Revenue
                        </div>

                        <div className="value">
                          {formatCurrency(incrementalRevenue)}
                        </div>
                      </div>

                      <div className="financial-main">
                        <div className="label">
                          Expected ROI
                        </div>

                        <div className="value">
                          {expectedRoi.toFixed(2)}×
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* RIGHT */}

              <div>
                {/* GUARDRAILS */}

                <div className="panel">
                  <SectionHeader
                    icon={ShieldCheck}
                    title="Guardrails"
                    subtitle="MAYA cannot exceed predefined experiment limits."
                  />

                  <div className="panel-body">
                    <div className="guardrail-list">
                      <div className="guardrail">
                        <div className="guardrail-left">
                          <Lock size={14} />
                          Budget
                        </div>

                        <div className="guardrail-right">
                          {formatCurrency(aiBudget)} / ₹10,000
                        </div>
                      </div>

                      <div className="guardrail">
                        <div className="guardrail-left">
                          <Lock size={14} />
                          Discount
                        </div>

                        <div className="guardrail-right">
                          {aiDiscount}% / 10%
                        </div>
                      </div>

                      <div className="guardrail">
                        <div className="guardrail-left">
                          <Lock size={14} />
                          Audience
                        </div>

                        <div className="guardrail-right">
                          {formatNumber(aiAudience)} / 1,500
                        </div>
                      </div>

                      <div className="guardrail">
                        <div className="guardrail-left">
                          <ShieldCheck size={14} />
                          Validation
                        </div>

                        <div className="guardrail-right">
                          {guardrailsApproved
                            ? "APPROVED"
                            : "BLOCKED"}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* AGENT LOOP */}

                <div className="panel">
                  <SectionHeader
                    icon={Zap}
                    title="Autonomous Loop"
                    subtitle="The complete MAYA decision cycle."
                  />

                  <div className="panel-body">
                    <div
                      style={{
                        display: "flex",
                        flexDirection: "column",
                        gap: "11px",
                      }}
                    >
                      {[
                        ["DISCOVER", "Find hidden opportunity"],
                        ["HYPOTHESIZE", "Generate explanations"],
                        ["CHALLENGE", "Rank evidence"],
                        ["EXPERIMENT", "Test safely"],
                        ["MEASURE", "Observe outcome"],
                        ["ADAPT", "Recover and learn"],
                      ].map(([title, description], index) => (
                        <div
                          key={title}
                          style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "11px",
                          }}
                        >
                          <div
                            style={{
                              width: 28,
                              height: 28,
                              borderRadius: 8,
                              background:
                                index === 5 &&
                                statusRecovered
                                  ? "rgba(34,197,94,0.10)"
                                  : "rgba(124,58,237,0.09)",
                              color:
                                index === 5 &&
                                statusRecovered
                                  ? "#4ade80"
                                  : "#a78bfa",
                              display: "flex",
                              alignItems: "center",
                              justifyContent: "center",
                              fontSize: 9,
                              fontWeight: 800,
                            }}
                          >
                            {index + 1}
                          </div>

                          <div>
                            <div
                              style={{
                                fontSize: 11,
                                fontWeight: 800,
                              }}
                            >
                              {title}
                            </div>

                            <div
                              style={{
                                fontSize: 9,
                                color: "#687589",
                                marginTop: 2,
                              }}
                            >
                              {description}
                            </div>
                          </div>

                          {index < 5 && (
                            <ArrowRight
                              size={12}
                              style={{
                                marginLeft: "auto",
                                color: "#3f4b5d",
                              }}
                            />
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* FAILURE DIAGNOSIS */}

                <div className="panel">
                  <SectionHeader
                    icon={AlertTriangle}
                    title="Failure Diagnosis"
                    subtitle="MAYA analyzes why the first experiment failed."
                  />

                  <div className="panel-body">
                    <div
                      style={{
                        padding: 15,
                        borderRadius: 11,
                        border:
                          "1px solid rgba(239,68,68,0.14)",
                        background:
                          "rgba(239,68,68,0.045)",
                      }}
                    >
                      <div
                        style={{
                          display: "flex",
                          alignItems: "center",
                          gap: 8,
                          color: "#fca5a5",
                          fontSize: 11,
                          fontWeight: 800,
                          marginBottom: 8,
                        }}
                      >
                        <XCircle size={14} />
                        FIRST EXPERIMENT FAILED
                      </div>

                      <p
                        style={{
                          color: "#8995a8",
                          fontSize: 11,
                          lineHeight: 1.6,
                          margin: 0,
                        }}
                      >
                        {diagnosis.reason ||
                          diagnosis.failure_reason ||
                          firstExperiment.failure_reason ||
                          "The first treatment did not meet the required conversion threshold."}
                      </p>
                    </div>
                  </div>
                </div>

                {/* RECOVERY */}

                <div className="panel">
                  <SectionHeader
                    icon={RotateCcw}
                    title="Adaptive Recovery"
                    subtitle="MAYA changes the experiment instead of repeating the same mistake."
                  />

                  <div className="panel-body">
                    <div
                      style={{
                        padding: 15,
                        borderRadius: 11,
                        border:
                          "1px solid rgba(34,197,94,0.16)",
                        background:
                          "rgba(34,197,94,0.045)",
                      }}
                    >
                      <div
                        style={{
                          display: "flex",
                          alignItems: "center",
                          gap: 8,
                          color: "#86efac",
                          fontSize: 11,
                          fontWeight: 800,
                        }}
                      >
                        <CheckCircle2 size={14} />
                        RECOVERY EXPERIMENT
                      </div>

                      <div
                        style={{
                          marginTop: 13,
                          display: "grid",
                          gridTemplateColumns: "1fr 1fr",
                          gap: 9,
                        }}
                      >
                        <div className="data-chip">
                          Recovery Audience
                          <br />
                          <strong>
                            {formatNumber(
                              recovery?.recovery_audience_size || 608
                            )}
                          </strong>
                        </div>

                        <div className="data-chip">
                          Treatment Conversion
                          <br />
                          <strong>
                            {formatPercent(
                              recoveryTreatmentConversion
                            )}
                          </strong>
                        </div>

                        <div className="data-chip">
                          Conversion Lift
                          <br />
                          <strong>
                            +
                            {formatPoints(
                              recoveryConversionLift
                            )}
                          </strong>
                        </div>

                        <div className="data-chip">
                          Threshold
                          <br />
                          <strong>
                            {formatPoints(
                              recovery?.success_threshold || 0.03
                            )}
                          </strong>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* FULL AUTONOMOUS TIMELINE */}

            <div className="panel" style={{ marginTop: 18 }}>
              <SectionHeader
                icon={Activity}
                title="MAYA Autonomous Execution Timeline"
                subtitle="A transparent audit of the reasoning → experiment → recovery loop."
              />

              <div className="timeline">
                <TimelineStep
                  number={1}
                  icon={Lightbulb}
                  title="Opportunity Discovered"
                  status="DISCOVERED"
                  active
                  description={
                    opportunity.title ||
                    "MAYA found a cross-sell opportunity from verified merchant data."
                  }
                >
                  <div className="data-chip">
                    Product Signal:{" "}
                    <strong>
                      {opportunity.product_a || "Wireless Earbuds"}
                    </strong>
                  </div>

                  <div className="data-chip">
                    Cross-sell:{" "}
                    <strong>
                      {opportunity.product_b || "USB-C Cable"}
                    </strong>
                  </div>

                  <div className="data-chip">
                    Confidence:{" "}
                    <strong>
                      {opportunity.confidence || 82}%
                    </strong>
                  </div>
                </TimelineStep>

                <TimelineStep
                  number={2}
                  icon={Brain}
                  title="Hypothesis Challenged"
                  status="RANKED"
                  active
                  description={
                    selected?.reasoning ||
                    "MAYA compared competing explanations and selected the strongest evidence-backed hypothesis."
                  }
                >
                  <div className="data-chip">
                    Winner:{" "}
                    <strong>
                      {selected?.name ||
                        selected?.hypothesis ||
                        "High-Intent Segment"}
                    </strong>
                  </div>

                  <div className="data-chip">
                    Challenge Score:{" "}
                    <strong>
                      {Number(
                        selected?.challenge_score ||
                          selected?.updated_confidence ||
                          0.88
                      ) > 1
                        ? Number(
                            selected?.challenge_score ||
                              selected?.updated_confidence ||
                              88
                          ).toFixed(0)
                        : (
                            Number(
                              selected?.challenge_score ||
                                selected?.updated_confidence ||
                                0.88
                            ) * 100
                          ).toFixed(0)}
                      %
                    </strong>
                  </div>
                </TimelineStep>

                <TimelineStep
                  number={3}
                  icon={Brain}
                  title="AI Decision"
                  status={aiMode}
                  active
                  description={
                    aiRecommendation?.recommended_experiment ||
                    `MAYA selected ${aiSegment} for a targeted ${aiDiscount}% incentive experiment.`
                  }
                >
                  <div className="data-chip">
                    Segment: <strong>{aiSegment}</strong>
                  </div>

                  <div className="data-chip">
                    Product: <strong>{aiProduct}</strong>
                  </div>

                  <div className="data-chip">
                    Budget:{" "}
                    <strong>{formatCurrency(aiBudget)}</strong>
                  </div>

                  <div className="data-chip">
                    Audience:{" "}
                    <strong>{formatNumber(aiAudience)}</strong>
                  </div>
                </TimelineStep>

                <TimelineStep
                  number={4}
                  icon={ShieldCheck}
                  title="Guardrails Validated"
                  status={
                    guardrailsApproved
                      ? "APPROVED"
                      : "BLOCKED"
                  }
                  active={guardrailsApproved}
                  failed={!guardrailsApproved}
                  description={
                    guardrailsApproved
                      ? "The experiment remained inside MAYA's financial and audience limits."
                      : "The recommendation exceeded a MAYA safety constraint."
                  }
                >
                  <div className="data-chip">
                    Discount: <strong>{aiDiscount}%</strong>
                  </div>

                  <div className="data-chip">
                    Budget:{" "}
                    <strong>{formatCurrency(aiBudget)}</strong>
                  </div>

                  <div className="data-chip">
                    Audience:{" "}
                    <strong>{formatNumber(aiAudience)}</strong>
                  </div>
                </TimelineStep>

                <TimelineStep
                  number={5}
                  icon={FlaskConical}
                  title="Experiment Executed"
                  status={
                    firstExperiment?.status || "FAILED"
                  }
                  failed={!firstExperiment?.success}
                  success={firstExperiment?.success}
                  description={
                    firstExperiment?.success
                      ? "The initial experiment met the success threshold."
                      : "The first experiment intentionally failed, allowing MAYA to demonstrate autonomous failure recovery."
                  }
                >
                  <div className="data-chip">
                    Control:{" "}
                    <strong>
                      {formatPercent(
                        firstExperiment?.control_conversion ||
                          0.068
                      )}
                    </strong>
                  </div>

                  <div className="data-chip">
                    Treatment:{" "}
                    <strong>
                      {formatPercent(treatmentConversion)}
                    </strong>
                  </div>

                  <div className="data-chip">
                    Lift:{" "}
                    <strong>
                      {formatPoints(conversionLift)}
                    </strong>
                  </div>

                  <div className="data-chip">
                    Required:{" "}
                    <strong>
                      {formatPoints(
                        firstExperiment?.success_threshold ||
                          0.03
                      )}
                    </strong>
                  </div>
                </TimelineStep>

                <TimelineStep
                  number={6}
                  icon={RotateCcw}
                  title="Failure Diagnosed"
                  status="ADAPT"
                  active
                  description={
                    diagnosis.reason ||
                    diagnosis.failure_reason ||
                    firstExperiment?.failure_reason ||
                    "MAYA identified diluted audience intent and adapted the targeting strategy."
                  }
                >
                  <div className="data-chip">
                    Action:{" "}
                    <strong>
                      Narrow audience
                    </strong>
                  </div>

                  <div className="data-chip">
                    Strategy:{" "}
                    <strong>
                      Higher-intent targeting
                    </strong>
                  </div>
                </TimelineStep>

                <TimelineStep
                  number={7}
                  icon={CheckCircle2}
                  title="Recovery Experiment"
                  status={
                    recovery?.success
                      ? "RECOVERED"
                      : "FAILED"
                  }
                  success={recovery?.success}
                  failed={!recovery?.success}
                  description={
                    recovery?.success
                      ? "MAYA adapted the audience and recovered the experiment."
                      : "The adapted experiment still failed to reach the required threshold."
                  }
                >
                  <div className="data-chip">
                    Recovery Audience:{" "}
                    <strong>
                      {formatNumber(
                        recovery?.recovery_audience_size ||
                          608
                      )}
                    </strong>
                  </div>

                  <div className="data-chip">
                    Treatment:{" "}
                    <strong>
                      {formatPercent(
                        recoveryTreatmentConversion
                      )}
                    </strong>
                  </div>

                  <div className="data-chip">
                    Lift:{" "}
                    <strong>
                      +
                      {formatPoints(
                        recoveryConversionLift
                      )}
                    </strong>
                  </div>

                  <div className="data-chip">
                    Result:{" "}
                    <strong>
                      {recovery?.success
                        ? "SUCCESS"
                        : "FAILED"}
                    </strong>
                  </div>
                </TimelineStep>
              </div>
            </div>

            {/* FINAL STATUS */}

            <div className="status-banner">
              <div className="status-banner-left">
                <div className="status-banner-icon">
                  {statusRecovered ? (
                    <CheckCircle2 size={20} />
                  ) : (
                    <AlertTriangle size={20} />
                  )}
                </div>

                <div>
                  <h3>
                    MAYA autonomous execution complete
                  </h3>

                  <p>
                    Discover → Hypothesize → Challenge →
                    Experiment → Measure → Adapt
                  </p>
                </div>
              </div>

              <div className="status-large">
                {finalStatus}
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;