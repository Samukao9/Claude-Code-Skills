import React from "react";
import { Composition } from "remotion";
import { G4Video } from "./G4Video";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="G4Video"
        component={G4Video}
        durationInFrames={420}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
