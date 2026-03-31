import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  spring,
  useVideoConfig,
} from "remotion";
import { G4Compass, G4Text } from "./G4Logo";

export const LogoRevealScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Compass rotation and scale
  const compassRotation = interpolate(frame, [0, 60], [180, 0], {
    extrapolateRight: "clamp",
  });

  const compassScale = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 60 },
  });

  const compassOpacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: "clamp",
  });

  // G4 text entrance
  const textScale = spring({
    frame: frame - 30,
    fps,
    config: { damping: 14, stiffness: 80 },
  });

  const textOpacity = interpolate(frame, [30, 50], [0, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });

  // Gold particles / sparkles
  const sparkleOpacity = interpolate(frame, [40, 55, 70, 85], [0, 0.8, 0.8, 0], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });

  // Glow pulse
  const glowIntensity = interpolate(
    frame,
    [50, 65, 80],
    [0, 30, 15],
    { extrapolateRight: "clamp", extrapolateLeft: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0F2137",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* Background radial glow */}
      <div
        style={{
          position: "absolute",
          width: 800,
          height: 800,
          borderRadius: "50%",
          background: `radial-gradient(circle, rgba(184,150,62,${glowIntensity / 100}) 0%, transparent 70%)`,
        }}
      />

      {/* Sparkle particles */}
      {[...Array(8)].map((_, i) => {
        const angle = (i / 8) * Math.PI * 2;
        const radius = 220 + Math.sin(frame * 0.05 + i) * 30;
        const x = Math.cos(angle + frame * 0.02) * radius;
        const y = Math.sin(angle + frame * 0.02) * radius;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: `calc(50% + ${x}px)`,
              top: `calc(50% + ${y}px)`,
              width: 6,
              height: 6,
              borderRadius: "50%",
              backgroundColor: "#B8963E",
              opacity: sparkleOpacity * (0.5 + Math.sin(frame * 0.1 + i) * 0.5),
              boxShadow: "0 0 10px #B8963E",
            }}
          />
        );
      })}

      {/* Logo container */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 40,
        }}
      >
        {/* Compass */}
        <div
          style={{
            transform: `scale(${compassScale}) rotate(${compassRotation}deg)`,
            opacity: compassOpacity,
            filter: `drop-shadow(0 0 ${glowIntensity}px rgba(184,150,62,0.5))`,
          }}
        >
          <G4Compass size={250} />
        </div>

        {/* G4 text */}
        <div
          style={{
            transform: `scale(${Math.max(0, textScale)})`,
            opacity: textOpacity,
            filter: `drop-shadow(0 0 ${glowIntensity}px rgba(184,150,62,0.3))`,
          }}
        >
          <G4Text fontSize={200} color="#FFFFFF" />
        </div>
      </div>
    </AbsoluteFill>
  );
};
