import React from 'react';

function AWSBedrockLogo({ height = "32" }) {
  return (
    <svg height={height} viewBox="0 0 160 40" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* AWS Smile Arrow */}
      <g>
        <path
          d="M28 24C28 24 24 28 18 28C12 28 8 24 8 24"
          stroke="#FF9900"
          strokeWidth="2.5"
          strokeLinecap="round"
        />
        <path
          d="M26 22L28 24L26 26"
          stroke="#FF9900"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        {/* AWS Box/Cube */}
        <rect x="10" y="10" width="16" height="10" fill="none" stroke="#FF9900" strokeWidth="1.5" />
        <path d="M10 10L18 6L26 10" stroke="#FF9900" strokeWidth="1.5" strokeLinejoin="round" />
        <path d="M18 6V16" stroke="#FF9900" strokeWidth="1.5" />
      </g>

      {/* Text - AWS */}
      <text x="34" y="18" fontFamily="Arial, sans-serif" fontSize="14" fontWeight="700" fill="#FF9900">
        AWS
      </text>

      {/* Text - Bedrock */}
      <text x="34" y="30" fontFamily="Arial, sans-serif" fontSize="11" fontWeight="600" fill="#bdc3c7">
        Bedrock
      </text>
    </svg>
  );
}

export default AWSBedrockLogo;
