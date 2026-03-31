import React from "react";
import { AbsoluteFill, Series, useVideoConfig } from "remotion";
import { IntroScene } from "./components/IntroScene";
import { LogoRevealScene } from "./components/LogoRevealScene";
import { FeaturesScene } from "./components/FeaturesScene";
import { CtaScene } from "./components/CtaScene";

export const G4Video: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#0F2137" }}>
      <Series>
        <Series.Sequence durationInFrames={90}>
          <IntroScene />
        </Series.Sequence>
        <Series.Sequence durationInFrames={120}>
          <LogoRevealScene />
        </Series.Sequence>
        <Series.Sequence durationInFrames={120}>
          <FeaturesScene />
        </Series.Sequence>
        <Series.Sequence durationInFrames={90}>
          <CtaScene />
        </Series.Sequence>
      </Series>
    </AbsoluteFill>
  );
};
