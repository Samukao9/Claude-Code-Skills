import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  spring,
  useVideoConfig,
} from "remotion";
import { G4Compass } from "./G4Logo";

export const CtaScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Background pulse
  const pulse = Math.sin(frame * 0.05) * 0.02 + 1;

  // Compass fades in and slowly rotates
  const compassOpacity = interpolate(frame, [0, 30], [0, 0.15], {
    extrapolateRight: "clamp",
  });
  const compassRotation = frame * 0.3;

  // Main CTA text
  const ctaScale = spring({
    frame: frame - 10,
    fps,
    config: { damping: 12, stiffness: 60 },
  });

  const ctaOpacity = interpolate(frame, [10, 30], [0, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });

  // Tagline
  const taglineOpacity = interpolate(frame, [35, 55], [0, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });

  const taglineY = interpolate(frame, [35, 55], [20, 0], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });

  // Button / CTA box
  const buttonOpacity = interpolate(frame, [55, 70], [0, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });

  const buttonScale = spring({
    frame: frame - 55,
    fps,
    config: { damping: 14, stiffness: 100 },
  });

  // Final fade out
  const fadeOut = interpolate(frame, [80, 90], [1, 0], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0F2137",
        justifyContent: "center",
        alignItems: "center",
        opacity: fadeOut,
      }}
    >
      {/* Background compass watermark */}
      <div
        style={{
          position: "absolute",
          transform: `scale(${pulse}) rotate(${compassRotation}deg)`,
          opacity: compassOpacity,
        }}
      >
        <G4Compass size={600} color="#B8963E" />
      </div>

      {/* Gradient overlay */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "radial-gradient(ellipse at center, transparent 30%, #0F2137 80%)",
        }}
      />

      {/* Content */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 30,
          zIndex: 1,
        }}
      >
        {/* Main CTA */}
        <div
          style={{
            transform: `scale(${Math.max(0, ctaScale)})`,
            opacity: ctaOpacity,
          }}
        >
          <span
            style={{
              fontFamily: "'Arial Black', sans-serif",
              fontSize: 72,
              fontWeight: 900,
              color: "#FFFFFF",
              textAlign: "center",
              display: "block",
            }}
          >
            Transforme seu
          </span>
          <span
            style={{
              fontFamily: "'Arial Black', sans-serif",
              fontSize: 72,
              fontWeight: 900,
              color: "#B8963E",
              textAlign: "center",
              display: "block",
            }}
          >
            Negócio
          </span>
        </div>

        {/* Tagline */}
        <div
          style={{
            opacity: taglineOpacity,
            transform: `translateY(${taglineY}px)`,
          }}
        >
          <span
            style={{
              fontFamily: "'Arial', sans-serif",
              fontSize: 22,
              color: "rgba(255,255,255,0.7)",
              letterSpacing: "0.1em",
            }}
          >
            A G4 é o seu parceiro estratégico de crescimento
          </span>
        </div>

        {/* CTA Button */}
        <div
          style={{
            opacity: buttonOpacity,
            transform: `scale(${Math.max(0, buttonScale)})`,
            marginTop: 20,
          }}
        >
          <div
            style={{
              padding: "18px 60px",
              border: "2px solid #B8963E",
              borderRadius: 8,
              backgroundColor: "rgba(184,150,62,0.1)",
            }}
          >
            <span
              style={{
                fontFamily: "'Arial', sans-serif",
                fontSize: 20,
                fontWeight: 700,
                color: "#B8963E",
                letterSpacing: "0.15em",
                textTransform: "uppercase",
              }}
            >
              Saiba Mais
            </span>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
