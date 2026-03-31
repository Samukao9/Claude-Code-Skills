import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  spring,
  useVideoConfig,
} from "remotion";

const FEATURES = [
  { icon: "🎯", title: "Estratégia", desc: "Planejamento preciso para resultados extraordinários" },
  { icon: "🚀", title: "Inovação", desc: "Tecnologia de ponta para transformar negócios" },
  { icon: "📈", title: "Crescimento", desc: "Escala e performance para o seu sucesso" },
];

export const FeaturesScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleOpacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: "clamp",
  });

  const titleY = interpolate(frame, [0, 20], [30, 0], {
    extrapolateRight: "clamp",
  });

  // Decorative line
  const lineWidth = spring({
    frame: frame - 10,
    fps,
    config: { damping: 20, stiffness: 80 },
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0F2137",
        justifyContent: "center",
        alignItems: "center",
        padding: 80,
      }}
    >
      {/* Section title */}
      <div
        style={{
          position: "absolute",
          top: 100,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 16,
          opacity: titleOpacity,
          transform: `translateY(${titleY}px)`,
        }}
      >
        <span
          style={{
            fontFamily: "'Arial', sans-serif",
            fontSize: 18,
            color: "#B8963E",
            letterSpacing: "0.3em",
            textTransform: "uppercase",
          }}
        >
          O que nos define
        </span>
        <div
          style={{
            width: lineWidth * 120,
            height: 2,
            backgroundColor: "#B8963E",
          }}
        />
      </div>

      {/* Features grid */}
      <div
        style={{
          display: "flex",
          gap: 60,
          marginTop: 40,
        }}
      >
        {FEATURES.map((feature, i) => {
          const delay = 20 + i * 20;

          const cardScale = spring({
            frame: frame - delay,
            fps,
            config: { damping: 14, stiffness: 80 },
          });

          const cardOpacity = interpolate(
            frame,
            [delay, delay + 15],
            [0, 1],
            { extrapolateRight: "clamp", extrapolateLeft: "clamp" }
          );

          const borderGlow = interpolate(
            frame,
            [delay + 30, delay + 45, delay + 60],
            [0, 1, 0.4],
            { extrapolateRight: "clamp", extrapolateLeft: "clamp" }
          );

          return (
            <div
              key={i}
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 20,
                padding: 40,
                width: 280,
                borderRadius: 16,
                backgroundColor: "rgba(184,150,62,0.05)",
                border: `1px solid rgba(184,150,62,${0.1 + borderGlow * 0.3})`,
                transform: `scale(${Math.max(0, cardScale)})`,
                opacity: cardOpacity,
                boxShadow: `0 0 ${borderGlow * 20}px rgba(184,150,62,${borderGlow * 0.15})`,
              }}
            >
              <span style={{ fontSize: 48 }}>{feature.icon}</span>
              <span
                style={{
                  fontFamily: "'Arial Black', sans-serif",
                  fontSize: 28,
                  fontWeight: 900,
                  color: "#B8963E",
                }}
              >
                {feature.title}
              </span>
              <span
                style={{
                  fontFamily: "'Arial', sans-serif",
                  fontSize: 16,
                  color: "rgba(255,255,255,0.7)",
                  textAlign: "center",
                  lineHeight: 1.5,
                }}
              >
                {feature.desc}
              </span>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
