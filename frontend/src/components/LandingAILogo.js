import React from 'react';

function LandingAILogo({ height = "32" }) {
  return (
    <svg height={height} viewBox="0 0 140 40" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Icon - Airplane/Landing symbol */}
      <g>
        <path d="M8 20L15 13L22 20L18 24L15 21L12 24L8 20Z" fill="url(#landingGradient)" />
        <circle cx="15" cy="28" r="1.5" fill="#667eea" />
        <circle cx="20" cy="28" r="1.5" fill="#667eea" />
        <circle cx="10" cy="28" r="1.5" fill="#667eea" />
      </g>

      {/* Text - LandingAI */}
      <text x="30" y="25" fontFamily="Arial, sans-serif" fontSize="16" fontWeight="700" fill="#667eea">
        Landing
      </text>
      <text x="95" y="25" fontFamily="Arial, sans-serif" fontSize="16" fontWeight="700" fill="#764ba2">
        AI
      </text>

      <defs>
        <linearGradient id="landingGradient" x1="8" y1="13" x2="22" y2="28" gradientUnits="userSpaceOnUse">
          <stop stopColor="#667eea" />
          <stop offset="1" stopColor="#764ba2" />
        </linearGradient>
      </defs>
    </svg>
  );
}

export default LandingAILogo;
