import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  allowedDevOrigins: ["192.168.1.19"],
  output: "standalone",
};

export default nextConfig;
