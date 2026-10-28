import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // Static site: every page is built from skills/ at build time.
  output: 'export',
  trailingSlash: true,
  devIndicators: false,
};

export default nextConfig;
