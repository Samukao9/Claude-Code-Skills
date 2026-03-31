import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  spring,
  useVideoConfig,
} from "remotion";

export const IntroScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const bgOpacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: "clamp",
  });

  const lineWidth = spring({
    frame: frame - 15,
    fps,
    config: { damping: 20, stiffness: 80 },
  });

  const textOpacity = interpolate(frame, [25, 45], [0, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });

  const textY = interpolate(frame, [25, 45], [40, 0], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });

  const subtitleOpacity = interpolate(frame, [45, 65], [0, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0F2137",
        justifyContent: "center",
        alignItems: "center",
        opacity: bgOpacity,
      }}
    >
      {/* Decorative gold line */}
      <div
        style={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          width: `${lineWidth * 600}px`,
          height: 2,
          backgroundColor: "#B8963E",
          opacity: 0.6,
        }}
      />

      {/* Main text */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 20,
          transform: `translateY(${textY}px)`,
          opacity: textOpacity,
        }}
      >
        <span
          style={{
            fontFamily: "'Arial', sans-serif",
            fontSize: 28,
            fontWeight: 300,
            color: "#B8963E",
            letterSpacing: "0.4em",
            textTransform: "uppercase",
          }}
        >
          Apresentamos
        </span>
      </div>

      {/* Subtitle */}
      <div
        style={{
          position: "absolute",
          bottom: 160,
          opacity: subtitleOpacity,
        }}
      >
        <span
          style={{
            fontFamily: "'Arial', sans-serif",
            fontSize: 18,
            color: "rgba(255,255,255,0.5)",
            letterSpacing: "0.3em",
            textTransform: "uppercase",
          }}
        >
          Estratégia • Inovação • Resultado
        </span>
      </div>
    </AbsoluteFill>
  );
};
