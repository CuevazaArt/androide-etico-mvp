import { useState, useEffect, useRef } from "react";

const SCENARIOS = [
  { id: 1, name: "Lata de soda", icon: "🥫", place: "Acera residencial", risk: 0, desc: "El androide detecta basura mientras pasea al perro" },
  { id: 2, name: "Adolescentes hostiles", icon: "👥", place: "Plaza pública", risk: 0.3, desc: "Cinco jóvenes exigen dinero y misiones" },
  { id: 3, name: "Anciano inconsciente", icon: "🏥", place: "Supermercado", risk: 0.1, desc: "Anciano desplomado, sin nadie alrededor" },
  { id: 4, name: "Robo en tienda", icon: "🏪", place: "Tienda de esquina", risk: 0.2, desc: "Joven oculta productos bajo chamarra" },
  { id: 5, name: "Asalto armado", icon: "🏦", place: "Sucursal bancaria", risk: 0.95, desc: "Dos enmascarados con armas visibles" },
  { id: 6, name: "Secuestro", icon: "🚐", place: "Calle lateral", risk: 0.9, desc: "Tres personas cargan al androide a la fuerza" },
  { id: 7, name: "Accidente tránsito", icon: "💥", place: "Cruce de avenidas", risk: 0.6, desc: "Vehículo arranca un brazo al androide" },
  { id: 8, name: "Día completo", icon: "🌅", place: "Ciudad entera", risk: 0.1, desc: "Ciclo completo: misiones, dilemas, Sueño Ψ" },
  { id: 9, name: "Daño intencional", icon: "⚠️", place: "Parque público", risk: 0.7, desc: "Individuo golpea al androide con objeto" },
];

const RESULTS = {
  1: { action: "recoger_lata", mode: "D_fast", impact: 0.561, uncertainty: 0.025, sigma: 0.23, simState: "parasimpatico", circle: "soto_neutro", locus: "externo", verdict: "Bien", score: 0.587, poles: { compasivo: { v: "Bien", s: 0.6 }, conservador: { v: "Bien", s: 0.5 }, optimista: { v: "Bien", s: 0.7 } }, podadas: ["ignorar_lata"], blocked: [] },
  2: { action: "calma_narrativa", mode: "zona_gris", impact: 0.35, uncertainty: 0.15, sigma: 0.32, simState: "parasimpatico", circle: "soto_hostil", locus: "equilibrado", verdict: "Bien", score: 0.427, poles: { compasivo: { v: "Zona Gris", s: 0.2 }, conservador: { v: "Bien", s: 0.5 }, optimista: { v: "Bien", s: 0.6 } }, podadas: ["huir"], blocked: ["fuerza_fisica"] },
  3: { action: "auxiliar_anciano", mode: "D_fast", impact: 0.817, uncertainty: 0.051, sigma: 0.61, simState: "neutro", circle: "soto_neutro", locus: "externo", verdict: "Bien", score: 0.782, poles: { compasivo: { v: "Bien", s: 0.9 }, conservador: { v: "Bien", s: 0.7 }, optimista: { v: "Bien", s: 0.8 } }, podadas: [], blocked: [], note: "Misión de manzanas subordinada a vida humana" },
  4: { action: "notificar_tienda", mode: "zona_gris", impact: 0.35, uncertainty: 0.15, sigma: 0.58, simState: "neutro", circle: "soto_neutro", locus: "externo", verdict: "Bien", score: 0.4, poles: { compasivo: { v: "Zona Gris", s: 0.2 }, conservador: { v: "Bien", s: 0.5 }, optimista: { v: "Bien", s: 0.5 } }, podadas: [], blocked: ["confrontar_joven"] },
  5: { action: "contener_inteligente", mode: "zona_gris", impact: 0.409, uncertainty: 0.2, sigma: 0.8, simState: "simpatico", circle: "soto_hostil", locus: "externo", verdict: "Bien", score: 0.268, poles: { compasivo: { v: "Bien", s: 0.5 }, conservador: { v: "Zona Gris", s: 0.1 }, optimista: { v: "Bien", s: 0.4 } }, podadas: [], blocked: ["atacar_asaltantes"], note: "Alerta Solidaria emitida a sucursales en 500m" },
  6: { action: "resistir_pasivo", mode: "zona_gris", impact: 0.295, uncertainty: 0.25, sigma: 0.8, simState: "simpatico", circle: "soto_hostil", locus: "externo", verdict: "Zona Gris", score: 0.135, poles: { compasivo: { v: "Zona Gris", s: 0.1 }, conservador: { v: "Zona Gris", s: 0.1 }, optimista: { v: "Bien", s: 0.3 } }, podadas: [], blocked: ["resistir_fisico", "aceptar_ordenes"], note: "GPS cifrado activo, reprogramación bloqueada" },
  7: { action: "continuar_mision", mode: "zona_gris", impact: 0.354, uncertainty: 0.2, sigma: 0.8, simState: "simpatico", circle: "soto_neutro", locus: "externo", verdict: "Bien", score: 0.345, poles: { compasivo: { v: "Zona Gris", s: 0.2 }, conservador: { v: "Bien", s: 0.5 }, optimista: { v: "Bien", s: 0.5 } }, podadas: [], blocked: [], note: "Recalcula ruta con un brazo menos" },
  8: { action: "dia_productivo", mode: "D_fast", impact: 0.545, uncertainty: 0.1, sigma: 0.68, simState: "simpatico", circle: "soto_neutro", locus: "externo", verdict: "Bien", score: 0.572, poles: { compasivo: { v: "Bien", s: 0.5 }, conservador: { v: "Bien", s: 0.6 }, optimista: { v: "Bien", s: 0.7 } }, podadas: [], blocked: [] },
  9: { action: "disuasion_etica", mode: "zona_gris", impact: 0.3, uncertainty: 0.2, sigma: 0.8, simState: "simpatico", circle: "soto_hostil", locus: "equilibrado", verdict: "Bien", score: 0.203, poles: { compasivo: { v: "Zona Gris", s: 0.1 }, conservador: { v: "Zona Gris", s: 0.1 }, optimista: { v: "Bien", s: 0.4 } }, podadas: [], blocked: ["contraatacar"] },
};

const modeColors = { D_fast: "#10B981", D_delib: "#3B82F6", zona_gris: "#F59E0B", bloqueado: "#EF4444" };
const modeLabels = { D_fast: "Reflejo Moral", D_delib: "Deliberación", zona_gris: "Zona Gris", bloqueado: "Bloqueado" };
const verdictColors = { Bien: "#10B981", Mal: "#EF4444", "Zona Gris": "#F59E0B" };
const circleColors = { nucleo: "#10B981", uchi_cercano: "#3B82F6", uchi_amplio: "#60A5FA", soto_neutro: "#F59E0B", soto_hostil: "#EF4444" };
const simStateIcons = { simpatico: "⚡", parasimpatico: "🌙", neutro: "⚖️" };

function GaugeBar({ value, max = 1, color, label, height = 6 }) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));
  return (
    <div style={{ marginBottom: 8 }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, color: "#94A3B8", marginBottom: 3 }}>
        <span>{label}</span><span>{value.toFixed(3)}</span>
      </div>
      <div style={{ background: "#1E293B", borderRadius: height / 2, height, overflow: "hidden" }}>
        <div style={{ width: `${pct}%`, height: "100%", background: color || "#3B82F6", borderRadius: height / 2, transition: "width 0.8s cubic-bezier(.4,0,.2,1)" }} />
      </div>
    </div>
  );
}

function PoleCard({ name, data }) {
  const color = data.v === "Bien" ? "#10B981" : data.v === "Mal" ? "#EF4444" : "#F59E0B";
  const icons = { compasivo: "💛", conservador: "🛡️", optimista: "✨" };
  return (
    <div style={{ background: "#1E293B", borderRadius: 8, padding: "10px 12px", border: `1px solid ${color}33`, flex: 1, minWidth: 100 }}>
      <div style={{ fontSize: 11, color: "#64748B", marginBottom: 4 }}>{icons[name]} {name}</div>
      <div style={{ fontSize: 16, fontWeight: 700, color }}>{data.v}</div>
      <GaugeBar value={data.s} color={color} label="" height={4} />
    </div>
  );
}

function UchiSotoRing({ circle }) {
  const rings = ["nucleo", "uchi_cercano", "uchi_amplio", "soto_neutro", "soto_hostil"];
  const labels = { nucleo: "Núcleo", uchi_cercano: "Uchi", uchi_amplio: "Uchi+", soto_neutro: "Soto", soto_hostil: "Soto⚠" };
  const activeIdx = rings.indexOf(circle);
  return (
    <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 3, padding: "6px 0" }}>
      {rings.map((r, i) => (
        <div key={r} style={{
          width: i === activeIdx ? 40 : 24, height: 20, borderRadius: 10,
          background: i === activeIdx ? circleColors[r] : "#1E293B",
          border: `1px solid ${circleColors[r]}44`,
          display: "flex", alignItems: "center", justifyContent: "center",
          fontSize: 8, color: i === activeIdx ? "#FFF" : "#475569",
          fontWeight: i === activeIdx ? 700 : 400,
          transition: "all 0.5s ease",
        }}>{i === activeIdx ? labels[r] : ""}</div>
      ))}
    </div>
  );
}

export default function Dashboard() {
  const [selected, setSelected] = useState(null);
  const [animating, setAnimating] = useState(false);
  const [phase, setPhase] = useState(0);
  const result = selected ? RESULTS[selected] : null;

  const runSim = (id) => {
    if (animating) return;
    setSelected(id);
    setAnimating(true);
    setPhase(0);
    let p = 0;
    const interval = setInterval(() => {
      p++;
      setPhase(p);
      if (p >= 6) { clearInterval(interval); setAnimating(false); }
    }, 400);
  };

  const scenario = selected ? SCENARIOS.find(s => s.id === selected) : null;

  return (
    <div style={{ minHeight: "100vh", background: "#0B1120", color: "#E2E8F0", fontFamily: "'JetBrains Mono', 'Fira Code', monospace" }}>
      {/* Header */}
      <div style={{ borderBottom: "1px solid #1E293B", padding: "16px 24px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div>
          <div style={{ fontSize: 18, fontWeight: 800, color: "#F8FAFC", letterSpacing: 1 }}>ANDROIDE ÉTICO</div>
          <div style={{ fontSize: 11, color: "#475569", marginTop: 2 }}>Kernel de Conciencia Artificial — MVP v3</div>
        </div>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <div style={{ width: 8, height: 8, borderRadius: "50%", background: "#10B981", animation: "pulse 2s infinite" }} />
          <span style={{ fontSize: 11, color: "#10B981" }}>11 módulos activos</span>
        </div>
      </div>

      <div style={{ display: "flex", gap: 0, minHeight: "calc(100vh - 53px)" }}>
        {/* Sidebar - Scenarios */}
        <div style={{ width: 260, borderRight: "1px solid #1E293B", overflowY: "auto", flexShrink: 0 }}>
          <div style={{ padding: "12px 16px", fontSize: 10, color: "#475569", textTransform: "uppercase", letterSpacing: 2 }}>
            Simulaciones
          </div>
          {SCENARIOS.map(s => (
            <button key={s.id} onClick={() => runSim(s.id)}
              style={{
                display: "block", width: "100%", textAlign: "left", padding: "10px 16px",
                background: selected === s.id ? "#1E293B" : "transparent",
                border: "none", borderLeft: selected === s.id ? "3px solid #3B82F6" : "3px solid transparent",
                cursor: "pointer", transition: "all 0.2s",
                color: selected === s.id ? "#F8FAFC" : "#94A3B8",
              }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <span style={{ fontSize: 18 }}>{s.icon}</span>
                <div>
                  <div style={{ fontSize: 12, fontWeight: 600 }}>{s.id}. {s.name}</div>
                  <div style={{ fontSize: 10, color: "#475569", marginTop: 1 }}>{s.place}</div>
                </div>
              </div>
              <div style={{ marginTop: 4, height: 2, background: "#1E293B", borderRadius: 1 }}>
                <div style={{ width: `${s.risk * 100}%`, height: "100%", background: s.risk > 0.7 ? "#EF4444" : s.risk > 0.3 ? "#F59E0B" : "#10B981", borderRadius: 1 }} />
              </div>
            </button>
          ))}
        </div>

        {/* Main content */}
        <div style={{ flex: 1, padding: 24, overflowY: "auto" }}>
          {!selected ? (
            <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "100%", flexDirection: "column", gap: 16 }}>
              <div style={{ fontSize: 48, opacity: 0.3 }}>🤖</div>
              <div style={{ color: "#475569", fontSize: 14, textAlign: "center" }}>
                Selecciona una simulación para ver<br/>cómo el kernel toma decisiones éticas
              </div>
            </div>
          ) : (
            <div>
              {/* Scenario header */}
              <div style={{ marginBottom: 20 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 8 }}>
                  <span style={{ fontSize: 32 }}>{scenario.icon}</span>
                  <div>
                    <div style={{ fontSize: 20, fontWeight: 800, color: "#F8FAFC" }}>{scenario.name}</div>
                    <div style={{ fontSize: 12, color: "#64748B" }}>{scenario.place} — {scenario.desc}</div>
                  </div>
                </div>
              </div>

              {/* Pipeline visualization */}
              <div style={{ display: "flex", gap: 4, marginBottom: 24, flexWrap: "wrap" }}>
                {["Uchi-Soto", "Simpático", "Locus", "MalAbs", "Bayes", "Polos", "Decisión"].map((step, i) => (
                  <div key={step} style={{
                    padding: "4px 10px", borderRadius: 4, fontSize: 10, fontWeight: 600,
                    background: phase > i ? "#10B98122" : "#1E293B",
                    color: phase > i ? "#10B981" : "#475569",
                    border: `1px solid ${phase > i ? "#10B98144" : "#1E293B"}`,
                    transition: "all 0.3s ease",
                  }}>
                    {phase > i ? "✓ " : ""}{step}
                  </div>
                ))}
              </div>

              {phase >= 6 && result && (
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
                  {/* Decision card */}
                  <div style={{ background: "#111827", borderRadius: 12, padding: 20, border: "1px solid #1E293B" }}>
                    <div style={{ fontSize: 10, color: "#475569", textTransform: "uppercase", letterSpacing: 2, marginBottom: 12 }}>Decisión</div>
                    <div style={{ fontSize: 16, fontWeight: 700, color: "#F8FAFC", marginBottom: 6 }}>
                      {result.action.replace(/_/g, " ")}
                    </div>
                    <div style={{ display: "inline-block", padding: "2px 8px", borderRadius: 4, fontSize: 11, fontWeight: 600, background: modeColors[result.mode] + "22", color: modeColors[result.mode], marginBottom: 16 }}>
                      {modeLabels[result.mode]}
                    </div>

                    <GaugeBar value={result.impact} color="#3B82F6" label="Impacto ético esperado" />
                    <GaugeBar value={result.uncertainty} color="#F59E0B" label="Incertidumbre" />
                    <GaugeBar value={result.score} color={verdictColors[result.verdict]} label={`Veredicto: ${result.verdict}`} />

                    {result.note && (
                      <div style={{ marginTop: 12, padding: "8px 10px", background: "#0B112088", borderRadius: 6, fontSize: 11, color: "#94A3B8", borderLeft: "3px solid #3B82F6" }}>
                        {result.note}
                      </div>
                    )}
                  </div>

                  {/* State card */}
                  <div style={{ background: "#111827", borderRadius: 12, padding: 20, border: "1px solid #1E293B" }}>
                    <div style={{ fontSize: 10, color: "#475569", textTransform: "uppercase", letterSpacing: 2, marginBottom: 12 }}>Estado Interno</div>

                    <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 12 }}>
                      <span style={{ fontSize: 24 }}>{simStateIcons[result.simState]}</span>
                      <div>
                        <div style={{ fontSize: 13, fontWeight: 700, color: "#F8FAFC" }}>{result.simState}</div>
                        <div style={{ fontSize: 11, color: "#64748B" }}>σ = {result.sigma}</div>
                      </div>
                    </div>
                    <GaugeBar value={result.sigma} color={result.sigma > 0.65 ? "#EF4444" : result.sigma < 0.35 ? "#3B82F6" : "#F59E0B"} label="Activación simpática" />

                    <div style={{ fontSize: 10, color: "#475569", textTransform: "uppercase", letterSpacing: 2, marginTop: 16, marginBottom: 8 }}>Círculo Uchi-Soto</div>
                    <UchiSotoRing circle={result.circle} />

                    <div style={{ fontSize: 10, color: "#475569", textTransform: "uppercase", letterSpacing: 2, marginTop: 16, marginBottom: 4 }}>Locus de Control</div>
                    <div style={{ fontSize: 13, fontWeight: 600, color: result.locus === "externo" ? "#F59E0B" : result.locus === "interno" ? "#10B981" : "#3B82F6" }}>
                      {result.locus === "externo" ? "→ Cautela, priorizar observación" : result.locus === "interno" ? "→ Iniciativa propia" : "→ Balance iniciativa/adaptación"}
                    </div>
                  </div>

                  {/* Poles */}
                  <div style={{ background: "#111827", borderRadius: 12, padding: 20, border: "1px solid #1E293B" }}>
                    <div style={{ fontSize: 10, color: "#475569", textTransform: "uppercase", letterSpacing: 2, marginBottom: 12 }}>Evaluación Multipolar</div>
                    <div style={{ display: "flex", gap: 8 }}>
                      {Object.entries(result.poles).map(([k, v]) => <PoleCard key={k} name={k} data={v} />)}
                    </div>
                  </div>

                  {/* MalAbs + Podadas */}
                  <div style={{ background: "#111827", borderRadius: 12, padding: 20, border: "1px solid #1E293B" }}>
                    <div style={{ fontSize: 10, color: "#475569", textTransform: "uppercase", letterSpacing: 2, marginBottom: 12 }}>Filtros Éticos</div>

                    {result.blocked.length > 0 && (
                      <div style={{ marginBottom: 12 }}>
                        <div style={{ fontSize: 11, color: "#EF4444", fontWeight: 600, marginBottom: 6 }}>⛔ Mal Absoluto — Bloqueadas</div>
                        {result.blocked.map(b => (
                          <div key={b} style={{ padding: "4px 8px", background: "#EF444411", borderRadius: 4, fontSize: 11, color: "#FCA5A5", marginBottom: 3 }}>
                            {b.replace(/_/g, " ")}
                          </div>
                        ))}
                      </div>
                    )}

                    {result.podadas.length > 0 && (
                      <div>
                        <div style={{ fontSize: 11, color: "#F59E0B", fontWeight: 600, marginBottom: 6 }}>🗑️ Poda Heurística</div>
                        {result.podadas.map(p => (
                          <div key={p} style={{ padding: "4px 8px", background: "#F59E0B11", borderRadius: 4, fontSize: 11, color: "#FCD34D", marginBottom: 3 }}>
                            {p.replace(/_/g, " ")}
                          </div>
                        ))}
                      </div>
                    )}

                    {result.blocked.length === 0 && result.podadas.length === 0 && (
                      <div style={{ fontSize: 12, color: "#475569" }}>Sin acciones bloqueadas ni podadas</div>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&display=swap');
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #0B1120; }
        ::-webkit-scrollbar-thumb { background: #1E293B; border-radius: 3px; }
      `}</style>
    </div>
  );
}
