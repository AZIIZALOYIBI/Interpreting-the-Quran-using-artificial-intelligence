const outputMode = process.env.NEXT_OUTPUT_MODE;
const isStaticExport = outputMode === "export";

const normalizeBasePath = (value) => {
  if (!value) return "";
  if (value === "/") return "";
  return value.startsWith("/") ? value : `/${value}`;
};

const repoName = (process.env.GITHUB_REPOSITORY || "").split("/")[1] || "";
const defaultExportBasePath =
  repoName && !repoName.endsWith(".github.io") ? `/${repoName}` : "";
const basePath = normalizeBasePath(
  process.env.NEXT_PUBLIC_BASE_PATH || (isStaticExport ? defaultExportBasePath : ""),
);

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  ...(isStaticExport
    ? {
        output: "export",
        trailingSlash: true,
        images: { unoptimized: true },
        ...(basePath ? { basePath, assetPrefix: basePath } : {}),
      }
    : {}),
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
    NEXT_PUBLIC_BASE_PATH: basePath,
  },
};

export default nextConfig;
