/** @type {import('next').NextConfig} */
const nextConfig = {
    async rewrites() {
        return [
          {
            source: '/api/:path*',
            destination: 'https://13.126.42.91/:path*',
          },
        ]
      },
};

export default nextConfig;