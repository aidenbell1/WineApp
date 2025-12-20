/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  // Environment variables exposed to browser
  env: {
    NEXT_PUBLIC_API_URL:
      process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  },

  // Image optimization
  images: {
    domains: [],
  },
};

module.exports = nextConfig;
