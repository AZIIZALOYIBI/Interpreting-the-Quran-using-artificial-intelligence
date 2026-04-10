import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: process.env.NEXT_OUTPUT_MODE === "export" ? "export" : "standalone",
};

export default nextConfig;
