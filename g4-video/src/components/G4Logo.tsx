import React from "react";

export const G4Compass: React.FC<{
  size?: number;
  color?: string;
  opacity?: number;
}> = ({ size = 300, color = "#B8963E", opacity = 1 }) => {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 400 400"
      fill="none"
      style={{ opacity }}
    >
      {/* Outer ring */}
      <circle
        cx="200"
        cy="200"
        r="150"
        stroke={color}
        strokeWidth="12"
        fill="none"
      />
      {/* Inner ring */}
      <circle
        cx="200"
        cy="200"
        r="100"
        stroke={color}
        strokeWidth="8"
        fill="none"
      />
      {/* Center dot */}
      <circle cx="200" cy="200" r="20" fill={color} />
      {/* Cardinal points - compass arrows */}
      {/* North arrow */}
      <polygon points="200,30 185,80 200,65 215,80" fill={color} />
      {/* South */}
      <polygon points="200,370 215,320 200,335 185,320" fill={color} />
      {/* East */}
      <polygon points="370,200 320,185 335,200 320,215" fill={color} />
      {/* West */}
      <polygon points="30,200 80,215 65,200 80,185" fill={color} />
      {/* Diagonal cross lines */}
      <line
        x1="80"
        y1="80"
        x2="320"
        y2="320"
        stroke={color}
        strokeWidth="8"
      />
      <line
        x1="320"
        y1="80"
        x2="80"
        y2="320"
        stroke={color}
        strokeWidth="8"
      />
      {/* NE arrow tip */}
      <polygon points="320,55 290,100 310,90 320,110" fill={color} />
      {/* Horizontal and vertical cross */}
      <line
        x1="50"
        y1="200"
        x2="350"
        y2="200"
        stroke={color}
        strokeWidth="8"
      />
      <line
        x1="200"
        y1="50"
        x2="200"
        y2="350"
        stroke={color}
        strokeWidth="8"
      />
    </svg>
  );
};

export const G4Text: React.FC<{
  fontSize?: number;
  color?: string;
  opacity?: number;
}> = ({ fontSize = 180, color = "#0F2137", opacity = 1 }) => {
  return (
    <span
      style={{
        fontFamily: "'Arial Black', 'Helvetica Neue', sans-serif",
        fontSize,
        fontWeight: 900,
        color,
        letterSpacing: "-0.02em",
        lineHeight: 1,
        opacity,
      }}
    >
      G4
    </span>
  );
};
